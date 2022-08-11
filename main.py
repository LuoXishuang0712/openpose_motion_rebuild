from draw_3d import draw3d
from recognize import op_container
from rebuild import rebuild2d, CapContainer
import cv2
import numpy as np

body_line = [
    (0, 1), (0, 15), (0, 16), (1, 2), (1, 5), (1, 8), (2, 3), (3, 4), (5, 6), (6, 7), 
    (8, 9), (8, 12), (9, 10), (10, 11), (11, 22), (11, 24), (12, 13), (13, 14), 
    (14, 19), (14, 21), (15, 17), (16, 18), (19, 20), (22, 23)
]

recg = op_container("../openpose/models/")
recg.setImage("./imgs/keqing_left_side.jpg")
left = recg.getKeyPoint()
# cv2.imwrite("./left.jpg", recg.getImage())
recg.setImage("./imgs/keqing_right_side.jpg")
right = recg.getKeyPoint()
# cv2.imwrite("./right.jpg", recg.getImage())

rebuilder = rebuild2d(45, 315)
left_cap = CapContainer(315, left[0])
right_cap = CapContainer(45, right[0])

out = rebuilder.calc_depth(left_cap, right_cap)
print(out)

line = []
for i in range(len(body_line)):
    item = body_line[i]
    if i != 0 and (out[item[0]][2] == 0 or out[item[1]][2] == 0):
        continue
    line.append([
        [out[item[0]][0], out[item[1]][0]],
        [out[item[0]][1], out[item[1]][1]],
        [out[item[0]][2], out[item[1]][2]]
    ])

np.delete(out, [i for i in range(1, 25) if out[i][2] == 0])

# todo : 动作旋转矫正（alpha平面->基准平面）

drawer = draw3d()
drawer.set_data(out)
drawer.set_line(line)
drawer.show()