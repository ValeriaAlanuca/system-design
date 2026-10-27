"""Ejercicio 1: repartir las reservas de ReservaU en 4 shards, uno por
campus (reparto por lista).

Corre esto para ver el resultado:

    python3 sharding_por_campus_ejercicio1.py

Y las pruebas con:

    pytest test_sharding_por_campus_ejercicio1.py
"""

from datos_reservas import generar_reservas

SHARD_DE_CAMPUS = {
    "Campus Norte": 0,
    "Campus Sur": 1,
    "Campus Centro": 2,
    "Campus Este": 3,
}


def shard_por_campus(reserva):
    # TODO: devuelve el numero de shard (0 a 3) que le corresponde a la
    # reserva segun su campus, usando el diccionario SHARD_DE_CAMPUS.
    return SHARD_DE_CAMPUS[reserva.campus]


def contar_por_shard(reservas, cantidad_de_shards):
    # TODO: devuelve una lista con "cantidad_de_shards" posiciones, donde
    # la posicion i es cuantas reservas caen en el shard i segun
    # shard_por_campus(...).
    contar = [0 for i in range(cantidad_de_shards)]
    for reserva in reservas:
        shard = shard_por_campus(reserva)
        contar[shard] += 1
    return contar

if __name__ == "__main__":
    conteo = contar_por_shard(generar_reservas(), 4)
    print("Reservas por shard (campus):", conteo)
    print("El shard mas cargado tiene", max(conteo), "de", sum(conteo), "reservas")
