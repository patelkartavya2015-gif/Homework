from pathlib import Path

import cv2


OUTPUTS = {
	"Small": (200, "input_image_small.jpg"),
	"Medium": (400, "input_image_medium.jpg"),
	"Large": (600, "input_image_large.jpg"),
}


def main():
	image_path = Path(input("Enter the image path: ").strip().strip('"')).expanduser()
	image = cv2.imread(str(image_path), cv2.IMREAD_COLOR)
	if image is None:
		print(f"Could not load an image from: {image_path}")
		return

	height, width = image.shape[:2]
	crop_size = min(height, width)
	top = (height - crop_size) // 2
	left = (width - crop_size) // 2
	square_image = image[top:top + crop_size, left:left + crop_size]

	output_directory = image_path.resolve().parent
	interpolation = cv2.INTER_AREA
	if crop_size < 600:
		interpolation = cv2.INTER_CUBIC

	for label, (side_length, filename) in OUTPUTS.items():
		resized = cv2.resize(
			square_image,
			(side_length, side_length),
			interpolation=interpolation,
		)
		output_path = output_directory / filename
		if not cv2.imwrite(str(output_path), resized):
			print(f"Could not save resized image: {output_path}")
			continue

		print(f"Saved {label.lower()} image: {output_path}")
		cv2.imshow(f"{label} - {side_length}x{side_length}", resized)

	print("Press any key in an image window to close all previews.")
	cv2.waitKey(0)
	cv2.destroyAllWindows()


if __name__ == "__main__":
	main()

