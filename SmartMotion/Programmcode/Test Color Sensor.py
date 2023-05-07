import RPi.GPIO as GPIO
import time

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

if __name__ == '__main__':
    try:
        while True:
            print('Hello')
            r, g, b = read_color()
            print("Farbe: R=%d, G=%d, B=%d" % (r, g, b))
            

    except KeyboardInterrupt:
        print("Programm abgebrochen.")
        GPIO.cleanup()
        print('leave')
