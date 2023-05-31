import RPi.GPIO as GPIO
import cv2
import time

# GPIO-Pin für das Relais
RELAY_PIN = 17

# Minimale Flächengröße der erkannten Konturen
MIN_CONTOUR_AREA = 1000

# Farbschwellenwerte für die Rot- und Grün-Erkennung (HSV-Farbraum)
RED_LOWER = (0, 70, 50)
RED_UPPER = (10, 255, 255)
GREEN_LOWER = (40, 70, 50)
GREEN_UPPER = (80, 255, 255)
YELLOW_LOWER = (20, 70, 50)
YELLOW_UPPER = (40, 255, 255)

# GPIO-Pins für den Ultraschallsensor
TRIGGER_PIN = 23
ECHO_PIN = 24

# GPIO-Pins für den Farbsensor (TCS3200)
S0_PIN = 27
S1_PIN = 22
S2_PIN = 5
S3_PIN = 6
OUT_PIN = 10
OE_PIN = 13

# GPIO-Pins für den Steppermotor
MOTOR_PIN = 16

# Frequenz der Farben
BLUE_FREQ = 500
ORANGE_FREQ = 1000


# Funktion zum Ein- und Ausschalten des Relais
def toggle_relay(state):
    GPIO.output(RELAY_PIN, state)


# Funktion zum Drehen des Steppermotors nach links
def rotate_left():
    global rotate_counter
    p.ChangeDutyCycle(5)
    time.sleep(3)
    p.ChangeDutyCycle(7.5)
    rotate_counter += 1


# Funktion zum Drehen des Steppermotors nach rechts
def rotate_right():
    global rotate_counter
    p.ChangeDutyCycle(10)
    time.sleep(3)
    p.ChangeDutyCycle(7.5)
    rotate_counter += 1


# Funktion zum Ausweichen nach links
def escape_left():
    p.ChangeDutyCycle(5)
    time.sleep(0.5)
    p.ChangeDutyCycle(7.5)


# Funktion zum Asuweichen nach rechts
def escape_right():
    p.ChangeDutyCycle(10)
    time.sleep(0.5)
    p.ChangeDutyCycle(7.5)


# Funktion zur Verarbeitung der Konturen
def process_contours(contours, frame, color):
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > MIN_CONTOUR_AREA:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)


# Funktion zur Distanzmessung mit dem Ultraschallsensor
def measure_distance():
    GPIO.output(TRIGGER_PIN, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIGGER_PIN, GPIO.LOW)

    start_time = time.time()
    end_time = time.time()

    while GPIO.input(ECHO_PIN) == 0:
        start_time = time.time()

    while GPIO.input(ECHO_PIN) == 1:
        end_time = time.time()

    duration = end_time - start_time
    distance = duration * 34300 / 2

    return distance


# Funktion zur Farberkennung mit dem TCS3200 Farbsensor
def detect_color():
    GPIO.output(S2_PIN, GPIO.LOW)
    GPIO.output(S3_PIN, GPIO.LOW)
    time.sleep(0.1)
    blue_value = GPIO.input(OUT_PIN)

    GPIO.output(S2_PIN, GPIO.HIGH)
    GPIO.output(S3_PIN, GPIO.HIGH)
    time.sleep(0.1)
    orange_value = GPIO.input(OUT_PIN)

    if blue_value == 0:
        return BLUE_FREQ
    elif orange_value == 0:
        return ORANGE_FREQ
    else:
        return 0


def measure_frequency():
    frequency = detect_color()

    # Farberkennung basierend auf der Frequenz
    if frequency == BLUE_FREQ:
        rotate_left()
        return "Blau"
    elif frequency == ORANGE_FREQ:
        rotate_right()
        return "Orange"
    else:
        return "Unbekannt"


# Initialisierung der GPIO-Pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN, GPIO.OUT)
toggle_relay(GPIO.LOW)  # Relais anschalten

# Initialisieren des Servos
GPIO.setup(MOTOR_PIN, GPIO.OUT)
p = GPIO.PWM(MOTOR_PIN, 50)
p.start(2.5)

# Initialisierung des Ultraschallsensors
GPIO.setup(TRIGGER_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

# Initialisierung des Farbsensors (TCS3200)
GPIO.setup(S0_PIN, GPIO.OUT)
GPIO.setup(S1_PIN, GPIO.OUT)
GPIO.setup(S2_PIN, GPIO.OUT)
GPIO.setup(S3_PIN, GPIO.OUT)
GPIO.setup(OUT_PIN, GPIO.IN)
GPIO.setup(OE_PIN, GPIO.OUT)
GPIO.output(OE_PIN, GPIO.LOW)  # OE-Pin aktivieren

# Initialisierung der Kamera
cam = cv2.VideoCapture(0)

# Initialisierung der Variablen
rotate_counter = 0
yellow_detected = False

while True:
    ret, frame = cam.read()

    if not ret:
        print("Fehler beim Lesen des Frames von der Kamera")
        break

    # Umwandeln des Frames in den HSV-Farbraum
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Erkennung der roten, grünen und gelben Farbe
    red_mask = cv2.inRange(hsv, RED_LOWER, RED_UPPER)
    green_mask = cv2.inRange(hsv, GREEN_LOWER, GREEN_UPPER)
    yellow_mask = cv2.inRange(hsv, YELLOW_LOWER, YELLOW_UPPER)

    # Erosion und Dilatation, um das Rauschen zu reduzieren
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    red_mask = cv2.erode(red_mask, kernel, iterations=2)
    red_mask = cv2.dilate(red_mask, kernel, iterations=2)
    green_mask = cv2.erode(green_mask, kernel, iterations=2)
    green_mask = cv2.dilate(green_mask, kernel, iterations=2)
    yellow_mask = cv2.erode(yellow_mask, kernel, iterations=2)
    yellow_mask = cv2.dilate(yellow_mask, kernel, iterations=2)

    # Konturerkennung
    red_contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    green_contours, _ = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    yellow_contours, _ = cv2.findContours(yellow_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Verarbeitung der Konturen
    process_contours(red_contours, frame, (0, 0, 255))  # Rahmen um rote Konturen in Rot zeichnen
    process_contours(green_contours, frame, (0, 255, 0))  # Rahmen um grüne Konturen in Grün zeichnen
    process_contours(yellow_contours, frame, (0, 255, 255))  # Rahmen um gelbe Konturen in Gelb zeichnen

    # Distanzmessung
    distance = measure_distance()
    cv2.putText(frame, f"Distanz: {distance:.2f} cm", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # Farberkennung
    color = measure_frequency()
    cv2.putText(frame, f"Farbe: {color}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # Aufteilung des Bildschirms in Viertel
    height, width, _ = frame.shape
    quarter_width = int(width / 4)

    # Überprüfung, ob ein rotes oder grünes Objekt im rechten Viertel ist und die Distanz kleiner als 30 cm ist
    if any([x < quarter_width for x, _, _, _ in cv2.boundingRect(contour) for contour in
            red_contours]) and distance < 30:
        escape_right()
        cv2.putText(frame, "Nach rechts ausweichen", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    elif any([x < quarter_width for x, _, _, _ in cv2.boundingRect(contour) for contour in
              green_contours]) and distance < 30:
        escape_left()
        cv2.putText(frame, "Nach links ausweichen", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    elif any([x < quarter_width for x, _, _, _ in cv2.boundingRect(contour) for contour in
              yellow_contours]) and distance < 30:
        yellow_detected = True
        cv2.putText(frame, "Gelbes Objekt erkannt", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        toggle_relay(GPIO.HIGH)
    else:
        cv2.putText(frame, "Geradeaus fahren", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # Zeichnen eines gelben Rahmens, wenn ein gelbes Objekt erkannt wurde
    if yellow_detected:
        cv2.rectangle(frame, (0, 0), (width, height), (0, 255, 255), 2)

    # Anzeige des Frames
    cv2.imshow("Objekterkennung", frame)

    # Beenden, wenn die Taste "q" gedrückt wird
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Freigeben der Ressourcen
GPIO.output(RELAY_PIN, GPIO.LOW)  # Relais ausschalten
toggle_relay(GPIO.LOW)
cam.release()
cv2.destroyAllWindows()
GPIO.cleanup()
