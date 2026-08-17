"""
NEURONAL-CITY — Simulation Engine
Phase 1 (MVP): City core — manages a group of agents living together
through shared days, and exports the city's history as JSON snapshots
(the bridge to the web visualization).

Phase 3.2 adds a random event system: each day there's a chance a
city-wide event triggers (economic or wellbeing related), temporarily
modifying shared conditions like food price, income, hunger decay,
or rent.
"""

import json
import random
from agente import Agente, HUNGER_THRESHOLD, DEFAULT_FOOD_COST

# --- City economy settings ---
RENTA_MONTO = 25          # rent charged periodically
RENTA_CADA_DIAS = 7       # how often rent is due ("once a week")

# --- Event system settings ---
PROBABILIDAD_EVENTO_DIARIO = 0.08  # configurable: chance per day that an event triggers

# Each event defines temporary modifiers applied while it's active.
# "efectos_por_profesion" is reserved for a future phase — it lets an
# event affect professions differently (e.g. a tech layoff hitting
# "programador" harder). It's not used yet in Phase 3.2; every event
# currently applies its effects equally to all agents.
EVENTOS = [
    {
        "id": "inflacion",
        "nombre": "Inflación alimentaria",
        "descripcion": "El precio de la comida subió 50%",
        "duracion_dias": 5,
        "efectos": {"multiplicador_precio_comida": 1.5},
        "efectos_por_profesion": {},  # reserved for a future phase
    },
    {
        "id": "festival",
        "nombre": "Festival de la ciudad",
        "descripcion": "La comunidad celebra junta: el hambre baja más lento estos días",
        "duracion_dias": 3,
        "efectos": {"multiplicador_hambre_decay": 0.5},
        "efectos_por_profesion": {},
    },
    {
        "id": "crisis",
        "nombre": "Crisis económica",
        "descripcion": "Los ingresos por trabajo bajaron 25%",
        "duracion_dias": 4,
        "efectos": {"multiplicador_ingreso": 0.75},
        "efectos_por_profesion": {},
    },
    {
        "id": "bono",
        "nombre": "Bono gubernamental",
        "descripcion": "Cada agente recibió un bono directo",
        "duracion_dias": 1,
        "efectos": {"bono_directo": 30},
        "efectos_por_profesion": {},
    },
    {
        "id": "aumento_renta",
        "nombre": "Aumento de renta",
        "descripcion": "El monto de la próxima renta se duplicó",
        "duracion_dias": 7,
        "efectos": {"multiplicador_renta": 2.0},
        "efectos_por_profesion": {},
    },
    {
        "id": "escasez",
        "nombre": "Escasez de comida",
        "descripcion": "El precio de la comida se disparó temporalmente",
        "duracion_dias": 2,
        "efectos": {"multiplicador_precio_comida": 2.0},
        "efectos_por_profesion": {},
    },
]


class Ciudad:
    def __init__(self, nombre="Neuronal City"):
        self.nombre = nombre
        self.agentes = []
        self.dia_actual = 0
        self.historial = []  # one snapshot dict per day
        self.precio_comida = DEFAULT_FOOD_COST  # shared by the whole city; events can modify it temporarily

        # --- Event system state ---
        self.probabilidad_evento_diario = PROBABILIDAD_EVENTO_DIARIO
        self.evento_activo = None  # dict with event info + días restantes, or None
        self.multiplicador_precio_comida = 1.0
        self.multiplicador_ingreso = 1.0
        self.multiplicador_hambre_decay = 1.0
        self.multiplicador_renta = 1.0

    def agregar_agente(self, agente):
        self.agentes.append(agente)

    def _disparar_evento(self):
        """If no event is active, roll the dice — there's a chance a
        new random event starts today. Only one event can be active
        at a time."""
        if self.evento_activo is not None:
            return  # a event is already running; wait for it to end

        if random.random() >= self.probabilidad_evento_diario:
            return  # no event today

        evento = random.choice(EVENTOS)
        self.evento_activo = {
            **evento,
            "dias_restantes": evento["duracion_dias"],
        }

        efectos = evento["efectos"]
        self.multiplicador_precio_comida = efectos.get("multiplicador_precio_comida", 1.0)
        self.multiplicador_ingreso = efectos.get("multiplicador_ingreso", 1.0)
        self.multiplicador_hambre_decay = efectos.get("multiplicador_hambre_decay", 1.0)
        self.multiplicador_renta = efectos.get("multiplicador_renta", 1.0)

        if "bono_directo" in efectos:
            for agente in self.agentes:
                agente.recibir_dinero(efectos["bono_directo"])

    def _actualizar_evento_activo(self):
        """Count down the active event's remaining days. When it runs
        out, reset all modifiers back to normal."""
        if self.evento_activo is None:
            return

        self.evento_activo["dias_restantes"] -= 1
        if self.evento_activo["dias_restantes"] <= 0:
            self.evento_activo = None
            self.multiplicador_precio_comida = 1.0
            self.multiplicador_ingreso = 1.0
            self.multiplicador_hambre_decay = 1.0
            self.multiplicador_renta = 1.0

    def avanzar_dia(self):
        """Make every agent live one day, applying any active event's
        effects, charge rent if it's due, then advance the day counter."""
        self.dia_actual += 1

        self._disparar_evento()

        precio_comida_efectivo = round(self.precio_comida * self.multiplicador_precio_comida)
        for agente in self.agentes:
            agente.vivir_un_dia(
                precio_comida=precio_comida_efectivo,
                multiplicador_ingreso=self.multiplicador_ingreso,
                multiplicador_hambre_decay=self.multiplicador_hambre_decay,
            )

        if self.dia_actual % RENTA_CADA_DIAS == 0:
            monto_renta_efectivo = round(RENTA_MONTO * self.multiplicador_renta)
            for agente in self.agentes:
                agente.pagar_renta(monto_renta_efectivo)

        self._actualizar_evento_activo()

    def reporte_del_dia(self):
        """Print the state of every agent for the current day."""
        print(f"--- {self.nombre} | Día {self.dia_actual} ---")
        if self.evento_activo:
            print(f"  ⚡ Evento activo: {self.evento_activo['nombre']} "
                  f"({self.evento_activo['dias_restantes']} días restantes)")
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
                "brecha_economica": 0,
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
            "brecha_economica": max(dineros) - min(dineros),
            "hambre_promedio": round(sum(hambres) / poblacion, 2),
            "energia_promedio": round(sum(energias) / poblacion, 2),
        }

    def _evento_para_json(self):
        """Serializable representation of the active event, or None."""
        if self.evento_activo is None:
            return None
        return {
            "nombre": self.evento_activo["nombre"],
            "descripcion": self.evento_activo["descripcion"],
            "dias_restantes": self.evento_activo["dias_restantes"],
        }

    def snapshot_del_dia(self):
        """Capture the current day's state as a serializable snapshot,
        including city-wide metrics and the active event (if any)."""
        return {
            "dia": self.dia_actual,
            "metricas": self.calcular_metricas(),
            "evento_activo": self._evento_para_json(),
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
    ciudad.simular(dias=40)

    ciudad.exportar_historial("historial.json")
    print(f"\n=== Historial exportado a historial.json ({len(ciudad.historial)} días) ===")