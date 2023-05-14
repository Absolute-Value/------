class Player:
    def __init__(self, x:int=5, y:int=5):
        self.x = x
        self.y = y
        self.max_health = 5
        self.health = self.max_health
        self.mp = 5
        self.max_mp = 5
        self.attack_power = 1
        self.level = 1
        self.experience = 0
        self.experience_to_level_up = 2
        self.inventory = {"ポーション":1}

    def attack(self, enemy):
        enemy.health -= self.attack_power
        return ["プレイヤーの こうげき！", f"{enemy.name}に{self.attack_power}ダメージ"]

    def heal(self, value:int=3):
        value = min(self.max_health - self.health, value)
        self.health += value
        return [f"HPが{value}かいふくした"]
        
    def gain_experience(self, experience):
        self.experience += experience
        states = [f"{experience}けいけんち をてにいれた"]
        return states

    def level_up(self):
        status = [f"レベルUP！", "ステータスUP！"]
        self.level += 1
        status.append(f"HP ({self.max_health} -> {self.max_health+2})")
        self.max_health += 2
        self.health = self.max_health
        status.append(f"MP ({self.max_mp} -> {self.mp+1})")
        self.max_mp += 1
        self.mp = min(self.max_mp, self.mp+10)
        if self.level % 2 == 0:
            status.append(f"AT ({self.max_health} -> {self.max_health+1})")
            self.attack_power += 1
        
        self.experience -= self.experience_to_level_up
        self.experience_to_level_up += int(1.5*self.experience_to_level_up)
        
        return status