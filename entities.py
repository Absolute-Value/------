class Entity:
    def __init__(self, x:int, y:int, name:str="None", health:int=1, attack_power:int=1, exp:int=0):
        self.x = x
        self.y = y
        self.health = health
        self.name = name
        self.attack_power = attack_power
        self.exp = exp
        
class Enemy(Entity):
    def __init__(self, x:int, y:int, name:str="Bone", health:int=3, attack_power:int=1, exp:int=1):
        super().__init__(x, y, name, health, attack_power, exp)

    def attack(self, player):
        player.health = max(0,player.health-self.attack_power)
        return [f"{self.name}の こうげき", f"{self.attack_power}ダメージをうけた！"]