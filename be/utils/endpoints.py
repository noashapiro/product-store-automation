import os

def get_url(suffix: str = None):
    base_url = os.environ.get("BASE_URL", "http://localhost:3000")
    if suffix is None:
        return base_url
    return base_url + suffix

