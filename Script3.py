import requests
import urllib.parse

# URLs de la API de GraphHopper
geocode_url = "https://graphhopper.com/api/1/geocode?"
route_url = "https://graphhopper.com/api/1/route?"

# Función para obtener datos de geocodificación
def geocode_location(location, key):
    url = geocode_url + urllib.parse.urlencode({"q": location, "limit": "1", "key": key})
    reply = requests.get(url)
    json_data = reply.json()
    status_code = reply.status_code
    return json_data, status_code

# Función para calcular la ruta y obtener detalles del viaje
def calculate_route(origin, destination, mode, key):
    # Geocodificación de origen y destino
    origin_data, origin_status = geocode_location(origin, key)
    destination_data, destination_status = geocode_location(destination, key)

    if origin_status == 200 and destination_status == 200:
        origin_lat = origin_data['hits'][0]['point']['lat']
        origin_lng = origin_data['hits'][0]['point']['lng']
        destination_lat = destination_data['hits'][0]['point']['lat']
        destination_lng = destination_data['hits'][0]['point']['lng']

        # Calcular ruta entre origen y destino
        url = route_url + urllib.parse.urlencode({
            "point": f"{origin_lat},{origin_lng}",
            "point": f"{destination_lat},{destination_lng}",
            "vehicle": mode,
            "key": key
        })
        reply = requests.get(url)
        route_data = reply.json()
        status_code = reply.status_code

        if status_code == 200:
            distance = route_data['paths'][0]['distance'] / 1000  # distancia en kilómetros
            time_seconds = route_data['paths'][0]['time'] / 1000  # tiempo en segundos

            # Convertir tiempo de segundos a horas y minutos
            time_hours = int(time_seconds / 3600)
            time_minutes = int((time_seconds % 3600) / 60)

            # Construir narrativa del viaje
            narrative = f"Viajando desde {origin} a {destination} en {mode}, tomará aproximadamente {time_hours} horas y {time_minutes} minutos."

            return distance, time_hours, time_minutes, narrative
        else:
            return None, None, None, "Error al calcular la ruta."
    else:
        return None, None, None, "Error al obtener las coordenadas de geocodificación."

def main():
    print("Calculador de ruta y duración de viaje entre Santiago de Chile y Lima, Peru")
    print("Ingrese 'e' en cualquier momento para salir.\n")

    key = input("0d842c46-d8f2-4b54-8f01-6f5c01c7e016:")

    while True:
        mode = input("Ingrese el tipo de medio de transporte (ej. car, foot, bike): ")
        if mode.lower() == 'e':
            break
        
        distance, time_hours, time_minutes, narrative = calculate_route("Santiago de Chile", "Lima, Peru", mode, key)
        
        if distance is not None:
            print(f"\nDistancia entre Santiago de Chile y Lima, Peru:")
            print(f"- Kilómetros: {distance:.2f} km")
            
            print(f"\nDuración estimada del viaje en {mode}:")
            print(f"- {time_hours} horas y {time_minutes} minutos\n")
            
            print(f"Narrativa del viaje:\n{narrative}\n")
        else:
            print("Error al calcular la ruta. Por favor verifica los datos ingresados.\n")

if __name__ == "__main__":
    main()