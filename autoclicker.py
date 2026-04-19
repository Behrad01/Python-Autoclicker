import time
import pynput
import threading

ms = pynput.mouse.Controller()   # variable for mouse controller

start_stop_event = threading.Event()   # key event for starting and stopping autoclicker
quit_program_event = threading.Event()   # key event to exit the program

print(('-' * 10) + ' Autoclicker ' + ('-' * 10) + '\n')

key_to_start = input('> Key to start: ').lower()   # catching user input for key to start
key_to_stop =  input('> Key to stop: ').lower()    # catching user input for key to stop

# validating user input
if key_to_start == key_to_stop:
    raise ValueError("'Key to start' and 'Key to stop' can't share the same hotkey.")
elif key_to_start == 'q' or key_to_stop == 'q':
    raise ValueError("'Key to start' or 'Key to stop' can't be assigned to 'q'.")

# catching user input for clicking delay
try:
    clicking_delay = float(input('> Clicking delay: '))
except ValueError:
    raise ValueError('Please enter a valid clicking delay.')   # raising error if clicking delay input isn't valid

print('\n' + ('-' * 33) + '\n')

# defining keyboard listener function
def keyboard_listener():
    # defining on_press function
    def on_press(k):
        # catching keylogs
        try:
            key = k.char
        except AttributeError:   
            return   # ignoring special keys for hotkeys
        
        # declaring actions for event keys
        if key == key_to_start:
            start_stop_event.set()
            print('> Autoclicker started!')
        elif key == key_to_stop:
            start_stop_event.clear()
            print('> Autoclicker stopped!')
        elif key == 'q':
            start_stop_event.clear()
            quit_program_event.set()
            print('> Successfully exited program!')
            return False
        
    with pynput.keyboard.Listener(on_press=on_press) as listener:
        listener.join()   # starting keyboard listener

# setting up keyboard_listener thread
keyboard_listener_thread = threading.Thread(target=keyboard_listener)
keyboard_listener_thread.start()

# showing saved data
print(f"> Data saved! press '{key_to_start}' to start, '{key_to_stop}' to stop and 'q' to quit.\n\n" + '-' * 33 + '\n')

# defining autoclicker function
def autoclicker(delay):
    ms.click(pynput.mouse.Button.left, 1)   # left clicking once
    time.sleep(delay)   # setting up delay for each click

# starting program
while True:
    if start_stop_event.is_set():
        autoclicker(clicking_delay)   # starting autoclicker with clicking delay
    elif quit_program_event.is_set():
        break   # exiting program if 'q' is pressed
    else:
        time.sleep(0.01)   # short delay to avoid high cpu usage in idle
