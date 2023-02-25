from __future__ import annotations

import logging
import os

import cv2
import numpy as np
import numpy.typing as npt


class PseudoImage:
    def __init__(
        self,
        image_scale: int = 30,
        font_str: str = "FONT_HERSHEY_SIMPLEX",
        font_scale: float = 0.4,
    ):
        self.image_scale = image_scale
        self.font_scale = font_scale
        self.font = getattr(cv2, font_str)

    def __call__(
        self, src_path: str, target_channel: int = 0
    ) -> npt.NDArray[np.uint8] | None:
        """Loads an image with the given filename, generates a pseudocolor image, and saves it.

        Args:
            filename (str): _description_
            target_channel (int, optional): _description_. Defaults to 0.

        Returns:
            Optional[tuple[npt.NDArray[np.uint8], npt.NDArray[np.uint8]]]: オリジナル画像と疑似カラー画像のペア。ファイルが存在しない場合はNoneを返します。
        """
        logging.info(f"Load path: {src_path}")
        if not os.path.exists(src_path):
            logging.error(f"No such file: {src_path}")
            return None
        image = cv2.imread(src_path, cv2.IMREAD_ANYCOLOR)
        logging.debug(f"src image shape: {image.shape}")
        pseudol_image = self.make_pseudol(image, target_channel)
        logging.debug(f"dst image shape: {pseudol_image.shape}")
        return pseudol_image

    def make_pseudol(
        self, image: npt.NDArray[np.uint8], target_channel: int
    ) -> npt.NDArray[np.uint8]:
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
