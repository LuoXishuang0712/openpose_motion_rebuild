from importop import op
import numpy as np
import cv2

class op_container:
    def __init__(self, model_path='./models/') -> None:
        self.datum = None
        self.opWrapper = op.WrapperPython()
        params = dict()
        params['model_folder'] = model_path
        self.opWrapper.configure(params)
        self.opWrapper.start()
    
    def setImage(self, img):
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
