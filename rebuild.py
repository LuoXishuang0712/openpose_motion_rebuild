from copy import deepcopy
import numpy as np

def motion_adjust(motion : np.ndarray, angle):
    '''params:
       motion: the motion to be adjusted
       angle: the adjust angle in degree, 0 <= theta < 360
       alert: this function only adjust motion on the X-Y flat
       return:
       the corrected motion
    '''
    assert motion.shape[0] == 25
    motion = deepcopy(motion)
    angle = util.degree2radius(util.angle_normalization(angle))
    x, y = deepcopy(motion.T[:2])
    motion.T[0] = x * np.cos(angle) - y * np.sin(angle)
    motion.T[1] = x * np.sin(angle) + y * np.cos(angle)
    return motion

class util:
    @staticmethod
    def angle_normalization(angle):
        while(angle < 0):
            angle += 360
        return angle % 360
    
    @staticmethod
    def degree2radius(degree):
        return degree * np.pi / 180

class CapContainer:
    def __init__(self, angle, data : np.ndarray) -> None:
        assert data.shape[0] == 25 , "please specify the person in the array"
        self._angle = util.angle_normalization(angle)
        self.data = data
    
    def set_angle(self, angle):
        self._angle = util.angle_normalization(angle)
    
    def get_angle(self):
        return self._angle

class RebuildFailException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
    
    def __str__(self) -> str:
        return super().__str__()

class rebuild2d:
    _cannot_ignore = [0, 1, 2, 5, 8] # joints where are used for location

    def __init__(self, alpha, beta) -> None:
        '''params:
           alpha, beta: the two angles of cameras in degree
        '''
        alpha = util.angle_normalization(alpha)
        beta = util.angle_normalization(beta)
        assert alpha != beta and alpha != beta - 180
        alpha, beta = sorted([alpha, beta]) # alpha is alway smaller than beta
        if beta - alpha < 45:
            print('[warning] now the camera angle is smaller than 45 degree, '
                  'which may cause the unprecious calculation of the depth.')
        self.alpha = alpha
        self.beta = beta

    def calc_depth(self, data_alpha : CapContainer, data_beta : CapContainer, ignore : list =[]) -> np.ndarray:
        if data_alpha.get_angle() != self.alpha:
            data_alpha, data_beta = data_beta, data_alpha
        assert data_alpha.get_angle() == self.alpha and data_beta.get_angle() == self.beta
        assert len([i for i in ignore if i in self._cannot_ignore]) == 0 , "some specify joint(s) are cannot be ignored."
        alpha = deepcopy(data_alpha.data)
        beta = deepcopy(data_beta.data)

        # set the '0' point as zero point XD
        alpha.T[:1] -= alpha[0][0]
        alpha.T[1:2] -= alpha[0][1]
        beta.T[:1] -= beta[0][0]
        beta.T[1:2] -= beta[0][1]

        return self.calc_depth_uncheck(alpha, beta, ignore)
    
    def calc_depth_uncheck(self, alpha : np.ndarray, beta : np.ndarray, ignore : list) -> np.ndarray:
        result = np.zeros((25, 3))
        for i in range(1, 25):
            if i in ignore:
                continue
            if alpha[i][2] == 0 or beta[i][2] == 0:
                if i in self._cannot_ignore:
                    raise RebuildFailException("the %d joint is excepted, but cannot found in the data" % i)
                else:
                    continue
            result[i] = self.calc_depth_line(alpha[i], beta[i])
        return result
            
    def calc_depth_line(self, alpha_line : np.ndarray, beta_line : np.ndarray) -> np.ndarray:
        assert alpha_line[2] != 0 and beta_line[2] != 0
        tri_angle = util.degree2radius(self.alpha - self.beta)
        result = np.zeros((3))
        result[0] = alpha_line[0] # x
        result[2] = np.mean([alpha_line[1], beta_line[1]]) # z
        p = -beta_line[0]
        q = alpha_line[0]
        if p > 0 and q < 0:
            result[1] = q * np.tan(tri_angle) - q * (np.cos(tri_angle) * np.sin(tri_angle)) ** -1 + p * (np.sin(tri_angle) ** -1)
            # print("method 1 ", end='')
        else:
            result[1] = p * (np.sin(tri_angle) ** -1) + q * (np.tan(tri_angle) ** -1)
            # print("method 2 ", end='')
        # print(result[1])
        return result # [x, y, z] about the alpha plane