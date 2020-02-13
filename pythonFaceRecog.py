# import the necessary packages
from imutils import paths
import face_recognition
import pickle
import cv2
import os
from imutils.video import VideoStream
from imutils.video import FPS
import imutils
import sys
import time
from dotenv import load_dotenv
from RFID import RFID

cwd = os.getcwd()
load_dotenv(cwd+"/.env")

class python_face_recognition():
    
    def __init__(self, encodings='encodings.pickle'):
        self.encoding = encodings
        self.cwd = os.getcwd()
        
# =============================================================================
#           ENCODING
# =============================================================================
        
    def encode(self,
                 dataset='dataset', 
                 detection_method='hog'):

        print("[INFO] quantifying faces...")
        imagePaths = list(paths.list_images(dataset))
        
        knownEncodings = []
        knownNames = []
        

        for (i, imagePath) in enumerate(imagePaths):
        	# extract the person name from the image path
        	print("[INFO] processing image {}/{}".format(i + 1,
        		len(imagePaths)))
        	name = imagePath.split(os.path.sep)[-2]
        
        	image = cv2.imread(imagePath)
        	rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        	boxes = face_recognition.face_locations(rgb,
        		model=detection_method)
        
        	encodings = face_recognition.face_encodings(rgb, boxes)
        
        	for encoding in encodings:

        		knownEncodings.append(encoding)
        		knownNames.append(name)
        

        print("[INFO] serializing encodings...")
        data = {"encodings": knownEncodings, "names": knownNames}
        f = open(self.encoding, "wb")
        f.write(pickle.dumps(data))
        f.close()
        
# =============================================================================
#         RECOGNISATION
# =============================================================================
    
    def recognise(self, 
                  cascade='haarcascade_frontalface_default.xml'):
        print("[INFO] loading encodings + face detector...")
        data = pickle.loads(open(self.encoding, "rb").read())
        detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        
        print("[INFO] starting video stream...")
        vs = VideoStream(src=0).start()
        time.sleep(2.0)
        
        fps = FPS().start()
        
        while True:

        	frame = vs.read()
        	frame = imutils.resize(frame, width=500)
        	
        	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        	rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        	rects = detector.detectMultiScale(gray, scaleFactor=1.1, 
        		minNeighbors=5, minSize=(30, 30),
        		flags=cv2.CASCADE_SCALE_IMAGE)
        
        	boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]
        
        	encodings = face_recognition.face_encodings(rgb, boxes)
        	names = []
        
        	for encoding in encodings:

        		matches = face_recognition.compare_faces(data["encodings"],
        			encoding)
        		name = "Unknown"
        
        		# check to see if we have found a match
        		if True in matches:

        			matchedIdxs = [i for (i, b) in enumerate(matches) if b]
        			counts = {}
                    
        			for i in matchedIdxs:
        				name = data["names"][i]
        				counts[name] = counts.get(name, 0) + 1
        			name = max(counts, key=counts.get)
        		
        		names.append(name)
        		rfid = RFID()
        		rfid.RFID_db(operation='match', name=name.lower())
                
        
        	for ((top, right, bottom, left), name) in zip(boxes, names):
        		cv2.rectangle(frame, (left, top), (right, bottom),
        			(0, 255, 0), 2)
        		y = top - 15 if top - 15 > 15 else top + 15
        		cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
        			0.75, (0, 255, 0), 2)
        
        	cv2.imshow("Frame", frame)
        	key = cv2.waitKey(1) & 0xFF
        
        	if key == ord("q"):
        		break
        
        	fps.update()
        
        fps.stop()
        print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
        print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
        
        cv2.destroyAllWindows()
        vs.stop()
        
        
# run = python_face_recognition()
# if str(sys.argv[1]).lower() == 'encode':
#     run.encode()

# elif str(sys.argv[1]).lower() == 'recognise':
#     run.recognise()

# else:
#     print('flase')