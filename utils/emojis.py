import requests
from PIL import Image
from io import BytesIO
import os
import hashlib
from PIL import UnidentifiedImageError

def emoji_to_filename(e):
        return '-'.join(f"{ord(c):x}" for c in e) + ".png"

