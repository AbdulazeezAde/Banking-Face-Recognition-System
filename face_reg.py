from imutils import paths
import face_recognition
import pickle
from datetime import datetime
import cv2
# from skimage import io
import os, time, re
 
def encode_image(picture):
    #get paths of each file in folder named Images
    #Images here contains my data(folders of various persons)
    print(picture)
    start = datetime.now()
    # picture = 't.jpeg'
    # image = cv2.imread('t.jpeg')

    # data = {}
    # data['encodings'] = []
    # data['names'] = []
    # loop over the image paths

    data = pickle.loads(open('encode', "rb").read())
    # print(data['names'])

    # for (i, imagePath) in enumerate(imagePaths):
    # extract the person name from the image path
    # name = picture[:-4]
    find = re.compile(r"^[^.]*")
    name = re.search(find, picture).group(0)
    # print('Name is {}'.format(imagePath.split(os.path.sep)[-1][:-4]))
    # load the input image and convert it from BGR (OpenCV ordering)
    # to dlib ordering (RGB)
    
    # image = io.imread(picture)
    image = cv2.imread('static/uploads/{}' .format(picture))
    print('the image is {}'.format(image))
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    #Use Face_recognition to locate faces
    boxes = face_recognition.face_locations(rgb,model='hog')
    # compute the facial embedding for the face
    encodings = face_recognition.face_encodings(rgb, boxes)
    # loop over the encodings 
    for encoding in encodings:
        data['encodings'].append(encoding)
        data['names'].append(name)
    #save emcodings along with their names in dictionary data
    # print(knownNames)
    print(datetime.now() - start)
    print(data['names'])
    # data = {"encodings": knownEncodings, "names": knownNames}
    #use pickle to save data into a file for later use
    f = open("encode", "wb")
    f.write(pickle.dumps(data))
    f.close()

def image_search(picture):
    """
    docstring
    """#find path of xml file containing haarcascade file
    cascPathface = os.path.dirname(
    cv2.__file__) + "/data/haarcascade_frontalface_alt2.xml"
    # load the harcaascade in the cascade classifier
    faceCascade = cv2.CascadeClassifier(cascPathface)
    # load the known faces and embeddings saved in last file
    data = pickle.loads(open('encode', "rb").read()) #face_enc
    print(data['names'])
    #Find path to the image you want to detect face and pass it here
    
    image = cv2.imread('static/output/{}' .format(picture))
    
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    #convert image to Greyscale for haarcascade
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray,
                                        scaleFactor=1.1,
                                        minNeighbors=5,
                                        minSize=(60, 60),
                                        flags=cv2.CASCADE_SCALE_IMAGE)
    
    # the facial embeddings for face in input
    encodings = face_recognition.face_encodings(rgb)
    names = []
    # loop over the facial embeddings incase
    # we have multiple embeddings for multiple fcaes
    for encoding in encodings:
        #Compare encodings with encodings in data["encodings"]
        #Matches contain array with boolean values and True for the embeddings it matches closely
        #and False for rest
        matches = face_recognition.compare_faces(data["encodings"],
        encoding, 0.6)
        print(matches)
        #set name =inknown if no encoding matches
        name = "Unknown"
        # check to see if we have found a match
        if True in matches:
            #Find positions at which we get True and store them
            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}
            # loop over the matched indexes and maintain a count for
            # each recognized face face
            for i in matchedIdxs:
                #Check the names at respective indexes we stored in matchedIdxs
                name = data["names"][i]
                #increase count for the name we got
                counts[name] = counts.get(name, 0) + 1
                #set name which has highest count
                name = max(counts, key=counts.get)
        # update the list of names
        names.append(name)
        # loop over the recognized faces
        for ((x, y, w, h), name) in zip(faces, names):
            # rescale the face coordinates
            # draw the predicted face name on the image
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(image, name, (x, y), cv2.FONT_HERSHEY_SIMPLEX,
                0.75, (0, 255, 0), 2)
        # cv2.imshow("Frame", image)
        cv2.imwrite('static/uploads/output.jpeg', image)
        print('Found {} image'.format(names))
        
    return 'output.jpeg', names