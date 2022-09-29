from importop import importop
import numpy as np
import cv2
from typing import Union

openpose_base_path = "/home/luoxishuang/openpose/"
op = importop(openpose_base_path + "build/python/")()

class op_container:
    def __init__(self, model_path : str='models/') -> None:
        self.datum = None
        self.opWrapper = op.WrapperPython()
        params = dict()
        model_path = model_path if model_path[0] == "/" else openpose_base_path + model_path
        params['model_folder'] = model_path
        # params['net_resolution'] = '320x176'  # optimize for fewer GPU memory
        self.opWrapper.configure(params)
        self.opWrapper.start()
    
    def setImage(self, img: Union[str, np.ndarray]):
        if isinstance(img, str):
            img = cv2.imread(img)
        if not isinstance(img, np.ndarray):
            raise ValueError("please use imread by opencv")
        self.datum = op.Datum()
        self.datum.cvInputData = img
        self.opWrapper.emplaceAndPop(op.VectorDatum([self.datum]))
    
    def getKeyPoint(self):
        if self.datum is None:
            raise ValueError("No available image to be recognized")
        return self.datum.poseKeypoints
    
    def getImage(self):
        if self.datum is None:
            raise ValueError("No available image to be recognized")
        return self.datum.cvOutputData
