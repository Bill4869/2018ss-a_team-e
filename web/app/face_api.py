import base64
import cv2
import requests
from statistics import mean

class FaceAPI():
    def __init__(self, path):
        self.faces = []
        self.img_path = path

        self.bf_matcher = cv2.BFMatcher(cv2.NORM_HAMMING)
        self.detector = cv2.AKAZE_create()
        self.img = cv2.imread(self.img_path, cv2.IMREAD_GRAYSCALE)
        (kp, self.des) = self.detector.detectAndCompute(self.img, mask=None)

        subscription_key = 'ee6e75bcc92144b4a2ffd3160dbb05fa'
        face_api_url = 'https://japaneast.api.cognitive.microsoft.com/face/v1.0/detect'
        image_data = open(self.img_path, 'rb').read()
        headers = {
            'Ocp-Apim-Subscription-Key': subscription_key,
            'Content-Type': 'application/octet-stream'
        }
        params = {
            'returnFaceId': 'true',
            'returnFaceLandmarks': 'false',
            'returnFaceAttributes': 'age,gender',
        }
        response = requests.post(face_api_url, params=params, headers=headers, data=image_data)
        response.raise_for_status()
        self.faces = response.json()

    def detect_face(self):
        if self.faces:
            rect = self.faces[0]['faceRectangle']
            return rect['left'], rect['top'], rect['width'], rect['height']
        else:
            return []

    def get_face_attributes(self):
        if self.faces:
            return {'gender': self.faces[0]['faceAttributes']['gender'], 'age': self.faces[0]['faceAttributes']['age']}
        else:
            return {'gender': 'unknown', 'age': 'unknown'}

    def feature_detection(self, img_path):
        comparing_img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        (comparing_kp, comparing_des) = self.detector.detectAndCompute(comparing_img, mask=None)
        matches = self.bf_matcher.match(self.des, comparing_des)
        dist = [m.distance for m in matches]
        return sum(dist) / len(dist)

    def feature_detection_all(self, cards, base_dir):
        similalities = {}
        for card in cards:
            if self.img_path == (base_dir + card.icon.for_comparing.url):
                continue
            similalities[card.id] = self.feature_detection(base_dir + card.icon.for_comparing.url)
        return similalities

    def mosaic_filter(self, area, ratio=0.05):
        src = cv2.imread(self.img_path)

        if area != []:
            x = area[0]
            y = area[1]
            w = area[2]
            h = area[3]

            # for x, y, w, h in area:
            image = cv2.resize(src[y:y+h, x:x+w], None, fx=ratio, fy=ratio, interpolation=cv2.INTER_NEAREST)
            src[y:y+h, x:x+w] = cv2.resize(image, (w, h), interpolation=cv2.INTER_NEAREST)

        retval, buffer = cv2.imencode('.jpg', src)

        return 'data:image/jpg;base64,' + base64.b64encode(buffer).decode()