from pathlib import Path
from typing import cast

import cv2
import numpy as np
import numpy.typing as npt
from loguru import logger


class PseudoImage:
    """Converts an image to a pseudo-color image with pixel values as text."""

    def __init__(
        self,
        image_scale: int = 30,
        font_str: str = "FONT_HERSHEY_SIMPLEX",
        font_scale: float = 0.4,
        image_root: Path = Path("images"),
    ):
        """Initialize PseudoImage.

        Args:
            image_scale: Scale factor for the output image.
            font_str: OpenCV font attribute name.
            font_scale: Font scale for text rendering.
            image_root: Root directory path for images.
        """
        self.image_scale = image_scale
        self.font_scale = font_scale
        self.image_root = image_root
        self.font = getattr(cv2, font_str)

    def __call__(
        self, filename: str, target_channel: int = 0
    ) -> tuple[npt.NDArray[np.uint8], npt.NDArray[np.uint8]] | None:
        """Process an image file and generate its pseudo-color version.

        Args:
            filename: Name of the image file to process.
            target_channel: Color channel index to use for brightness.

        Returns:
            Tuple of (original image, pseudo image), or None if file not found.
        """
        src_path = self.image_root / filename
        logger.info(f"load path: {src_path}")
        if not src_path.exists():
            logger.error(f"no such file: {src_path}")
            return None
        dst_path = src_path.with_stem(f"{src_path.stem}_pseudo").with_suffix(".png")
        raw = cv2.imread(str(src_path), cv2.IMREAD_ANYCOLOR)
        if raw is None:
            logger.error(f"failed to read image: {src_path}")
            return None
        image = cast(npt.NDArray[np.uint8], raw)
        logger.debug(f"src image shape: {image.shape}")

        pseudol_image = self.make_pseudol(image, target_channel)
        logger.info(f"dst path: {dst_path}")
        logger.debug(f"dst image shape: {pseudol_image.shape}")
        cv2.imwrite(str(dst_path), pseudol_image)
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
        height, width = image.shape[:2]
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
                    y * self.image_scale + self.image_scale // 2,
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
