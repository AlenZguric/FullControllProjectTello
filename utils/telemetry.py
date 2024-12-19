def scale_wifi_signal(db_value):
    """
    Skalira snagu WiFi signala (u dB) na skalu od 0% do 100%.
    """
    min_db = -90  # Minimalna vrednost (loša konekcija)
    max_db = -30  # Maksimalna vrednost (odlična konekcija)
    scaled_value = max(0, min(100, int((db_value - min_db) / (max_db - min_db) * 100)))
    return f"{scaled_value}% ({db_value} dB)"

def get_telemetry_data(tello):
    current_height = tello.get_height()
    wifi_signal_db = tello.query_wifi_signal_noise_ratio()
    return {
        "Battery": f"{tello.get_battery()}%",
        "Height": f"{current_height} cm",
        "Speed X": f"{tello.get_speed_x()} cm/s",
        "Speed Y": f"{tello.get_speed_y()} cm/s",
        "Speed Z": f"{tello.get_speed_z()} cm/s",
        "WiFi Signal": scale_wifi_signal(wifi_signal_db)
    }
