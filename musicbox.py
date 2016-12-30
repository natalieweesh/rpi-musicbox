import pygame.mixer
from pygame.mixer import Sound
from gpiozero import Button, LED, RGBLED
from signal import pause
from functools import partial, update_wrapper
import time

def wrapped_partial(func, *args, **kwargs):
    partial_func = partial(func, *args, **kwargs)
    update_wrapper(partial_func, func)
    return partial_func

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.mixer.init()

sound_pins = {
    2: Sound("samples/drum_tom_mid_hard.wav"),
    3: Sound("samples/drum_cymbal_open.wav")
}
led_pins = {
    0: LED(8, initial_value=False),
    1: LED(7, initial_value=False)
}
rgb = RGBLED(5, 6, 13)
rgb.color = (0, 0, 0)
#rgb.blink(on_time=0.5, off_time=0.5, on_color=(1,1,1))

buttons = [Button(pin) for pin in sound_pins]

def do_stuff(sound, led):
    sound.play()
    led.on()

for i, button in enumerate(buttons):
    sound = sound_pins[button.pin.number]
    led = led_pins[i]
    button.when_pressed = wrapped_partial(do_stuff, sound=sound, led=led)
    button.when_released = led.off

while True:
    for i in range(0,3):
        rgb.color=(0,0,0)
        time.sleep(0.5)
        if i == 0:
            rgb.color=(1,0,0)
        elif i == 1:
            rgb.color=(0,1,0)
        else:
            rgb.color=(0,0,1)
        time.sleep(0.5)

pause()
