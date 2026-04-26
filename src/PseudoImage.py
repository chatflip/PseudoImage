import logging
import os
from typing import Optional, cast

import cv2
import numpy as np
import numpy.typing as npt


class PseudoImage:
    """Converts an image to a pseudo-color image with pixel values as text."""

    def __init__(
        self,
        image_scale: int = 30,
        font_str: str = "FONT_HERSHEY_SIMPLEX",
        font_scale: float = 0.4,
        image_root: str = "images",
    ):
        """Initialize PseudoImage.

        Args:
            image_scale: Scale factor for the output image.
            font_str: OpenCV font attribute name.
            font_scale: Font scale for text rendering.
            image_root: Root directory for images.
        """
        self.image_scale = image_scale
        self.font_scale = font_scale
        self.image_root = image_root
        self.font = getattr(cv2, font_str)

    def __call__(
        self, filename: str, target_channel: int = 0
    ) -> Optional[tuple[npt.NDArray[np.uint8], npt.NDArray[np.uint8]]]:
        """Process an image file and generate its pseudo-color version.

        Args:
            filename: Name of the image file to process.
            target_channel: Color channel index to use for brightness.

        Returns:
            Tuple of (original image, pseudo image), or None if file not found.
        """
        src_path = os.path.join(self.image_root, filename)
        logging.info(f"load path: {src_path}")
        if not os.path.exists(src_path):
            logging.error(f"no such file: {src_path}")
            return None
        name, _ = os.path.splitext(filename)
        dst_path = os.path.join(self.image_root, f"{name}_pseudo.png")
        raw = cv2.imread(src_path, cv2.IMREAD_ANYCOLOR)
        if raw is None:
            logging.error(f"failed to read image: {src_path}")
            return None
        image = cast(npt.NDArray[np.uint8], raw)
        logging.debug(f"src image shape: {image.shape}")

        pseudol_image = self.make_pseudol(image, target_channel)
        logging.info(f"dst path: {dst_path}")
        logging.debug(f"dst image shape: {pseudol_image.shape}")
        cv2.imwrite(dst_path, pseudol_image)
        return image, pseudol_image

    def make_pseudol(
        self, image: npt.NDArray[np.uint8], target_channel: int
    ) -> npt.NDArray[np.uint8]:
        """Generate a pseudo-color image with pixel brightness values as text.

        Args:
            image: Input image array.
            target_channel: Color channel index to use for brightness.

        Returns:
            Pseudo-color image with pixel values rendered as text.
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
                )
        return pseudol_image
