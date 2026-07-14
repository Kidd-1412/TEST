import RPi.GPIO as GPIO
import time

ROW = [5,6,13,19,26,16,20,21]
COL = [12,25,24,23,18,15,14,4]


HEART= [
    [0,0,0,0,0,0,0,0],
    [0,1,1,0,0,1,1,0],
    [1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1],
    [0,1,1,1,1,1,1,0],
    [0,0,1,1,1,1,0,0],
    [0,0,0,1,1,0,0,0],
    [0,0,0,0,0,0,0,0]
]

# GPIO 初始化
GPIO.setmode(GPIO.BCM)
for r in ROW:
    GPIO.setup(r, GPIO.OUT)
    GPIO.output(r, GPIO.LOW)
for c in COL:
    GPIO.setup(c, GPIO.OUT)
    GPIO.output(c, GPIO.HIGH)

def display_with_brightness(brightness):

    pwm_period = 0.005  # PWM周期 5ms
    on_time = pwm_period * (brightness / 100)
    off_time = pwm_period - on_time
    
    # 逐行扫描
    for r in range(8):
        for c in range(8):
            if HEART[r][c]:
                GPIO.output(COL[c], GPIO.LOW)   # 需要亮的列拉低
            else:
                GPIO.output(COL[c], GPIO.HIGH)  # 不亮的列拉高
            if brightness > 0:
                GPIO.output(ROW[r], GPIO.HIGH)
                time.sleep(on_time)
                GPIO.output(ROW[r], GPIO.LOW)
                time.sleep(off_time)

try:
   
    while True:
        for brightness in range(0, 101, 2):
            start_time = time.time()
            while time.time() - start_time < 0.03:  # 每个亮度保持30ms
                display_with_brightness(brightness)
        
        # 渐灭 100% → 0%
        for brightness in range(100, -1, -2):
            start_time = time.time()
            while time.time() - start_time < 0.03:
                display_with_brightness(brightness)

except KeyboardInterrupt:
    GPIO.cleanup()