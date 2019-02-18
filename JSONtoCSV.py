import json

# this could be hardcoded... but making it dynamic is more fun!
def read_project_names_txt(filepath):
	# open file
	file = open(filepath, 'r', encoding='utf-8')

	# fill list of project_names
	project_names = []
	for project in file:
		project_names.append(project)

	# when done, close file and return project list
	file.close()
	return project_names

def read_settings_data_json(jsonfilepath, txtfilepath):
	print("running read_settings_data...")
	# open json, read from it, close it
	file = open(jsonfilepath, 'r', encoding='utf-8')
	data = json.load(file)
	file.close()


	# iterate through projects and add them to the csv
	project_names = read_project_names_txt(txtfilepath)
	counter = 0

	for project in project_names:
		project = project.rstrip()
		for user in data[project]["members"]:
			print("user is", user["name"])
			counter = counter + 1

	print("counter is", counter)

	# #
	# for mats in data['Materials']:
	# 	CreateImportedMatDefaults(mats['Name'])

	# for obj in data['Objects']:
	# 	if obj['Type'] in 'MESH':
	# 		if obj['Name'] in bpy.data.objects: # will work with brender objects ('000000_name')
	# 			ApplyMaterialToAll.general(obj['Name'],obj['Material'])
			
	# 	if obj['Type'] in 'CURVE' and obj['Name'].endswith('.wireframe'):
	# 		# does the wireframe exist yet?
	# 		# only do wireframe creation once
	# 		if GetCommonName(obj['Parent'].split("_",1)[1]) not in BRENDER_wf_names:
	# 			# wireframes havent been documented, create
	# 			# assuming only one wireframed object
	# 			myaddon.wireframe_obj_string = GetCommonName(obj['Parent'].split("_",1)[1])
	# 			myaddon.wf_bevel_depth = obj['Wireframe Depth']
	# 			myaddon.wf_bevel_resolution = obj['Wireframe Resolution']
	# 			myaddon.wf_offset = obj['Wireframe Offset']
	# 			myaddon.wf_extrude = obj['Wireframe Extrude']
	# 			WireframeOverlay.apply_wireframe(myaddon.wireframe_obj_string)
	# 			BRENDER_wf_names.append(myaddon.wireframe_obj_string)
	# 			# apply material
	# 			ApplyMaterialToAll.general(obj['Name'],obj['Material'])
	# 		else:
	# 			# already created
	# 			continue
	# 		# bpy.data.objects[obj['Name']].active_material = obj['Material']
	# 	if obj['Type'] in 'LAMP':
	# 		if obj['Name'] == 'brenderDefaults.Lamp':
	# 			lightSetup2D.execute(bpy.context, bpy.context)
	# 		else:
	# 			# create lamp
	# 			# NOTE: Lamp Creation doesnt include intensity, radius, etc at the moment
	# 			bpy.ops.object.lamp_add()
	# 			new_obj = bpy.context.active_object
	# 			new_obj.data.type=obj['Sub Type']
	# 			new_obj.name = obj['Name']
	# 			new_obj.location = mathutils.Vector((obj['Loc X'], obj['Loc Y'], obj['Loc Z']))
	# 			new_obj.rotation_euler = mathutils.Euler((obj['Euler 0'], obj['Euler 1'], obj['Euler 2']), obj['Euler Order'])
	# 			new_obj.select = False

	# 	if obj['Type'] in 'CAMERA':
	# 		if obj['Name'] == 'brenderDefaults.Camera':
	# 			cameraSetup2D.execute(bpy.context, bpy.context)
	# 		else:
	# 			# create lamp
	# 			# NOTE: Lamp Creation doesnt include intensity, radius, etc at the moment
	# 			bpy.ops.object.camera_add()
	# 			new_obj = bpy.context.active_object
	# 			new_obj.data.type=obj['Sub Type']
	# 			new_obj.name = obj['Name']
	# 			new_obj.location = mathutils.Vector((obj['Loc X'], obj['Loc Y'], obj['Loc Z']))
	# 			new_obj.rotation_euler = mathutils.Euler((obj['Euler 0'], obj['Euler 1'], obj['Euler 2']), obj['Euler Order'])
	# 			new_obj.select = False
	

	return

# main function
if __name__ == "__main__":
	jsonfilename = "output.json"
	txtfilename = "projects.txt"
	outputfilename = "projectlist.csv"

	read_settings_data_json(jsonfilename, txtfilename);