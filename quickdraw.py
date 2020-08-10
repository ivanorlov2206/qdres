import threading
import time

import cv2
from keras.models import load_model
import numpy as np
from collections import deque
import os
from PIL import Image
from keras import backend as K


class QuickDraw():
    model = None

    def __init__(self, mname):
        self.model = load_model(mname)
        self.keras_predict(np.zeros((50, 50, 1), dtype=np.uint8))

    def clear(self):
        K.clear_session()



    classes = ['book', 'sun', 'banana', 'apple', 'bowtie', 'ice cream', 'eye', 'square', 'cup', 'door', 'sword', 'star', 'fish', 'donut', 'mountain']



    def classif(self, fname):
        # ------------ image preprocessing ---------------------
        digit2 = cv2.imread(fname)
        blackboard_gray = cv2.cvtColor(digit2, cv2.COLOR_BGR2GRAY)
        blur1 = cv2.medianBlur(blackboard_gray, 15)
        blur1 = cv2.GaussianBlur(blur1, (5, 5), 0)
        thresh1 = cv2.threshold(blur1, 127, 255, cv2.THRESH_BINARY)[1]
        # -------------- image segmentation----------------------
        blackboard_cnts = cv2.findContours(thresh1.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[0]
        if len(blackboard_cnts) >= 1:
            cnt = max(blackboard_cnts, key=cv2.contourArea)
            # print(cv2.contourArea(cnt))
            if cv2.contourArea(cnt) > 2000:
                x, y, w, h = cv2.boundingRect(cnt)
                digit = blackboard_gray[y:y + h, x:x + w]
                pred_probab, pred_class = self.keras_predict(self.pre_image(digit))
        return self.classes[pred_class]



    def pre_image(self, img):
        h, w = img.shape
        nw = w
        nh = h
        if w > h:
            nh = int(224 / w * h)
            nw = 224
            print(12121)
        else:
            nw = int(224 / h * w)
            nh = 224
        img = cv2.resize(img, (nw, nh))
        iy = (224 - nh) // 2
        ix = (224 - nw) // 2
        nimg = np.zeros((224, 224), dtype=np.uint8)
        nimg[iy:iy + nh, ix:ix + nw] = img
        return nimg


    def keras_predict(self, image):
        processed = self.keras_process_image(image)
        pred_probab = self.model.predict(processed)[0]
        pred_class = list(pred_probab).index(max(pred_probab))
        return max(pred_probab), pred_class


    def keras_process_image(self, img):
        image_x = 28
        image_y = 28
        img = cv2.resize(img, (image_x, image_y))
        img = np.array(img, dtype=np.float32)
        img = (img > 0) * 1
        print(img)
        img = np.reshape(img, (-1, image_x, image_y, 1))
        return img
