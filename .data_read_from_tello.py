import cv2
from djitellopy import tello
import math
import KeyPressFunc as kp
from time import sleep

# Inicijalizacija tipkovnice
kp.init()

def calculate_total_speed(speedX, speedY, speedZ):
    """
    Izračun ukupne brzine drona na temelju komponenti brzine u X, Y i Z osi.
    """
    return math.sqrt(speedX**2 + speedY**2 + speedZ**2)

def get_status_data(drone):
    """
    Dohvaćanje trenutnih statusnih podataka drona i njihovo vraćanje kao varijable.
    """
    activeMotorTime = drone.get_flight_time()
    battery = drone.get_battery()
    height = drone.get_height()
    tof = drone.get_distance_tof()
    speedX = 0.1 * drone.get_speed_x()
    speedY = 0.1 * drone.get_speed_y()
    speedZ = 0.1 * drone.get_speed_z()
    totalSpeed = calculate_total_speed(speedX, speedY, speedZ)
    return activeMotorTime, battery, height, tof, speedX, speedY, speedZ, totalSpeed

def get_keyboard_input(drone):
    """
    Dohvaćanje unosa s tipkovnice za kontrolu drona.
    """
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 50

    if kp.getKey('LEFT'): lr = -speed
    elif kp.getKey('RIGHT'): lr = speed

    if kp.getKey('UP'): fb = speed
    elif kp.getKey('DOWN'): fb = -speed

    if kp.getKey('w'): ud = speed
    elif kp.getKey('s'): ud = -speed

    if kp.getKey('a'): yv = -speed
    elif kp.getKey('d'): yv = speed

    if kp.getKey('q'): 
        drone.land()
        print("Dron je sletio.")
    if kp.getKey('e'): 
        drone.takeoff()
        print("Dron je poletio.")

    return [lr, fb, ud, yv]

def process_tello_video(drone):
    """
    Prikaz videa s glavne kamere u jednom prozoru, a donje kamere u drugom.
    """
    while True:
        # Unos s tipkovnice
        inputs = get_keyboard_input(drone)
        drone.send_rc_control(inputs[0], inputs[1], inputs[2], inputs[3])
        sleep(0.05)

        # Dohvati frame iz glavne kamere
        forward_frame = drone.get_frame_read().frame
        if forward_frame is not None:
            forward_frame = cv2.cvtColor(forward_frame, cv2.COLOR_RGB2BGR)
            forward_frame = cv2.resize(forward_frame, (500, 500))

            # Dohvati statusne podatke
            activeMotorTime, battery, height, tof, speedX, speedY, speedZ, totalSpeed = get_status_data(drone)
            cv2.putText(forward_frame, f'Battery: {battery}%', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(forward_frame, f'Height: {height} cm', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(forward_frame, f'TOF: {tof} cm', (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(forward_frame, f'Speed X: {speedX:.2f} m/s', (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(forward_frame, f'Speed Y: {speedY:.2f} m/s', (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(forward_frame, f'Speed Z: {speedZ:.2f} m/s', (10, 180), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(forward_frame, f'Total Speed: {totalSpeed:.2f} m/s', (10, 210), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Prikaz glavne kamere
            cv2.imshow("Glavna Kamera", forward_frame)

        # Promijeni na downward kameru i dohvati frame
        drone.set_video_direction(drone.CAMERA_DOWNWARD)
        downward_frame = drone.get_frame_read().frame
        if downward_frame is not None:
            downward_frame = cv2.cvtColor(downward_frame, cv2.COLOR_RGB2BGR)
            downward_frame = cv2.resize(downward_frame, (320, 240))

            # Prikaz downward kamere
            cv2.imshow("Donja Kamera", downward_frame)

        # Pritisni 'z' za prekid programa
        if kp.getKey('z') or cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Očisti prozore
    cv2.destroyAllWindows()

def main():
    """
    Glavna metoda za spajanje na dron i prikaz videa s obje kamere.
    """
    drone = tello.Tello()
    drone.connect()
    drone.streamon()
    process_tello_video(drone)

if __name__ == "__main__":
    main()
