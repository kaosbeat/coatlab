import board, time, random
import synthio
import ulab.numpy as np
import analogio
import audiobusio
import digitalio
from digitalio import DigitalInOut, Direction, Pull
import audiomixer
import audiocore
import random
import keypad

notes = (33, 34, 31) # possible notes to play MIDI A1, A1#, G1
note_duration = 5   # how long each note plays for
num_voices = 5       # how many voices for each note
lpf_basef = 1030      # filter lowest frequency
lpf_resonance = 1.2  # filter q

# for PWM audio with an RC fil
# for I2S audio with external I2S DAC board
#ESP32 WROOM DA
# MOSI = IO13  >>> PCM5102 BCK
# MISO = IO12  >>> PCM5102 LCK
# SCK = IO14   >>> PCM5102 DIN
i2s_bck = board.IO13
i2s_lck = board.IO12
i2s_din = board.IO14
audio = audiobusio.I2SOut(bit_clock=i2s_bck, word_select=i2s_lck, data=i2s_din)

mixer = audiomixer.Mixer(voice_count=4, channel_count=1, sample_rate=44100, buffer_size=128, bits_per_sample=16, samples_signed=True)
synth = synthio.Synthesizer(channel_count=2, sample_rate=44100)
audio.play(mixer)
# mixer.voice[0].play(synth)
# mixer.voice[0].level = 0.4

# 15
# 2
# 4
# 16
# 17
# 5
# 18

switch = DigitalInOut(board.IO19)
switch.direction = Direction.INPUT
switch.pull = Pull.DOWN

# print("sampletest")

kicktrigger = digitalio.DigitalInOut(board.IO15)
kicktrigger.switch_to_input(pull=digitalio.Pull.DOWN)
kicktriggerready = True
snaretrigger = digitalio.DigitalInOut(board.IO16)
snaretrigger.switch_to_input(pull=digitalio.Pull.DOWN)
snaretriggerready = True
hhtrigger = digitalio.DigitalInOut(board.IO17)
hhtrigger.switch_to_input(pull=digitalio.Pull.DOWN)
hhtriggerready = True
# # Or, after switch_to_input
# switch.pull = digitalio.Pull.UP


kick_pin = board.IO15
snare_pin = board.IO16
hh_pin = board.IO17

# keys = keypad.Keys( (kick_pin, snare_pin, hh_pin), value_when_pressed=False, pull=True)

# mixer.voice[0].play(k)

            
led = digitalio.DigitalInOut(board.IO2)
led.direction = digitalio.Direction.OUTPUT


s = audiocore.WaveFile("snare.wav")
k = audiocore.WaveFile("kick.wav")
h = audiocore.WaveFile("hh1.wav")

print("playing")
# audio.play(k)
mixer.voice[0].play(k)

while True:
    # event = keys.events.get()
    # if (event!=None and event.pressed):
    #     if event.key_number == 0:
    #         mixer.voice[0].play(k)
    #     if event.key_number == 1:
    #         mixer.voice[1].play(s)
    #     if event.key_number == 2:
    #         mixer.voice[2].play(h)

####################

# stop = "here"
# if (stop):
    if kicktriggerready:
        if kicktrigger.value == True :
            # mixer.voice[0].stop()
            mixer.voice[0].play(k)
            kicktriggerready = False
            if switch.value:
                led.value = False
                print("OIN")
            else:
                led.value = True
                print("OFF")
    else:
        if kicktrigger.value == False:
            kicktriggerready = True
        
    # print(  kicktrigger.value)
    # if not mixer.voice[0].playing:

    # if not mixer.voice[1].playing:
    if snaretriggerready:
        if snaretrigger.value == True :
            mixer.voice[1].stop()
            mixer.voice[1].play(s)
            snaretriggerready = False
    else:
        if snaretrigger.value == False:
            snaretriggerready = True
            
    if hhtriggerready:

        # if not mixer.voice[2].playing:
        if hhtrigger.value == True :
            mixer.voice[2].play(h)       

##############################
        # pass
    # else:
    #     if random.random() > 0.4:
    #         # mixer.voice[1].play(s)
    #         mixer.voice[0].play(k)

    #         # audio.play(s)
    #         # audio.play(k)
            
    #         led.value = True 
    #     else:
    #         # audio.play(s)
    #         mixer.voice[0].play(s)
            
    #         # time.sleep(0.4)
    #         led.value = False 
print("stopped")