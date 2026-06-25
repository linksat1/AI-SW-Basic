import os
from pathlib import Path

from PIL import Image


def convert_png_to_jpg(images_dir: Path) -> None:
    if not images_dir.exists() or not images_dir.is_dir():
        raise FileNotFoundError(f"Directory not found: {images_dir}")

    for png_path in images_dir.glob("*.png"):
        jpg_path = png_path.with_suffix(".jpg")

        with Image.open(png_path) as img:
            if img.mode in ("RGBA", "LA"):
                background = Image.new("RGB", img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[-1])
                output = background
            else:
                output = img.convert("RGB")

            output.save(jpg_path, format="JPEG", quality=95)

        print(f"Converted: {png_path.name} -> {jpg_path.name}")


if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parent
    images_dir = base_dir / "images"
    convert_png_to_jpg(images_dir)
    print("모든 PNG 파일을 JPG로 변환했습니다.")
