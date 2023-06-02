import RPi.GPIO as GPIO
import time
import cv2
from time import sleep

# GPIO-Pins für den Servomotor und das Relais
servo_pin = 18
relay_pin = 26
button_pin = 16

# Farbbereiche für Blau und Orange
blue_lower = (100, 0, 0)
blue_upper = (255, 100, 100)
orange_lower = (0, 100, 200)
orange_upper = (100, 200, 255)

# Initialisierung der GPIO-Pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)
GPIO.setup(relay_pin, GPIO.OUT)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Funktion zum Steuern des Servomotors
def steer_servo(angle):
    pwm = GPIO.PWM(servo_pin, 50)  # PWM mit einer Frequenz von 50 Hz
    pwm.start(2.5)  # Startposition des Servomotors

    # Berechnung des Tastverhältnisses für den gewünschten Winkel
    duty_cycle = (angle / 18.0) + 2.5

    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(0.3)  # Wartezeit, damit der Servomotor die Position erreichen kann
    pwm.stop()

# Funktion zur Erkennung der Farbe
def detect_color(pixel):
    if blue_lower[0] <= pixel[0] <= blue_upper[0] and \
       blue_lower[1] <= pixel[1] <= blue_upper[1] and \
       blue_lower[2] <= pixel[2] <= blue_upper[2]:
        return "blue"
    elif orange_lower[0] <= pixel[0] <= orange_upper[0] and \
         orange_lower[1] <= pixel[1] <= orange_upper[1] and \
         orange_lower[2] <= pixel[2] <= orange_upper[2]:
        return "orange"
    else:
        return "unknown"

# Hauptprogramm
try:
    counter = 0
    button_pressed = False

    cap = cv2.VideoCapture(0)  # Verwendung der ersten USB-Kamera (Index 0)

    while True:
        if GPIO.input(button_pin) == GPIO.LOW:
            button_pressed = True

        if button_pressed:
            # Erfasse ein Bild von der Kamera
            ret, frame = cap.read()
            if not ret:
                continue

            # Führe Farberkennung durch
            height, width, _ = frame.shape
            center_x = width // 2
            center_y = height // 2
            pixel = frame[center_y, center_x]

            color = detect_color(pixel)

            if color == "blue":
                print("Erkannte Farbe: Blau")
                steer_servo(90)  # Linkskurve für 2 Sekunden
                time.sleep(2)
                steer_servo(0)  # Servomotor zurück in die Ausgangsposition
                counter += 1
            elif color == "orange":
                print("Erkannte Farbe: Orange")
                steer_servo(-90)  # Rechtskurve für 2 Sekunden
                time.sleep(2)
                steer_servo(0)  # Servomotor zurück in die Ausgangsposition
                counter += 1

            button_pressed = False

        if counter >= 12:
            time.sleep(2)  # Warte 2 Sekunden
            break

except KeyboardInterrupt:
    print("Programm abgebrochen.")

finally:
    cap.release()  # Kamera freigeben
    GPIO.output(relay_pin, GPIO.LOW)  # Relais ausschalten
    GPIO.cleanup()
