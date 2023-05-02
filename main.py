import time
import RPi.GPIO as GPIO
import cv2

# Ab Hier wird der Servomotor programmiert

# GPIO-Pin für den Servomotor
Servo_PIN = 13

# Initialisieren der GPIO-Pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(Servo_PIN, GPIO.OUT)

# Erstellen des PWM Objekt
p= GPIO.PWM(Servo_PIN, 100)
p.start(2.5)

# Funktionen des Servomotors

def block_turn(angle):
    p.ChangeDutyCycle(angle)
    

# Ab Hier beginnt der Part für die Webcam und die Farberkennung
# Initialisiere die Webcam
cam = cv2.VideoCapture(0)
GPIO.setwarnings(False)

while True:
    # Lese das aktuelle Bild von der Webcam ein
    _, frame = cam.read()

    if frame is None:
        print("Error while reading frame from the webcam")
        break
    # Konvertiere das Bild in den HSV-Farbraum
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Definiere die Farbräume für Rot und Grün
    lower_red = (0,100,100) # this range of hsv value for red color
    upper_red = (20,255,255)
    lower_green = (35,100,100) # this range of hsv value for green color
    upper_green = (77,255,255)

    # Erstelle Masken für Rot und Grün
    mask_red = cv2.inRange(hsv, lower_red, upper_red)
    mask_green = cv2.inRange(hsv, lower_green, upper_green)

    #Kontouren des Gesichts
    contours_red, _ = cv2.findContours(mask_red, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_green, _ = cv2.findContours(mask_green, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Bitweise AND der Masken mit dem Originalbild, um die gewünschten Farben hervorzuheben
    res_red = cv2.bitwise_and(frame, frame, mask=mask_red)
    res_green = cv2.bitwise_and(frame, frame, mask=mask_green)

    # Split the image into left and right parts
    frame_width = frame.shape[1]
    frame_heigh = frame.shape[0]

    quarter_width = frame_width // 4
    left_quartar_x = quarter_width
    right_quarter_x = frame_width - quarter_width

    #Variable für die Ausgaben
    result = 0

    # Iterate through the contours of red
    for c in contours_red:
        result = 0
        # Get the bounding rectangle of the contour
        x, y, w, h = cv2.boundingRect(c)
        # Get the center x-coordinate of the bounding rectangle
        contour_center_x = x + w // 2
        # Check if the center x-coordinate of the bounding rectangle is on the right half of the frame
        if x < left_quartar_x:
            result = 10
            block_turn(10)
            time.sleep(0.3)
            block_turn(14)
            time.sleep(0.3)
            block_turn(12)
            time.sleep(1)
            break
    # Iterate through the contours of green
    for c in contours_green:
        result = 0
        # Get the bounding rectangle of the contour
        x, y, w, h = cv2.boundingRect(c)
        # Get the center x-coordinate of the bounding rectangle
        contour_center_x = x + w // 2
        # Check if the center x-coordinate of the bounding rectangle is on the left half of the frame
        if x > right_quarter_x:
            result = 20
            break
    print(result)

    # Kontouren in den Originalen Frame einfügen
    for c in contours_red:
        cv2.drawContours(frame, [c], -1, (0,0,255), 2)
    for c in contours_green:
        cv2.drawContours(frame, [c], -1, (0,255,0), 2)

    # Zeige das Ergebnis auf dem Bildschirm an
    cv2.imshow("Original", frame)
    cv2.imshow("Rot", res_red)
    cv2.imshow("Gruen", res_green)

    # Warte auf Taste 'q', um das Programm zu beenden
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Freigabe der Ressourcen
cam.release()
cv2.destroyAllWindows()
p.stop()
GPIO.cleanup()
