import math
import folium
import webbrowser

# Clase Ciudad con coordenadas reales
class Ciudad:
    def __init__(self, nombre, lat, lon):
        self.nombre = nombre
        self.lat = lat
        self.lon = lon

    def distancia(self, otra):
        # Aprox. distancia en km usando Haversine
        R = 6371
        dlat = math.radians(otra.lat - self.lat)
        dlon = math.radians(otra.lon - self.lon)
        a = math.sin(dlat / 2)**2 + math.cos(math.radians(self.lat)) * math.cos(math.radians(otra.lat)) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

# Lista de ciudades (excluyendo las madrileñas)
ciudades = [
    Ciudad("Barcelona", 41.3874, 2.1686),
    Ciudad("Sevilla", 37.3891, -5.9845),
    Ciudad("Valencia", 39.4699, -0.3763),
    Ciudad("Villarreal", 39.9365, -0.1022),
    Ciudad("San Sebastián", 43.3183, -1.9812),
    Ciudad("Bilbao", 43.2630, -2.9350),
    Ciudad("Vitoria-Gasteiz", 42.8469, -2.6727),
    Ciudad("Pamplona", 42.8125, -1.6458),
    Ciudad("Girona", 41.9794, 2.8214),
    Ciudad("Vigo", 42.2406, -8.7207),
    Ciudad("Palma de Mallorca", 39.5696, 2.6502),
    Ciudad("Las Palmas de G.C.", 28.1235, -15.4363),
    Ciudad("Granada", 37.1773, -3.5986),
    Ciudad("Cádiz", 36.5271, -6.2886),
    Ciudad("Valladolid", 41.6523, -4.7245)
]

# Ciudad de origen
madrid = Ciudad("Madrid", 40.4168, -3.7038)

# Algoritmo Nearest Neighbor
def tsp_nearest_neighbor(ciudades):
    ruta = [madrid]
    no_visitadas = ciudades.copy()
    actual = madrid
    while no_visitadas:
        siguiente = min(no_visitadas, key=lambda c: actual.distancia(c))
        ruta.append(siguiente)
        no_visitadas.remove(siguiente)
        actual = siguiente
    ruta.append(madrid)
    return ruta

# Ejecutar el algoritmo
ruta_optima = tsp_nearest_neighbor(ciudades)

# Mostrar la ruta y distancias
print("📍 Ruta de partidos fuera de casa para el Atlético de Madrid:\n")
distancia_total = 0
for i in range(len(ruta_optima) - 1):
    origen = ruta_optima[i]
    destino = ruta_optima[i + 1]
    distancia = origen.distancia(destino)
    distancia_total += distancia
    print(f"{origen.nombre} ➜ {destino.nombre} : {distancia:.2f} km")

print(f"\n🧭 Distancia total del viaje: {distancia_total:.2f} km\n")

# Crear el mapa
mapa = folium.Map(location=[madrid.lat, madrid.lon], zoom_start=6)

# Añadir marcadores numerados
for idx, ciudad in enumerate(ruta_optima):
    folium.Marker(
        location=[ciudad.lat, ciudad.lon],
        popup=f"{idx + 1}. {ciudad.nombre}",
        icon=folium.Icon(color='red' if ciudad.nombre == "Madrid" else 'blue')
    ).add_to(mapa)

# Dibujar línea de ruta
puntos = [[ciudad.lat, ciudad.lon] for ciudad in ruta_optima]
folium.PolyLine(puntos, color="blue", weight=3, opacity=0.7).add_to(mapa)

# Guardar y abrir el mapa
archivo = "ruta_atletico.html"
mapa.save(archivo)
webbrowser.open(archivo)
