import maya.cmds as cmds

node = cmds.ls(selection=True)
object = node[0]
print ("node " + node[0])
print ("Object " + object)

indices = cmds.polyUVSet(node, query=True, allUVSetsIndices=True)
UVsSets = []

SetCopyFrom = 'UVmap'
SetCopyTo = 'map1'

# Get UVs Set
for i in indices[:]:
    name = cmds.getAttr(node[0] + ".uvSet[" + str(i) + "].uvSetName")
    print("Found uv set called " + name)
    UVsSets.append(name)

defaultUVSet = UVsSets[0]

restUvSets = []

print ('Objects UV Sets', UVsSets)
# Cleaning UV Set.
for i in UVsSets:
    print ("Loop")
    if i == SetCopyFrom:
        print ("Yes it is")
        cmds.polyUVSet(copy=True, nuv=SetCopyTo, uvSet=SetCopyFrom)
    else:
        if i != defaultUVSet:
            print ("Delete a " + i)
            cmds.polyUVSet(delete=True, uvSet=i)

# Get UVs Set
for i in indices[:]:
    name = cmds.getAttr(node[0] + ".uvSet[" + str(i) + "].uvSetName")
    print("Found uv set called " + name)
    restUvSets.append(name)
print (restUvSets)

deleteLast = restUvSets[1]

if restUvSets[0] != 'map1':
    cmds.polyUVSet(rename=True, newUVSet='map1', uvSet=defaultUVSet)

cmds.polyUVSet(delete=True, uvSet=deleteLast)


