import RPi.GPIO as GPIO
import time
from Adafruit_LED_Backpack.SevenSegment import SevenSegment

timing = False
t1 = time.time()

def my_callback(channel):
    global timing, t1
    if not timing:
        t1 = time.time()
        timing = True
    else:
        t2 = time.time()
        # stopwatch = t2 - t1
        # print(stopwatch)
        timing = False


def my_callback2(channel):
    print("Falling edge detected on Raspberry Pi pin 40")


def main():
    global timing, t1
    disp = SevenSegment(address = 0x70)
    disp.begin()
    t1 = time.time()

    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(40, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    GPIO.add_event_detect(40, GPIO.FALLING, callback=my_callback, bouncetime=300)

    disp.clear()

    while 1:

        try:
            pass
            # print(GPIO.input(40))
        except KeyboardInterrupt:
            disp.clear()
            GPIO.cleanup()

        if timing:
            current = time.time() - t1
            if current < 10:
                strc = str(current)
                str1 = strc[0]
                str2 = strc[2]
                str3 = strc[3]
                str4 = strc[4]
                dec = 0
            elif current < 100:
                strc = str(current)
                str1 = strc[0]
                str2 = strc[1]
                str3 = strc[3]
                str4 = strc[4]
                dec = 1
            elif current < 1000:
                strc = str(current)
                str1 = strc[0]
                str2 = strc[1]
                str3 = strc[2]
                str4 = strc[4]
                dec = 2
            else:
                strc = str(current)
                str1 = strc[0]
                str2 = strc[1]
                str3 = strc[2]
                str4 = strc[3]
                dec = -1

            # print(current)
            current = round(current,0)
            disp.set_digit(0, int(str1))
            disp.set_digit(1, int(str2))
            disp.set_digit(2, int(str3))
            disp.set_digit(3, int(str4))
            disp.set_decimal(dec,True)

        else:
            disp.set_digit(0, int(0))
            disp.set_digit(1, int(0))
            disp.set_digit(2, int(0))
            disp.set_digit(3, int(0))

        disp.write_display()
        time.sleep(0.025)

    GPIO.cleanup()


if __name__ == "__main__":
    main()
