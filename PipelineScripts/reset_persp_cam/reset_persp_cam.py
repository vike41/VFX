import pymel.core as pm
def reset_persp_cam():
    if pm.objExists("|persp"):
        perspective_camera = pm.PyNode("|persp")
        pm.camera(perspective_camera, e=True, startupCamera = False)
        pm.delete(perspective_camera)

    new_perspective_camera = pm.camera()
    new_perspective_camera[0].rename("|persp")
    new_perspective_camera[0].hide()
    pm.camera(new_perspective_camera[0], e=True, startupCamera = True)
    pm.reorder(new_perspective_camera[0], front=True)
