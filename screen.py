import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import subprocess
import threading
import time
import board
import adafruit_hcsr04
import math

sonar_right = adafruit_hcsr04.HCSR04(trigger_pin=board.D5, echo_pin=board.D6)
sonar_left = adafruit_hcsr04.HCSR04(trigger_pin=board.D13, echo_pin=board.D19)

debug = False


frame_map = {
    "blink": 2,
    "angry": 4,
    "test": 6,
    "test2": 3,
    "bored": 5,
    "excited": 3,
    "sad": 5,
    "sleepy": 4,
    "shaky": 6,
    "spiral": 3
}


########################################################################
#                          Setup  Display
########################################################################


RST = 0

disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
disp.begin()
disp.clear()
disp.display()

width = disp.width
height = disp.height

image1 = Image.new('1', (width, height))

draw = ImageDraw.Draw(image1)
draw.rectangle((0,0,width,height), outline=0, fill=0)

padding = 0
top = padding

bottom = height-padding
x = 0
# font = ImageFont.load_default()  #Default Font Settings
font = ImageFont.truetype('Minecraft.ttf', 14)  # Use the Opensource Minecraft font


# Write Anna B-day splash.
disp.clear()
disp.display()
draw.text((x, top+18),       "Anna's B-Day 2020" ,  font=font, fill=255)
draw.text((x, top+34),     "anna@egloff.tech", font=font, fill=255)



# Display image.
disp.image(image1)
disp.display()
time.sleep(2)


########################################################################
#                             Functions
########################################################################
def write_log(log_text):
    if debug == True:
        print(log_text)

class renderAnimation:
    # Example non-blocking usage
    # a = renderAnimation()  
    # current_animation = ["blink",1]
    # animation_thread = threading.Thread(target=a.animationLoop, args=current_animation)
    # animation_thread.start()
    # animation_thread.join()
    
    
    def __init__(self): 
        self._running = True
        
    def terminate(self): 
        self._running = False
        
    def animation(self, animation, loop_count):
        while loop_count > 0:
            self._running = True
            num_of_frames = frame_map[animation]
            current_img = 1
            direction = "forward"
            draw.rectangle((0,0,width,height), outline=0, fill=0)
            write_log("Current Status: %s" % self._running)
            while self._running:
                draw.rectangle((0,0,width,height), outline=0, fill=0)
                image_name = "./%s/%s.png" % (animation, current_img)
                write_log("CurrentImage = %s" % image_name)
                image = Image.open(image_name)
                image = image.convert('L')
                # image = image.convert('1') # Basic original convert to B&W
                image = image.point(lambda x: 0 if x<20 else 255, '1') # Round to white convert to B&W
                disp.image(image)
                disp.display()
                if current_img == num_of_frames:
                    self._running = False
                current_img += 1
                write_log("Current Image: %s, Current Direction: %s" % (current_img, direction))
            loop_count -= 1
        return(0)
    
    def animationLoop(self, animation, loop_count):
        while loop_count > 0:
            self._running = True
            num_of_frames = frame_map[animation]
            current_img = 1
            direction = "forward"
            draw.rectangle((0,0,width,height), outline=0, fill=0)
            write_log("Current Status: %s" % self._running)
            while self._running:
                draw.rectangle((0,0,width,height), outline=0, fill=0)
                image_name = "./%s/%s.png" % (animation, current_img)
                write_log("CurrentImage = %s" % image_name)
                image = Image.open(image_name)
                image = image.convert('L')
                # image = image.convert('1') # Basic original convert to B&W
                image = image.point(lambda x: 0 if x<20 else 255, '1') # Round to white convert to B&W
                disp.image(image)
                disp.display()
                if current_img == num_of_frames:
                    direction = "reverse"
                if current_img == 1  and direction == "reverse":
                    self._running = False
                if direction == "forward":
                    current_img += 1
                else:
                    current_img -= 1
                write_log("Current Image: %s, Current Direction: %s" % (current_img, direction))
            loop_count -= 1
        return(0)


class measure:
    
    def left_distance():
        number_of_samples = 1
        distance = 0
        try:
            # for i in range(number_of_samples):
                distance += sonar_left.distance
                # time.sleep(.25)
            # distance = distance / (number_of_samples + 1)
        except RuntimeError:
            distance = 0
        return distance
    
    def right_distance():
        number_of_samples = 3
        distance = 0
        try:
            # for i in range(number_of_samples):
                distance += sonar_right.distance
                time.sleep(.3)
            #     time.sleep(.25)
            # distance = distance / (number_of_samples + 1)
        except RuntimeError:
            distance = 0
        return distance


class movement:
    def forward():
        print("Forward")

    def reverse():
        print("Revers")
    
    def left():
        print("Left")
        
    def right():
        print("Right")

if __name__ == '__main__':
    
    
    font = ImageFont.truetype('Minecraft.ttf', 36)
   
    while True:
        current_left = measure.left_distance()
        time.sleep(.1)
        current_right = measure.right_distance()
        disp.clear()
        disp.display()
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        draw.text((8, top+14), str(math.ceil(current_left)),  font=font, fill=255)      
        draw.text((72, top+14), str(math.ceil(current_right)),  font=font, fill=255)
        # Display image.
        disp.image(image1)
        disp.display()
        # time.sleep(.5)
    
    
    
    
    
    
    # 
    # a = renderAnimation()  
    # current_animation = ["blink",1]
    # animation_thread = threading.Thread(target=a.animationLoop, args=current_animation)
    # animation_thread.start()
    # animation_thread.join()
    # 
    # time.sleep(.5)
    # a = renderAnimation()
    # current_animation = ["angry",1]
    # animation_thread = threading.Thread(target=a.animationLoop, args=current_animation)
    # animation_thread.start() 
    # animation_thread.join()
    # 
    # time.sleep(.5)
    # a = renderAnimation()
    # current_animation = ["bored",1]
    # animation_thread = threading.Thread(target=a.animationLoop, args=current_animation)
    # animation_thread.start()
    # animation_thread.join()
    # 
    # time.sleep(.5)
    # a = renderAnimation()
    # current_animation = ["excited",1]
    # animation_thread = threading.Thread(target=a.animationLoop, args=current_animation)
    # animation_thread.start() 
    # animation_thread.join()
    # 
    # time.sleep(.5)
    # a = renderAnimation()
    # current_animation = ["sad",1]
    # animation_thread = threading.Thread(target=a.animationLoop, args=current_animation)
    # animation_thread.start() 
    # animation_thread.join()
    # 
    # time.sleep(.5)
    # a = renderAnimation()
    # current_animation = ["sleepy",1]
    # animation_thread = threading.Thread(target=a.animation, args=current_animation)
    # animation_thread.start() 
    # animation_thread.join()
    # 
    # time.sleep(.5)
    # a = renderAnimation()
    # current_animation = ["shaky",1]
    # animation_thread = threading.Thread(target=a.animation, args=current_animation)
    # animation_thread.start()
    # animation_thread.join()
    # 
    # time.sleep(.5)
    # a = renderAnimation()
    # current_animation = ["spiral",6]
    # animation_thread = threading.Thread(target=a.animation, args=current_animation)
    # animation_thread.start()
    # animation_thread.join()
    # 


