try:
    from .importop import importop
except ImportError:
    from importop import importop
import numpy as np
import cv2
from typing import Union

class op_container:
    def __init__(self, openpose_base_path: str, model_path : str='models/', python_build_path: str="build/python/") -> None:
        self.openpose_base_path = openpose_base_path if openpose_base_path[-1] == "/" else openpose_base_path + "/"
        pyopenpose_path = openpose_base_path + python_build_path if python_build_path[0] != "/" else python_build_path
        self.op = importop(pyopenpose_path)()
        if self.op is None:
            raise ImportError("Cannot found openpose, check the path")
        self.datum = None
        self.opWrapper = self.op.WrapperPython()
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
        self.datum = self.op.Datum()
        self.datum.cvInputData = img
        self.opWrapper.emplaceAndPop(self.op.VectorDatum([self.datum]))
    
    def getKeyPoint(self):
        if self.datum is None:
            raise ValueError("No available image to be recognized")
        return self.datum.poseKeypoints
    
    def getImage(self):
        if self.datum is None:
            raise ValueError("No available image to be recognized")
        return self.datum.cvOutputData
