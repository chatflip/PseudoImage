import os

import cv2
import numpy as np
import numpy.typing as npt


class PseudoImage:
    def __init__(
        self,
        image_scale: int = 30,
        font: int = cv2.FONT_HERSHEY_SIMPLEX,
        font_scale: float = 0.4,
    ):
        self.image_scale = image_scale
        self.font = font
        self.font_scale = font_scale

    def __call__(self, src_path: str) -> None:
        target_channel = 0

        print(f"load path: {src_path}")
        if not os.path.exists(src_path):
            print(f"no such path: {src_path}")
            return
        image = cv2.imread(src_path)
        print(f"src image shape: {image.shape}")

        pseudol_image = self.make_pseudol(image, target_channel)

        name, _ = os.path.splitext(src_path)
        dst_path = f"{name}_pseudo.png"
        print(f"dst image shape: {pseudol_image.shape}")
        cv2.imwrite(dst_path, pseudol_image)
        print(f"save path: {dst_path}")

    def make_pseudol(
        self, image: npt.NDArray[np.uint8], target_channel: int
    ) -> npt.NDArray[np.uint8]:
        height, width, channel = image.shape
        pseudol_size = (height * self.image_scale, width * self.image_scale, 1)
        pseudol_image = np.zeros((pseudol_size), dtype=np.uint8)
        for y in range(height):
            for x in range(width):
                value = image[y, x, target_channel]
                pseudol_image[
                    y * self.image_scale : (y + 1) * self.image_scale,
                    x * self.image_scale : (x + 1) * self.image_scale,
                ] = value
                if value >= 127:
                    put_color = 0
                else:
                    put_color = 255
                cv2.putText(
                    pseudol_image,
                    str(value),
                    (
                        x * self.image_scale,
                        y * self.image_scale + int(self.image_scale / 2),
                    ),
                    self.font,
                    self.font_scale,
                    put_color,
                    1,
                    cv2.LINE_AA,
                )
        return pseudol_image
