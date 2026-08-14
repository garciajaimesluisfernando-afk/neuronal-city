"""
NEURONAL-CITY — Simulation Engine
Phase 1 (MVP): City core — manages a group of agents living together
through shared days, and exports the city's history as JSON snapshots
(the bridge to the web visualization).
"""

import json
from agente import Agente, HUNGER_THRESHOLD


class Ciudad:
    def __init__(self, nombre="Neuronal City"):
        self.nombre = nombre
        self.agentes = []
        self.dia_actual = 0
        self.historial = []  # one snapshot dict per day

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
            
    def calcular_metricas(self):
        """Compute city-wide summary statistics for the current state."""
        poblacion = len(self.agentes)

        if poblacion == 0:
            return {
                "poblacion": 0,
                "agentes_hambre_critica": 0,
                "agentes_sin_dinero": 0,
                "dinero_total": 0,
                "dinero_promedio": 0,
                "dinero_max": 0,
                "dinero_min": 0,
                "hambre_promedio": 0,
                "energia_promedio": 0,
            }

        agentes_hambre_critica = sum(
            1 for a in self.agentes if a.hambre <= HUNGER_THRESHOLD
        )
        agentes_sin_dinero = sum(1 for a in self.agentes if a.dinero == 0)

        dineros = [a.dinero for a in self.agentes]
        dinero_total = sum(dineros)
        dinero_promedio = dinero_total / poblacion

        hambres = [a.hambre for a in self.agentes]
        energias = [a.energia for a in self.agentes]

        return {
            "poblacion": poblacion,
            "agentes_hambre_critica": agentes_hambre_critica,
            "agentes_sin_dinero": agentes_sin_dinero,
            "dinero_total": dinero_total,
            "dinero_promedio": round(dinero_promedio, 2),
            "dinero_max": max(dineros),
            "dinero_min": min(dineros),
            "hambre_promedio": round(sum(hambres) / poblacion, 2),
            "energia_promedio": round(sum(energias) / poblacion, 2),
        }
        
    def snapshot_del_dia(self):
        """Capture the current day's state as a serializable snapshot,
        including city-wide metrics."""
        return {
            "dia": self.dia_actual,
            "metricas": self.calcular_metricas(),
            "agentes": [agente.to_dict() for agente in self.agentes],
        }

    def simular(self, dias):
        """Run the city for a number of days, printing a report and
        recording a snapshot each day."""
        for _ in range(dias):
            self.avanzar_dia()
            self.reporte_del_dia()
            self.historial.append(self.snapshot_del_dia())

    def exportar_historial(self, ruta):
        """Write the full day-by-day history to a JSON file."""
        with open(ruta, "w", encoding="utf-8") as archivo:
            json.dump(self.historial, archivo, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    ciudad = Ciudad()

    ciudad.agregar_agente(Agente("Luis", "programador"))
    ciudad.agregar_agente(Agente("Ana", "mesero"))
    ciudad.agregar_agente(Agente("Carlos", "repartidor"))
    ciudad.agregar_agente(Agente("Pedro", "mesero", hambre=20, energia=100, dinero=0))

    print(f"=== Iniciando simulación de {ciudad.nombre} con {len(ciudad.agentes)} agentes ===\n")
    ciudad.simular(dias=7)

    ciudad.exportar_historial("historial.json")
    print(f"\n=== Historial exportado a historial.json ({len(ciudad.historial)} días) ===")