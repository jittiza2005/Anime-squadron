import os
import time
import pyautogui as pag
import keyboard as key
from datetime import date, datetime

LAST_DONE_FILE = "last_done.txt"
AIZEN_STATE_FILE = "aizen_state.txt"
SHENRON_STATE_FILE = "shenron_state.txt"


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


def wait_for_pixels(pixel1=(0, 0, 255, 255, 255)):
    x, y, r, g, b = pixel1

    while True:
        check_stop()

        if pag.pixelMatchesColor(x, y, (r, g, b)):
            return True

        time.sleep(0.2)


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


def daily_macro():
    safe_sleep(1)
    wait_for_pixels(pixel1=(1024, 462, 0, 51, 20))  # check for home screen
    safe_sleep(0.3)
    pag.moveTo(1001, 291, duration=0.2)  # click play
    safe_sleep(0.1)
    pag.click()
    wait_for_pixels(pixel1=(1419, 493, 34, 157, 0))  # wait for create room
    safe_sleep(0.3)
    pag.moveTo(1443, 501, duration=0.2)  # move to create room
    safe_sleep(0.1)
    pag.click()
    wait_for_pixels(pixel1=(1576, 432, 40, 188, 0))  # wait for type selection
    safe_sleep(0.3)
    pag.moveTo(1525, 500, duration=0.2)  # move to challenge
    safe_sleep(0.1)
    pag.click()
    wait_for_pixels(pixel1=(1186, 406, 25, 97, 21))  # wait for challenge selection
    safe_sleep(0.3)
    pag.moveTo(1313, 218, duration=0.2)  # move to daily challenge
    safe_sleep(0.1)
    pag.click()
    pag.moveTo(1579, 437, duration=0.2)  # move to create room
    safe_sleep(0.1)
    pag.click()
    pag.moveTo(1707, 447, duration=0.2)  # move to start
    safe_sleep(0.1)
    pag.click()
    safe_sleep(10)
    wait_for_pixels(pixel1=(1350, 450, 136, 138, 0))  # wait for victory screen
    safe_sleep(0.5)
    pag.moveTo(1483, 445, duration=0.2)  # move to leave
    safe_sleep(0.1)
    pag.click()
    print("daily macro done")


def aizen_100_macro():
    state_day, detect_count = load_count_state(AIZEN_STATE_FILE)

    while detect_count < 100:
        check_stop()

        wait_for_pixels(pixel1=(0, 0, 255, 255, 255))  #start code on this line

        detect_count += 1
        save_count_state(AIZEN_STATE_FILE, state_day, detect_count)

        print(f"Aizen trait shard detected {detect_count}/100")

    print("Aizen trait shard reached 100 today")


def shenron_100_macro():
    state_day, detect_count = load_count_state(SHENRON_STATE_FILE)

    while detect_count < 100:
        check_stop()

        wait_for_pixels(pixel1=(0, 0, 255, 255, 255))  # start code on this line

        detect_count += 1
        save_count_state(SHENRON_STATE_FILE, state_day, detect_count)

        print(f"Shenron trait shard detected {detect_count}/100")

    print("Shenron trait shard reached 100 today")


def thirty_min_macro():
    print("30 minute macro")
    # your 30-minute code here


while True:
    check_stop()

    today_text = get_today_text()
    saved_daily_day = read_last_done_day()

    if saved_daily_day != today_text:
        daily_macro()

        write_last_done_day(today_text)

        save_count_state(AIZEN_STATE_FILE, today_text, 0)
        save_count_state(SHENRON_STATE_FILE, today_text, 0)

        aizen_100_macro()
        shenron_100_macro()

    else:
        _, aizen_count = load_count_state(AIZEN_STATE_FILE)
        _, shenron_count = load_count_state(SHENRON_STATE_FILE)

        if aizen_count < 100:
            aizen_100_macro()

        if shenron_count < 100:
            shenron_100_macro()

    last_30_min_run = None

    while get_today_text() == today_text:
        check_stop()

        now = datetime.now()
        current_slot = now.strftime("%Y-%m-%d %H:%M")

        if now.minute in (0, 30):
            if last_30_min_run != current_slot:
                thirty_min_macro()
                last_30_min_run = current_slot

        safe_sleep(1)