import pymel.core as pm
class ResetPerspectiveCamera():
    def __init__(self, perp_camera):
        self.perp_camera = perp_camera

    def reset_persp_cam(self):
        if pm.objExists("|persp"):
            perspective_camera = pm.PyNode("|persp")
            pm.camera(perspective_camera, e=True, startupCamera = False)
            pm.delete(perspective_camera)
    def create_new_perp_camera(self):
        new_perspective_camera = pm.camera()
        new_perspective_camera[0].rename("|persp")
        new_perspective_camera[0].hide()
        pm.camera(new_perspective_camera[0], e=True, startupCamera = True)
        pm.reorder(new_perspective_camera[0], front=True)

if __name__ == "__main__":
    RPC = ResetPerspectiveCamera('camera')
    RPC.reset_persp_cam()
    RPC.create_new_perp_camera()