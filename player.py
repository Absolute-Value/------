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
        self.health -= damage
        if self.health <= 0:
            print("Player was killed ! Game over .")
            self.game_over = True

    def gain_experience(self, experience):
        self.experience += experience
        if self.experience >= self.experience_to_level_up:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.max_health += 5
        self.health = self.max_health
        self.experience -= self.experience_to_level_up
        self.experience_to_level_up *= 2
        print(f"Player leveled up ! ({self.level-1}->{self.level}) ")
        print("HP increased and fully healed .")