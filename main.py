import time
import RPi.GPIO as GPIO
import cv2

# Ab Hier wird der Servomotor programmiert

# GPIO-Pin für den Servomotor
Servo_PIN = 14

# PMW-Frequenz und Duty-Cicle
PMW_FREQ = 50 # Frequenz in Hertz
DUTY_CICLE_MIN = 5 # Minimaler Duty-Cicle in Prozent
DUTY_CICLE_MAX = 20 # Maximaler Duty-Cicle in Prozent

# Initialisieren der GPIO-Pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(Servo_PIN, GPIO.OUT)

# Erstellen des PWM Objekt
pwm = GPIO.PWM(Servo_PIN, PMW_FREQ)

# Funktionen des Servomotors

def block_turn(servo_angle):
    # Berechnung des Duty Cycles entsprechend des gewünschten Winkels
    duty_cycle = DUTY_CICLE_MIN + (servo_angle/ 180.0) * (DUTY_CICLE_MAX - DUTY_CICLE_MIN)
    pwm.start(duty_cycle)
    time.sleep(0.1)  # Wartezeit für Servomotor, um auf Position zu kommen
    pwm.stop()


# Ab Hier beginnt der Part für die Webcam und die Farberkennung
# Initialisiere die Webcam
cam = cv2.VideoCapture(0)

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