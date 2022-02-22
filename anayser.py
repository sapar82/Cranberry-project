
  
from turtle import width
import numpy as np
import cv2
import time
import matplotlib.pyplot as plt
  
# Capturing video through webcam
webcam = cv2.VideoCapture(0)
counter = []
# Start a while loop

all_mean = []
for w in range(200):
      
    # Reading the video from the
    # webcam in image frames
    
    # Convert the imageFrame in 
    # BGR(RGB color space) to 
    # HSV(hue-saturation-value)
    # color space
    _, imageFrame = webcam.read()
    
    b,g,r = cv2.split(imageFrame)

    thresh = cv2.threshold(r, 150, 200, cv2.THRESH_BINARY)[1]

    counter.append(w)

    zeros = np.zeros(thresh.shape[:2], dtype="uint8")

    merged = cv2.merge([zeros, zeros, thresh])
    
    division = (2, 2)
    x_size, y_size, channels = imageFrame.shape
            
    width = x_size//division[0]
    height = y_size//division[1]
    
    mean_array = np.ndarray((2,2))
    for i in range(division[0]):
        for j in range(division[1]):
            
            cropped_image = merged[i*width:(i+1)*width, j*height:(j+1)*height ]
            
            mean = cv2.mean(cropped_image)

            mean_array[i, j] = mean[2]
            
    all_mean.append(mean_array)

    # Program Termination
    cv2.imshow("Multiple Color Detection in Real-TIme", merged)
    
    

    # Program Termination
    
    if cv2.waitKey(10) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break

del all_mean[0: 30]
del counter[0:30]

array1 = [i[0][0] for i in all_mean]
array2 = [i[0][1] for i in all_mean]
array3 = [i[1][0] for i in all_mean]
array4 = [i[1][1] for i in all_mean]
plt.plot(counter, array1)
plt.plot(counter, array2)
plt.plot(counter, array3)
plt.plot(counter, array4)
plt.show()