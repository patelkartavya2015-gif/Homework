from pathlib import Path

import cv2


def main():
	image_path = Path(__file__).with_name("Me.jpeg")
	output_path = Path(__file__).with_name("Me_annotated.jpeg")
	image = cv2.imread(str(image_path))

	if image is None:
		raise FileNotFoundError(f"Could not open image: {image_path}")

	height, width = image.shape[:2]
	annotated = image.copy()

	# A translucent band keeps the measurement readable over the photo.
	band_height = min(112, height)
	overlay = annotated.copy()
	cv2.rectangle(overlay, (0, 0), (width, band_height), (28, 35, 38), -1)
	cv2.addWeighted(overlay, 0.68, annotated, 0.32, 0, annotated)

	left = 2
	right = width - 3
	arrow_y = 40
	arrow_color = (70, 220, 245)
	cv2.arrowedLine(annotated, (left, arrow_y), (right, arrow_y), arrow_color, 3, tipLength=0.025)
	cv2.arrowedLine(annotated, (right, arrow_y), (left, arrow_y), arrow_color, 3, tipLength=0.025)

	label = f"IMAGE WIDTH  |  {width} px"
	font = cv2.FONT_HERSHEY_SIMPLEX
	font_scale = 0.85
	text_size, _ = cv2.getTextSize(label, font, font_scale, 2)
	text_x = (width - text_size[0]) // 2
	cv2.putText(annotated, label, (text_x, 88), font, font_scale, (255, 255, 255), 2, cv2.LINE_AA)

	if not cv2.imwrite(str(output_path), annotated):
		raise OSError(f"Could not save annotated image: {output_path}")

	print(f"Image size: {width} x {height} px")
	print(f"Annotated image saved to: {output_path}")


if __name__ == "__main__":
	main()
