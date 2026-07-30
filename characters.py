from abc import ABC, abstractmethod
import random


class Character(ABC):

    def __init__(self, name: str, hp: int, attack_power: int):
        self._name         = name
        self._hp           = hp
        self._max_hp       = hp
        self._attack_power = attack_power
        self._is_alive     = True

    @property
    def name(self) -> str:
        return self._name

    @property
    def hp(self) -> int:
        return self._hp

    @property
    def max_hp(self) -> int:        # ← ditambah untuk kebutuhan HP bar di web
        return self._max_hp

    @property
    def is_alive(self) -> bool:
        return self._is_alive

    def take_damage(self, damage: int) -> int:
        self._hp = max(0, self._hp - damage)
        if self._hp == 0:
            self._is_alive = False
        return damage

    def get_animation_state(self) -> str:
        if not self._is_alive:
            return "death"
        return "idle"

    @abstractmethod
    def attack(self, target: 'Character') -> str:
        pass


class Player(Character):

    def __init__(self, name: str, hp: int, attack_power: int, mp: int):
        super().__init__(name, hp, attack_power)
        self._mp     = mp
        self._max_mp = mp

    @property
    def mp(self) -> int:
        return self._mp

    @property
    def max_mp(self) -> int:        # ← ditambah untuk kebutuhan MP bar di web
        return self._max_mp


class Hero(Player):

    def __init__(self, name: str):
        super().__init__(name, hp=120, attack_power=25, mp=20)
        self._shield_power = 15
        self._is_blocking  = False

    def attack(self, target: 'Character') -> str:
        actual = target.take_damage(self._attack_power)
        return f"⚔ {self._name} menebas! → -{actual} HP ke {target.name}"

    def block(self) -> str:
        cost = 5
        if self._mp >= cost:
            self._mp -= cost
            self._is_blocking = True
            return f"🛡 {self._name} bersiap bertahan! (-{self._shield_power} damage berikutnya)"
        return f"MP tidak cukup untuk block! (butuh {cost}, punya {self._mp})"

    def take_damage(self, damage: int) -> int:
        if self._is_blocking:
            reduced = max(0, damage - self._shield_power)
            self._is_blocking = False
            return super().take_damage(reduced)
        return super().take_damage(damage)


class Mage(Player):

    def __init__(self, name: str):
        super().__init__(name, hp=80, attack_power=12, mp=90)
        self._spell_power = 38

    def attack(self, target: 'Character') -> str:
        if self._mp >= 10:
            self._mp -= 10
            actual = target.take_damage(self._spell_power)
            return f"🔥 {self._name} melempar bola api! → -{actual} HP ke {target.name}"
        actual = target.take_damage(self._attack_power)
        return f"🪄 {self._name} memukul dengan tongkat! → -{actual} HP ke {target.name}"

    def cast_spell(self, target: 'Character') -> str:
        cost = 30
        if self._mp >= cost:
            self._mp -= cost
            actual = target.take_damage(self._spell_power * 2)
            return f"☄ {self._name} melepas METEOR! → -{actual} HP ke {target.name}"
        return f"MP tidak cukup! (butuh {cost}, punya {self._mp})"


class Monster(Character):

    def __init__(self, name: str, hp: int = 375, attack_power: int = 20):
        super().__init__(name, hp=hp, attack_power=attack_power)

    def attack(self, target: 'Character') -> str:
        is_critical = random.random() < 0.30
        raw_damage  = self._attack_power * (2 if is_critical else 1)
        actual      = target.take_damage(raw_damage)
        crit_text   = " 💥 CRITICAL!" if is_critical else ""
        return f"👾 {self._name} menyerang!{crit_text} → -{actual} HP ke {target.name}"

    def monster_turn(self, target: 'Character') -> str:
        return self.attack(target)
