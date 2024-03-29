import sys
import importlib

Dir = r'path'
if Dir not in sys.path:
    sys.path.append(Dir)

from reset_persp_cam import ResetPerspectiveCamera

RPC = ResetPerspectiveCamera('camera')
RPC.reset_persp_cam()
RPC.create_new_perp_camera()