#!/usr/bin/env python3
"""Combine screenshots into 2x2 grids (requires: pip install Pillow)."""

from pathlib import Path

from PIL import Image

SCRIPT_DIR = Path(__file__).resolve().parent
INPUT_DIR = SCRIPT_DIR / "screenshots"
OUTPUT_DIR = SCRIPT_DIR / "screenshot_outputs"
BATCH_SIZE = 4
GRID_COLS = 2
GRID_ROWS = 2
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp"}
BLANK_COLOR = (255, 255, 255)


def list_images(directory: Path) -> list[Path]:
    if not directory.is_dir():
        return []
    paths = [
        path
        for path in directory.iterdir()
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
    ]
    return sorted(paths, key=lambda path: path.name.lower())


def load_rgb(path: Path) -> Image.Image:
    with Image.open(path) as image:
        if image.mode in ("RGBA", "LA") or (
            image.mode == "P" and "transparency" in image.info
        ):
            rgba = image.convert("RGBA")
            background = Image.new("RGB", rgba.size, BLANK_COLOR)
            background.paste(rgba, mask=rgba.split()[-1])
            return background
        return image.convert("RGB")


def cell_size(images: list[Image.Image]) -> tuple[int, int]:
    if not images:
        return 1, 1
    return max(image.width for image in images), max(image.height for image in images)


def fit_cell(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    cell = Image.new("RGB", size, BLANK_COLOR)
    fitted = image.copy()
    fitted.thumbnail(size, Image.Resampling.LANCZOS)
    offset = ((size[0] - fitted.width) // 2, (size[1] - fitted.height) // 2)
    cell.paste(fitted, offset)
    return cell


def make_grid(images: list[Image.Image]) -> Image.Image:
    width, height = cell_size(images)
    grid = Image.new("RGB", (GRID_COLS * width, GRID_ROWS * height), BLANK_COLOR)

    slots = [
        (0, 0),
        (width, 0),
        (0, height),
        (width, height),
    ]
    for index, (x, y) in enumerate(slots):
        if index < len(images):
            grid.paste(fit_cell(images[index], (width, height)), (x, y))

    return grid


def save_grids(input_dir: Path = INPUT_DIR, output_dir: Path = OUTPUT_DIR) -> int:
    paths = list_images(input_dir)
    if not paths:
        print(f"No images found in {input_dir}")
        return 0

    output_dir.mkdir(parents=True, exist_ok=True)
    grid_count = 0

    for batch_start in range(0, len(paths), BATCH_SIZE):
        batch_paths = paths[batch_start : batch_start + BATCH_SIZE]
        batch_images = [load_rgb(path) for path in batch_paths]
        grid = make_grid(batch_images)

        grid_count += 1
        output_path = output_dir / f"grid_{grid_count:03d}.png"
        grid.save(output_path, format="PNG")
        names = ", ".join(path.name for path in batch_paths)
        print(f"Wrote {output_path.name} ({len(batch_paths)} image(s): {names})")

    return grid_count


def main() -> None:
    INPUT_DIR.mkdir(parents=True, exist_ok=True)
    count = save_grids()
    print(f"Done. Created {count} grid(s) in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
