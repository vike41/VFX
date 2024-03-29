import sys
import importlib

Dir = r'path'
if Dir not in sys.path:
    sys.path.append(Dir)

from define_texture_for_arnold import DefineTextureForArnold

DTFA = DefineTextureForArnold('TIEMetal',
                              path=r'path')

shader = DTFA.create_shader()
material = DTFA.create_material()
DTFA.connect_mat_to_shader(material, shader)

listed_files = DTFA.list_files()
existing_Maps = DTFA.define_exicting_maps(listed_files)

DTFA.define_shader_with_nodes(existing_Maps, listed_files)