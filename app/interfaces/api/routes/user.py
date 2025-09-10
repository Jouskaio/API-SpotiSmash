import logging
import uuid

from fastapi import APIRouter, HTTPException, Query, Request
from starlette.responses import RedirectResponse, JSONResponse
from app.infrastructure.lastfm.client import LastFMClientWithRetry
from app.infrastructure.spotify.client import SpotifyClientWithRetry
from app.use_cases.spotify.user_me import clean_user_me
from app.use_cases.spotify.user_profile import get_user_profile
from app.use_cases.spotify.user_tracks import get_current_user_profile_tracks

router = APIRouter()


@router.get("/user")
def get_user(id: str = Query(..., description="User ID (Spotify pseudo)")):
    spotify_client = SpotifyClientWithRetry()
    user = get_user_profile(spotify_client, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/user/me/clean")
def get_me(request: Request):
    user_token = request.cookies.get("spotify_token")

    if not user_token:
        raise HTTPException(status_code=401, detail="User not authenticated")

    # Créer une instance de SpotifyClientWithRetry sans le token d'accès
    spotify_client = SpotifyClientWithRetry(use_user_auth=True)

    # Authentifier l'utilisateur avec le token d'accès
    spotify_client.auth_manager.access_token = user_token

    user = clean_user_me(spotify_client)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.get("/user/tracks")
def get_user_tracks(id: str = Query(..., description="User ID (Spotify pseudo)")):
    spotify_client = SpotifyClientWithRetry()
    lastfm_client = LastFMClientWithRetry()
    user = get_user_profile(spotify_client, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    tracks = get_current_user_profile_tracks(spotify_client, user=user, lastfm_client=lastfm_client)
    if not tracks:
        raise HTTPException(status_code=204, detail="No tracks found")
    return tracks


@router.get("/callback")
def callback(request: Request):
    code = request.query_params.get("code")
    state = request.query_params.get("state")

    # Log des cookies reçus
    logging.info(f"Received cookies: {request.cookies}")
    logging.info(f"Received callback with code: {code}, state: {state}")

    # Vérifier l'état dans le cookie
    stored_state = request.cookies.get("spotify_auth_state")
    logging.info(f"Stored state from cookie: {stored_state}")

    if not code or not state or state != stored_state:
        raise HTTPException(status_code=400, detail="Missing or invalid code/state")

    spotify_client = SpotifyClientWithRetry(use_user_auth=True)
    token_info = spotify_client.auth_manager.get_access_token(code, as_dict=True)
    access_token = token_info.get("access_token")

    if not access_token:
        raise HTTPException(status_code=401, detail="Failed to get access token")

    # Sauvegarder le token dans le cache
    spotify_client.auth_manager.cache_handler.save_token_to_cache(token_info)

    # Stocker le token dans un cookie
    response = JSONResponse(content={"message": "Authentication successful"})
    response.set_cookie(
        key="spotify_token",
        value=access_token,
        httponly=True,
        max_age=3600,
        secure=True,  # Assurez-vous que votre application utilise HTTPS
        samesite='Lax',
        path='/'
    )
    return response
