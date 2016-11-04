# encoding: utf-8

"""
@author: ouwj
@file: test.py
@time: 2016/9/24 21:07
"""

from PIL import Image
import numpy as np
import math


filepath = 'mainPic.jpg'

im = Image.open(filepath)
(w, h) = im.size
print w, h

pix = np.array(im, dtype='int32')
#scale = 1.5
#im_big = im.resize((int(scale*w), int(scale*h)), Image.ANTIALIAS)
#rpix = pix[:, :, 0]
#gpix = pix[:, :, 1]
#bpix = pix[:, :, 2]
imr = im.transpose(Image.ROTATE_90)
pixr = np.array(imr, dtype='int32')
#imr.save('rotatePic.jpg', 'jpeg')
#im_big.save('bigPic.jpg', 'jpeg')

patch1 = pix[100:500, 100:400]
print patch1.shape
patch2 = pixr[100:500, 100:400]
patch3 = patch1.reshape((400*300*3))
patch4 = patch2.reshape((400*300*3))
print patch3 - patch4
diff = math.sqrt(sum((patch3-patch4) ** 2))
print diff

diffsum = 0.0
for i in range(400):
    for j in range(300):
        for k in range(3):
            diffsum += (patch1[i, j, k] - patch2[i, j, k]) * 1.0 * (patch1[i, j, k] - patch2[i, j, k])
print math.sqrt(diffsum)