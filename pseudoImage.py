import cv2
import numpy as np

if __name__ == '__main__':
    # 'blue': 0, 'green': 1,
    # 'red':  2, 'alpha': 3
    target_file = 'person.png'
    target_channel = 0
    img = cv2.imread(target_file, cv2.IMREAD_UNCHANGED)
    scale = 30
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.4
    height, width, channel = img.shape
    pseudol_size = (height * scale, width * scale, 1)
    pseudol_img = np.zeros((pseudol_size), dtype=np.uint8)
    for y in range(height):
        for x in range(width):
            value = img[y, x, target_channel]
            pseudol_img[y*scale: (y+1)*scale, x*scale: (x+1)*scale] = value
            if value >= 127:
                put_color = 0
            else:
                put_color = 255
            cv2.putText(pseudol_img, str(value),
                        (x*scale, y*scale+int(scale/2)),
                        font, font_scale, put_color, 1, cv2.LINE_AA)
    cv2.imwrite('pseudol_'+target_file, pseudol_img)
