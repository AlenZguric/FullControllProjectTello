from djitellopy import Tello
import time

tello = Tello()
tello.connect()
baterija = tello.get_battery()
start_height = tello.get_height()
print(f"baterija je na {baterija}")

print(f"početna visina {start_height}")
print(tello.get_barometer)

time.sleep(2)

tello.takeoff()
time.sleep(2)
get_height = tello.get_height()
current_height = start_height + get_height
print(f"trenutna visina {current_height}")

tello.move_up(113)
tello.move_down(140)
time.sleep(2)
tello.rotate_clockwise(180)
time.sleep(2)

get_height = tello.get_height()

current_height = start_height + get_height

print(f"trenutna visina {current_height}")

time.sleep(2)
tello.land()
