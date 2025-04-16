from fastapi import FastAPI, HTTPException, Query
from app.infrastructure.spotify.auth import get_spotify_client
from app.infrastructure.spotify.get_user_profile import get_user_profile

app = FastAPI()

@app.get("/user")
def get_user(id: str = Query(..., description="User ID (Spotify pseudo)")):
    """
    Get a user profile from Spotify API.
    :param id: str
    :return: User object
    """
    spotify_client = get_spotify_client()
    user = get_user_profile(spotify_client, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user