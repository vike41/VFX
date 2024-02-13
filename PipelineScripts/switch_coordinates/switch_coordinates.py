import maya.cmds as cmds


def MoveToAxe():
    node = cmds.ls(selection=True)
    newTransform = [-1.431, 5.835, 33.528]
    newRotation = [0, 26.5, 0]
    print ("Node Name is: ", node)

    #cmds.xform(node, ws = True, ro = (newRotation[0], newRotation[1],  newRotation[2]))
    #cmds.xform(node, ws = True, rt = (newTransform[0],newTransform[1], newTransform[2])

    cmds.move (newTransform[0],newTransform[1], newTransform[2], node)
    cmds.rotate (newRotation[0], newRotation[1],  newRotation[2], node)

#MoveToAxe()

def MoveToOrignAxe():
    node = cmds.ls(selection=True)
    newTransform = [0, 0, 0]
    newRotation = [0, 0, 0]
    print ("Node Name is: ", node)

    #cmds.xform(node, ws = True, ro = (newRotation[0], newRotation[1],  newRotation[2]))
    #cmds.xform(node, ws = True, rt = (newTransform[0],newTransform[1], newTransform[2])

    cmds.move (newTransform[0],newTransform[1], newTransform[2], node)
    cmds.rotate (newRotation[0], newRotation[1],  newRotation[2], node)

MoveToOrignAxe()
