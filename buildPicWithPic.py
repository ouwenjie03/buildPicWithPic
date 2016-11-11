# encoding: utf-8

"""
@author: ouwj
@file: buildPicWithPic.py
@time: 2016/11/2 9:29
"""

from PIL import Image
import numpy as np
import os
import math


class BuildPicWithPic:
    def __init__(self):
        self.TMP_DIR = 'small_pic_dir'
        self.MAX_CURRENT_NUM = 15
        self.channel_index = []
        self.matchDist = None
        self.small_h = 40
        self.small_w = 30
        self.big_h = 4000
        self.big_w = 3000
        self.isRotate = False

    def load_picture(self, pic_path, new_w=-1, new_h=-1):
        im = Image.open(pic_path)
        (w, h) = im.size
        if w > h:
            im = im.transpose(Image.ROTATE_270)
            self.isRotate = True
        if new_w == -1 and new_h == -1:
            return np.array(im, dtype='int64')
        if new_w == -1:
            new_w = w
        if new_h == -1:
            new_h = h
        im = im.resize((new_w, new_h), Image.ANTIALIAS)
        return np.array(im, dtype='int64')

    def save_picture(self, im_arr, pic_path, new_w=-1, new_h=-1):
        im = Image.fromarray(im_arr)
        (w, h) = im.size
        if self.isRotate:
            im = im.transpose(Image.ROTATE_90)
        if new_w == -1 and new_h == -1:
            im.save(pic_path, 'jpeg')
        if new_w == -1:
            new_w = w
        if new_h == -1:
            new_h = h

        im = im.resize((new_w, new_h), Image.ANTIALIAS)
        im.save(pic_path, 'jpeg')

    def preprocess_dir(self, dst_dir_path):
        pic_paths = os.listdir(dst_dir_path)
        idx = 0
        for pic_path in pic_paths:
            im = Image.open(dst_dir_path + '\\' + pic_path)
            (w, h) = im.size
            if w > h:
                im = im.transpose(Image.ROTATE_270)
            im = im.resize((self.small_w, self.small_h), Image.ANTIALIAS)
            im.save(self.TMP_DIR+'\\'+str(idx)+'.jpg', 'jpeg')
            idx += 1

    def find_match_picture(self, patch_arr, dst_arrs):
        idx = -1
        min_diff = 1e12
        match_idx = -1
        h, w, c = patch_arr.shape
        patch_arr_1d = patch_arr.reshape((w*h*c))
        for dst_arr in dst_arrs:
            idx += 1
            dst_arr_1d = dst_arr.reshape((w*h*c))
            diff = math.sqrt(sum((patch_arr_1d-dst_arr_1d) ** 2))
            diff *= (0.5 + self.matchDist[idx])
            if diff < min_diff:
                min_diff = diff
                match_idx = idx
        self.matchDist[match_idx] += 0.01
        return match_idx

    def build_picture(self, src_arr, dst_arrs):
        h, w, c = src_arr.shape
        result_arr = np.zeros((h, w, c), dtype='int64')
        patch_w = self.small_w
        patch_h = self.small_h
        len_w = w / patch_w
        len_h = h / patch_h
        self.matchDist = [0]*len(dst_arrs)
        for i in range(len_h):
            for j in range(len_w):
                patch_arr = src_arr[i*patch_h:(i+1)*patch_h, j*patch_w:(j+1)*patch_w]
                match_idx = self.find_match_picture(patch_arr, dst_arrs)
                #print i, j, match_idx
                result_arr[i*patch_h:(i+1)*patch_h, j*patch_w:(j+1)*patch_w] = dst_arrs[match_idx]

        return result_arr

    def main(self, src_pic_path, dst_pics_dir, save_pic_path):
        print 'src picture loading...'
        src_arr = self.load_picture(src_pic_path, new_w=self.big_w, new_h=self.big_h)
        print 'preprocessing...'
        self.preprocess_dir(dst_pics_dir)
        dst_arrs = []
        print 'dst picture loading...'
        pic_paths = os.listdir(self.TMP_DIR)
        for pic_path in pic_paths:
            dst_arr = self.load_picture(self.TMP_DIR+'\\'+pic_path)
            dst_arrs.append(dst_arr)
        print 'picture building...'
        result_arr = self.build_picture(src_arr, dst_arrs)
        alpha = 0.7
        beta = 1-alpha
        result_arr = alpha * result_arr + beta * src_arr
        print 'picture saving...'
        result_arr = result_arr.astype('uint8')
        self.save_picture(result_arr, save_pic_path)

if __name__ == "__main__":
    builder = BuildPicWithPic()
    builder.main('mainPic.jpg', 'dst_dir_2', 'result.jpg')