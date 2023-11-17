import cv2
# import numpy
# import pytesseract

frameWidth=640
frameHeight=480
nPlateCascade=cv2.CascadeClassifier('./haarcascade_russian_plate_number.xml')
print(nPlateCascade)
minArea=300
color=(255,0,255)

cap=cv2.VideoCapture("./assets/ford_fiesta.mp4")
cap.set(3,frameWidth)
cap.set(4,frameHeight)
cap.set(10,150)

count=0
while True:
    success,ing=cap.read()
    if success:
     imgGray = cv2.cvtColor(ing, cv2.COLOR_BGR2GRAY)
    # Resto del código
    else:
     break  # Salir del bucle si no se puede leer ningún fotograma

    imgGray=cv2.cvtColor(ing,cv2.COLOR_BGR2GRAY)
    numberPlates=nPlateCascade.detectMultiScale(imgGray,1.1,10)
    for(x,y,w,h) in numberPlates:
        area=w+h
        if area>minArea:
            cv2.rectangle(ing,(x,y),(x+w,y+h),(255,0,255),2)
            cv2.putText(ing,"Placa",(x,y-5),
                         cv2.FONT_HERSHEY_COMPLEX_SMALL,1,color,2)
            ingRoi=ing[y:y+h,x:x+w]
            cv2.imshow("ROI",ingRoi)

    cv2.imshow("resultado",ing)

    if cv2.waitKey(1)& 0xFF==ord('s'):
        cv2.inwrite("NoPlate_"+str(count)+".jpg",ingRoi)
        cv2.rectangle(ing,(0,200),(640,300),(0,255,0),cv2.FILLED)
        cv2.putText(ing,"Resultado",(150,265),cv2.FONT_HERSHEY_DUPLEX,
                    2,(0,0,255),2)
        cv2.imshow("Resultado",ing)
        cv2.waitKey(500)
        count +=1