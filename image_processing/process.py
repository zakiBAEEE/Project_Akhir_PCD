import cv2
from matplotlib import pyplot as plt
import numpy as np
import imutils
from easyocr import Reader

def points(location):
    """
    Take locations of 4 points and return them in specific order
    bottom_right, top_right, bottom_left, top_left
    :param location: 4 random points
    :return: list of points in order: bottom_right, top_right, bottom_left, top_left
    """
    comparelist = []
    sortedlist = []
    for point in location:
        comparelist.append(np.sum(point))

    for i in range(4):
        max_pos = comparelist.index(max(comparelist[:]))
        sortedlist.append(location[max_pos])
        comparelist[max_pos] = 0

    return sortedlist

def filtered_text(text):
    """
    Filters mistakes from reading extra marks etc...
    Made for Finnish Licence plates
    :param text: String
    :return: Modified text
    """
    ftext = ''
    firstnum = True
    for letter in text:
        if letter.isalpha():
            ftext += letter.capitalize()

        elif letter.isnumeric():
            if firstnum:
                ftext += '-'
                firstnum = False
            ftext += letter
    return ftext




#read image and make copy of it
import cv2
import numpy as np
import imutils
from matplotlib import pyplot as plt
from easyocr import Reader

def points(location):
    """
    Take locations of 4 points and return them in specific order
    bottom_right, top_right, bottom_left, top_left
    :param location: 4 random points
    :return: list of points in order: bottom_right, top_right, bottom_left, top_left
    """
    comparelist = []
    sortedlist = []
    for point in location:
        comparelist.append(np.sum(point))

    for i in range(4):
        max_pos = comparelist.index(max(comparelist[:]))
        sortedlist.append(location[max_pos])
        comparelist[max_pos] = 0

    return sortedlist

def filtered_text(text):
    """
    Filters mistakes from reading extra marks etc...
    Made for Finnish Licence plates
    :param text: String
    :return: Modified text
    """
    ftext = ''
    firstnum = True
    for letter in text:
        if letter.isalpha():
            ftext += letter.capitalize()
        elif letter.isnumeric():
            if firstnum:
                ftext += '-'
                firstnum = False
            ftext += letter
    return ftext

def process_image(image_path):
    try:
        img = cv2.imread(image_path)
        img_original = img.copy()

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # plt.imshow(cv2.cvtColor(gray, cv2.COLOR_BGR2RGB))
        # plt.show()
        nfilter = cv2.bilateralFilter(gray, 11, 17, 17)  # Noise reduction
        edged = cv2.Canny(nfilter, 30, 200)  # Edge detection
        # plt.imshow(cv2.cvtColor(edged, cv2.COLOR_BGR2RGB))
        # plt.show()

        mainpoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(mainpoints)
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

        (bottom_right, top_right, bottom_left, top_left) = points(location)

        if top_right[0][0] - top_left[0][0] < top_right[0][1] - top_left[0][1]:
            top_width = (((bottom_left[0][0] - top_left[0][0]) ** 2) + ((bottom_left[0][1] - top_left[0][1]) ** 2))
            bottom_width = np.sqrt(((bottom_right[0][0] - top_right[0][0]) ** 2) + ((bottom_right[0][1] - top_right[0][1]) ** 2))
            right_height = np.sqrt(((bottom_right[0][0] - bottom_left[0][0]) ** 2) + ((bottom_right[0][1] - bottom_left[0][1]) ** 2))
            left_height = np.sqrt(((top_left[0][0] - top_right[0][0]) ** 2) + ((top_left[0][1] - top_right[0][1]) ** 2))
            max_width = max(int(bottom_width), int(top_width)) // 100
            max_height = max(int(right_height), int(left_height))
            input_points = np.float32([top_left[0], top_right[0], bottom_left[0], bottom_right[0]])
            converted_points = np.float32([[0, 0], [0, max_height], [max_width, 0], [max_width, max_height]])
        else:
            top_width = (((top_right[0][0] - top_left[0][0]) ** 2) + ((top_right[0][1] - top_left[0][1]) ** 2))
            bottom_width = np.sqrt(((bottom_right[0][0] - bottom_left[0][0]) ** 2) + ((bottom_right[0][1] - bottom_left[0][1]) ** 2))
            right_height = np.sqrt(((top_right[0][0] - bottom_right[0][0]) ** 2) + ((top_right[0][1] - bottom_right[0][1]) ** 2))
            left_height = np.sqrt(((top_left[0][0] - bottom_left[0][0]) ** 2) + ((top_left[0][1] - bottom_left[0][1]) ** 2))
            max_width = max(int(bottom_width), int(top_width)) // 100
            max_height = max(int(right_height), int(left_height))
            input_points = np.float32([top_left[0], top_right[0], bottom_left[0], bottom_right[0]])
            converted_points = np.float32([[0, 0], [max_width, 0], [0, max_height], [max_width, max_height]])

        matrix = cv2.getPerspectiveTransform(input_points, converted_points)
        img_output = cv2.warpPerspective(img_original, matrix, (max_width, max_height))
        # plt.imshow(cv2.cvtColor(img_output, cv2.COLOR_BGR2RGB))
        # plt.show()

        (x, y) = np.where(mask == 255)
        (x1, y1) = (np.min(x), np.min(y))
        (x2, y2) = (np.max(x), np.max(y))
        cropped_image = gray[x1:x2+1, y1:y2+1]

        reader = Reader(['en'])
        result = reader.readtext(img_output)

        if result:
            text = filtered_text(result[0][-2])
            return text
        else:
            return "No text found"

    except Exception as e:
        print("Error during image processing or OCR:", e)
        return "No text found"
