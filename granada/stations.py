import sys

from obspy import UTCDateTime
from obspy.clients.fdsn import Client
from obspy.clients.fdsn.header import FDSNNoDataException, FDSNNoServiceException
from obspy.geodetics import degrees2kilometers, locations2degrees

LATITUD_EPICENTRO = 37.1076
LONGITUD_EPICENTRO = -3.6456   
def obtener_estaciones():
    client = Client("IGN")
    starttime = UTCDateTime("2026-08-14T23:00:00")
    endtime = UTCDateTime("2026-08-15T23:00:00")     
    #Inventory → Network → Station → Channel
    inventory = client.get_stations(starttime=starttime, endtime=endtime, latitude=LATITUD_EPICENTRO, 
                                    longitude=LONGITUD_EPICENTRO, maxradius=2, level="station")
    return inventory

try:
    inventario = obtener_estaciones() #no guarda una función. Ejecuta obtener_estaciones() y guarda en inventario el valor del return,
except FDSNNoServiceException:
    print("No se pudo contactar con el servicio (¿sin red, o el cliente no ofrece 'station'?)")
    sys.exit(1)
except FDSNNoDataException:
    print("El servicio respondió, pero no hay estaciones con esos filtros")
    sys.exit(1)
else:
    print(inventario)

## Sabiendo las coordenadas del epicentro, calcular que 
# estación está mas cerca del epicentro.
def distancia_al_epicentro_km(latitud, longitud):
    """Distancia en km entre un punto (latitud, longitud) y el epicentro."""
    grados = locations2degrees(latitud, longitud, LATITUD_EPICENTRO, LONGITUD_EPICENTRO)
    return degrees2kilometers(grados)


for estacion in inventario[0]:
    distancia = distancia_al_epicentro_km(estacion.latitude, estacion.longitude)
    print(f"{estacion.code}: {distancia:.1f} km")