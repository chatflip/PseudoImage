import argparse
import logging

import cv2
from PseudoImage import PseudoImage


def main(args: argparse.Namespace) -> None:
    log_level = getattr(logging, args.log_level)
    logging.basicConfig(level=log_level)
    pseudo_image_maker = PseudoImage(
        args.image_scale,
        args.font,
        args.font_scale,
    )
    pseudo_image = pseudo_image_maker(args.src_path)
    cv2.imwrite(args.dst_path, pseudo_image)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--src_path", default="images/sample.jpg", type=str)
    parser.add_argument("--dst_path", default="images/image_pseudo.png", type=str)
    parser.add_argument(
        "--log_level",
        default="DEBUG",
        type=str,
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
    )
    parser.add_argument("--image_scale", default=30, type=int)
    parser.add_argument("--font", default="FONT_HERSHEY_SIMPLEX", type=str)
    parser.add_argument("--font_scale", default=0.4, type=float)
    args = parser.parse_args()
    main(args)
