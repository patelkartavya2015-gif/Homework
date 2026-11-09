import cv2
import numpy as np
import matplotlib.pyplot as plt

def display_image(title, image):
    plt.figure(figsize=(8, 8))
    if len(image.shape) == 2:  # Grayscale image
        plt.imshow(image, cmap='gray')
    else:  # Color image
        plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title(title)
    plt.axis('off')
    plt.show()

def interactive_edge_detection(image_path):
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Image might be missing or not found. Please check the path and try again.")
        return

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    display_image("Grayscale Image", gray_image)

    print("Select an option:")
    print("1. Sobel Edge Detection \n 2. Canny Edge Detection \n 3. Laplacian Edge Detection \n 4. Gaussian Smoothing \n 5. Median Filtering \n 6. Exit")

    while True:
        choice = input("Enter your choice (1-6): ")

        if choice == '1':
            sobel_x = cv2.Sobel(gray_image, cv2.CV_64F, 1, 0, ksize=5)
            sobel_y = cv2.Sobel(gray_image, cv2.CV_64F, 0, 1, ksize=5)
            combined_sobel = cv2.bitwise_or(sobel_x.astype(np.uint8), sobel_y.astype(np.uint8))
            display_image("Sobel Edge Detection", combined_sobel)

        elif choice == '2':
            print("Adjust threshold values for Canny Edge Detection(default: 100 and 200):")
            lower_threshold = int(input("Enter lower threshold (0-255): "))
            upper_threshold = int(input("Enter upper threshold (0-255): "))
            edges = cv2.Canny(gray_image, lower_threshold, upper_threshold)
            display_image("Canny Edge Detection", edges)


        elif choice == '3':
            laplacian = cv2.Laplacian(gray_image, cv2.CV_64F)
            display_image("Laplacian Edge Detection", laplacian)

        elif choice == '4':
            print("Adjust kernel size for Gaussian Smoothing (default: 5):")
            kernel_size = int(input("Enter kernel size (odd number): "))
            gaussian_blur = cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
            display_image("Gaussian Smoothing", gaussian_blur)

        elif choice == '5':
            print("Adjust kernel size for Median Filtering (default: 5):")
            kernel_size = int(input("Enter kernel size (odd number): "))
            median_filtered = cv2.medianBlur(image, kernel_size)
            display_image("Median Filtering", median_filtered)

        elif choice == '6':
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please select a valid option.")
if __name__ == "__main__":
    interactive_edge_detection("Edge detection/Me.jpeg")