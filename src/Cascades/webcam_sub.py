# Import the necessary libraries

import rospy 
from sensor_msgs.msg import Image # Image is the message type
from cv_bridge import CvBridge # Package to convert between ROS and OpenCV Images
from cv_bridge.core import CvBridgeError
import cv2 # OpenCV library
 
def callback(ros_image):
 
  # Used to convert between ROS and OpenCV images
  br = CvBridge()
  try:
    cv_image = br.imgmsg_to_cv2(ros_image, "bgr8")
  except CvBridgeError as e:
      print(e)
 
  recognizer = cv2.face.LBPHFaceRecognizer_create()
  recognizer.read('trainer/trainer.yml')
  cascadePath= cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
  #eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

  cascadePath = "haarcascade_frontalface_default.xml"
  print(cascadePath)
  faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + cascadePath);

  font = cv2.FONT_HERSHEY_SIMPLEX

  #iniciate id counter
  id = 0

 # names related to ids: example ==> Dalel: id=1,  etc
  names = ['', 'Dalel', 'Zeineb', 'Amine', 'Fedi', 'Ghada', 'Ghada','Mohamed'] 
 # Initialize and start realtime video capture
  cam = cv2.VideoCapture(0)
  cam.set(3, 640) # set video widht
  cam.set(4, 480) # set video height

 # Define min window size to be recognized as a face
  minW = 0.1*cv_image.get(3)
  minH = 0.1*cv_image.get(4)

  while True:


    ret, img =cv_image.read()
    img = cv2.flip(img, 1) 

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale( 
      gray,
      scaleFactor = 1.2,
      minNeighbors = 5,
      minSize = (int(minW), int(minH)),
    )

    for(x,y,w,h) in faces:
     cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)

     id, confidence = recognizer.predict(gray[y:y+h,x:x+w])

     # Check if confidence is less them 100 ==> "0" is perfect match 
    if (confidence < 100):
       id = names[id]
       confidence = "  {0}%".format(round(100 - confidence))
    else:


      id = "unknown"
      confidence = "  {0}%".format(round(100 - confidence))
      cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
      cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)  
    
    cv2.imshow("Image window", cv_image)
    k= cv2.waitKey(3)
    if k == 27:
        break
 

def receive_message():
 
  # Tells rospy the name of the node.
  # Anonymous = True makes sure the node has a unique name. Random
  # numbers are added to the end of the name. 
  rospy.init_node('video_sub_py', anonymous=True)
   
  # Node is subscribing to the video_frames topic
  rospy.Subscriber("/usb_cam/image_raw", Image, callback)
 
  # spin() simply keeps python from exiting until this node is stopped
  rospy.spin()
 
  # Close down the video stream when done
  cv2.destroyAllWindows()
  
if __name__ == '__main__':
  receive_message()