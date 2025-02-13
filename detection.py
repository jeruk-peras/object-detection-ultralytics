import json
import os

# save
with open('models.json', 'r') as openfile:
    json_object = json.load(openfile)
    
model_save = [
    {
        "model_name": "Penyakit Tomat",
        "model_path": "model/best.pt",
        "model": "Yolov8"
    }
]
# json_object += model_save

# json_object = json.dumps(json_object, indent=4)
# # Writing to sample.json
# with open("models.json", "w") as outfile:
#     outfile.write(json_object)
    
# print(json_object)




with open('models.json', 'r') as openfile:
    json_object = json.load(openfile)
    
# load
models = []

for row in json_object:
    models += [ row['model_name'] + " " + row['model_path'] + " " + row['model'] ]
    
print(models)


if os.path.exists("models/yolo11n.pt") : 
    print('ok')
else :
    print('no')
    
    
with open('models.json', 'r') as openfile:
    data = json.load(openfile)
    
model_name = "Tomato Leaf"
model = "YOLOv11"

data_model = {}
for row in data:
    models += [ row['model_name'] + " " + row['model_path'] + " " + row['model'] ]

    if  row["model"] == model and row["model_name"] == model_name:
        data_model['path'] = row['model_path']
        data_model['name'] = row['model_name']
        break;

print(data_model)
    
    
    