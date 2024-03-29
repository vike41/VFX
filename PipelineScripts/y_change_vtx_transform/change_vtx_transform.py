from maya import cmds
import maya.api.OpenMaya as om
import maya.OpenMayaMPx as mpx
import re

# first - area  / second - target / third - neutral
sel_items = cmds.ls(sl=True)
print ("sel_items", sel_items)
# Neutral Mesh: changeable mesh
sel_neutral = cmds.ls(sel_items, tail=1)
print ("sel_neutral", sel_neutral)

# Target Mesh: reference mesh
sel_target = cmds.ls(sel_items, tail=2)
sel_target.remove(sel_target[len(sel_target) - 1])
print ("sel_target", sel_target)

strTargetName = sel_target[0] + '.vtx'

# get a object in a World 0
getNeutralPos = cmds.xform(sel_neutral, q=True, ws=True, t=True)
getTargetPos = cmds.xform(sel_target, q=True, ws=True, t=True)

# set a object in to Changeble Mesh
print ("getNeutralPos", getNeutralPos)
cmds.xform(sel_target, t=(getNeutralPos[0], getNeutralPos[1], getNeutralPos[2]))

# Set VTXs (Area) in the list (Target Mesh)
ls_targetVtx = cmds.ls(sel_items)
ls_targetVtx.remove(ls_targetVtx[len(ls_targetVtx) - 1])
ls_targetVtx.remove(ls_targetVtx[len(ls_targetVtx) - 1])
print ("ls_target", ls_targetVtx)
# for each in ls_targetVtx:
#    print (each)
# Create a list of VTX`s as individuell
# vtx_list = cmds.ls()
test_ls = cmds.ls()
gap_ls = cmds.ls()
for each in ls_targetVtx:
    if ':' in each:
        # print ("it is ")

        # newstring = ''.join([i for i in each if i.isdigit()])
        new_result = re.findall('\[[0-9]+\:[0-9]+\]', each)
        print(new_result)
        emp_lis = []
        for z in new_result[0].split(":"):
            emp_lis.append(str(z))

        for x in range(0, len(emp_lis)):
            emp_lis[x] = emp_lis[x].replace("[", "")
            emp_lis[x] = emp_lis[x].replace("]", "")

        print(emp_lis)
        print(each)
        vtx1 = emp_lis[0]
        vtx2 = emp_lis[1]
        print(emp_lis)
        print (vtx1)
        print (vtx2)

        # Fill a gap
        vtx1Int = int(vtx1)
        vtx2Int = int(vtx2)
        print ('vtx1Int', vtx1Int)
        llist = [i for i in range(vtx1Int, vtx2Int + 1)]
        print ('llist', llist)
        gap_ls.extend(llist)

        # Transfer to Vtx String

        # ToVtxString1 = sel_target[0]  + '.vtx' + '[' + vtx1 + ']'
        # ToVtxString2 = sel_target[0]  + '.vtx' + '[' + vtx2 + ']'
        ##print ("ToVtxString1", ToVtxString1)
        # Add a string to the List
        # vtx_list.append(ToVtxString1)
        # vtx_list.append(ToVtxString2)
        # print ("vtx_list", vtx_list)
    else:
        test_ls.append(each)
        # remade: str to ind !!!

print ("strTargetName", strTargetName)
vtx_index_toStr = cmds.ls()
counter_1 = 0
# print ("!!!test_ls !!!",len(test_ls),test_ls)


# print ("!!!test_ls !!!",len(test_ls),test_ls)
ls_indVTX = []

ls_indVTX = [x for x in gap_ls if isinstance(x, int)]

print ("ls_indVTX integers", ls_indVTX)

# print ('gap_ls', gap_ls)
# print ('test_ls', len(test_ls), test_ls)


llist = cmds.ls()

for all in ls_indVTX:
    allInt = str(all)
    all1 = sel_target[0] + '.vtx' + '[' + allInt + ']'
    llist.append(all1)

llist.extend(test_ls)

print (llist)
target_VTXs = cmds.ls()
for element in reversed(llist):
    if strTargetName not in element:
        # print ("out ", element)
        llist.remove(element)

print ("llist", llist)

# sort a list

count = 0
for all in llist:
    all = all.replace(strTargetName + '[', "")
    all = all.replace("]", "")
    llist[count] = all
    count = count + 1
    print (all)

print ("llist not sorted", llist)
llist.sort(key=int)
print ("llist sorted", llist)
print (llist)
VTXs_target = cmds.ls()
for all in llist:
    allInt = str(all)
    l = strTargetName + '[' + allInt + ']'
    VTXs_target.append(l)
print (llist)
print (VTXs_target)

for element in reversed(VTXs_target):
    if strTargetName not in element:
        # print ("out ", element)
        VTXs_target.remove(element)
print (VTXs_target)

# Split ls_target and assign a new Mesh name
ls_neutralVtx = cmds.ls()
var_split = ('.')
nameTarget = sel_target[0]
# print ("nameTarget",nameTarget)
nameNeutral = sel_neutral[0]
# print ("sel_neutral", sel_neutral[0])
item = ('')
newItem = ("")

# ls_neutralVtx = [s.replace('Mesh', 'neutral') for s in ls_target_lVtx]
ls_neutralVtx = [s.replace(nameTarget, nameNeutral) for s in VTXs_target]

print ("Number of elements in llist list:", len(ls_neutralVtx))
print ("Replaced Names in ls_neutral", ls_neutralVtx)

print ("Number of elements in target list:", len(VTXs_target))
print ("Names in target list, ls_target_lVtx", VTXs_target)

# Store a Transform of VTX Target
Pos_item_target = cmds.xform(VTXs_target, q=True, t=True, ws=True)
print ("Number of elements in a llist:", len(Pos_item_target))
print ("Pos_item_target", Pos_item_target)

Pos_item_neutral = cmds.xform(ls_neutralVtx, q=True, t=True, ws=True)
print ("Number of elements in a Pos_item_neutral:", len(Pos_item_neutral))
print ("Pos_item_neutral", Pos_item_neutral)
targetPos = cmds.xform(ls_targetVtx, q=1, t=1, ws=1)
print ("targetPos", targetPos)

# counter for index in list
list_index = 0
# counter for xyz
counter = 0

# for each in Pos_item_target:
for vtx in ls_neutralVtx:
    # print ("ls_neutralVtx", ls_neutralVtx)
    # print ("ls_TargetVtx", llist)

    # print ("vtx", vtx)
    # n_Vtx = ls_neutralVtx [list_index]
    xt = Pos_item_target[counter]
    # print ("xt", xt)
    # print ("counter", counter)
    yt = Pos_item_target[counter + 1]
    # print ("yt", yt)
    # print ("counter", counter)
    zt = Pos_item_target[counter + 2]
    # print ("zt", zt)
    # print ("counter", counter)
    cmds.xform(vtx, t=(xt, yt, zt), ws=True)
    counter = counter + 3
    # print ("counter", counter)
    list_index = list_index + 1
    # print ("list_index", list_index)

# print ("netLsVtx", netLsVtx)

# Reset Transform Target Mesh back
cmds.xform(sel_target, t=(getTargetPos[0], getTargetPos[1], getTargetPos[2]))

# Recalculate normals
cmds.PolygonSoftenHarden(sel_neutral, a=180)



