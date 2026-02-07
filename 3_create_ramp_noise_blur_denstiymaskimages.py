import json
from PIL import Image, ImageDraw, ImageFilter
import math
import random

# ---------------------------------------------
# Setup
# ---------------------------------------------

WIDTH = 2048
HEIGHT = 2048

INPUT_JSON = "horse_uv_faces_triangulated_TMP_test.json"

OUTPUT_TILE_1001 = "horse_density_1001.png"
OUTPUT_TILE_1002 = "horse_density_1002.png"

OUTPUT_TILE_1001_RAMP = "horse_density_1001_ramp.png"
OUTPUT_TILE_1002_RAMP = "horse_density_1002_ramp.png"

# Ramp settings (UV space)
RAMP_CENTER_U = 0.5
RAMP_CENTER_V = 1.0

# Painterly block noise (local variation)
NOISE_SCALE = 32
NOISE_STRENGTH = 0.1

# Low-frequency smooth noise (global variation)
LOW_NOISE_SCALE = 4.0
LOW_NOISE_STRENGTH = 0.08

# Final smoothing
BLUR_RADIUS = 4.0

# ---------------------------------------------
# 1. Load UV data from JSON
# ---------------------------------------------

with open(INPUT_JSON, "r") as f:
    data = json.load(f)

# ---------------------------------------------
# 2. Create grayscale output images
# ---------------------------------------------

img_1001 = Image.new("L", (WIDTH, HEIGHT), 0)
img_1002 = Image.new("L", (WIDTH, HEIGHT), 0)

draw_1001 = ImageDraw.Draw(img_1001)
draw_1002 = ImageDraw.Draw(img_1002)

# ---------------------------------------------
# 3. Convert UV coordinates to pixel space
# ---------------------------------------------

def uv_to_pixel(u, v):
    x = int(u * (WIDTH - 1))
    y = int((1.0 - v) * (HEIGHT - 1))  # Y flip
    return (x, y)

# ---------------------------------------------
# 4. Rasterize triangles with density values
# ---------------------------------------------

for face in data:
    density = int(face["density"])  # already 0–255
    uvs = face["uvs"]

    if not uvs or len(uvs) != 3:
        continue

    tile = int(uvs[0][0])  # 0 → 1001, 1 → 1002
    poly_pixels = []

    for u, v in uvs:
        u_local = u - tile
        if u_local < 0.0 or u_local > 1.0:
            continue
        poly_pixels.append(uv_to_pixel(u_local, v))

    if len(poly_pixels) != 3:
        continue

    if tile == 0:
        draw_1001.polygon(poly_pixels, fill=density)
    elif tile == 1:
        draw_1002.polygon(poly_pixels, fill=density)

# ---------------------------------------------
# 5. Save base density maps
# ---------------------------------------------

img_1001.save(OUTPUT_TILE_1001)
img_1002.save(OUTPUT_TILE_1002)

print("Base density map generation completed")

# =========================================================
# 6. Procedural refinement: ramp + layered noise
# =========================================================

def block_noise(u, v):
    iu = int(u * NOISE_SCALE)
    iv = int(v * NOISE_SCALE)
    random.seed(iu * 73856093 ^ iv * 19349663)
    return random.uniform(-1.0, 1.0)

def low_freq_noise(u, v):
    return math.sin(u * LOW_NOISE_SCALE) * math.sin(v * LOW_NOISE_SCALE)

def apply_ramp_and_noise(img):
    pixels = img.load()

    for y in range(HEIGHT):
        for x in range(WIDTH):

            u = x / (WIDTH - 1)
            v = 1.0 - (y / (HEIGHT - 1))

            # Radial ramp
            dx = u - RAMP_CENTER_U
            dy = v - RAMP_CENTER_V
            dist = math.sqrt(dx * dx + dy * dy)
            ramp = max(0.0, 1.0 - dist)

            base = pixels[x, y] / 255.0

            # Layered noise
            low_n = 1.0 + low_freq_noise(u, v) * LOW_NOISE_STRENGTH
            block_n = 1.0 + block_noise(u, v) * NOISE_STRENGTH

            #final_value = base
            #final_value = base * ramp * block_n
            #final_value = base * ramp * low_n
            final_value = base * ramp * low_n * block_n
            final_value = max(0.0, min(1.0, final_value))

            pixels[x, y] = int(final_value * 255)

    return img

# Apply per UDIM
img_1001_ramp = apply_ramp_and_noise(img_1001.copy())
img_1002_ramp = apply_ramp_and_noise(img_1002.copy())

# Final blur pass
img_1001_ramp = img_1001_ramp.filter(ImageFilter.GaussianBlur(BLUR_RADIUS))
img_1002_ramp = img_1002_ramp.filter(ImageFilter.GaussianBlur(BLUR_RADIUS))

img_1001_ramp.save(OUTPUT_TILE_1001_RAMP)
img_1002_ramp.save(OUTPUT_TILE_1002_RAMP)

print("Procedural ramp + layered noise refinement completed")
print(" -", OUTPUT_TILE_1001_RAMP)
print(" -", OUTPUT_TILE_1002_RAMP)
