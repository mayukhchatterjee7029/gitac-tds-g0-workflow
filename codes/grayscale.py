from pathlib import Path
from PIL import Image
import numpy as np

# Mapping: (scrambled_row, scrambled_col, original_row, original_col)
MAPPING = [
    (0, 0, 2, 1), (0, 1, 1, 1), (0, 2, 4, 1), (0, 3, 0, 3), (0, 4, 0, 1),
    (1, 0, 1, 4), (1, 1, 2, 0), (1, 2, 2, 4), (1, 3, 4, 2), (1, 4, 2, 2),
    (2, 0, 0, 0), (2, 1, 3, 2), (2, 2, 4, 3), (2, 3, 3, 0), (2, 4, 3, 4),
    (3, 0, 1, 0), (3, 1, 2, 3), (3, 2, 3, 3), (3, 3, 4, 4), (3, 4, 0, 2),
    (4, 0, 3, 1), (4, 1, 1, 2), (4, 2, 1, 3), (4, 3, 0, 4), (4, 4, 4, 0),
]

INPUT = Path("jigsaw.webp")
OUTPUT = Path("reconstructed_grayscale.png")

img = Image.open(INPUT).convert("RGB")
w, h = img.size
tw, th = w // 5, h // 5

assert w % 5 == 0 and h % 5 == 0, "Image dimensions must be divisible by 5"

# Reassemble the 5x5 grid
reconstructed = Image.new("RGB", (w, h))
for sr, sc, orow, ocol in MAPPING:
    tile = img.crop((sc * tw, sr * th, (sc + 1) * tw, (sr + 1) * th))
    reconstructed.paste(tile, (ocol * tw, orow * th))

# Exact luminance-based grayscale conversion:
# Y = 0.2126 R + 0.7152 G + 0.0722 B
arr = np.asarray(reconstructed, dtype=np.float64)
gray = (
    0.2126 * arr[..., 0]
    + 0.7152 * arr[..., 1]
    + 0.0722 * arr[..., 2]
)

# Half-up rounding to 8-bit grayscale
gray = np.floor(gray + 0.5).astype(np.uint8)

Image.fromarray(gray, mode="L").save(OUTPUT, format="PNG", optimize=True)
print(f"Wrote {OUTPUT}")