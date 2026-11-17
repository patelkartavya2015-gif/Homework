import argparse
from pathlib import Path

import cv2
import numpy as np


FILTERS = {
	"Original": "0",
	"Grayscale": "1",
	"Sepia": "2",
	"Negative": "3",
	"Warm": "4",
	"Cool": "5",
}
CHANNEL_STEP = 10


def apply_filter(image, filter_name):
	if filter_name == "Original":
		return image.copy()
	if filter_name == "Grayscale":
		gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		return cv2.cvtColor(gray_image, cv2.COLOR_GRAY2BGR)
	if filter_name == "Sepia":
		sepia_matrix = np.array(
			[
				[0.272, 0.534, 0.131],
				[0.349, 0.686, 0.168],
				[0.393, 0.769, 0.189],
			],
			dtype=np.float32,
		)
		return np.clip(cv2.transform(image, sepia_matrix), 0, 255).astype(np.uint8)
	if filter_name == "Negative":
		return 255 - image
	if filter_name == "Warm":
		warm_image = image.copy()
		warm_image[:, :, 2] = np.clip(warm_image[:, :, 2].astype(np.int16) + 35, 0, 255)
		return warm_image
	if filter_name == "Cool":
		cool_image = image.copy()
		cool_image[:, :, 0] = np.clip(cool_image[:, :, 0].astype(np.int16) + 35, 0, 255)
		return cool_image
	raise ValueError(f"Unknown filter: {filter_name}")


def adjust_channels(image, red, green, blue):
	offsets = np.array([blue, green, red], dtype=np.int16)
	return np.clip(image.astype(np.int16) + offsets, 0, 255).astype(np.uint8)


def load_image(image_path):
	image_path = image_path.expanduser()
	image = cv2.imread(str(image_path), cv2.IMREAD_COLOR)
	if image is None:
		print(f"Could not load an image from: {image_path}")
		return None
	return image


def save_image(image, source_path):
	filename = input("Enter a filename for the edited image (or press Enter to cancel): ").strip()
	if not filename:
		return

	output_path = Path(filename).expanduser()
	if not output_path.suffix:
		output_path = output_path.with_suffix(".jpg")
	if not output_path.is_absolute():
		output_path = source_path.parent / output_path
	if output_path.resolve() == source_path.resolve():
		print("Choose a different filename so the original image is not overwritten.")
		return

	if not cv2.imwrite(str(output_path), image):
		print(f"Could not save the image to: {output_path}")
		return
	print(f"Saved edited image: {output_path}")


def draw_instructions(image, filter_name, red, green, blue):
	preview = image.copy()
	lines = [
		f"Filter: {filter_name}  |  R: {red:+d}  G: {green:+d}  B: {blue:+d}",
		"0-5: choose filter | r/g/b: increase channel | R/G/B: decrease",
		"u: load image | s: save image | q or Esc: quit",
	]
	for line_number, text in enumerate(lines):
		position = (12, 28 + line_number * 26)
		cv2.putText(preview, text, position, cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 0), 3)
		cv2.putText(preview, text, position, cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1)
	return preview


def main():
	print("Pres 1-5 keys to change the filters, q to not save and s to save")
	default_image = Path(__file__).with_name("Me.jpeg")
	parser = argparse.ArgumentParser(
		description="Apply color filters and adjust RGB channels with the keyboard."
	)
	parser.add_argument(
		"image",
		nargs="?",
		type=Path,
		default=default_image,
		help="image to edit (defaults to Me.jpeg in this folder)",
	)
	args = parser.parse_args()

	image_path = args.image.expanduser()
	image = load_image(image_path)
	if image is None:
		parser.error(f"Could not open image: {image_path}")

	filter_name = "Original"
	red = green = blue = 0
	filter_by_key = {ord(key): name for name, key in FILTERS.items()}
	channel_by_key = {
		ord("r"): ("red", 1),
		ord("R"): ("red", -1),
		ord("g"): ("green", 1),
		ord("G"): ("green", -1),
		ord("b"): ("blue", 1),
		ord("B"): ("blue", -1),
	}

	cv2.namedWindow("Color Filters", cv2.WINDOW_NORMAL)
	cv2.resizeWindow("Color Filters", 900, 700)
	try:
		while True:
			filtered_image = apply_filter(image, filter_name)
			edited_image = adjust_channels(filtered_image, red, green, blue)
			cv2.imshow(
				"Color Filters",
				draw_instructions(edited_image, filter_name, red, green, blue),
			)
			key = cv2.waitKey(30) & 0xFF

			if key in (ord("q"), 27):
				break
			if key in filter_by_key:
				filter_name = filter_by_key[key]
				continue
			if key in channel_by_key:
				channel, direction = channel_by_key[key]
				value = {"red": red, "green": green, "blue": blue}[channel]
				value = int(np.clip(value + direction * CHANNEL_STEP, -255, 255))
				if channel == "red":
					red = value
				elif channel == "green":
					green = value
				else:
					blue = value
				continue
			if key == ord("u"):
				image_file = input("Enter the image path to load (or press Enter to cancel): ").strip()
				if image_file:
					new_path = Path(image_file.strip('"')).expanduser()
					new_image = load_image(new_path)
					if new_image is not None:
						image_path = new_path
						image = new_image
						filter_name = "Original"
						red = green = blue = 0
				continue
			if key == ord("s"):
				save_image(edited_image, image_path)
	finally:
		cv2.destroyAllWindows()


if __name__ == "__main__":
	main()