"""Lista los canales de la estación EXARM (código, location_code y frecuencia
de muestreo) y descarga la traza del canal vertical alrededor del terremoto."""
import sys

from obspy import UTCDateTime
from obspy.clients.fdsn import Client
from obspy.clients.fdsn.header import FDSNNoDataException, FDSNNoServiceException

RED = "ES"
ESTACION = "EXARM"
NIVEL = "channel"
CANAL = "HNZ"
HORA_COMIENZO = UTCDateTime("2026-08-14T23:04:20")
HORA_FIN = UTCDateTime("2026-08-14T23:06:00")
SERVICIO = "IGN"
LOCALIZACION = ""

try:
    client = Client(SERVICIO)
except ValueError:
    print(f"El servicio '{SERVICIO}' es desconocido")
    sys.exit(1)
except FDSNNoServiceException:
    print(f"No se pudo contactar con el servicio '{SERVICIO}' (¿sin red o servicio caído?)")
    sys.exit(1)

def obtener_canales():
    try:
        inventario = client.get_stations(starttime=HORA_COMIENZO, endtime=HORA_FIN, network=RED, station=ESTACION, level=NIVEL, channel="*", matchtimeseries=True)
    except FDSNNoServiceException:
        print("Error de cliente: No se puede conectar con el servicio")
        sys.exit(1)
    except FDSNNoDataException:
        print("Error de cliente: El servicio no contiene datos según el filtro aplicado")
        sys.exit(1)
    else:
        for red in inventario:
            for estacion in red:
                for canal in estacion:
                    print(canal.code, canal.location_code, canal.sample_rate)

def obtener_sismograma():
    try:
        onda = client.get_waveforms(network=RED,station=ESTACION,channel=CANAL,starttime=HORA_COMIENZO,endtime=HORA_FIN, location=LOCALIZACION)
    except FDSNNoServiceException:
        print("Error: No se pudo contactar con el servicio")
        sys.exit(1)
    except FDSNNoDataException:
        print("Error: No se pudo descargar la traza")
        sys.exit(1)
    else:
        #return onda.plot()
        return onda

if __name__ == "__main__":
    obtener_sismograma()
