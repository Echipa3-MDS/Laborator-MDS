from os import path

DISPLAY_WIDTH = 1024
DISPLAY_HEIGHT = 576
ROOT_DIR = path.join(path.dirname(path.abspath(__file__)), '..', '')
RES_DIR = path.join(ROOT_DIR, 'res', '')
RES_ANIMATIONS_DIR = path.join(RES_DIR, 'textures', 'animations', '')
RES_STATIC_TEXTURES_DIR = path.join(RES_DIR, 'textures', 'static', '')
RES_AUDIO_DIR = path.join(RES_DIR, 'audio', '')
RES_FONTS_DIR = path.join(RES_DIR, 'fonts', '')
