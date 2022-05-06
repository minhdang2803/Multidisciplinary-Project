import tensorflow.compat.v1 as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
import numpy as np
import cv2
import time
from firebase import firebase

# loading the stored model from file
model = load_model(r'Fire-64x64-color-v7-soft.h5')

#cap = cv2.VideoCapture(r'VIDEO_FILE_NAME')
#cap = cv2.VideoCapture('https://10.229.14.192:4747/video')
#cap = cv2.VideoCapture('http://192.168.43.1:4747/video')
cap = cv2.VideoCapture(0)
#time.sleep(2)

if cap.isOpened():  # try to get the first frame
    rval, frame = cap.read()
else:
    rval = False


IMG_SIZE = 64
# IMG_SIZE = 224

#Connect to firebase
Data = firebase.FirebaseApplication('https://smarthome-comeherebae-default-rtdb.firebaseio.com/', None)
framecount = 0
notfirecount = 0
while(1):

    rval, image = cap.read()
    if rval == True:
        orig = image.copy()

        # image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image = cv2.resize(image, (IMG_SIZE, IMG_SIZE))
        image = image.astype("float") / 255.0
        image = img_to_array(image)
        image = np.expand_dims(image, axis=0)

        tic = time.time()
        fire_prob = model.predict(image)[0][0] * 100
        toc = time.time()
        print("Time taken = ", toc - tic)
        print("FPS: ", 1 / np.float64(toc - tic))
        print("Fire Probability: ", fire_prob)
        print("Predictions: ", model.predict(image))
        print(image.shape)
         
        if fire_prob > 90: 
            framecount += 1
            if framecount > 15:
                notfirecount = 0
                Data.put('/fire', 'state', 1)
        elif Data.get('/fire', 'state') == 1 and notfirecount >= 15:
            Data.put('/fire', 'state', 0)
        else:
            framecount = 0
            notfirecount+=1
        
        label = "Fire Probability: " + str(fire_prob)
        cv2.putText(orig, label, (10, 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        cv2.imshow("Output", orig)

        key = cv2.waitKey(10)
        if key == 27:  # exit on ESC
            break
    elif rval == False:
        break
end = time.time()

cap.release()
cv2.destroyAllWindows()
