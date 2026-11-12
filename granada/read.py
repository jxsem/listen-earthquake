"""Lista los canales de la estación EXARM (código, location_code y frecuencia
de muestreo) y descarga la traza del canal vertical alrededor del terremoto."""
from obspy import UTCDateTime
from obspy.clients.fdsn import Client

RED = "ES"
ESTACION = "EXARM"
NIVEL = "channel"
CANAL = "HNZ"
HORA_COMIENZO = UTCDateTime("2026-08-14T23:04:20")
HORA_FIN = UTCDateTime("2026-08-14T23:06:00")
SERVICIO = "IGN"
LOCALIZACION = ""


def crear_cliente():
    """Crea el cliente FDSN del servicio. Lanza ValueError o FDSNException si falla."""
    return Client(SERVICIO)


def obtener_canales(client):
    """Imprime código, location_code y frecuencia de muestreo de cada canal."""
    inventario = client.get_stations(starttime=HORA_COMIENZO, endtime=HORA_FIN, network=RED, station=ESTACION, level=NIVEL, channel="*", matchtimeseries=True)
    for red in inventario:
        for estacion in red:
            for canal in estacion:
                print(canal.code, canal.location_code, canal.sample_rate)


def obtener_sismograma(client):
    """Descarga la traza (Stream) del canal CANAL entre HORA_COMIENZO y HORA_FIN.

    Lanza FDSNNoDataException o FDSNNoServiceException si el IGN falla: lo decide quien llama.
    """
    return client.get_waveforms(network=RED, station=ESTACION, channel=CANAL, starttime=HORA_COMIENZO, endtime=HORA_FIN, location=LOCALIZACION)
