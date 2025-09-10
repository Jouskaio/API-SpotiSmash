import os
import logging
import re
import webbrowser
import http.client as http_client

from app.config.settings import LOG_FILE


def setup_logging():
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format=log_format)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("pylast").setLevel(logging.WARNING)
    logging.getLogger("http.client").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    http_client.HTTPConnection.debuglevel = 0

    class SpotifyAuthHandler(logging.StreamHandler):
        def emit(self, record):
            msg = self.format(record)
            match = re.search(r"https://accounts\\.spotify\\.com/authorize\\?[^\\s]+", msg)
            if match:
                url = match.group(0)
                webbrowser.open(url)
            super().emit(record)

    logging.getLogger().addHandler(SpotifyAuthHandler())