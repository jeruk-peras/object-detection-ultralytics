import os, shutil
from ultralytics import YOLO, RTDETR


class Object_Detection:
            
    def __predic_img(self, img, model, conf, iou, model_path):
        
        # hapus data sebelumnya 
        if os.path.exists(os.path.join('predict')):    
            shutil.rmtree(os.path.join('predict'))
            
        if model == "RT-DTER":  
            self.model_rtdtr = RTDETR(model_path)
            result = self.model_rtdtr.predict(img, conf=conf, iou=iou, save_txt=True, save=True, project="predict", name="image")
        elif model == "YOLOv10":
            self.model_yolo = YOLO(model_path)
            result = self.model_yolo.predict(img, conf=conf, iou=iou, save_txt=True, save=True, project="predict", name="image")
        elif model == "YOLOv11":
            self.model_yolo = YOLO(model_path)
            result = self.model_yolo.predict(img, conf=conf, iou=iou, save_txt=True, save=True, project="predict", name="image")        
        elif model == "YOLOv9":
            self.model_yolo = YOLO(model_path)
            result = self.model_yolo.predict(img, conf=conf, iou=iou, save_txt=True, save=True, project="predict", name="image")        
        elif model == "YOLOv8":
            self.model_yolo = YOLO(model_path)
            result = self.model_yolo.predict(img, conf=conf, iou=iou, save_txt=True, save=True, project="predict", name="image")        
        
        return result
         
    def detection_img(self, img, model, conf, iou, model_path):
        results = self.__predic_img(img, model, conf, iou, model_path)
        
        return results
