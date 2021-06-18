import os
import cv2
from tensorflow.keras.preprocessing.image import load_img,img_to_array
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input,decode_predictions
import PIL
from PIL import Image



model=VGG16()


def load_video(video_filename):
    print("splitting into frames...\n")
    vidcap = cv2.VideoCapture(video_filename)
    success,image = vidcap.read()
    count = 0

    while success:
      #resize every image to 224x224  
      image=cv2.resize(image,(224,224),interpolation = cv2.INTER_AREA)
      # save frame as JPEG file
      cv2.imwrite("temp/frame%d.jpg" % count, image)           
      
      #getting every nth frame 
      sampling_rate=5
      i=0
      while i<sampling_rate:
        success,image = vidcap.read()
        i += 1

      count += 1
    
    print("Frames read: ",count-1)

def predict(video_filename):
    load_video(video_filename)
    labels=[]
    print("Predicting frames...")
    for file in os.listdir('templates/temp'):
        print(file+"\n")
        #constructing full path of each image
        full_path='templates/temp/'+file

        
        image = load_img(full_path,target_size=(224,224))
        image = img_to_array(image)
        image=image.reshape((1,image.shape[0],image.shape[1],image.shape[2]))
        image=preprocess_input(image)
        yhat=model.predict(image)
        label = decode_predictions(yhat)
        label = label[0][0]
        pred_value = '%s (%.2f%%)'%(label[1],label[2]*100)
        #label=decode_predictions(y_pred,top=1)
        #img_prediction={"frame":file.replace(".jpg",""),"prediction":label[0][0][1],"certainity":label[0][0][2]}
        #labels.append(img_prediction)

    return pred_value