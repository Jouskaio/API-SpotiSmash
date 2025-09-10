from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

router = APIRouter()

@router.get("/callback", response_class=HTMLResponse)
async def spotify_callback(request: Request):
    code = request.query_params.get("code")
    return f"""
        <html>
            <head><title>Spotify Auth</title></head>
            <body>
                <h1>✅ Auth Successful</h1>
                <p>Copy this code and paste it into your terminal:</p>
                <code>{code}</code>
            </body>
        </html>
    """