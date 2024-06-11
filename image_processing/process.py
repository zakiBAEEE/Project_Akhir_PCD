
import cv2
import numpy as np
import imutils
import easyocr

def process_image(image_path):
    # Membaca gambar
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Gambar tidak dapat dibaca. Pastikan jalur gambar benar.")

    # Konversi gambar ke grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Mengurangi noise dengan bilateral filter
    bfilter = cv2.bilateralFilter(gray, 11, 17, 17)

    # Deteksi tepi dengan Canny
    edged = cv2.Canny(bfilter, 30, 200)

    # Temukan kontur dalam gambar
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
        raise ValueError("Tidak ada kontur yang ditemukan yang memiliki 4 titik sudut.")

    # Membuat masker dan menggambar kontur
    mask = np.zeros(gray.shape, np.uint8)
    cv2.drawContours(mask, [location], 0, 255, -1)

    # Memastikan mask tidak kosong sebelum melakukan operasi min dan max
    (x, y) = np.where(mask == 255)
    if x.size == 0 or y.size == 0:
        raise ValueError("Mask tidak memiliki area yang sesuai. Tidak ada kontur yang valid ditemukan.")

    (x1, y1) = (np.min(x), np.min(y))
    (x2, y2) = (np.max(x), np.max(y))
    cropped_image = gray[x1:x2+1, y1:y2+1]

    # Membaca teks dengan EasyOCR
    reader = easyocr.Reader(['en'])
    result = reader.readtext(cropped_image)

    # Mengambil hanya teks dari plat nomor
    text = result[0][-2]
    return text
