class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.health = 5
        self.max_health = 5
        self.attack_power = 1
        self.defense = False
        self.level = 1
        self.experience = 0
        self.experience_to_level_up = 20

    def attack(self, enemy):
        enemy.health -= self.attack_power
        return f"Player did {self.attack_power} damage to {enemy.name} ."

    def take_damage(self, damage):
        self.health = max(0,self.health-damage)

    def heal(self, value=0.3):
        self.health = min(self.max_health, self.health + int(self.max_health*value))
        
    def gain_experience(self, experience):
        self.experience += experience
        states = [f"Player got {experience} exp ."]
        if self.experience >= self.experience_to_level_up:
            states.extend(self.level_up())
        return states

    def level_up(self):
        status = [f"Player leveled up !"]
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