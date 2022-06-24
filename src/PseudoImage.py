import logging
import os

import cv2
import numpy as np


class PseudoImage:
    def __init__(
        self,
        image_scale=30,
        font_str="FONT_HERSHEY_SIMPLEX",
        font_scale=0.4,
        image_root="images",
    ):
        self.image_scale = image_scale
        self.font_scale = font_scale
        self.image_root = image_root
        self.font = getattr(cv2, font_str)

    def __call__(self, filename, target_channel=0):
        src_path = os.path.join(self.image_root, filename)
        logging.info(f"load path: {src_path}")
        if not os.path.exists(src_path):
            logging.error(f"no such file: {src_path}")
            return
        name, _ = os.path.splitext(filename)
        dst_path = os.path.join(self.image_root, f"{name}_pseudo.png")
        image = cv2.imread(src_path, cv2.IMREAD_ANYCOLOR)
        logging.debug(f"src image shape: {image.shape}")

        pseudol_image = self.make_pseudol(image, target_channel)
        logging.info(f"dst path: {dst_path}")
        logging.debug(f"dst image shape: {pseudol_image.shape}")
        cv2.imwrite(dst_path, pseudol_image)
        return image, pseudol_image

    def make_pseudol(self, image, target_channel):
        height, width, _ = image.shape
        pseudol_shape = (self.image_scale * height, self.image_scale * width)
        pseudol_image = np.zeros(pseudol_shape, dtype=np.uint8)
        for y in range(height):
            for x in range(width):
                brightness = image[y, x, target_channel]
                pseudol_image[
                    y * self.image_scale : (y + 1) * self.image_scale,
                    x * self.image_scale : (x + 1) * self.image_scale,
                ] = brightness
                put_color = 0 if brightness >= 127 else 255
                text_poisition = (
                    x * self.image_scale,
                    y * self.image_scale + int(self.image_scale / 2),
                )
                cv2.putText(
                    pseudol_image,
                    str(brightness),
                    text_poisition,
                    self.font,
                    self.font_scale,
                    put_color,
                    1,
                    cv2.LINE_AA,
                )
        return pseudol_image
