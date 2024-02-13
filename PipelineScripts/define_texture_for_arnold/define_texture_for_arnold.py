#Dev by Vitalii Kens
import maya.cmds as cmds
import pymel.core as pm
import os

class DefineTextureForArnold(object):
    # Constructor
    def __init__(self, name, path=None, targetShaderMark="MDL", targetShadingGroupMark="SG", targetShaderType="lambert",
                 textureExtensions=('.png', '.exr' , '.tx')):
        self.path = path
        self.targetShaderMark = targetShaderMark
        self.targetShaderType = targetShaderType
        self.textureExtensions = textureExtensions
        self.targetShadingGroupMark = targetShadingGroupMark
        self.name = name


        self.defineShaderWithNodes()


        #self.listFiles()
        #self.findTexMaps()


    def createShader(self):
        print("SD", self.name)
        sg = cmds.sets(name="%sSG" % self.name, empty=True, renderable=True, noSurfaceShader=True)
        return sg

    def createMaterial(self, node_type="aiStandardSurface"):
        material = cmds.shadingNode(node_type, name=self.name, asShader=True)
        return material

    def createFileTexture(self, map, name):
        p2dName = 'p2d'+ name + map
        fileTextureName = name + 'FileNode' + map
        tex = pm.shadingNode('file', name=fileTextureName, asTexture=True, isColorManaged=True)
        cmds.setAttr(tex + '.uvTilingMode', 3)
        cmds.setAttr(tex + '.colorSpace', 'Utility-Raw', type='string')

        if not pm.objExists(p2dName):
            pm.shadingNode('place2dTexture', name=p2dName, asUtility=True)

        p2d = pm.PyNode(p2dName)

        pm.connectAttr(p2d.outUV, tex.uvCoord)
        pm.connectAttr(p2d.outUvFilterSize, tex.uvFilterSize)
        pm.connectAttr(p2d.vertexCameraOne, tex.vertexCameraOne)
        pm.connectAttr(p2d.vertexUvOne, tex.vertexUvOne)
        pm.connectAttr(p2d.vertexUvThree, tex.vertexUvThree)
        pm.connectAttr(p2d.vertexUvTwo, tex.vertexUvTwo)
        pm.connectAttr(p2d.coverage, tex.coverage)
        pm.connectAttr(p2d.mirrorU, tex.mirrorU)
        pm.connectAttr(p2d.mirrorV, tex.mirrorV)
        pm.connectAttr(p2d.noiseUV, tex.noiseUV)
        pm.connectAttr(p2d.offset, tex.offset)
        pm.connectAttr(p2d.repeatUV, tex.repeatUV)
        pm.connectAttr(p2d.rotateFrame, tex.rotateFrame)
        pm.connectAttr(p2d.rotateUV, tex.rotateUV)
        pm.connectAttr(p2d.stagger, tex.stagger)
        pm.connectAttr(p2d.translateFrame, tex.translateFrame)
        pm.connectAttr(p2d.wrapU, tex.wrapU)
        pm.connectAttr(p2d.wrapV, tex.wrapV)

        return tex

    def createColorCorrection(self, name):
        #Need to fixed Normal Correction False ref in defineShaderWithNodes
        if name != 'Normal':
            CCNode = cmds.shadingNode('aiColorCorrect', asShader=True, name=name + 'CC')
        else:
            CCNode = 'noo'
        return CCNode

    def createAiNormal(self):
        NormaNode = cmds.shadingNode('aiNormalMap', asShader=True, name=self.name + 'createAiNormal')
        return NormaNode

    #-----------------Connect Nodes -------------------------
    def connectMatToShader(self, matName, shaderName):
        cmds.connectAttr("%s.outColor" % matName, "%s.surfaceShader" % shaderName)


    def defineShaderWithNodes(self):
        name=self.name
        mapList = ['BaseColor', 'Metallic', 'Rougness','Normal', 'Speclvl', 'Opacity', 'Emission' ]

        material = self.createMaterial()
        shader = self.createShader()
        self.connectMatToShader(material, shader)
        listFiles = self.listFiles()
        print ('!ListFiles',listFiles )
        existingMaps = self.defineExictingMaps(listFiles, mapList)

        for index in existingMaps:
            fileNode = self.createFileTexture(index, name)
            Correction = self.createColorCorrection(index)
            aiNormal = self.createAiNormal()
            if index == 'BaseColor':
                cmds.connectAttr("%s.outColor" % Correction, "%s.baseColor" % material)
                cmds.connectAttr("%s.outColor" % fileNode, "%s.input" % Correction)
                fileTexChanel = self.findTexMaps(listFiles, index)
                self.setNewPathFileNode (index, fileTexChanel)
                print ("BaseCreated")

            elif index == 'Metallic':
                cmds.connectAttr("%s.outAlpha" % Correction, "%s.metalness" % material)
                cmds.connectAttr("%s.outColor" % fileNode, "%s.input" % Correction)
                fileTexChanel = self.findTexMaps(listFiles, index)
                self.setNewPathFileNode (index, fileTexChanel)
                print ("MetallicCreated")

            elif index == 'Speclvl':
                cmds.connectAttr("%s.outColor" % Correction, "%s.specularColor" % material)
                cmds.connectAttr("%s.outColor" % fileNode, "%s.input" % Correction)
                fileTexChanel = self.findTexMaps(listFiles, index)
                self.setNewPathFileNode (index, fileTexChanel)
                print ("SpeclvlCreted")

            elif index == 'Rougness':
                cmds.connectAttr("%s.outAlpha" % Correction, "%s.specularRoughness" % material)
                cmds.connectAttr("%s.outColor" % fileNode, "%s.input" % Correction)
                fileTexChanel = self.findTexMaps(listFiles, index)
                self.setNewPathFileNode (index, fileTexChanel)
                print ("RougnessCreted")

            elif index == 'Opacity':
                cmds.connectAttr("%s.outColor" % Correction, "%s.opacity" % material)
                cmds.connectAttr("%s.outColor" % fileNode, "%s.input" % Correction)
                fileTexChanel = self.findTexMaps(listFiles, index)
                self.setNewPathFileNode (index, fileTexChanel)
                print ("OpacityCreted")

            elif index == 'Emission':
                cmds.connectAttr("%s.outAlpha" % Correction, "%s.emission" % material)
                cmds.connectAttr("%s.outColor" % fileNode, "%s.input" % Correction)
                cmds.connectAttr("%s.outColor" % Correction, "%s.emissionColor" % material)
                fileTexChanel = self.findTexMaps(listFiles, index)
                self.setNewPathFileNode (index, fileTexChanel)
                print ("EmissionCreted")

            elif index == 'Normal':
                cmds.connectAttr("%s.outValue" % aiNormal, "%s.normalCamera" % material)
                cmds.connectAttr("%s.outColor" % fileNode, "%s.input" % aiNormal)
                fileTexChanel = self.findTexMaps(listFiles, index)
                self.setNewPathFileNode (index, fileTexChanel)
                print ("NormalCreted")
                #createFileTexture(index)
                #cmds.connectAttr("%s.input" % Correction, "%s.outColor" % material)
                #createAiNormal
            else:
                pass

    def setNewPathFileNode(self, mapType, texName):

        fileNodeName = self.name + "FileNode" + mapType
        print ("FFF" , fileNodeName)
        definePath = self.path + '/' + texName
        print ("definePath" , definePath)
        cmds.setAttr(fileNodeName + '.fileTextureName', definePath , type='string')


    def findDummy (self):
        pass
    def assignMaps(self):
        pass
    def defineExictingMaps(self, list, maps):
        print ("LIST: ", list)
        print ("MAPS: ", maps)
        count = 0
        foundedMapsList = []

        for index in list:
            for item in maps:
                if item in index:
                    foundedMapsList.append(item)
                    count = count +1
                else:
                    pass
                    #print ("Dont")
        print ("foundedMapList", foundedMapsList)
        #TODO Remove duplicated elements
        exportetTypeMaps = set(foundedMapsList)

        print ("exportetTypeMaps", exportetTypeMaps)
        return exportetTypeMaps

    def listFiles(self):
        directory = self.path
        files = []
        for filename in os.listdir(directory):
            if os.path.isfile(os.path.join(directory, filename)):
                files.append(filename)
        print ("List Files", files)
        return files



    def findTexMaps(self, texList, textureChanel):
        itemFound = []
        print("Tex List: ", texList)
        print("textureChanel: ", textureChanel)
        for item in texList:
            if textureChanel in item and self.name in item:
                # Item found, set the flag and break out of the loop
                itemFound = item
                print ("itemFound ", itemFound)
                break
            else:
                pass
                #print('Nope')


        return itemFound



# Create an instance of the class


if __name__ == "__main__":
    new_instance = DefineTextureForArnold('TIEMetal', path=r'path')