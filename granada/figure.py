"""Dibuja el sismograma de una traza y lo guarda como imagen."""


def guardar_figura(traza, ruta):
    """Dibuja la traza y guarda la figura en un fichero de imagen.

    Args:
        traza: Stream de ObsPy (lo que devuelve obtener_sismograma).
        ruta: ruta del fichero de salida; la extensión (.png) decide el formato.
    """
    traza.plot(outfile=ruta)

