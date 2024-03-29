import maya.cmds as cmds
import pymel.core as pm


class DeformEdgeFlow():

    def __init__(self,
                 input_component=None):
        self.input_component = input_component

    def select_component(self):
        component = cmds.ls(selection=True, flatten=True)
        print('component', component)
        return component

    @staticmethod
    def convert_into_vtx(input_list):
        selected_vertices = cmds.polyListComponentConversion(input_list, fromEdge=True, toVertex=True)
        return selected_vertices

    @staticmethod
    def convert_into_edges(input_list):
        selected_edges = cmds.polyListComponentConversion(input_list, toEdge=True)
        return selected_edges

    @staticmethod
    def convert_into_faces(input_list):
        selected_faces = cmds.polyListComponentConversion(input_list, toFace=True)
        return selected_faces

    @staticmethod
    def convert_vrt_numbers(vrt_list):
        list_with_indices = []
        for item in vrt_list:
            if ':' in item:
                result = item.split('[', 1)
                chose_second_element = result[1]
                conv_into_string = str(chose_second_element[1])
                print('d', conv_into_string)
                remove_char = conv_into_string.replace('[', '').replace(']', '')
                list_with_indices.append(remove_char)
            return list_with_indices

    @staticmethod
    def fill_hole_between_vtx(input_list):
        print('input_list', input_list)
        for item in input_list:
            if ':' in item:
                split_item = item.split(':')
                print(split_item)

    @staticmethod
    def create_curve(selected_components):
        curve_name = 'Test'
        vertices = selected_components[0], selected_components[-1]
        print ('vertices', vertices)
        poly_curve = cmds.curve(d=1, p=vertices, n=curve_name)
        return poly_curve


if __name__ == "__main__":
    DEF = DeformEdgeFlow()
    selected_components = DEF.select_component()
    vrt_list = DEF.convert_into_vtx(selected_components)
    vtx_numbers = DEF.convert_vrt_numbers(vrt_list)
    gap = DEF.fill_hole_between_vtx(vtx_numbers)
    # create = DEF.create_curve(vrt_list)