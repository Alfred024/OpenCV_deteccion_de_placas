import cv2
# import numpy
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
    
    # Si puede leer el archivo MP4 procederá a ejecutar el programa
    # Reading the frame of .mp4 file
    success,videoFrame=cap.read()
    if success == False:
        break 

    # Se cambia el color de la imagen a escala de grises
    # La razón de esta acción se explica aquí: https://www.isahit.com/blog/why-to-use-grayscale-conversion-during-image-processing#:~:text=It%20helps%20in%20simplifying%20algorithms,It%20enhances%20easy%20visualisation.
    imgGray=cv2.cvtColor(videoFrame,cv2.COLOR_BGR2GRAY)
    
    # detectMultiScale: Detects objects of different sizes in the input image. The detected objects are returned as a list of rectangles.
    # detectMultiScale:params
    # par1 -> image:Matrix of the type CV_8U containing an image where objects are detected., 
    # par2 -> scaleFactor: Parameter specifying how much the image size is reduced at each image scale., 
    # par3 -> minNeighbors: Parameter specifying how many neighbors each candidate rectangle should have to retain it.
    numberPlates=nPlateCascade.detectMultiScale(imgGray,1.1,10)
    
    for(x,y,w,h) in numberPlates:
        area=w*h
        if area>minArea:
            
            # rectangle:params
            # image
            # start_point
            # end_point
            # color (of border)
            # thickness (of border width in px)
            cv2.rectangle(videoFrame,(x,y),(x+w,y+h),borderColor,2)
            cv2.putText(videoFrame,"Placa",(x,y-5),
                         cv2.FONT_HERSHEY_COMPLEX_SMALL,1,borderColor,2)
            
            # Frame en RGB
            plateDetectedFrame=videoFrame[y:y+h,x:x+w]
            cv2.imshow("ROI",plateDetectedFrame)

    # Shows completr videoFrame
    cv2.imshow("resultado",videoFrame)

    if cv2.waitKey(1)& 0xFF==ord('s'):
        cv2.inwrite("NoPlate_"+str(count)+".jpg",plateDetectedFrame)
        cv2.rectangle(videoFrame,(0,200),(640,300),(0,255,0),cv2.FILLED)
        cv2.putText(videoFrame,"Resultado",(150,265),cv2.FONT_HERSHEY_DUPLEX,
                    2,(0,0,255),2)
        cv2.imshow("Resultado",videoFrame)
        cv2.waitKey(500)
        count +=1