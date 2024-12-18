def get_telemetry_data(tello):
    return {
        "Battery": f"{tello.get_battery()}%",
        "Height": f"{tello.get_height()} cm",
        "Speed": f"{tello.get_speed_x()} cm/s",
        "WiFi": f"{tello.query_wifi_signal_noise_ratio()}%"
    }
