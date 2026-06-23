import os
import time
import pyautogui as pag
import keyboard as key
from datetime import date, datetime
import pydirectinput

SAVE_FOLDER = "save_data"

os.makedirs(SAVE_FOLDER, exist_ok=True)

LAST_DONE_FILE = os.path.join(SAVE_FOLDER, "last_done.txt")


def check_stop():
    if key.is_pressed('f4'):
        print("Stopped")
        raise SystemExit


def safe_sleep(seconds):
    end_time = time.time() + seconds

    while time.time() < end_time:
        check_stop()
        remaining = end_time - time.time()
        time.sleep(min(0.05, remaining))

pydirectinput.PAUSE = 0.05


def direct_click(x, y, clicks=1):
    pydirectinput.moveTo(x, y, duration=0.2)
    safe_sleep(0.15)

    for _ in range(clicks):
        pydirectinput.mouseDown()
        safe_sleep(0.12)
        pydirectinput.mouseUp()
        safe_sleep(0.15)


def wait_for_pixels(pixel1=(0, 0, 255, 255, 255), tolerance=20):
    x, y, r, g, b = pixel1

    while True:
        check_stop()

        if pag.pixelMatchesColor(x, y, (r, g, b), tolerance=tolerance):
            return True

        time.sleep(0.2)


def get_today_text():
    current_time = datetime.now()

    if current_time.hour >= 17:
        return current_time.date().isoformat()

    yesterday = date.fromordinal(current_time.date().toordinal() - 1)

    return yesterday.isoformat()


def read_last_done_day():
    if not os.path.exists(LAST_DONE_FILE):
        return ""

    with open(LAST_DONE_FILE, "r") as file:
        return file.read().strip()


def write_last_done_day(day_text):
    with open(LAST_DONE_FILE, "w") as file:
        file.write(day_text)


def open_type_selection():
    wait_for_pixels(pixel1=(1024, 462, 0, 46, 18))  # home screen
    safe_sleep(0.3)

    direct_click(1001, 291, clicks=1)  # play
    direct_click(1001, 293, clicks=1)

    wait_for_pixels(pixel1=(1419, 493, 34, 157, 0))  # create room
    safe_sleep(0.3)

    direct_click(1443, 502, clicks=1)
    direct_click(1442, 501, clicks=1)

    wait_for_pixels(pixel1=(1590, 155, 255, 255, 255))  # type selection


def open_challenge():
    direct_click(1525, 508, clicks=1) # move to challenge
    direct_click(1524, 506, clicks=1)

    wait_for_pixels(pixel1=(1589, 151, 255, 255, 255)) # wait for challenge selection


def open_raid():
    direct_click(1664, 500, clicks=1) # move to raid
    direct_click(1662, 500, clicks=1)

    wait_for_pixels(pixel1=(1589, 151, 255, 255, 255)) # wait for raid selection


def create_room():
    direct_click(1584, 438, clicks=1)  # move to create room
    direct_click(1582, 438, clicks=1)


def start_room():
    direct_click(1706, 452, clicks=1)  # move to start
    direct_click(1704, 452, clicks=1)

def leave_setup_to_home():
    print("Leaving setup to home")

    # replace these with your actual buttons
    wait_for_pixels(pixel1=(1506, 512, 0, 134, 0)) # wait for game to load

    safe_sleep(0.2)
    direct_click(1883, 589, clicks=1) # move to setting
    direct_click(1882, 589, clicks=1)

    wait_for_pixels(pixel1=(1205, 171, 255, 255, 255))  # wait for setting menu

    direct_click(1595, 268, clicks=1)  # move to teleport
    direct_click(1594, 268, clicks=1)

    safe_sleep(1)

def daily_macro():
    safe_sleep(1)
    open_type_selection() # room type selection
    safe_sleep(0.3)

    open_challenge() # open challenge
    safe_sleep(0.3)

    direct_click(1267, 218, clicks=1)  # move to daily challenge
    direct_click(1265, 218, clicks=1)

    safe_sleep(0.2)
    create_room() # move to create room
    wait_for_pixels(pixel1=(1687, 453, 33, 152, 0))  # wait for start screen
    safe_sleep(0.2)

    start_room() # move to start

    safe_sleep(10)
    wait_for_pixels(pixel1=(1350, 450, 132, 134, 0))  # wait for victory screen
    safe_sleep(0.3)

    direct_click(1483, 445, clicks=1)  # move to leave
    direct_click(1482, 445, clicks=1)

    safe_sleep(0.1)
    print("daily macro done")

def aizen_setup():
    print("Aizen setup starting")

    # Home -> Play -> Challenge -> Aizen -> Create Room -> Start

    safe_sleep(1)

    open_type_selection() # open room type selection
    safe_sleep(0.5)

    open_challenge() # open challenge menu
    safe_sleep(0.5)

    direct_click(985, 322, clicks=1)  # select Aizen
    direct_click(984, 322, clicks=1)

    safe_sleep(0.5)

    create_room() # create room

    wait_for_pixels(pixel1=(1341, 437, 32, 149, 0)) # wait for Start button

    safe_sleep(0.5)

    start_room() # start game

    print("Aizen setup done")


def aizen_macro(rounds=100):

    # Run setup once
    aizen_setup()

    # Loop a fixed number of rounds
    for count in range(rounds):

        check_stop()  # F4 emergency stop

        # Display progress
        print(f"Aizen {count + 1}/{rounds}")

        # Give game time to load
        safe_sleep(10)

        # Wait until victory screen appears
        wait_for_pixels(pixel1=(1060, 428, 127, 129, 0))

        safe_sleep(0.3)

        # Replay unless this is the final round
        if count < rounds - 1:

            direct_click(1084, 426, clicks=1)
            direct_click(1083, 426, clicks=1)

            safe_sleep(0.1)

    # After final round, leave back to home
    direct_click(1174, 429, clicks=1)
    direct_click(1173, 429, clicks=1)

    safe_sleep(0.2)

    print("Aizen done")


def shenron_setup():
    print("Shenron setup starting")

    # Put home screen -> start Shenron game code here.
    # This only runs once before the Shenron loop starts.

    safe_sleep(1)
    open_type_selection()  # room type selection
    safe_sleep(0.3)

    open_raid() # open raid
    safe_sleep(0.3)

    direct_click(985, 237, clicks=1)  # move to gt city
    direct_click(984, 237, clicks=1)

    safe_sleep(0.2)

    direct_click(1141, 298, clicks=1)  # move to select act 4
    direct_click(1140, 298, clicks=1)

    safe_sleep(0.3)

    direct_click(1305, 338, clicks=1)  # move to select hard
    direct_click(1304, 338, clicks=1)

    safe_sleep(0.2)

    create_room()  # move to create room

    wait_for_pixels(pixel1=(1341, 437, 32, 149, 0)) # wait for Start button

    safe_sleep(0.2)

    start_room()  # move to start

    print("Shenron setup done")

def shenron_macro(rounds=100):
    shenron_setup()  # setup only once

    for count in range(rounds):

        check_stop()  # F4 emergency stop

        print(f"Shenron {count + 1}/{rounds}")

        safe_sleep(10)

        wait_for_pixels(
            pixel1=(1016, 427, 133, 135, 0)) # wait for victory screen

        safe_sleep(0.3)

        # Replay unless this is the final round
        if count < rounds - 1:

            direct_click(1084, 426, clicks=1)
            direct_click(1083, 426, clicks=1)

            safe_sleep(0.1)

    # After the final round, leave back home
    direct_click(1190, 427, clicks=1)
    direct_click(1189, 427, clicks=1)

    safe_sleep(0.2)

    print("Shenron done")

def griffith_setup():
    print("Griffith setup starting")

    safe_sleep(1)
    open_type_selection()  # room type selection
    safe_sleep(0.3)

    open_raid()  # open raid
    safe_sleep(0.3)

    direct_click(991, 281, clicks=1) # move to Eclipse
    direct_click(990, 281, clicks=1)

    safe_sleep(0.2)

    direct_click(1141, 298, clicks=1)  # move to select act 4
    direct_click(1140, 298, clicks=1)

    safe_sleep(0.2)

    create_room()  # move to create room

    wait_for_pixels(pixel1=(1341, 437, 32, 149, 0)) # wait for Start button

    safe_sleep(0.2)

    start_room()  # move to start

    print("Griffith setup done")

def griffith_macro(rounds=100):
    griffith_setup()  # setup only once

    for count in range(rounds):

        check_stop()  # F4 emergency stop

        print(f"Griffith {count + 1}/{rounds}")

        safe_sleep(10)

        wait_for_pixels(
            pixel1=(1018, 427, 133, 135, 0)) # wait for victory screen

        safe_sleep(0.3)

        # Replay unless this is the final round
        if count < rounds - 1:

            direct_click(1017, 430, clicks=1)
            direct_click(1016, 430, clicks=1)

            safe_sleep(0.1)

    # After the final round, leave back home
    direct_click(1210, 427, clicks=1)
    direct_click(1209, 427, clicks=1)

    safe_sleep(0.2)

    print("Griffith done")

def regular_challenge_setup():
    print("Regular challenge setup")

    safe_sleep(1)
    open_type_selection() # room type selection
    safe_sleep(0.3)

    open_challenge() # open challenge
    safe_sleep(0.3)

    direct_click(1270, 279, clicks=1) # move to regular challenge
    direct_click(1269, 279, clicks=1)

    safe_sleep(0.2)

    create_room()

    wait_for_pixels(pixel1=(1341, 437, 32, 149, 0))  # wait for Start button

    safe_sleep(0.2)

    start_room()


def regular_challenge_one_round():
    print("Regular challenge round")

    safe_sleep(10)

    wait_for_pixels(pixel1=(1351, 450, 132, 134, 0)) # wait for victory screen

    safe_sleep(0.3)

def thirty_min_macro():
    print("30 minute macro")
    # your 30-minute code here

    safe_sleep(5)

    wait_for_pixels(pixel1=(1351, 450, 132, 134, 0)) # wait for victory screen

    safe_sleep(0.3)

    direct_click(1485, 450, clicks=1)  # leave
    direct_click(1483, 450, clicks=1)

    safe_sleep(0.1)


while True:
    check_stop()

    # Determine the current reset day (5 PM reset)
    today_text = get_today_text()

    # Read the last completed reset day
    saved_daily_day = read_last_done_day()

    # If today's daily tasks have not been completed
    if saved_daily_day != today_text:

        # Complete Daily Challenge once
        daily_macro()

        wait_for_pixels(pixel1=(1024, 462, 0, 46, 18))  # home screen

        # Run Aizen fixed number of rounds
        aizen_macro(100)

        # Run Shenron fixed number of rounds
        shenron_macro(100)

        # Run Griffith fixed number of rounds
        griffith_macro(100)

        # Save today's reset day
        write_last_done_day(today_text)

    # Stores the last xx:00 or xx:30 that was executed
    last_30_min_run = None

    # Start the first Regular Challenge
    regular_challenge_setup()

    while True:
        check_stop()

        # If 5 PM reset happened before entering a round
        if get_today_text() != today_text:
            leave_setup_to_home()
            break

        # Play one Regular Challenge round
        regular_challenge_one_round()

        # If 5 PM reset happened after finishing a round
        if get_today_text() != today_text:
            thirty_min_macro()
            break

        # Get current real-world time
        now = datetime.now()

        current_slot = now.strftime("%Y-%m-%d %H:%M")

        # Every xx:00 or xx:30
        if now.minute in (0, 30):

            # Only execute once for that time slot
            if last_30_min_run != current_slot:

                # Leave current game and return home
                thirty_min_macro()

                # Check if 5 PM reset happened while leaving
                if get_today_text() != today_text:
                    break

                # Start a fresh Regular Challenge room
                regular_challenge_setup()

                # Record that this slot has already run
                last_30_min_run = current_slot

            else:
                # Continue replaying current challenge
                direct_click(1351, 450, clicks=1)
                direct_click(1350, 450, clicks=1)

        else:
            # Continue replaying current challenge
            direct_click(1351, 450, clicks=1)
            direct_click(1350, 450, clicks=1)

        safe_sleep(0.1)