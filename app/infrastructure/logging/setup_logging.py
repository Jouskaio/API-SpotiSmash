import os
import logging
import re
import webbrowser

from app.config.settings import LOG_FILE


def setup_logging():
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format=log_format)

    class SpotifyAuthHandler(logging.StreamHandler):
        def emit(self, record):
            msg = self.format(record)
            match = re.search(r"https://accounts\\.spotify\\.com/authorize\\?[^\\s]+", msg)
            if match:
                url = match.group(0)
                webbrowser.open(url)
            super().emit(record)

    logging.getLogger().addHandler(SpotifyAuthHandler())