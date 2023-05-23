import time
import RPi.GPIO as GPIO
import cv2
import asyncio

# GPIO-Pins für Servomotor, Farbsensor und Ultraschallsensor
SERVO_PIN = 13
COLOR_SENSOR_PINS = {
    'S0': 17,
    'S1': 27,
    'S2': 22,
    'S3': 23,
    'OUT': 24
}
ULTRASONIC_TRIGGER_PIN = 26
ULTRASONIC_ECHO_PIN = 19
RELAY_PIN = 18

# Farbfilterfrequenzen
COLOR_FREQUENCIES = {
    0: (False, False),
    1: (False, True),
    2: (True, False),
    3: (True, True)
}

# Farbbereiche für Rot und Grün im HSV-Farbraum
LOWER_RED = (0, 100, 100)
UPPER_RED = (20, 255, 255)
LOWER_GREEN = (40, 50, 50)
UPPER_GREEN = (80, 255, 255)

# Initialisierung der GPIO-Pins
def setup_gpio_pins():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SERVO_PIN, GPIO.OUT)
    GPIO.setup(ULTRASONIC_TRIGGER_PIN, GPIO.OUT)
    GPIO.setup(ULTRASONIC_ECHO_PIN, GPIO.IN)
    GPIO.setup(RELAY_PIN, GPIO.OUT)
    for pin in COLOR_SENSOR_PINS.values():
        GPIO.setup(pin, GPIO.OUT)

# Initialisierung des Servomotors
def setup_servo():
    p = GPIO.PWM(SERVO_PIN, 100)
    p.start(2.5)
    return p

# Servomotor-Funktionen
def block_turn(p, angle):
    p.ChangeDutyCycle(angle)

# Farbsensor-Funktionen
async def set_color(freq):
    # Iteriere über die Farbsensor-Pins und die Zustände entsprechend der Frequenz
    for pin, state in zip(COLOR_SENSOR_PINS.values(), COLOR_FREQUENCIES[freq]):
        # Setze den Ausgangszustand des Pins entsprechend des gewünschten Frequenzbits
        GPIO.output(pin, state)
        await asyncio.sleep(0)  # Kurze Pause, um die Kontrolle abzugeben



async def read_color():
    # Setzt die Frequenz auf rot
    await set_color(0)
    await asyncio.sleep(0.1)  # Eine kurze Pause, um die Messung zu stabilisieren
    # Misst den Farbwert für Rot
    red = pulse_in(COLOR_SENSOR_PINS['OUT'], GPIO.LOW)

    # Setzt die Frequenz auf grün
    await set_color(1)
    await asyncio.sleep(0.1)  # Eine kurze Pause, um die Messung zu stabilisieren
    # Misst den Farbwert für Grün
    green = pulse_in(COLOR_SENSOR_PINS['OUT'], GPIO.LOW)

    # Setzt die Frequenz auf blau
    await set_color(2)
    await asyncio.sleep(0.1)  # Eine kurze Pause, um die Messung zu stabilisieren
    # Misst den Farbwert für Blau
    blue = pulse_in(COLOR_SENSOR_PINS['OUT'], GPIO.LOW)

    # Gibt die Farbwerte für Rot, Grün und Blau als Tupel zurück
    return red, green, blue


def pulse_in(pin, state):
    # Startzeit erfassen
    start_time = time.time()

    # Warten, bis das Signal am Pin den gewünschten Zustand erreicht
    while GPIO.input(pin) != state:
        pass

    # Warten, bis das Signal am Pin den Zustand ändert (andere Zustand als zuvor)
    while GPIO.input(pin) == state:
        pass

    # Stopzeit erfassen
    stop_time = time.time()

    # Berechnung der Dauer des Signals in Mikrosekunden und Rückgabe des Ergebnisses
    return (stop_time - start_time) * 1000000


# Ultraschallsensor-Funktionen
async def distance():
    # Triggersignal senden
    GPIO.output(ULTRASONIC_TRIGGER_PIN, True)
    await asyncio.sleep(0.00001)
    GPIO.output(ULTRASONIC_TRIGGER_PIN, False)

    # Start- und Endzeit initialisieren
    start_time = time.time()
    end_time = time.time()

    # Startzeit erfassen, wenn das Echosignal den Zustand 0 hat
    while GPIO.input(ULTRASONIC_ECHO_PIN) == 0:
        start_time = time.time()

    # Endzeit erfassen, wenn das Echosignal den Zustand 1 hat
    while GPIO.input(ULTRASONIC_ECHO_PIN) == 1:
        end_time = time.time()

    # Zeitdifferenz berechnen
    time_diff = end_time - start_time

    # Entfernung berechnen unter Berücksichtigung der Schallgeschwindigkeit
    distance = (time_diff * 34300) / 2

    return distance


# Relais-Funktionen
def toggle_relay():
    GPIO.output(RELAY_PIN, GPIO.HIGH)

# Webcam und Farberkennung
def setup_webcam():
    cam = cv2.VideoCapture(0)
    return cam


def detect_colors(frame):
    # Konvertierung des Bildes in den HSV-Farbraum
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Erstellung einer Maske für rote Farben
    mask_red = cv2.inRange(hsv, LOWER_RED, UPPER_RED)

    # Erstellung einer Maske für grüne Farben
    mask_green = cv2.inRange(hsv, LOWER_GREEN, UPPER_GREEN)

    # Konturen für rote Farben finden
    contours_red, _ = cv2.findContours(mask_red, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Konturen für grüne Farben finden
    contours_green, _ = cv2.findContours(mask_green, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Konturen für rote und grüne Farben zurückgeben
    return contours_red, contours_green

def distance():
    # Trig-Pin auf HIGH setzen
    GPIO.output(ULTRASONIC_TRIGGER_PIN, True)

    # Eine kurze Pause einlegen
    asyncio.sleep(0.00001)

    # Trig-Pin auf LOW setzen
    GPIO.output(ULTRASONIC_TRIGGER_PIN, False)

    # Start- und Stop-Zeitpunkte initialisieren
    start_time = 0
    stop_time = 0

    # Startzeit erfassen
    while GPIO.input(ULTRASONIC_ECHO_PIN) == 0:
        start_time = time.time()

    # Stopzeit erfassen
    while GPIO.input(ULTRASONIC_ECHO_PIN) == 1:
        stop_time = time.time()

    # Zeitdifferenz berechnen
    time_diff = stop_time - start_time

    # Schallgeschwindigkeit (in cm/s) berücksichtigen und Entfernung berechnen
    distance = (time_diff * 34300) / 2

    return distance


def process_contours(frame, contours_red, contours_green, **kwargs):

    cam = setup_webcam()

    ret, frame = cam.read()

    p = setup_servo()
    required_pixel_count = kwargs.get('required_pixel_count', 0)
    frame_height, frame_width = frame.shape[:2]
    quarter_width = frame_width // 4
    left_quarter_x = quarter_width
    right_quarter_x = frame_width - quarter_width


    # Verarbeitung der roten Konturen
    for c in contours_red:
        x, y, w, h = cv2.boundingRect(c)
        contour_center_x = x + w // 2

        # Überprüfen, ob sich die Kontur im linken Viertel befindet und die Entfernung kleiner als 20 ist
        if w >= required_pixel_count:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)  # Rotes Rechteck zeichnen
            if x < left_quarter_x and distance() < 20:
                # Blockiere Drehung des Servos um 10 Grad
                block_turn(p, 10)
                asyncio.sleep(1)
                # Blockiere Drehung des Servos um 5 Grad
                block_turn(p, 5)
                asyncio.sleep(1)

                # Blockiere Drehung des Servos um 7,5 Grad
                block_turn(p, 7.5)

                return 0

    # Verarbeitung der grünen Konturen
    for c in contours_green:
        x, y, w, h = cv2.boundingRect(c)
        contour_center_x = x + w // 2

        if w <= required_pixel_count:

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Grünes Rechteck zeichnen
            # Überprüfen, ob sich die Kontur im rechten Viertel befindet und die Entfernung kleiner als 20 ist
            if x > right_quarter_x and distance() < 20:
                # Blockiere Drehung des Servos um 5 Grad
                block_turn(p, 5)
                asyncio.sleep(1)

                # Blockiere Drehung des Servos um 10 Grad
                block_turn(p, 10)
                asyncio.sleep(1)

                # Blockiere Drehung des Servos um 7,5 Grad
                block_turn(p, 7.5)

                return 0

    # Farbwerte lesen
    red, green, blue = read_color()

    # Überprüfen der Farbwerte
    if blue > red and blue > green:
        # Blockiere Drehung des Servos um 5 Grad
        block_turn(p, 5)
        asyncio.sleep(2)

        # Blockiere Drehung des Servos um 7,5 Grad
        block_turn(p, 7.5)
    elif red > blue and red > green:
        # Blockiere Drehung des Servos um 10 Grad
        block_turn(p, 10)
        asyncio.sleep(2)

        # Blockiere Drehung des Servos um 7,5 Grad
        block_turn(p, 7.5)

    return 0


async def main():
    # GPIO-Pins einrichten
    setup_gpio_pins()

    # Servo initialisieren
    p = setup_servo()

    # Webcam initialisieren
    cam = setup_webcam()

    while True:
        # Einzelbild von der Webcam erfassen
        _, frame = cam.read()

        # Relais umschalten
        toggle_relay()

        if frame is None:
            print("Fehler beim Lesen des Frames von der Webcam")
            break

        # Farbkonturen erkennen
        contours_red, contours_green = detect_colors(frame)

        # Konturen verarbeiten
        contours_red, contours_green = detect_colors(frame)
        result = process_contours(frame, contours_red, contours_green, required_pixel_count=100)

        # Originalbild anzeigen
        cv2.imshow("Original", frame)

        # Auf Tastendruck 'q' beenden
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Kurze Pause
        asyncio.sleep(0.01)

    # Webcam freigeben
    cam.release()

    # OpenCV-Fenster schließen
    cv2.destroyAllWindows()

    # Servo stoppen
    p.stop()

    # GPIO bereinigen
    GPIO.cleanup()


if __name__ == '__main__':
    main()