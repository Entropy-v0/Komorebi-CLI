"""Módulo que define la entidad inmutable ReferenciaToken para el índice B-Tree."""


class ReferenciaToken:
    """Representa una ocurrencia inmutable de un token en un archivo y línea específicos.
    
    Se utiliza como valor asociado a las claves del Árbol B de indexación global,
    vinculando cada identificador con el ID único del archivo y el número de línea (base 1).
    """

    __slots__ = ("_id_archivo", "_linea")

    def __init__(self, id_archivo: str, linea: int) -> None:
        id_limpio = str(id_archivo).strip()
        if not id_limpio:
            raise ValueError("El id_archivo de ReferenciaToken no puede estar vacío.")
        if int(linea) < 1:
            raise ValueError("El número de línea en ReferenciaToken debe ser mayor o igual a 1.")

        object.__setattr__(self, "_id_archivo", id_limpio)
        object.__setattr__(self, "_linea", int(linea))

    @property
    def id_archivo(self) -> str:
        """Retorna el identificador único del archivo donde aparece el token."""
        return self._id_archivo

    @property
    def linea(self) -> int:
        """Retorna el número de línea (base 1) donde aparece el token."""
        return self._linea

    def __setattr__(self, nombre: str, valor: object) -> None:
        raise AttributeError("ReferenciaToken es una entidad inmutable y no permite modificar sus atributos.")

    def __eq__(self, otro: object) -> bool:
        if not isinstance(otro, ReferenciaToken):
            return False
        return self._id_archivo == otro._id_archivo and self._linea == otro._linea

    def __hash__(self) -> int:
        return hash((self._id_archivo, self._linea))

    def __lt__(self, otro: object) -> bool:
        if not isinstance(otro, ReferenciaToken):
            return NotImplemented
        return (self._id_archivo, self._linea) < (otro._id_archivo, otro._linea)

    def __repr__(self) -> str:
        return f"ReferenciaToken(id_archivo={self._id_archivo!r}, linea={self._linea})"

    def __str__(self) -> str:
        return f"{self._id_archivo}:{self._linea}"

