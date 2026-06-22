import os
import time
import pyautogui as pag
import keyboard as key
from datetime import date, datetime
import pydirectinput

SAVE_FOLDER = "save_data"

os.makedirs(SAVE_FOLDER, exist_ok=True)

LAST_DONE_FILE = os.path.join(SAVE_FOLDER, "last_done.txt")
AIZEN_STATE_FILE = os.path.join(SAVE_FOLDER, "aizen_state.txt")
SHENRON_STATE_FILE = os.path.join(SAVE_FOLDER, "shenron_state.txt")
GRIFFITH_STATE_FILE = os.path.join(SAVE_FOLDER, "griffith_state.txt")


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


def check_for_pixels(pixel1=(0, 0, 255, 255, 255), timeout=5):
    x, y, r, g, b = pixel1
    end_time = time.time() + timeout

    while time.time() < end_time:
        check_stop()

        if pag.pixelMatchesColor(x, y, (r, g, b)):
            return True

        time.sleep(0.2)

    return False


def check_for_any_pixels(pixels, timeout=5):
    end_time = time.time() + timeout

    while time.time() < end_time:
        check_stop()

        for pixel in pixels:
            x, y, r, g, b = pixel

            if pag.pixelMatchesColor(
                x,
                y,
                (r, g, b),
                tolerance=20
            ):
                return True

        time.sleep(0.2)

    return False


def get_today_text():
    return date.today().isoformat()


def read_last_done_day():
    if not os.path.exists(LAST_DONE_FILE):
        return ""

    with open(LAST_DONE_FILE, "r") as file:
        return file.read().strip()


def write_last_done_day(day_text):
    with open(LAST_DONE_FILE, "w") as file:
        file.write(day_text)


def load_count_state(state_file):
    current_day = get_today_text()

    if not os.path.exists(state_file):
        return current_day, 0

    with open(state_file, "r") as file:
        lines = file.readlines()

    stored_day = lines[0].split("=")[1].strip()
    stored_count = int(lines[1].split("=")[1].strip())

    if stored_day != current_day:
        return current_day, 0

    return stored_day, stored_count


def save_count_state(state_file, day_text, count_number):
    with open(state_file, "w") as file:
        file.write(f"date={day_text}\n")
        file.write(f"count={count_number}")


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

    # Put home screen -> start Aizen game code here.
    # This only runs once before the Aizen loop starts.

    safe_sleep(1)
    open_type_selection()  # room type selection
    safe_sleep(0.3)

    open_challenge() # open challenge
    safe_sleep(0.3)

    direct_click(1264, 325, clicks=1)  # move to aizen challenge
    direct_click(1262, 325, clicks=1)

    safe_sleep(0.2)
    create_room()  # move to create room
    safe_sleep(0.2)

    start_room()  # move to start

    print("Aizen setup done")


def aizen_one_round():
    print("Aizen round starting")

    safe_sleep(10)

    wait_for_pixels(pixel1=(1351, 450, 132, 134, 0))  # wait for victory screen

    safe_sleep(0.3)

    found = check_for_pixels(
        pixel1=(1334, 415, 252, 163, 0),
        timeout=5
    )  # check if Aizen trait shard appeared

    return found


def aizen_100_macro():
    state_day, detect_count = load_count_state(AIZEN_STATE_FILE)

    aizen_setup()

    while detect_count < 100:
        check_stop()

        found = aizen_one_round()

        if found:
            detect_count += 1
            save_count_state(AIZEN_STATE_FILE, state_day, detect_count)
            print(f"Aizen trait shard detected {detect_count}/100")
        else:
            print("Aizen trait shard not found, restarting round")

        direct_click(1351, 450, clicks=1)  # move to replay
        direct_click(1350, 450, clicks=1)

        safe_sleep(0.1)

    print("Aizen trait shard reached 100 today")


def shenron_setup():
    print("Shenron setup starting")

    # Put home screen -> start Shenron game code here.
    # This only runs once before the Shenron loop starts.

    safe_sleep(1)
    open_type_selection()  # room type selection
    safe_sleep(0.3)

    open_raid() # open raid
    safe_sleep(0.3)

    direct_click(1267, 218, clicks=1)  # move to gt city
    direct_click(1265, 218, clicks=1)

    safe_sleep(0.2)

    direct_click(1447, 294, clicks=1)  # move to select act 4
    direct_click(1445, 294, clicks=1)

    safe_sleep(0.3)

    direct_click(1644, 334, clicks=1)  # move to select hard
    direct_click(1643, 334, clicks=1)

    safe_sleep(0.2)
    create_room()  # move to create room
    safe_sleep(0.2)

    start_room()  # move to start

    print("Shenron setup done")


def shenron_one_round():
    print("Shenron round starting")

    # Put only the repeating Shenron round code here.
    # This is the part that loops after the game is already running.

    safe_sleep(10)

    wait_for_pixels(pixel1=(1351, 450, 132, 134, 0))  # wait for victory screen

    safe_sleep(0.3)

    found = check_for_pixels(
        pixel1=(1260, 415, 255, 172, 0),
        timeout=5
    ) # check if shenron trait shard appeared

    return found


def shenron_100_macro():
    state_day, detect_count = load_count_state(SHENRON_STATE_FILE)

    shenron_setup()

    while detect_count < 100:
        check_stop()

        found = shenron_one_round()

        if found:
            detect_count += 0.5
            save_count_state(SHENRON_STATE_FILE, state_day, detect_count)
            print(f"Shenron trait shard detected {detect_count}/100")
        else:
            print("Shenron trait shard not found, restarting round")

        direct_click(1351, 450, clicks=1)  # move to replay
        direct_click(1350, 450, clicks=1)
        safe_sleep(0.1)

    print("Shenron trait shard reached 100 today")


def griffith_setup():
    print("Griffith setup starting")

    safe_sleep(1)
    open_type_selection()  # room type selection
    safe_sleep(0.3)

    open_raid()  # open raid
    safe_sleep(0.3)

    direct_click(1267, 277, clicks=1) # move to Eclipse
    direct_click(1265, 277, clicks=1)

    safe_sleep(0.2)

    direct_click(1447, 294, clicks=1)  # move to select act 4
    direct_click(1445, 294, clicks=1)

    safe_sleep(0.2)
    create_room()  # move to create room
    safe_sleep(0.2)

    start_room()  # move to start

    print("Griffith setup done")


def griffith_one_round():
    print("Griffith round starting")

    safe_sleep(10)

    wait_for_pixels(pixel1=(1639, 197, 248, 70, 71)) # pop up

    direct_click(1639, 197, clicks=1)  # close pop up
    direct_click(1638, 197, clicks=1)

    wait_for_pixels(pixel1=(1298, 451, 132, 134, 0))  # wait for victory screen

    safe_sleep(0.3)

    found = check_for_pixels(
        pixel1=(1334, 415, 252, 163, 0),
        timeout=5
    )  # check if griffith trait shard appeared

    return found


def griffith_100_macro():
    state_day, detect_count = load_count_state(GRIFFITH_STATE_FILE)

    griffith_setup()

    while detect_count < 100:
        check_stop()

        found = griffith_one_round()

        if found:
            detect_count += 1
            save_count_state(GRIFFITH_STATE_FILE, state_day, detect_count)
            print(f"Griffith trait shard detected {detect_count}/100")
        else:
            print("Griffith trait shard not found, restarting round")

        direct_click(1298, 450, clicks=1)  # move to replay
        direct_click(1230, 450, clicks=1)
        safe_sleep(0.1)

    print("Griffith trait shard reached 100 today")


def regular_challenge_setup():
    print("Regular challenge setup")

    safe_sleep(1)
    open_type_selection()
    safe_sleep(0.3)

    open_challenge()
    safe_sleep(0.3)

    direct_click(1270, 279, clicks=1)
    direct_click(1269, 279, clicks=1)

    safe_sleep(0.2)
    create_room()
    safe_sleep(0.2)

    start_room()


def regular_challenge_one_round():
    print("Regular challenge round")

    safe_sleep(10)

    wait_for_pixels(pixel1=(1351, 450, 132, 134, 0))

    safe_sleep(0.3)

    direct_click(1351, 450, clicks=1)  # replay
    direct_click(1350, 450, clicks=1)

    safe_sleep(0.1)


def thirty_min_macro():
    print("30 minute macro")
    # your 30-minute code here

    safe_sleep(5)

    wait_for_pixels(pixel1=(1351, 450, 132, 134, 0))

    safe_sleep(0.3)

    direct_click(1485, 450, clicks=1)  # leave
    direct_click(1483, 450, clicks=1)

    safe_sleep(0.1)


while True:
    check_stop()

    today_text = get_today_text()
    saved_daily_day = read_last_done_day()

    if saved_daily_day != today_text:
        daily_macro()

        write_last_done_day(today_text)

        save_count_state(AIZEN_STATE_FILE, today_text, 0)
        save_count_state(SHENRON_STATE_FILE, today_text, 0)
        save_count_state(GRIFFITH_STATE_FILE, today_text, 0)

        aizen_100_macro()
        shenron_100_macro()
        griffith_100_macro()

    else:
        _, aizen_count = load_count_state(AIZEN_STATE_FILE)
        _, shenron_count = load_count_state(SHENRON_STATE_FILE)
        _, griffith_count = load_count_state(GRIFFITH_STATE_FILE)

        if aizen_count < 100:
            aizen_100_macro()

        if shenron_count < 100:
            shenron_100_macro()

        if griffith_count < 100:
            griffith_100_macro()

    last_30_min_run = None

    regular_challenge_setup()

    while get_today_text() == today_text:
        check_stop()

        regular_challenge_one_round()

        now = datetime.now()

        current_slot = now.strftime("%Y-%m-%d %H:%M")

        if now.minute in (0, 30):

            if last_30_min_run != current_slot:
                thirty_min_macro()

                regular_challenge_setup()

                last_30_min_run = current_slot