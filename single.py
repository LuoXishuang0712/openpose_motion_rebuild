from draw_3d import draw3d
from recognize import op_container
from rebuild import rebuild2d, CapContainer, motion_adjust
import cv2
import numpy as np
import os

test_folder = "./test_dataset/"

def get_last_dot(filename : str):
    pos = len(filename)
    for char in filename[::-1]:
        pos -= 1
        if char == '.':
            return pos
    return -1

if __name__ == "__main__":
    if not os.path.exists(test_folder):
        os.mkdir(test_folder)
    for file in os.listdir(test_folder):
        if file[:get_last_dot(file)].endswith("_reg") or file[get_last_dot(file):] == ".npy":
            continue
        print(file)
        recg = op_container("/home/luoxishuang/openpose/")
        recg.setImage(test_folder + file)
        print(recg.getKeyPoint())
        np.save(test_folder + file[:get_last_dot(file)] + ".npy", recg.getKeyPoint())
        cv2.imwrite(test_folder + file[:get_last_dot(file)] + "_reg.jpg", recg.getImage())

