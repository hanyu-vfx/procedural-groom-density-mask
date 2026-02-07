import maya.cmds as cmds
import json
import os

# ---------------------------------------------
# Setup
# ---------------------------------------------

SOURCE_MESH = "test_horse_body_low"
TEMP_MESH = SOURCE_MESH + "_TMP"

REGION_DENSITY = {
    "density_body": 255,
    "density_head": 30,
    "density_leg": 30,
    "density_ear": 255,
    "density_else": 255
}

project_dir = cmds.workspace(q=True, rd=True)
output_json = os.path.join(project_dir, "horse_uv_faces_triangulated_TMP_test.json")

# ---------------------------------------------
# 1. Duplicate the source mesh
# ---------------------------------------------

if cmds.objExists(TEMP_MESH):
    cmds.delete(TEMP_MESH)

TEMP_MESH = cmds.duplicate(SOURCE_MESH, name=TEMP_MESH)[0]

# ---------------------------------------------
# 2. Recreate region sets based on the duplicated mesh
# ---------------------------------------------

TEMP_REGION_SETS = {}

for region_name, density in REGION_DENSITY.items():
    if not cmds.objExists(region_name):
        continue

    temp_set = region_name + "_TMP"
    if cmds.objExists(temp_set):
        cmds.delete(temp_set)

    TEMP_REGION_SETS[region_name] = temp_set
    cmds.sets(name=temp_set, empty=True)

    faces = cmds.sets(region_name, q=True)
    faces = cmds.filterExpand(faces, sm=34)

    for f in faces:
        # Source face → Temp face
        idx = f.split("[")[-1][:-1]
        temp_face = f"{TEMP_MESH}.f[{idx}]"
        if cmds.objExists(temp_face):
            cmds.sets(temp_face, add=temp_set)

# ---------------------------------------------
# 3. Triangulate the duplicated mesh
# ---------------------------------------------

cmds.polyTriangulate(TEMP_MESH, ch=False)

# ---------------------------------------------
# 4. Extract UV data from the triangulated mesh
# ---------------------------------------------

export_data = []

for region_name, density in REGION_DENSITY.items():
    temp_set = TEMP_REGION_SETS.get(region_name)
    if not temp_set or not cmds.objExists(temp_set):
        continue

    faces = cmds.sets(temp_set, q=True)
    faces = cmds.filterExpand(faces, sm=34)
    if not faces:
        continue

    for face in faces:
        uvs = cmds.polyListComponentConversion(face, toUV=True)
        uvs = cmds.filterExpand(uvs, sm=35)

        if not uvs or len(uvs) != 3:
            continue

        uv_coords = []
        for uv in uvs:
            u, v = cmds.polyEditUV(uv, q=True)
            uv_coords.append([u, v])

        export_data.append({
            "region": region_name,
            "density": density,
            "uvs": uv_coords
        })

# ---------------------------------------------
# 5. Export data to JSON
# ---------------------------------------------

with open(output_json, "w") as f:
    json.dump(export_data, f, indent=4)

print("UV triangle data export completed")
print(output_json)

# ---------------------------------------------
# 6. Clean up temporary mesh and sets
# ---------------------------------------------

cmds.delete(TEMP_MESH)
for s in TEMP_REGION_SETS.values():
    if cmds.objExists(s):
        cmds.delete(s)

print("Temporary mesh and sets cleaned up")
