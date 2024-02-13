import sys
import importlib

Dir = r'path'
if Dir not in sys.path:
    sys.path.append(Dir)

from define_texture_for_arnold import DefineTextureForArnold

new_instance = DefineTextureForArnold('TIEMetal', path=r'path')


