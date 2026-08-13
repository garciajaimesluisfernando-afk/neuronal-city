"""
NEURONAL-CITY — Simulation Engine
Phase 1 (MVP): City core — manages a group of agents living together
through shared days.
"""

from agente import Agente


class Ciudad:
    def __init__(self, nombre="Neuronal City"):
        self.nombre = nombre
        self.agentes = []
        self.dia_actual = 0

    def agregar_agente(self, agente):
        self.agentes.append(agente)

    def avanzar_dia(self):
        """Make every agent live one day, then advance the city's day counter."""
        self.dia_actual += 1
        for agente in self.agentes:
            agente.vivir_un_dia()

    def reporte_del_dia(self):
        """Print the state of every agent for the current day."""
        print(f"--- {self.nombre} | Día {self.dia_actual} ---")
        for agente in self.agentes:
            print(f"  {agente}")

    def simular(self, dias):
        """Run the city for a number of days, printing a report each day."""
        for _ in range(dias):
            self.avanzar_dia()
            self.reporte_del_dia()


if __name__ == "__main__":
    ciudad = Ciudad()

    ciudad.agregar_agente(Agente("Luis", "programador"))
    ciudad.agregar_agente(Agente("Ana", "mesero"))
    ciudad.agregar_agente(Agente("Carlos", "repartidor"))
    ciudad.agregar_agente(Agente("Pedro", "mesero", hambre=20, energia=100, dinero=0))

    print(f"=== Iniciando simulación de {ciudad.nombre} con {len(ciudad.agentes)} agentes ===\n")
    ciudad.simular(dias=7)