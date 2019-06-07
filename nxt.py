# Adapted from Anton's Mindstorms Hacks:
# https://antonsmindstorms.com/2018/10/27/how-to-control-lego-nxt-from-your-laptop-with-a-gamepad/

#!python 
from jaraco.nxt import *
from jaraco.nxt.messages import *
import time
import sdl2
import math
 
# Connect to the controller (joystick) using SDL
sdl2.SDL_Init(sdl2.SDL_INIT_JOYSTICK)
joystick = sdl2.SDL_JoystickOpen(0)
 
# Open the NXT Bluetooth connection
conn = Connection('/dev/tty.NXT-DevB')

# Helper function to limit the range of a value 
def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)
 
# Main loop
while True:
    sdl2.SDL_PumpEvents()
 
    # Read controller stick Y-inputs and normalize the value
    # to a range of -100 to 100
    joy_1 = -sdl2.SDL_JoystickGetAxis(joystick, 1) / 327.67
    joy_3 = -sdl2.SDL_JoystickGetAxis(joystick, 3) / 327.67

    m1 = clamp(joy_1,-100,100)
    m2 = clamp(joy_3,-100,100)

    # Check left/right triggers (10,11) for 3rd motor control
    if sdl2.SDL_JoystickGetButton(joystick, 10): m0 = -30
    elif sdl2.SDL_JoystickGetButton(joystick, 11): m0 = 30
    else: m0 = 0
 
    # Print values to console (mostly for debugging)
    print('m0: %d' % m0)
    print('m1: %d' % m1)
    print('m2: %d' % m2)

    # Build the list of three motor commands to send to NXT
    cmds = []
    cmds.append(SetOutputState(
                0,
                motor_on=True,
                set_power=m0,
                run_state=RunState.running,
                use_regulation=True,                
                regulation_mode=RegulationMode.motor_speed))
 
    cmds.append(SetOutputState(
                1,
                motor_on=True,
                set_power=m1,
                run_state=RunState.running,
                use_regulation=True,
                regulation_mode=RegulationMode.motor_speed))

    cmds.append(SetOutputState(
                2,
                motor_on=True,
                set_power=m2,
                run_state=RunState.running,
                use_regulation=True,
                regulation_mode=RegulationMode.motor_speed))
 
    map(conn.send, cmds) 

    # Wait a bit before sending more commands.
    # If we don't, the Bluetooth buffer overflows.
    time.sleep(0.05)

    # End the program if Button 0 (select) is pressed.
    if sdl2.SDL_JoystickGetButton(joystick, 0) : break
 
# Clean up by closing the connection
conn.close()
