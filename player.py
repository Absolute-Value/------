class Player:
    def __init__(self, x:int=5, y:int=5):
        self.x = x
        self.y = y
        self.max_health = 5
        self.health = self.max_health
        self.attack_power = 1
        self.defense = False
        self.level = 1
        self.experience = 0
        self.experience_to_level_up = 2

    def attack(self, enemy):
        enemy.health -= self.attack_power
        return f"{enemy.name}に{self.attack_power}ダメージあたえた"

    def take_damage(self, damage):
        self.health = max(0,self.health-damage)

    def heal(self, value:int=3):
        self.health = min(self.max_health, self.health + value)
        
    def gain_experience(self, experience):
        self.experience += experience
        states = [f"{experience}けいけんち をてにいれた"]
        if self.experience >= self.experience_to_level_up:
            states.extend(self.level_up())
        return states

    def level_up(self):
        status = [f"レベルアップ！"]
        self.level += 1
        status.append(f"HP ({self.max_health} -> {self.max_health+2})")
        self.max_health += 2
        self.health = self.max_health
        if self.level % 2 == 0:
            status.append(f"AT ({self.max_health} -> {self.max_health+1})")
            self.attack_power += 1
        
        self.experience -= self.experience_to_level_up
        self.experience_to_level_up += int(1.5*self.experience_to_level_up)
        
        return status