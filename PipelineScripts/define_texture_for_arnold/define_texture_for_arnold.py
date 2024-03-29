#Dev by Vitalii Kens
import maya.cmds as cmds
import pymel.core as pm
import os

class DefineTextureForArnold(object):
    # Constructor
    def __init__(self, name, path=None, target_shader_mark="HS", target_shading_group_mark="SGM", target_shader_type=("aiStandartSurface", "lambert"),
                 texture_extensions=('.png', '.exr', '.tx'), maps=('BaseColor', 'Metallic', 'Rougness', 'Normal', 'Speclvl', 'Opacity', 'Emission')):

        self.path = path
        self.targetShaderMark = target_shader_mark
        self.targetShaderType = target_shader_type
        self.textureExtensions = texture_extensions
        self.targetShadingGroupMark = target_shading_group_mark
        self.name = name
        self.maps = maps

    def create_shader(self):
        sg = cmds.sets(name="%sSG" % self.name, empty=True, renderable=True, noSurfaceShader=True)
        return sg

    def create_material(self, node_type="aiStandardSurface"):
        material = cmds.shadingNode(node_type, name=self.name, asShader=True)
        return material

    def create_file_texture(self, map, name):
        p2d_name = 'p2d'+ name + map
        file_texture_name = name + 'FileNode' + map
        tex = pm.shadingNode('file', name=file_texture_name, asTexture=True, isColorManaged=True)
        cmds.setAttr(tex + '.uvTilingMode', 3)
        cmds.setAttr(tex + '.colorSpace', 'Utility-Raw', type='string')

        if not pm.objExists(p2d_name):
            pm.shadingNode('place2dTexture', name=p2d_name, asUtility=True)

        p2d = pm.PyNode(p2d_name)

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

    def create_color_correction(self, name):
        #Need to fixed Normal Correction False ref in defineShaderWithNodes
        if name != 'Normal':
            cc_node = cmds.shadingNode('aiColorCorrect', asShader=True, name=name + 'CC')
        else:
            cc_node = 'noo'
        return cc_node

    def create_ai_normal(self):
        normal_node = cmds.shadingNode('aiNormalMap', asShader=True, name=self.name + 'createAiNormal')
        return normal_node

    #-----------------Connect Nodes -------------------------
    def connect_mat_to_shader(self, matName, shaderName):
        cmds.connectAttr("%s.outColor" % matName, "%s.surfaceShader" % shaderName)

    def define_shader_with_nodes(self):
        #TODO Repair Logic, make more configurable
        name=self.name
        for index in existing_maps:
            fileNode = self.create_file_texture(index, name)
            Correction = self.create_color_correction(index)
            aiNormal = self.create_ai_normal()
            if index == 'BaseColor':
                cmds.connectAttr("%s.outColor" % Correction, "%s.baseColor" % material)
                cmds.connectAttr("%s.outColor" % fileNode, "%s.input" % Correction)
                fileTexChanel = self.find_tex_maps(list_files, index)
                self.set_new_path_file_node (index, fileTexChanel)
                print ("Base is Created")

            elif index == 'Metallic':
                cmds.connectAttr("%s.outAlpha" % Correction, "%s.metalness" % material)
                cmds.connectAttr("%s.outColor" % fileNode, "%s.input" % Correction)
                fileTexChanel = self.find_tex_maps(list_files, index)
                self.set_new_path_file_node (index, fileTexChanel)
                print ("Metallic is Created")

            elif index == 'Speclvl':
                cmds.connectAttr("%s.outColor" % Correction, "%s.specularColor" % material)
                cmds.connectAttr("%s.outColor" % fileNode, "%s.input" % Correction)
                fileTexChanel = self.find_tex_maps(list_files, index)
                self.set_new_path_file_node (index, fileTexChanel)
                print ("Speclvl is Created")

            elif index == 'Rougness':
                cmds.connectAttr("%s.outAlpha" % Correction, "%s.specularRoughness" % material)
                cmds.connectAttr("%s.outColor" % fileNode, "%s.input" % Correction)
                fileTexChanel = self.find_tex_maps(list_files, index)
                self.set_new_path_file_node (index, fileTexChanel)
                print ("Roughness is Created")

            elif index == 'Opacity':
                cmds.connectAttr("%s.outColor" % Correction, "%s.opacity" % material)
                cmds.connectAttr("%s.outColor" % fileNode, "%s.input" % Correction)
                fileTexChanel = self.find_tex_maps(list_files, index)
                self.set_new_path_file_node (index, fileTexChanel)
                print ("Opacity is Created")

            elif index == 'Emission':
                cmds.connectAttr("%s.outAlpha" % Correction, "%s.emission" % material)
                cmds.connectAttr("%s.outColor" % fileNode, "%s.input" % Correction)
                cmds.connectAttr("%s.outColor" % Correction, "%s.emissionColor" % material)
                fileTexChanel = self.find_tex_maps(list_files, index)
                self.set_new_path_file_node (index, fileTexChanel)
                print ("Emission is Created")

            elif index == 'Normal':
                cmds.connectAttr("%s.outValue" % aiNormal, "%s.normalCamera" % material)
                cmds.connectAttr("%s.outColor" % fileNode, "%s.input" % aiNormal)
                fileTexChanel = self.find_tex_maps(list_files, index)
                self.set_new_path_file_node (index, fileTexChanel)
                print ("Normal is created")
                #createFileTexture(index)
                #cmds.connectAttr("%s.input" % Correction, "%s.outColor" % material)
                #createAiNormal
            else:
                print ("implement Error")
                return False
            return True

    def set_new_path_file_node(self, map_type, tex_name):
        file_node_name = self.name + "FileNode" + map_type
        define_path = self.path + '/' + tex_name
        cmds.setAttr(file_node_name + '.fileTextureName', define_path , type='string')

    def define_exicting_maps(self, maps_list):
        count = 0
        founded_maps_list = []

        for index in maps_list:
            for item in self.maps:
                if item in index:
                    founded_maps_list.append(item)
                    count = count + 1 # TODO Remove that dirt

                else:
                    pass
                    #print ("Dont")
        print ("foundedMapList", founded_maps_list)
        #TODO Remove duplicated elements
        exportet_type_maps = set(founded_maps_list)

        return exportet_type_maps

    def list_files(self):
        directory = self.path
        files = []
        for filename in os.listdir(directory):
            if os.path.isfile(os.path.join(directory, filename)):
                files.append(filename)
        print ("List Files", files)
        return files

    def find_tex_maps(self, tex_list, texture_chanel):
        #TODO make it clean
        item_found = []
        try:
            for item in tex_list:
                if texture_chanel in item and self.name in item:
                    # Item found, set the flag and break out of the loop
                    item_found = item
                    break
                else:
                    print('Nope')
        except ValueError:
            print ("can`t find any Textures")

        return item_found
# Create an instance of the class

if __name__ == "__main__":
    DTFA = DefineTextureForArnold('TIEMetal', path=r'path')

    shader = DTFA.create_shader()
    material = DTFA.create_material()
    DTFA.connect_mat_to_shader(material, shader)

    listed_files = DTFA.list_files()
    existing_Maps = DTFA.define_exicting_maps(listed_files)

    create_instance = DTFA.define_shader_with_nodes()