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
    # Inventory → Network → Station → Channel
    inventory = client.get_stations(starttime=starttime, endtime=endtime, latitude=LATITUD_EPICENTRO,
                                    longitude=LONGITUD_EPICENTRO, maxradius=2, level="station")
    return inventory


def distancia_al_epicentro_km(latitud, longitud):
    """Distancia en km entre un punto (latitud, longitud) y el epicentro."""
    grados = locations2degrees(latitud, longitud, LATITUD_EPICENTRO, LONGITUD_EPICENTRO)
    return degrees2kilometers(grados)


def main():
    try:
        inventario = obtener_estaciones()
    except FDSNNoServiceException:
        print("No se pudo contactar con el servicio (¿sin red, o el cliente no ofrece 'station'?)")
        sys.exit(1)
    except FDSNNoDataException:
        print("El servicio respondió, pero no hay estaciones con esos filtros")
        sys.exit(1)
    print(inventario)

    distancia_km_por_codigo = {}  # tabla: código de estación -> distancia en km
    for estacion in inventario[0]:
        distancia_km = distancia_al_epicentro_km(estacion.latitude, estacion.longitude)
        distancia_km_por_codigo[estacion.code] = distancia_km
        print(f"{estacion.code}: {distancia_km:.1f} km")

    codigo_mas_cercana = min(distancia_km_por_codigo, key=distancia_km_por_codigo.get)
    print(codigo_mas_cercana)


if __name__ == "__main__":
    main()
