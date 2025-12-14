import ultralytics
from ultralytics import YOLO
import cv2
from pyzbar.pyzbar import decode , ZBarSymbol
import numpy as np

class Decoder():
    def __init__(self):
        self.yolo_model=YOLO('trained_yolo_model/weights/best.pt')
    
    def decode(self,product_image):
        barcode_img=self.get_barcode_image(product_image)
        decoded_info=decode(barcode_img)
        if len(decoded_info)==0:
            sharpened_barcode_img=self.sharpen_image(barcode_img)
            decoded_info=decode(sharpened_barcode_img)
        if len(decoded_info)==0:
            raise ValueError("no Barcodes detected")
        barcode_bytes=decoded_info[0].data
        barcode_str=barcode_bytes.decode('utf-8')
        return barcode_str

    def get_barcode_image(self, product_image):
        #TODO:the model takes a path to an image, check if it can take the image itself
        detected_images=self.yolo_model(product_image)
        
        if detected_images[0].boxes.shape[0] == 0:
            raise ValueError("no Barcodes detected")
        
        x1,y1,x2,y2=map(int,detected_images[0].boxes.xyxy[0].tolist())
        image=detected_images[0].orig_img
        
        padding=7
        x1_padding,y1_padding=max(0,x1-padding),max(0,y1-padding)
        x2_padding,y2_padding=min(image.shape[1],x2+padding),min(image.shape[0],y2+padding)
        barcode_img=image[y1_padding:y2_padding,x1_padding:x2_padding]
        return barcode_img


    def sharpen_image(self,image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray=cv2.morphologyEx(gray, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, (1, 21)))

        cols_brightness = np.sum(gray, axis=0)
        cols_brightness_0to255=(cols_brightness/(image.shape[0]*255))*255

        thresh = gray.copy()
        for idx, val in enumerate(cols_brightness_0to255):
            if val< 150:
                thresh[:,idx] = 0
            else:
                thresh[:,idx]=255

        return thresh


