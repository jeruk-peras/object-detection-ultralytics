import torch
import streamlit as st
from PIL import Image
import json 
import os

torch.classes.__path__ = []

# classs detection
import model_detection
detektsi = model_detection.Object_Detection()

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
def model_save(model_name, model_path, model, file_type, file_size):
    with open('models.json', 'r') as openfile:
        json_object = json.load(openfile)
    
    model_save = [
        {
            "model_name": model_name,
            "model_path": model_path,
            "model": model,
            "file_type": file_type,
            "file_size": file_size,
        }
    ]
    json_object += model_save

    json_object = json.dumps(json_object, indent=4)
    # Writing to sample.json
    with open("models.json", "w") as outfile:
        outfile.write(json_object)
        
# mengambil data di models.json
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
st.title('Object Detection')
st.write('## Ultralytic Model Aplication')    
# st.write("Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.")


# end body Home

# sidebar
st.sidebar.title('Ultralytic Model Aplication')

# detect objek
st.sidebar.write('## Detect Object')
my_models = models_data() # list data model
enable_camera = st.sidebar.checkbox("Detect Form Camera :camera:")
selectbox = st.sidebar.selectbox("Select your model...",(my_models), index=None,placeholder="Select your model...",)
confidence =st.sidebar.slider("Confidence Threshold", 0.00, 1.00, value=0.25)
iou =st.sidebar.slider("IoU Threshold", 0.00, 1.00, value=0.70)

MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
UPLOAD_FOLDER = "uploads/"

if enable_camera == True :
    # col1, col2 = st.columns(2)
    # col1.write("Original Image :camera:")
    # menempilkan kamera
    picture = st.camera_input("Take a image :camera:", disabled=not enable_camera)
    # col2.write("Predict Image :wrench:")
    
    if picture: # jika gambar belum diambil
        
        if selectbox is None: #jika model belum dipilih
            st.sidebar.error("Please select your model first")
        else:
            # menyimpan gambar ke folder uploads
            image = Image.open(picture)        
            file_path = os.path.join(UPLOAD_FOLDER, picture.name)
            image.save(file_path)
            
            # mengambil data model
            model_select = selectbox.split('|')
            model_name = model_select[1]
            model = model_select[0]
            
            data = get_model(name=model_name, modell=model)
            print(data['model'], data['path'])
            
            # memdeteksi gambar
            detektsi.detection_img(img=file_path, conf=confidence, iou=iou, model=data['model'], model_path=data['path'])
            
            # hapus file uploads
            os.remove(os.path.join(UPLOAD_FOLDER, picture.name))
            
            # menampilkan hasil presiksi yang ada difolder predict/predict/
            fixed = Image.open('predict/predict/'+picture.name)
            st.write("Predict Image :wrench:")
            st.image(fixed)
            st.markdown("\n")
        
        
else:
    # upload gambar 
    detect_image = st.sidebar.file_uploader("Upload an image", type=["jpeg"])
    
    # deteksi gambar
    def detection(upload):
        tittle, title2 = st.columns([7,1])
        col1, col2 = st.columns(2)
        
        # meyimpan gambar ke folder uploas
        image = Image.open(upload)
        file_path = os.path.join(UPLOAD_FOLDER, upload.name)
        image.save(file_path)
        
        # menampilkan gambar 
        col1.write("Original Image :camera:")
        col1.image(image)
        
        # meganbil data model
        model_select = selectbox.split('|')
        model_name = model_select[1]
        model = model_select[0]
        
        data = get_model(name=model_name, modell=model)
        print(data['model'], data['path'])
        
        # deteksi gambar
        detek = detektsi.detection_img(img=file_path, conf=confidence, iou=iou, model=data['model'], model_path=data['path'])
        print(detek[0])
        # print(round(detek[0].speed['preprocess'], 1))
        # print(round(detek[0].speed['inference'], 1))
        # print(round(detek[0].speed['postprocess'], 1))
        
        preprocess = round(detek[0].speed['preprocess'], 1)
        inference = round(detek[0].speed['inference'], 1)
        postprocess = round(detek[0].speed['postprocess'], 1)
        
        tittle.write('### ' + model + " " + model_name)
        tittle.write('Speeds : Preprocess %sms, Inference %sms, Postprocess %sms' % (preprocess, inference, postprocess) )
        
        # hapus file uploads
        os.remove(os.path.join(UPLOAD_FOLDER, upload.name))
        
        # menampilkan hasil prediksi
        fixed = Image.open('predict/image/'+upload.name)
        col2.write("Predict Image :wrench:")
        col2.image(fixed)
        st.sidebar.markdown("\n")
        # st.sidebar.download_button("Download fixed image", convert_image(fixed), "fixed.png", "image/png")        
    
    if detect_image is not None: # jika gambar belum diupload
        if selectbox is None: #jika model belum dipilih
            st.sidebar.error("Please select your model first")
        elif detect_image.size > MAX_FILE_SIZE: 
            st.sidebar.error("The uploaded file is too large. Please upload an image smaller than 100MB.")
        else:
            detection(upload=detect_image) # deteksi

# detect_image = detect_image
# end detect


st.sidebar.write('---------------------------------')


# upload model

with st.sidebar.form('form_upload', border=False):
    st.write('## Upload Models')
    models = [
        "YOLOv8",
        "YOLOv9",
        "YOLOv10",
        "YOLOv11",
        "RT-DTER",
    ]

    # dropdown model
    selectmodel = st.selectbox("Select your model...",(models), index=None,placeholder="Select your model...",)

    model_name = st.text_input('Model Name', placeholder='Model Name')
    model_file = st.file_uploader("Upload an Model",)
    
    submitted = st.form_submit_button("Submit")
    
    if submitted: # jika form di submit
        MAX_FILE_SIZE = 100 * 1024 * 1024  # 5MB
        MODEL_FOLDER = "models/"

        # upload model
        def upload_model(upload, model, model_name):
            if os.path.exists("models/"+upload.name) : # jika file sudah ada
                st.error("File name is already. Please rename file and upload.")
            else :
                # upload model ke folder /models
                filename = upload.name         
                with open(os.path.join(MODEL_FOLDER, filename),"wb") as f: 
                    f.write(upload.getbuffer())   
                # simpan data model ke file models.json
                model_save(model=model, model_path=MODEL_FOLDER+''+filename, model_name=model_name, file_type=upload.type, file_size=upload.size)
                # informasi inteface
                file_detail = {'model_name': model_name, 'model':model, 'file_name' : upload.name, 'file_type': upload.type, "file_size": upload.size}
                st.write(file_detail)
                st.success("Model Uploaded")
            
        if model_file is not None: # jika model belum di upload
            if model_file.size > MAX_FILE_SIZE: # jika file terlalu besar
                st.error("The uploaded file is too large. Please upload an image smaller than 100MB.")
            else:
                # upload model
                upload_model(upload=model_file, model=selectmodel, model_name=model_name)

# end upload model
# end sidebar


# body
# dashborad
if enable_camera is False and detect_image is None:
    col1, col2 = st.columns(2)
    image = Image.open('demo-ori.jpg')
    col1.write("Original Image :camera:")
    col1.image(image)

    fixed = Image.open('demo-pred.jpg')
    col2.write("Predict Image :wrench:")
    col2.image(fixed)
    
    
    def delete_model(model_name, model, model_path):
        
        with open('models.json', 'r') as openfile:
            json_object = json.load(openfile)
    
        model_save = []
        for row in json_object:
            
            if row['model_name'] == model_name and row['model'] == model and row['model_path'] == model_path :
                
                if os.path.exists(row['model_path']) : 
                    os.remove(row['model_path'])
                    
                file_detail = {'model_name': model_name, 'model':model, 'file_name' : model_path, 'file_type': row['file_type'], "file_size": row['file_size']}
                st.write(file_detail)
                st.success("Model Deleted")
                continue
            else:
                model_save += [
                    {
                        "model_name": row['model_name'],
                        "model_path": row['model_path'],
                        "model": row['model'],
                        "file_type": row['file_type'],
                        "file_size": row['file_size'],
                    }
                ]
            
        print(model_save)

        json_object = json.dumps(model_save, indent=4)
        # Writing to sample.json
        with open("models.json", "w") as outfile:
            outfile.write(json_object)
            
    st.write('## Tabel Models')
    no, model_name, model, file_type, file_size, btn_del = st.columns([1, 3, 1, 3, 1, 1])
    def table_models():
        with open('models.json', 'r') as openfile:
            json_object = json.load(openfile)
            
        i = '1'
        j = 1
        no.write('No')
        model_name.write("Model Name")
        model.write('Model')
        file_type.write('File Type')
        file_size.write('File Size')
        btn_del.write('act')
        
        for row in json_object:
            no.button('%d' %j, key=row['model_path']+(i+'9'), type="tertiary")
            model_name.button(row['model_name'], key=row['model_path']+(i+'1'), type="tertiary")
            model.button(row['model'], key=row['model_path']+(i+'2'), type="tertiary")
            file_type.button(row['file_type'], key=row['model_path']+(i+'5'), type="tertiary")
            file_size.button('%d' %row['file_size'], key=row['model_path']+(i+'6'), type="tertiary")
            btn_del.button('Delete', key=row['model_path']+(i+'3'), type="tertiary", on_click= delete_model, args= [row['model_name'], row['model'], row['model_path']])
            
            i += '1'
            j += 1
        # return models
    
    table_models()
