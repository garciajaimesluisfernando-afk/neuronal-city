"""
NEURONAL-CITY — Simulation Engine
Phase 1 (MVP): Agent core logic.

An Agent has three needs:
- hunger (0-100): 0 = starving (critical), 100 = fully fed
- energy (0-100): 0 = exhausted, cannot work, 100 = fully rested
- money (0+, no upper limit): can't go negative

Each agent has a profession, which only affects how much money
it earns when it works.
"""

# Profession -> base income per day when working
PROFESSIONS = {
    "mesero": 15,
    "repartidor": 20,
    "programador": 40,
}

# Thresholds that trigger "urgent" behavior
HUNGER_THRESHOLD = 30
ENERGY_THRESHOLD = 30

# Daily natural decay/costs
HUNGER_DECAY_PER_DAY = 15
ENERGY_DECAY_WHEN_WORKING = 20
ENERGY_RECOVERY_WHEN_RESTING = 40
FOOD_COST = 10
FOOD_HUNGER_RECOVERY = 50


def clamp(value, minimum=0, maximum=100):
    """Keep a value within [minimum, maximum]."""
    return max(minimum, min(maximum, value))


class Agente:
    def __init__(self, nombre, profesion, hambre=100, energia=100, dinero=20):
        if profesion not in PROFESSIONS:
            raise ValueError(f"Profesión desconocida: {profesion}")

        self.nombre = nombre
        self.profesion = profesion
        self.hambre = clamp(hambre)
        self.energia = clamp(energia)
        self.dinero = max(0, dinero)  # money has no upper limit, but can't be negative
        self.ultima_accion = None  # for logging what happened each day

    def comer(self):
        """Eat if there's enough money. Reduces money, increases hunger stat."""
        if self.dinero >= FOOD_COST:
            self.dinero -= FOOD_COST
            self.hambre = clamp(self.hambre + FOOD_HUNGER_RECOVERY)
            self.ultima_accion = "comió"
        else:
            self.ultima_accion = "no pudo comer (sin dinero)"

    def descansar(self):
        """Rest to recover energy. Earns no money this day."""
        self.energia = clamp(self.energia + ENERGY_RECOVERY_WHEN_RESTING)
        self.ultima_accion = "descansó"

    def trabajar(self):
        """Work to earn money based on profession. Costs energy."""
        ingreso = PROFESSIONS[self.profesion]
        self.dinero += ingreso
        self.energia = clamp(self.energia - ENERGY_DECAY_WHEN_WORKING)
        self.ultima_accion = f"trabajó como {self.profesion} (+{ingreso})"

    def vivir_un_dia(self):
        """
        Decide and perform one action for the day, based on priority:
        1. Eat if hunger is low and there's money for it.
        2. Rest if energy is low.
        3. Otherwise, work.
        Hunger always decays naturally at the end of the day.
        """
        if self.hambre <= HUNGER_THRESHOLD:
            self.comer()
        elif self.energia <= ENERGY_THRESHOLD:
            self.descansar()
        else:
            self.trabajar()

        self.hambre = clamp(self.hambre - HUNGER_DECAY_PER_DAY)

    def __str__(self):
        return (
            f"{self.nombre} ({self.profesion}) | "
            f"Hambre: {self.hambre:3d} | Energía: {self.energia:3d} | "
            f"Dinero: {self.dinero:4d} | Acción: {self.ultima_accion}"
        )
        
    def to_dict(self):
        """Serializable representation of the agent's current state."""
        return {
            "nombre": self.nombre,
            "profesion": self.profesion,
            "hambre": self.hambre,
            "energia": self.energia,
            "dinero": self.dinero,
            "ultima_accion": self.ultima_accion,
        }


if __name__ == "__main__":
    print("=== Test 1: Agente recién creado ===")
    luis = Agente("Luis", "programador")
    print(luis)
    print()

    print("=== Test 2: Simulación de varios días (2 agentes) ===")
    ana = Agente("Ana", "mesero")
    for dia in range(1, 11):
        luis.vivir_un_dia()
        ana.vivir_un_dia()
        print(f"Día {dia}:")
        print(f"  {luis}")
        print(f"  {ana}")
    print()

    print("=== Test 3: Agente sin dinero y con hambre baja ===")
    pobre = Agente("Pedro", "mesero", hambre=20, energia=100, dinero=0)
    for dia in range(1, 4):
        pobre.vivir_un_dia()
        print(f"Día {dia}: {pobre}")