# USAGE
# When encoding on laptop, desktop, or GPU (slower, more accurate):
# python encode_faces.py --dataset dataset --encodings encodings.pickle --detection-method cnn
# When encoding on Raspberry Pi (faster, more accurate):
# python encode_faces.py --dataset dataset --encodings encodings.pickle --detection-method hog

# import the necessary packages
from imutils import paths
import face_recognition
import argparse
import pickle
import cv2
import os
import multiprocessing as mp
import gc

def caluculate_encoding(num, q_path, q_results):
    while q_path.qsize() > 0:
        path = q_path.get()
        print('Process %d: %s' % (num, path))
        print('Remaining %d ...' % q_path.qsize())
        name = path.split(os.path.sep)[-2]

        # load the input image and convert it from BGR (OpenCV ordering)
        # to dlib ordering (RGB)
        image = cv2.imread(path)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # detect the (x, y)-coordinates of the bounding boxes
        # corresponding to each face in the input image
        boxes = face_recognition.face_locations(rgb,
            model=args["detection_method"])

        # compute the facial embedding for the face
        encodings = face_recognition.face_encodings(rgb, boxes)

        # loop over the encodings
        for encoding in encodings:
            # add each encoding + name to our set of known names and encodings
            q_results.put((encoding, name))
        gc.collect()


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--dataset", default='dataset',
    help="path to input directory of faces + images")
ap.add_argument("-e", "--encodings", default='encodings_mt.pickle',
    help="path to serialized db of facial encodings")
ap.add_argument("-d", "--detection-method", type=str, default="hog",
    help="face detection model to use: either `hog` or `cnn`")
ap.add_argument("-j", "--workers", type=int, default=4,
    help="number of threads processing the images")
args = vars(ap.parse_args())

# grab the paths to the input images in our dataset
print("[INFO] quantifying faces...")
imagePaths = list(paths.list_images(args["dataset"]))
imageQueue = mp.Queue()
resultQueue = mp.Queue()
for p in imagePaths:
    imageQueue.put(p) 

# initialize the list of known encodings and known names
knownEncodings = []
knownNames = []
processes = []


for i in list(range(args['workers'])):
    p = mp.Process(target=caluculate_encoding, args=(i, imageQueue, resultQueue))
    # caluculate_encoding(q_path, encodings, names):
    p.start()
    processes.append(p)
for i in list(range(args['workers'])):
    processes[i].join()

while resultQueue.qsize() > 0:
    e, n = resultQueue.get()
    knownEncodings.append(e)
    knownNames.append(n)

# dump the facial encodings + names to disk
print("[INFO] serializing encodings...")
print(len(knownEncodings), len(knownNames))
data = {"encodings": knownEncodings, "names": knownNames}
f = open(args["encodings"], "wb")
f.write(pickle.dumps(data))
f.close()
