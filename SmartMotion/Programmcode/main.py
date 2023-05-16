import time
import RPi.GPIO as GPIO
import cv2

#Variable zum Messen der Zeit

timeForSteering = 0

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

# Ab hier wird der Farbsensor programmiert

# Zuordnung der GPIO Pins
S0 = 17
S1 = 27
S2 = 22
S3 = 23
OUT = 24

# Setzt die GPIO Pins als Ein- oder Ausgang
GPIO.setmode(GPIO.BCM)
GPIO.setup(S0, GPIO.OUT)
GPIO.setup(S1, GPIO.OUT)
GPIO.setup(S2, GPIO.OUT)
GPIO.setup(S3, GPIO.OUT)
GPIO.setup(OUT, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Setzt die Frequenz des Farbsensors
# 0 = kein Filter, 1 = 2% Filter, 2 = 20% Filter, 3 = 100% Filter
def set_color(freq):
    print('setColor')
    if freq == 0:
        GPIO.output(S2, False)
        GPIO.output(S3, False)
    elif freq == 1:
        GPIO.output(S2, False)
        GPIO.output(S3, True)
    elif freq == 2:
        GPIO.output(S2, True)
        GPIO.output(S3, False)
    elif freq == 3:
        GPIO.output(S2, True)
        GPIO.output(S3, True)

# Liest den Farbwert aus dem Sensor aus
def read_color():
    print('readColor')
    # Setzt die Frequenz auf rot
    set_color(0)

    # Wartet 0,1 Sekunden, um die Messung zu stabilisieren
    time.sleep(0.1)

    # Liest den Farbwert aus dem Sensor aus
    red = pulseIn(OUT, GPIO.LOW)

    # Setzt die Frequenz auf grün
    set_color(1)

    # Wartet 0,1 Sekunden, um die Messung zu stabilisieren
    time.sleep(0.1)

    # Liest den Farbwert aus dem Sensor aus
    green = pulseIn(OUT, GPIO.LOW)

    # Setzt die Frequenz auf blau
    set_color(2)

    # Wartet 0,1 Sekunden, um die Messung zu stabilisieren
    time.sleep(0.1)

    # Liest den Farbwert aus dem Sensor aus
    blue = pulseIn(OUT, GPIO.LOW)

    # Gibt den Farbwert als Tupel zurück
    return (red, green, blue)

# Liest den Puls von dem angegebenen Pin aus
def pulseIn(pin, state):
    print('pulse')
    #while GPIO.input(pin) != state:
    #    pass

    start_time = time.time()

    #while GPIO.input(pin) == state:
    #    pass

    stop_time = time.time()
    print('BLIB')

    return (stop_time - start_time) * 1000000
    
# Ab hier wird der Ultraschallsensor programmiert

# GPIO definieren (Modus, Pins, Output)
GPIO.setmode(GPIO.BCM)
GPIO_TRIGGER = 26
GPIO_ECHO = 19
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)


def entfernung():
    # Trig High setzen
    GPIO.output(GPIO_TRIGGER, True)

    # Trig Low setzen (nach 0.01ms)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    Startzeit = time.time()
    Endzeit = time.time()

    # Start/Stop Zeit ermitteln
    while GPIO.input(GPIO_ECHO) == 0:
        Startzeit = time.time()

    while GPIO.input(GPIO_ECHO) == 1:
        Endzeit = time.time()

    # Vergangene Zeit
    Zeitdifferenz = Endzeit - Startzeit
    # Schallgeschwindigkeit (34300 cm/s) einbeziehen
    entfernung = (Zeitdifferenz * 34300) / 2

    return entfernung

# Ab hier wird der DC Motor programmiert. Dieser ist an ein Relais angeschlossen
relay_pin = 18

# Initialisieren der GPIO-Pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(relay_pin, GPIO.OUT)

# Funktion zum Schalten des Relais
def toggle_relay():
    GPIO.output(relay_pin, GPIO.HIGH)  # Relais einschalten

# Ab Hier beginnt der Part für die Webcam und die Farberkennung
# Initialisiere die Webcam
cam = cv2.VideoCapture(0)
GPIO.setwarnings(False)



while True:
    # Lese das aktuelle Bild von der Webcam ein
    _, frame = cam.read()

    toggle_relay()

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
        if x < left_quartar_x and entfernung() < 20:
            block_turn(10)
            time.sleep(1)
            block_turn(5)
            time.sleep(1)
            block_turn(7.5)
            break

    # Iterate through the contours of green
    for c in contours_green and entfernung() < 20:
        result = 0
        # Get the bounding rectangle of the contour
        x, y, w, h = cv2.boundingRect(c)
        # Get the center x-coordinate of the bounding rectangle
        contour_center_x = x + w // 2
        # Check if the center x-coordinate of the bounding rectangle is on the left half of the frame
        if x > right_quarter_x:
            block_turn(5)
            time.sleep(1)
            block_turn(10)
            time.sleep(1)
            block_turn(7.5)
            break
    print(result)

    red, green, blue = read_color()

    # Prüfe, ob die erkannte Farbe Blau ist
    if blue > red and blue > green:
        # Führe die Aktion für Blau aus
        block_turn(5)
        time.sleep(2)
        block_turn(7.5)

        # Prüfe, ob die erkannte Farbe Orange ist
    if red > blue and red > green:
        # Führe die Aktion für Orange aus
        block_turn(10)
        time.sleep(2)
        block_turn(7.5)

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


    time.sleep(0.1)


# Freigabe der Ressourcen
cam.release()
cv2.destroyAllWindows()
p.stop()
GPIO.cleanup()
