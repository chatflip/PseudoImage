from __future__ import annotations

import logging
import os

import cv2
import numpy as np
import numpy.typing as npt


class PseudoImage:
    """Generates a pseudocolor image from a grayscale image."""

    def __init__(
        self,
        image_scale: int = 30,
        font_str: str = "FONT_HERSHEY_SIMPLEX",
        font_scale: float = 0.4,
    ):
        """Initializes the PseudoImage class.

        Args:
            image_scale (int, optional): The scale of the generated image.
                Defaults to 30.
            font_str (str, optional): The font type for the text.
                Defaults to "FONT_HERSHEY_SIMPLEX".
            font_scale (float, optional): The scale of the text.
                Defaults to 0.4.
        """
        self.image_scale = image_scale
        self.font_scale = font_scale
        self.font = getattr(cv2, font_str)

    def __call__(
        self, src_path: str, target_channel: int = 0
    ) -> npt.NDArray[np.uint8] | None:
        """Generates a pseudocolor image from a grayscale image.

        Args:
            src_path (str): The path to the source image.
            target_channel (int, optional):
                The channel to use for the pseudocolor image.
                Defaults to 0.

        Returns:
            npt.NDArray[np.uint8] | None: The pseudocolor image.
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
        """Generates a pseudocolor image from a grayscale image.

        Args:
            image (npt.NDArray[np.uint8]): The source image.
            target_channel (int): The channel to use for the pseudocolor image.

        Returns:
            npt.NDArray[np.uint8]: The pseudocolor image.
        """
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
                )  # type: ignore[call-overload]
        return pseudol_image
