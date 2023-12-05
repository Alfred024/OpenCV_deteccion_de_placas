import cv2
import numpy
from PIL import Image

#import pytesseract
# import pytesseract

frameWidth=640
frameHeight=480
# CascadeClassifier: detect objects in a video stream
# en este link hay una explicación acerca del algoritmo que clasifica los frames: 
# https://docs.opencv.org/4.x/db/d28/tutorial_cascade_classifier.html

# Fuente de Haarcascade: https://github.com/opencv/opencv/tree/master/data/haarcascades
nPlateCascade=cv2.CascadeClassifier('./haarcascade_russian_plate_number.xml')
print(nPlateCascade)
minArea=300
# Color rosita
borderColor=(255,0,255)

# VideoCapture: Open video file or image file sequence or a capturing device or a IP video stream for video capturing.
cap=cv2.VideoCapture("./assets/ford_fiesta.mp4")

# cv::VideoCaptureProperties {
#     cv::CAP_PROP_FRAME_WIDTH =3,
#     cv::CAP_PROP_FRAME_HEIGHT =4,
#     cv::CAP_PROP_BRIGHTNESS =10,
# }
cap.set(3,frameWidth)
cap.set(4,frameHeight)
cap.set(10,150)

count=0
plateText = ''

while True:
    success,videoFrame=cap.read()
    if success == False:
        break 

    imgGray=cv2.cvtColor(videoFrame,cv2.COLOR_BGR2GRAY)
    numberPlates=nPlateCascade.detectMultiScale(imgGray,1.1,10)
    plateDetectedFrame = None
    
    for(x_start,y_start,width,height) in numberPlates:
        cv2.rectangle(videoFrame,(x_start,y_start),(x_start+width,y_start+height),borderColor,2)
        cv2.putText(videoFrame,"Placa",(x_start,y_start-5),
        cv2.FONT_HERSHEY_COMPLEX_SMALL,1,borderColor,2)
        
        # Este son los valores RGB de la placa que captura en el video
        plateDetectedFrame=videoFrame[y_start:y_start+height,x_start:x_start+width]
        
        # Extracción de la altura y anchura del frame que detectó la placa
        heightPlate, widthPlate, frame = plateDetectedFrame.shape
        # Return a new array of given shape and type, filled with zeros.
        # (heightPlate, widthPlate) = shape of the array
        # quick and easy way to initialize an array with zeros before populating it
        # https://numpy.org/doc/stable/reference/generated/numpy.zeros.html
        RGB_matrix = numpy.zeros((heightPlate, widthPlate))
        
        blue_Matrix = numpy.matrix(plateDetectedFrame[:,:,0])
        green_Matrix = numpy.matrix(plateDetectedFrame[:,:,1])
        red_Matrix = numpy.matrix(plateDetectedFrame[:,:,2])
        
        # Llenamos la matriz con los valores binarios del color negro?
        for c in range(0, heightPlate):
            for r in range(0, widthPlate):
                max_val_matrix = max(blue_Matrix[c,r], green_Matrix[c,r], red_Matrix[c,r])
                # Esta operación obtiene los valores que representan el negro de la placa, 
                # para así procesar los caracteres de la misma
                RGB_matrix[c,r] = 255 - max_val_matrix
        
        # método explicación: https://docs.opencv.org/3.4/d7/d4d/tutorial_py_thresholding.html
        _, bin = cv2.threshold(RGB_matrix, 155,255, cv2.THRESH_BINARY)
        
        cv2.imshow("ROI",plateDetectedFrame)

    cv2.imshow("resultado",videoFrame)

    if cv2.waitKey(1)& 0xFF==ord('s'):
        cv2.inwrite("NoPlate_"+str(count)+".jpg",plateDetectedFrame)
        cv2.rectangle(videoFrame,(0,200),(640,300),(0,255,0),cv2.FILLED)
        cv2.putText(videoFrame,"Resultado",(150,265),cv2.FONT_HERSHEY_DUPLEX,
                    2,(0,0,255),2)
        cv2.imshow("Resultado",videoFrame)
        cv2.waitKey(500)
        count +=1