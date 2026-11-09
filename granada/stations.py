from obspy import UTCDateTime
from obspy.clients.fdsn import Client
from obspy.clients.fdsn.header import FDSNNoDataException, FDSNNoServiceException


def obtener_estaciones():
    client = Client("IGN")
    starttime = UTCDateTime("2026-08-14T23:00:00")
    endtime = UTCDateTime("2026-08-15T23:00:00")        
    inventory = client.get_stations(starttime=starttime, endtime=endtime, latitude=37.1076, longitude=-3.6456, maxradius=0.001, level="station")
    return inventory

try:
    inventario = obtener_estaciones() #no guarda una función. Ejecuta obtener_estaciones() y guarda en inventario el valor del return,
except FDSNNoServiceException:
    print("No se pudo contactar con el servicio (¿sin red, o el cliente no ofrece 'station'?)")
except FDSNNoDataException:
    print("El servicio respondió, pero no hay estaciones con esos filtros")
else:
    print(inventario)