
"""Ejercicio 3: la garantia de una reserva, en el contexto de Pagos.

Al reservar, ReservaU retiene una garantia en la tarjeta del estudiante.
Despues pasa una de dos cosas, una sola vez: se devuelve completa (el
estudiante jugo o cancelo a tiempo), o se cobra una parte o el total (no se
presento). En Pagos al estudiante se le llama titular: es la persona que
paga, no la que juega.

Dinero: value object inmutable con dos campos, centavos (int) y moneda
(str, tres letras, como "USD"). Se usa en centavos para no sumar dolares
con decimales de punto flotante.
- Al crearse: centavos negativo, ValueError("monto negativo"); moneda que
  no tiene exactamente tres letras, ValueError("moneda invalida").
- sumar(otro) y restar(otro): un Dinero nuevo. Con monedas distintas,
  ValueError("monedas distintas"). Si restar daria negativo, el
  ValueError("monto negativo") del propio Dinero.
- es_mayor_que(otro): True o False. Con monedas distintas, ValueError.
- texto(): por ejemplo "USD 5.00" o "USD 12.05".

GarantiaDeReserva: la raiz de un agregado. Se construye con
(id_garantia, id_reserva, titular, monto); id_reserva es el texto "r-1",
no un objeto Reserva. Empieza con estado "retenida" y cobrado igual a 0
en la moneda del monto.
- devolver(): pasa a "devuelta" y devuelve el Dinero a reintegrar.
- cobrar(monto_cobrado): pasa a "cobrada", guarda monto_cobrado en
  cobrado, y devuelve el Dinero a reintegrar (el monto menos lo cobrado).
  Si monto_cobrado es mayor que el monto, ValueError("el cobro supera la
  garantia").
- Si la garantia ya no esta "retenida", devolver() y cobrar() lanzan
  ValueError("la garantia ya fue resuelta").
- Dos garantias con el mismo id_garantia son la misma garantia.
Cuando un metodo lanza, la garantia queda exactamente como estaba.

Corre las pruebas con:

    pytest test_garantias_ejercicio3.py
"""

from dataclasses import dataclass


# TODO: escribe Dinero y GarantiaDeReserva.

@dataclass(frozen=True)
class Dinero:
    centavos: int
    moneda: str

    def __post_init__(self):
        if self.centavos < 0:
            raise ValueError("monto negativo")

        if len(self.moneda) != 3 or not self.moneda.isalpha():
            raise ValueError("moneda invalida")

    def sumar(self, otro):
        if self.moneda != otro.moneda:
            raise ValueError("monedas distintas")

        return Dinero(self.centavos + otro.centavos, self.moneda)

    def restar(self, otro):
        if self.moneda != otro.moneda:
            raise ValueError("monedas distintas")

        return Dinero(self.centavos - otro.centavos, self.moneda)

    def es_mayor_que(self, otro):
        if self.moneda != otro.moneda:
            raise ValueError("monedas distintas")

        return self.centavos > otro.centavos

    def texto(self):
        return f"{self.moneda} {self.centavos / 100:.2f}"


@dataclass(eq=False)
class GarantiaDeReserva:
    id_garantia: str
    id_reserva: str
    titular: str
    monto: Dinero

    def __post_init__(self):
        self.estado = "retenida"
        self.cobrado = Dinero(0, self.monto.moneda)

    def devolver(self):
        if self.estado != "retenida":
            raise ValueError("la garantia ya fue resuelta")

        self.estado = "devuelta"
        return self.monto

    def cobrar(self, monto_cobrado):
        if self.estado != "retenida":
            raise ValueError("la garantia ya fue resuelta")

        if monto_cobrado.es_mayor_que(self.monto):
            raise ValueError("el cobro supera la garantia")

        reintegro = self.monto.restar(monto_cobrado)

        self.cobrado = monto_cobrado
        self.estado = "cobrada"

        return reintegro

    def __eq__(self, otra):
        if not isinstance(otra, GarantiaDeReserva):
            return NotImplemented

        return self.id_garantia == otra.id_garantia

    def __hash__(self):
        return hash(self.id_garantia)
