import RPi.GPIO as GPIO

# Setze den Pin-Modus
GPIO.setmode(GPIO.BCM)

# Definiere den Pin, an dem der Taster angeschlossen ist
button_pin = 17

# Konfiguriere den Taster-Pin als Eingang
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Warte auf Tastendruck
print("Warte auf Tastendruck...")
GPIO.wait_for_edge(button_pin, GPIO.FALLING)

# Tastendruck erkannt
print("Taste gedrückt: 1")

# Bereinigung
GPIO.cleanup()
