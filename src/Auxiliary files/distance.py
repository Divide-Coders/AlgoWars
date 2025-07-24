import math

city_coordinates = {
    # Iran cities
    "Tehran": (51.4215, 35.6944),
    "Mashhad": (59.5439, 36.2970),
    "Isfahan": (51.6746, 32.6525),
    "Shiraz": (52.5311, 29.6100),
    "Tabriz": (46.2919, 38.0800),
    "Karaj": (50.9915, 35.8400),
    "Qom": (50.8800, 34.6400),
    "Ahvaz": (48.6706, 31.3290),
    "Kermanshah": (47.0650, 34.3142),
    "Urmia": (45.0760, 37.5527),
    "Rasht": (49.5890, 37.2809),
    "Zahedan": (60.8629, 29.4963),
    "Kerman": (57.0788, 30.2832),
    "Yazd": (54.3676, 31.8974),
    "Ardabil": (48.2934, 38.2498),
    "Bandar_Abbas": (56.2666, 27.1865),
    "Arak": (49.6892, 34.0917),
    "Zanjan": (48.4963, 36.6764),
    "Sanandaj": (46.9862, 35.3219),
    "Qazvin": (50.0041, 36.2797),
    # Israel cities
    "Tel_Aviv": (34.7806, 32.0809),
    "Jerusalem": (35.2137, 31.7683),
    "Haifa": (34.9896, 32.7940),
    "Beersheba": (34.7913, 31.2518),
    "Rishon_LeZion": (34.7894, 31.9642),
    "Petah_Tikva": (34.8875, 32.0871),
    "Ashdod": (34.6495, 31.8044),
    "Netanya": (34.8599, 32.3329),
    "Holon": (34.7792, 32.0103),
    "Bnei_Brak": (34.8338, 32.0849),
    "Rehovot": (34.8118, 31.8942),
    "Ashkelon": (34.5711, 31.6693),
    "Bat_Yam": (34.7519, 32.0231),
    "Herzliya": (34.8254, 32.1663),
    "Kfar_Saba": (34.9069, 32.1750),
    "Eilat": (34.9519, 29.5577),
    "Nazareth": (35.3048, 32.6996),
    "Tiberias": (35.5312, 32.7922),
    "Acre": (35.0699, 32.9281),
    "Lod": (34.8903, 31.9467)
}

def calculate_distance(city1, city2):
    # Check if cities exist in the dictionary
    if city1 not in city_coordinates or city2 not in city_coordinates:
        return "One of the cities is not in the list!"
    

    lon1, lat1 = city_coordinates[city1]
    lon2, lat2 = city_coordinates[city2]
    

    delta_x = lon2 - lon1  
    delta_y = lat2 - lat1  
    
    R = 6371e3  
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    
    a = math.sin(delta_phi/2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = R * c  
    
    return {
        "delta_x": delta_x,  
        "delta_y": delta_y,  
        "distance_meters": distance  
    }


def main():
    city1 = input("Enter the first city (e.g., Tehran): ")
    city2 = input("Enter the second city (e.g., Tel_Aviv): ")
    
    result = calculate_distance(city1, city2)
    
    if isinstance(result, str):
        print(result)
    else:
        print(f"Longitude difference (x): {result['delta_x']:.4f} degrees")
        print(f"Latitude difference (y): {result['delta_y']:.4f} degrees")
        print(f"Straight-line distance: {result['distance_meters'] / 1000:.2f} kilometers")

if __name__ == "__main__":
    main()