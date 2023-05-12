class Enemy:
    def __init__(self, x, y, health=2, attack_power=1):
        self.x = x
        self.y = y
        self.health = health
        self.attack_power = attack_power
        self.name = "Bone"

    def attack(self, player):
        if player.defense:
            return "Player defended the attack!"
        else:
            player.take_damage(self.attack_power)
            return f"{self.name} did {self.attack_power} damage to player!"

    def take_damage(self, damage):
        self.health -= damage

class Boss(Enemy):
    def __init__(self, x, y, health=5, attack_power=3):
        super().__init__(x, y, health, attack_power)
        self.name = "BoneKing"