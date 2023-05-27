import cv2
import time
import numpy

# Funktion zur Farberkennung
import cv2
import numpy as np


def detect_colors(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Rot
    mask_red = cv2.inRange(hsv, (0, 120, 70), (10, 255, 255))

    # Grün
    mask_green = cv2.inRange(hsv, (40, 50, 50), (80, 255, 255))

    contours_red, _ = cv2.findContours(mask_red, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_green, _ = cv2.findContours(mask_green, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    return contours_red, contours_green


# Funktion zur Verarbeitung der Konturen
# Funktion zur Verarbeitung der Konturen
# Funktion zur Verarbeitung der Konturen
def process_contours(frame, contours_red, contours_green, **kwargs):
    required_pixel_count = kwargs.get('required_pixel_count', 0)
    frame_height, frame_width = frame.shape[:2]
    quarter_width = frame_width // 4
    left_quarter_x = quarter_width
    right_quarter_x = frame_width - quarter_width

    for c in contours_red:
        x, y, w, h = cv2.boundingRect(c)
        contour_center_x = x + w // 2

        # Überprüfen, ob die Breite der Kontur ausreichend ist
        if w >= required_pixel_count:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)  # Rotes Rechteck zeichnen
            return 0

    for c in contours_green:
        x, y, w, h = cv2.boundingRect(c)
        contour_center_x = x + w // 2

        # Überprüfen, ob die Breite der Kontur ausreichend ist
        if w >= required_pixel_count:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Grünes Rechteck zeichnen
            return 0



    return 0



# Hauptfunktion
def main():
    cam = cv2.VideoCapture(0)

    while True:
        _, frame = cam.read()
        # Hier kommt der Code zur Erfassung des Frames und anderer Verarbeitungsschritte

        contours_red, contours_green = detect_colors(frame)
        result = process_contours(frame, contours_red, contours_green, required_pixel_count=100)

        cv2.imshow("Original", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        time.sleep(0.1)

    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
