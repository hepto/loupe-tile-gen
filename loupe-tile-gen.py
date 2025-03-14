import sys
import os
from PIL import Image
from resizeimage import resizeimage

def load_and_resize(image_path, size):
  image = Image.open(image_path).convert("RGBA")
  return resizeimage.resize_cover(image, size, resample=Image.LANCZOS)

def prepare_overlays(image_path):
  overlay = load_and_resize(image_path, (80, 80))
  overlay = overlay.convert("RGBA")  # Ensure it has an alpha channel

  mask = overlay.copy()
  mask.putalpha(127)  # Apply transparency workaround
  overlay.paste(mask, overlay)  # Ensure fully transparent areas stay transparent

  return overlay

def split_image(image_path):

  base_name = os.path.splitext(os.path.basename(image_path))[0]
  base_output_dir = os.path.join("output", base_name)

  subfolders = ["blank", "red", "green", "blue", "yellow"]
  for folder in subfolders:
    os.makedirs(os.path.join(base_output_dir, folder), exist_ok=True)

  # Load and resize the main image
  image = load_and_resize(image_path, (440, 260))

  # Define button colors and prepare buttons with transparency fix
  overlay_colors = ["red", "green", "blue", "yellow"]
  overlays = {color: prepare_overlays(os.path.join(f"overlays", f"overlay-{color}.png")) for color in overlay_colors}

  # Define row heights and column widths (excluding 10px gutters)
  row_heights = [80, 10, 80, 10, 80]
  col_widths = [80, 10, 80, 10, 80, 10, 80, 10, 80]

  # Compute y-coordinates for valid rows (excluding 10px gutters)
  y_coords = [0]
  for height in row_heights:
    y_coords.append(y_coords[-1] + height)
  valid_y_indices = [0, 2, 4]  # Keep only rows 1, 3, 5

  # Compute x-coordinates for valid columns (excluding 10px gutters)
  x_coords = [0]
  for width in col_widths:
    x_coords.append(x_coords[-1] + width)
  valid_x_indices = [0, 2, 4, 6, 8]  # Keep only columns 1, 3, 5, 7, 9


  # Crop and save each section with buttons
  for row_index, row in enumerate(valid_y_indices):
    for col_index, col in enumerate(valid_x_indices):
      left, top = x_coords[col], y_coords[row]
      right, bottom = x_coords[col + 1], y_coords[row + 1]

      cropped = image.crop((left, top, right, bottom))
      cropped.save(os.path.join(base_output_dir, f"blank", f"section_row{row_index+1}_col{col_index+1}.png"), format="PNG")

      # Apply each button dynamically
      for color in overlay_colors:
        blended = Image.new("RGBA", cropped.size)
        blended.paste(cropped, (0, 0))  # Place original crop
        blended = Image.alpha_composite(blended, overlays[color])  # Blend button with transparency fix

        blended.save(os.path.join(base_output_dir, f"{color}", f"section_row{row_index+1}_col{col_index+1}.png"), format="PNG")

  print(f"✅ Image '{image_path}' processed successfully! Tiles saved to '{base_output_dir}/'.")

# Run the script with an image path argument
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python split_image.py <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]
    split_image(image_path)
