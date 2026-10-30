import argparse
import matplotlib.pyplot as plt
from pathlib import Path

import cv2
import numpy as np


def rotate_image(image, angle):
	height, width = image.shape[:2]
	center = (width / 2, height / 2)
	rotation = cv2.getRotationMatrix2D(center, angle, 1.0)
	cosine = abs(rotation[0, 0])
	sine = abs(rotation[0, 1])
	rotated_width = int((height * sine) + (width * cosine))
	rotated_height = int((height * cosine) + (width * sine))
	rotation[0, 2] += (rotated_width / 2) - center[0]
	rotation[1, 2] += (rotated_height / 2) - center[1]
	return cv2.warpAffine(image, rotation, (rotated_width, rotated_height))


def adjust_color(image, brightness, saturation):
	hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV).astype(np.float32)
	hsv_image[:, :, 1] = np.clip(hsv_image[:, :, 1] * saturation, 0, 255)
	hsv_image[:, :, 2] = np.clip(hsv_image[:, :, 2] * brightness, 0, 255)
	return cv2.cvtColor(hsv_image.astype(np.uint8), cv2.COLOR_HSV2BGR)


def main():
	default_image = Path(__file__).with_name("Me.jpeg")
	parser = argparse.ArgumentParser(description="Rotate, brighten, crop, and save a photo.")
	parser.add_argument("image", nargs="?", type=Path, default=default_image)
	parser.add_argument("-o", "--output", type=Path, help="Output image path")
	parser.add_argument("--angle", type=float, default=0, help="Rotation in degrees counterclockwise")
	parser.add_argument("--brightness", type=float, default=1.10, help="Brightness multiplier")
	parser.add_argument("--saturation", type=float, default=1.08, help="Saturation multiplier")
	parser.add_argument(
		"--crop",
		type=int,
		nargs=4,
		metavar=("LEFT", "TOP", "WIDTH", "HEIGHT"),
		help="Crop rectangle in pixels, applied after rotation",
	)
	args = parser.parse_args()

	image_path = args.image.expanduser()
	image = cv2.imread(str(image_path), cv2.IMREAD_COLOR)
	if image is None:
		parser.error(f"Could not load an image from: {image_path}")

	rotated = rotate_image(image, args.angle)
	height, width = rotated.shape[:2]
	if args.crop is None:
		left = int(width * 0.075)
		top = int(height * 0.035)
		crop_width = width - left - int(width * 0.075)
		crop_height = height - top - int(height * 0.14)
	else:
		left, top, crop_width, crop_height = args.crop

	if left < 0 or top < 0 or crop_width <= 0 or crop_height <= 0:
		parser.error("Crop coordinates must be non-negative with positive width and height")
	if left + crop_width > width or top + crop_height > height:
		parser.error(f"Crop rectangle must fit within the rotated image ({width}x{height})")

	cropped = rotated[top:top + crop_height, left:left + crop_width]
	edited = adjust_color(cropped, args.brightness, args.saturation)
	output_path = args.output or image_path.with_name(f"{image_path.stem}_edited{image_path.suffix}")
	output_path = output_path.expanduser()
	if output_path.resolve() == image_path.resolve():
		parser.error("Output path must be different from the source image")
	if not cv2.imwrite(str(output_path), edited):
		parser.error(f"Could not save edited image to: {output_path}")

	print(f"Saved edited image: {output_path}")
	print(f"Final size: {edited.shape[1]}x{edited.shape[0]}")

	plt.figure("Edited image")
	plt.imshow(cv2.cvtColor(edited, cv2.COLOR_BGR2RGB))
	plt.axis("off")
	plt.tight_layout()
	plt.show()


if __name__ == "__main__":
	main()
