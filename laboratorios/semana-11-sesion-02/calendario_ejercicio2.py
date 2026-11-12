
"""Ejercicio 2: el agregado CalendarioDeCancha.

Un CalendarioDeCancha es el calendario de una cancha en un dia, con todas
sus reservas adentro. Es la raiz del agregado: nadie de afuera crea,
mueve ni borra una Reserva directamente; todo pasa por sus metodos, y
cada metodo deja el calendario cumpliendo sus dos reglas:

- Dos reservas del calendario no se solapan.
- Un estudiante no tiene mas de MAXIMO_HORAS_POR_ESTUDIANTE horas
  reservadas en este calendario.

Cuando una operacion romperia una regla, el metodo lanza ValueError con el
motivo y no cambia nada. Usa FranjaHoraria y Reserva de
franja_ejercicio1.py, completo.

Corre las pruebas con:

    pytest test_calendario_ejercicio2.py

No cambies los nombres de la clase ni de los metodos: los tests
dependen de que existan exactamente asi.
"""

from franja_ejercicio1 import FranjaHoraria, Reserva

MAXIMO_HORAS_POR_ESTUDIANTE = 2


class CalendarioDeCancha:
    def __init__(self, cancha, fecha):
        self.cancha = cancha
        self.fecha = fecha
        self._reservas = {}

    def horas_de(self, estudiante):
        # TODO 1: cuantas horas suman las reservas del estudiante en este
        # calendario.
        total = 0
        for reserva in self._reservas.values():
            if reserva.estudiante == estudiante:
                total += reserva.franja.duracion()
        return total

    def choca_con_otra(self, franja):
        for reserva in self._reservas.values():
            if reserva.franja.se_solapa_con(franja):
                return True
        return False

    def reservar(self, id_reserva, estudiante, inicio, fin):
        # TODO 2: crea la FranjaHoraria con la fecha del calendario (si es
        # invalida, su propio ValueError basta) y, en este orden:
        # - id ya usado en este calendario: ValueError("id repetido");
        # - se solapa con otra reserva: ValueError("franja ocupada");
        # - el estudiante pasaria de MAXIMO_HORAS_POR_ESTUDIANTE:
        #   ValueError("limite de horas alcanzado").
        # Si todo se cumple, guarda la Reserva en self._reservas por su id.
        franja = FranjaHoraria(self.fecha, inicio, fin)

        if id_reserva in self._reservas:
            raise ValueError("id repetido")

        if self.choca_con_otra(franja):
            raise ValueError("franja ocupada")

        if self.horas_de(estudiante) + franja.duracion() > MAXIMO_HORAS_POR_ESTUDIANTE:
            raise ValueError("limite de horas alcanzado")

        self._reservas[id_reserva] = Reserva(id_reserva, estudiante, franja)

    def mover(self, id_reserva, nuevo_inicio, nuevo_fin):
        # TODO 3: cambia la franja de una reserva existente, con las mismas
        # dos reglas, sin comparar la reserva consigo misma.
        # Si el id no existe: ValueError("reserva desconocida").
        if id_reserva not in self._reservas:
            raise ValueError("reserva desconocida")

        reserva = self._reservas[id_reserva]
        nueva_franja = FranjaHoraria(self.fecha, nuevo_inicio, nuevo_fin)

        for otra_id, otra_reserva in self._reservas.items():
            if otra_id != id_reserva:
                if otra_reserva.franja.se_solapa_con(nueva_franja):
                    raise ValueError("franja ocupada")

        horas_actuales = self.horas_de(reserva.estudiante) - reserva.franja.duracion()

        if horas_actuales + nueva_franja.duracion() > MAXIMO_HORAS_POR_ESTUDIANTE:
            raise ValueError("limite de horas alcanzado")

        reserva.franja = nueva_franja

    def cancelar(self, id_reserva):
        # TODO 4: borra la reserva. Si el id no existe:
        # ValueError("reserva desconocida").
        if id_reserva not in self._reservas:
            raise ValueError("reserva desconocida")

        del self._reservas[id_reserva]

    def reservas(self):
        # TODO 5: devuelve las reservas como una lista de tuplas
        # (id, estudiante, franja), ordenada por hora de inicio. Nada de
        # lo que devuelvas puede servir para cambiar el calendario desde
        # afuera.
        ordenadas = sorted(
            self._reservas.values(),
            key=lambda reserva: reserva.franja.inicio
        )

        return [
            (reserva.id, reserva.estudiante, reserva.franja)
            for reserva in ordenadas
        ]

