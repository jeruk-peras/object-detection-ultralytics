# import torch
import streamlit as st
from PIL import Image
import json 
import os

# torch.classes.__path__ = []

# classs detection
# import model_detection
import os, shutil
from ultralytics import YOLO, RTDETR

class Object_Detection:
            
    def __predic_img(self, img, model, model_path):
        
        # hapus data sebelumnya 
        if os.path.exists(os.path.join('predict')):    
            shutil.rmtree(os.path.join('predict'))
            
        if model == "RT-DTER":
            self.model_rtdtr = RTDETR(model_path)
            result = self.model_rtdtr.predict(img, conf=0.5, iou=0.7, save_txt=True, save=True, project="predict")
        elif model == "YOLOv10":
            self.model_yolo = YOLO(model_path)
            result = self.model_yolo.predict(img, conf=0.5, iou=0.7, save=True, project="predict")
        elif model == "YOLOv11":
            self.model_yolo = YOLO(model_path)
            result = self.model_yolo.predict(img, conf=0.5, iou=0.7, save=True, project="predict")        
        elif model == "YOLOv9":
            self.model_yolo = YOLO(model_path)
            result = self.model_yolo.predict(img, conf=0.5, iou=0.7, save=True, project="predict")        
        elif model == "YOLOv8":
            self.model_yolo = YOLO(model_path)
            result = self.model_yolo.predict(img, conf=0.5, iou=0.7, save=True, project="predic")        
        
        return result
         
    def detection_img(self, img, model, model_path):
        results = self.__predic_img(img, model, model_path)
        
        return results


detektsi = Object_Detection()

# ===========================
# function
# load model
def models_data():
    with open('models.json', 'r') as openfile:
        json_object = json.load(openfile)
    models = []
    for row in json_object:
        models += [ row['model'] + "|" + row['model_name'] ]
    return models

# upload model
def model_save(model_name, model_path, model):
    with open('models.json', 'r') as openfile:
        json_object = json.load(openfile)
    
    model_save = [
        {
            "model_name": model_name,
            "model_path": model_path,
            "model": model
        }
    ]
    json_object += model_save

    json_object = json.dumps(json_object, indent=4)
    # Writing to sample.json
    with open("models.json", "w") as outfile:
        outfile.write(json_object)
        
def get_model(name, modell):
    with open('models.json', 'r') as openfile:
        data = json.load(openfile)
    
    model_name = name
    model = modell

    data_model = {}
    for row in data:
        if  row["model"] == model and row["model_name"] == model_name:
            data_model['path'] = row['model_path']
            data_model['model'] = row['model']
            break;

    return data_model

# ======================================


st.set_page_config(page_title="Ultralytic Model Aplication", layout="wide")
# body Home
st.title('Objec Detection')
st.write('## Ultralytic Model Aplication')    
# st.write("Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.")


# end body Home

# sidebar
st.sidebar.title('Ultralytic Model Aplication')

# detect
st.sidebar.write('## Detect Objeck')
my_models = models_data()
selectbox = st.sidebar.selectbox(
    "Select your model...",
    (my_models), 
    index=None,
    placeholder="Select your model...",
)
detect_image = st.sidebar.file_uploader("Upload an image", type=["jpeg"])

MAX_FILE_SIZE = 100 * 1024 * 1024  # 5MB
UPLOAD_FOLDER = "uploads/"

def detection(upload):
    
    
    image = Image.open(upload)
    col1.write("Original Image :camera:")
    col1.image(image)
    
    model_select = selectbox.split('|')
    model_name = model_select[1]
    model = model_select[0]
    
    tittle.write('### ' + model + " " + model_name)
    
    file_path = os.path.join(UPLOAD_FOLDER, upload.name)
    image.save(file_path)
    
    data = get_model(name=model_name, modell=model)
    print(data['model'], data['path'])
    
    detektsi.detection_img(img=file_path, model=data['model'], model_path=data['path'])
    
    # hapus file uploads
    os.remove(os.path.join(UPLOAD_FOLDER, upload.name))
    
    
    fixed = Image.open('predict/predict/'+upload.name)
    col2.write("Predict Image :wrench:")
    col2.image(fixed)
    st.sidebar.markdown("\n")
    
    # st.sidebar.download_button("Download fixed image", convert_image(fixed), "fixed.png", "image/png")

tittle, titttle = st.columns(2)
col1, col2 = st.columns(2)

if detect_image is not None:
    if detect_image.size > MAX_FILE_SIZE:
        st.sidebar.error("The uploaded file is too large. Please upload an image smaller than 100MB.")
    else:
        detection(upload=detect_image)
        
# end detect


st.sidebar.write('---------------------------------')



# upload model
st.sidebar.write('## Upload Models')

models = [
    "YOLOv8",
    "YOLOv9",
    "YOLOv10",
    "YOLOv11",
    "RT-DTER",
]

selectmodel = st.sidebar.selectbox(
    "Select your model...",
    (models), 
    index=None,
    placeholder="Select your model...",
)

model_name = st.sidebar.text_input('Model Name', placeholder='Model Name')
model_file = st.sidebar.file_uploader("Upload an Model",)

MAX_FILE_SIZE = 100 * 1024 * 1024  # 5MB
MODEL_FOLDER = "models/"

def upload_model(upload, model, model_name):
    if os.path.exists("models/"+upload.name) : 
        st.sidebar.error("File name is already. Please rename file and upload.")
    else :
        # id = uuid.uuid4()
        filename = upload.name         
        # filename = id + "." + filename.split('.')[1]
        with open(os.path.join(MODEL_FOLDER, filename),"wb") as f: 
            f.write(upload.getbuffer())   
        model_save(model=model, model_path=MODEL_FOLDER+''+filename, model_name=model_name)
        
        file_detail = {'model_name': model_name, 'model':model, 'file_name' : upload.name, 'file_type': upload.type, "file_size": upload.size}
        st.sidebar.write(file_detail)
        st.sidebar.success("Model Uploaded")
    

if model_file is not None:
    if model_file.size > MAX_FILE_SIZE:        
        st.sidebar.error("The uploaded file is too large. Please upload an image smaller than 100MB.")
    else:
        upload_model(upload=model_file, model=selectmodel, model_name=model_name)

# end upload model
# end sidebar


# body

if detect_image is None:
    col1, col2 = st.columns(2)
    image = Image.open('demo-ori.jpg')
    col1.write("Original Image :camera:")
    col1.image(image)

    fixed = Image.open('demo-pred.jpg')
    col2.write("Predict Image :wrench:")
    col2.image(fixed)
