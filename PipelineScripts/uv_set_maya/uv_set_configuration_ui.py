import maya.cmds as cmds


class UV_RepairWindow(object):

    # constructor
    def __init__(self):
        self.window = "UV_RepairWindow"
        self.titel = "Clean UV Sets"
        self.size = (400, 400)

        # close old window if opend
        if cmds.window(self.window, exists=True):
            cmds.deleteUI(self.window, window=True)
        # Create new Window
        self.window = cmds.window(self.window, title=self.titel, widthHeight=self.size)

        cmds.columnLayout()
        cmds.text(self.titel)
        cmds.separator(height=20, width=100)

        # Input Values for UV Set copy from
        self.UVSetCopyFrom = cmds.textFieldGrp(label='UV Set Copy from')
        self.UVSetCopyTo = cmds.textFieldGrp(label='UV Set Copy to')

        # Display New Window
        cmds.showWindow()


myWindow = UV_RepairWindow()