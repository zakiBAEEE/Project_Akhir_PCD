import cv2
import imutils
import numpy as np
import easyocr
import os

def process_image(filepath):
    try:
        image_path = filepath
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        bfilter = cv2.bilateralFilter(gray, 11, 17, 17)  # Noise reduction
        edged = cv2.Canny(bfilter, 30, 200)  # Edge detection

        keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(keypoints)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

        location = None
        for contour in contours:
            approx = cv2.approxPolyDP(contour, 10, True)
            if len(approx) == 4:
                location = approx
                break

        if location is None:
            raise ValueError("No valid contours found for OCR")

        mask = np.zeros(gray.shape, np.uint8)
        new_image = cv2.drawContours(mask, [location], 0, 255, -1)
        new_image = cv2.bitwise_and(img, img, mask=mask)

        (x, y) = np.where(mask == 255)
        (x1, y1) = (np.min(x), np.min(y))
        (x2, y2) = (np.max(x), np.max(y))

        # # Ensure y2-2 does not go out of bounds
        # if x2 - 60 > y1:
        #     x2 -= 60
        cropped_image = gray[x1:x2+1, y1:y2+1]

        # Print cropped image dimensions for debugging
        print("Cropped image shape:", cropped_image.shape)

                # Create folder if it does not exist
        output_folder = 'cropped_images'
        os.makedirs(output_folder, exist_ok=True)

        # Save cropped image
        cropped_image_path = os.path.join(output_folder, os.path.basename(filepath))
        cv2.imwrite(cropped_image_path, cropped_image)
        print(f'Cropped image saved to: {cropped_image_path}')

        # Initialize EasyOCR reader
        reader = easyocr.Reader(['en'])

        # Perform OCR on cropped image
        result = reader.readtext(cropped_image)

        if result:
            text = result[0][-2]
            print(text)
            return text
        else:
            return "No text found"

    except Exception as e:
        print("Error during image processing or OCR:", e)
        return "No text found"

