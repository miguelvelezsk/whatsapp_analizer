import glob
from setuptools import setup

APP = ['main.py']
APP_NAME = "Datos de Amor"

DATA_FILES = [
    ('assets', ['assets/icon.avif', 'assets/icon.ico']),
    ('emojis_images', glob.glob('emojis_images/*')),
    ('music', ['music/Hostage.mp3']),
]

OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'assets/icon.icns',
    'packages': ['matplotlib', 'PySide6', 'PIL'],
    'includes': ['random', 'sys', 'os', 'pathlib', 'io', 're', 'collections', 'hashlib'],
    'resources': [
        'assets',
        'emojis_images',
        'file',
        'music',
        'services',
        'styles',
        'ui',
        'utils',
    ],
}

setup(
    app=APP,
    name=APP_NAME,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)

