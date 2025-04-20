from fastapi import APIRouter, HTTPException, Query
from app.infrastructure.spotify.auth import get_spotify_client
from app.use_cases.spotify.user_tracks import get_current_user_profile_tracks
from app.use_cases.spotify.user_profile import get_user_profile

router = APIRouter()

@router.get("/user")
def get_user(id: str = Query(..., description="User ID (Spotify pseudo)")):
    spotify_client = get_spotify_client()
    user = get_user_profile(spotify_client, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/user/tracks")
def get_user_tracks(id: str = Query(..., description="User ID (Spotify pseudo)")):
    spotify_client = get_spotify_client()
    user = get_user_profile(spotify_client, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    tracks = get_current_user_profile_tracks(spotify_client, user=user)
    if not tracks:
        raise HTTPException(status_code=204, detail="No tracks found")
    return tracks