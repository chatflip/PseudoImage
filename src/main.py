import argparse
import logging

from PseudoImage import PseudoImage


def main(args: argparse.Namespace) -> None:
    log_level = getattr(logging, args.log_level)
    logging.basicConfig(level=log_level)

    pseudo_image_maker = PseudoImage(
        args.image_scale,
        args.font,
        args.font_scale,
        args.image_root,
    )
    pseudo_image_maker(args.image_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--image_path", default="image.jpg", type=str)
    parser.add_argument(
        "--log_level",
        default="WARNING",
        type=str,
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
    )
    parser.add_argument("--image_scale", default=30, type=int)
    parser.add_argument("--font", default="FONT_HERSHEY_SIMPLEX", type=str)
    parser.add_argument("--font_scale", default=0.4, type=float)
    parser.add_argument("--image_root", default="images", type=str)
    args = parser.parse_args()
    print(type(args))
    main(args)
