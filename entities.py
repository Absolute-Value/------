class Entity:
    def __init__(self, x:int, y:int, name:str="None", health:int=1, attack_power:int=1):
        self.x = x
        self.y = y
        self.health = health
        self.name = name
        self.attack_power = attack_power
        
class Enemy(Entity):
    def __init__(self, x:int, y:int, name:str="Bone", health:int=2, attack_power:int=1):
        super().__init__(x, y, name, health, attack_power)

    def attack(self, player):
        if player.defense:
            return "Player defended the attack!"
        else:
            player.take_damage(self.attack_power)
            return f"{self.name} did {self.attack_power} damage to player!"

    def take_damage(self, damage):
        self.health -= damage