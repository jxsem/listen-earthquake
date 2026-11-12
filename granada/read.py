"""Lista los canales de una estación (código, location_code y frecuencia
de muestreo) y descarga la traza del canal vertical alrededor del terremoto."""
from obspy import UTCDateTime
from obspy.clients.fdsn import Client

RED = "ES"
NIVEL = "channel"
CANAL = "HNZ"
HORA_COMIENZO = UTCDateTime("2026-08-14T23:04:20")
HORA_FIN = UTCDateTime("2026-08-14T23:06:00")
SERVICIO = "IGN"
LOCALIZACION = ""


def crear_cliente():
    """Crea el cliente FDSN del servicio. Lanza ValueError o FDSNException si falla."""
    return Client(SERVICIO)


def obtener_canales(client, estacion):
    """Imprime código, location_code y frecuencia de muestreo de cada canal de la estación."""
    inventario = client.get_stations(starttime=HORA_COMIENZO, endtime=HORA_FIN, network=RED, station=estacion, level=NIVEL, channel="*", matchtimeseries=True)
    for red in inventario:
        for estacion_inventario in red:
            for canal in estacion_inventario:
                print(canal.code, canal.location_code, canal.sample_rate)


def obtener_sismograma(client, estacion):
    """Descarga la traza (Stream) del canal CANAL de la estación entre HORA_COMIENZO y HORA_FIN.

    Lanza FDSNNoDataException o FDSNNoServiceException si el IGN falla: lo decide quien llama.
    """
    return client.get_waveforms(network=RED, station=estacion, channel=CANAL, starttime=HORA_COMIENZO, endtime=HORA_FIN, location=LOCALIZACION)


if __name__ == "__main__":
    ESTACION_PRUEBA = "EXARM"
    cliente = crear_cliente()
    obtener_canales(cliente, ESTACION_PRUEBA)
    traza = obtener_sismograma(cliente, ESTACION_PRUEBA)
    print(traza)