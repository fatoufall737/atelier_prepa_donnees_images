from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageOps


def preprocess_image(image: Image.Image, size: int, grayscale: bool, normalize: bool) -> Image.Image:
    img = image.resize((size, size), Image.Resampling.LANCZOS)
    if grayscale:
        img = ImageOps.grayscale(img)
    if normalize:
        img = img.convert("F")
        img = img.point(lambda p: p / 255.0)
    return img


def process_images(input_dir: Path, output_dir: Path, size: int, grayscale: bool, normalize: bool) -> list[Path]:
    if not input_dir.exists():
        raise FileNotFoundError(f"Le dossier d'entrée est introuvable : {input_dir}")

    output_dir.mkdir(parents=True, exist_ok=True)
    generated: list[Path] = []

    for image_path in sorted(input_dir.iterdir()):
        if not image_path.is_file():
            continue
        if image_path.suffix.lower() not in {".png", ".jpg", ".jpeg", ".bmp", ".webp"}:
            continue

        with Image.open(image_path) as img:
            processed = preprocess_image(img, size, grayscale, normalize)
            destination = output_dir / f"{image_path.stem}_prep{image_path.suffix.lower()}"
            if grayscale and destination.suffix.lower() not in {".png", ".jpg", ".jpeg", ".bmp", ".webp"}:
                destination = output_dir / f"{image_path.stem}_prep.png"
            processed.save(destination)
            generated.append(destination)

    return generated


def create_demo_images(folder: Path) -> None:
    folder.mkdir(parents=True, exist_ok=True)
    if any(folder.iterdir()):
        return

    from PIL import Image as PILImage

    for index in range(3):
        img = PILImage.new("RGB", (300, 300), color=(index * 80 + 50, 150 + index * 40, 200 - index * 30))
        for x in range(0, 300, 40):
            for y in range(0, 300, 40):
                img.putpixel((x, y), (255, 255, 255))
        img.save(folder / f"demo_{index + 1}.png")


def main() -> None:
    parser = argparse.ArgumentParser(description="Atelier de préparation de données images")
    parser.add_argument("--input", type=Path, default=Path("demo_images"), help="Dossier contenant les images source")
    parser.add_argument("--output", type=Path, default=Path("output"), help="Dossier de sortie pour les images traitées")
    parser.add_argument("--size", type=int, default=224, help="Taille cible des images")
    parser.add_argument("--grayscale", action="store_true", help="Convertit les images en nuances de gris")
    parser.add_argument("--normalize", action="store_true", help="Normalise les pixels entre 0 et 1")
    args = parser.parse_args()

    create_demo_images(args.input)

    try:
        results = process_images(args.input, args.output, args.size, args.grayscale, args.normalize)
    except FileNotFoundError as exc:
        print(str(exc))
        raise SystemExit(1)

    print(f"{len(results)} images traitées dans {args.output}")
    for path in results:
        print(f"- {path}")


if __name__ == "__main__":
    main()
