import random

class Player:
    def __init__(self):
        self.health = 5
        self.level = 1
        self.attack_power = 1

    def level_up(self):
        self.level += 1
        self.attack_power += 1
        print("Level up! Player's level is now", self.level)

class Enemy:
    def __init__(self, x, y):
        self.health = 1
        self.x = x
        self.y = y

class Boss:
    def __init__(self, x, y):
        self.health = 10
        self.x = x
        self.y = y

class Game:
    def __init__(self, map_size):
        self.player = Player()
        self.map_size = map_size
        self.map = [["-" for _ in range(map_size)] for _ in range(map_size)]
        self.player_position = (0, 0)
        self.enemies = []
        self.boss = None
        self.generate_enemies()
        self.generate_boss()

    def generate_enemies(self):
        for _ in range(self.map_size // 2):
            x = random.randint(0, self.map_size - 1)
            y = random.randint(0, self.map_size - 1)
            enemy = Enemy(x, y)
            self.enemies.append(enemy)

    def generate_boss(self):
        x = random.randint(0, self.map_size - 1)
        y = random.randint(0, self.map_size - 1)
        self.boss = Boss(x, y)

    def print_map(self):
        for i in range(self.map_size):
            for j in range(self.map_size):
                if (i, j) == self.player_position:
                    print("P", end=" ")
                elif any(enemy.x == i and enemy.y == j for enemy in self.enemies):
                    print("E", end=" ")
                elif self.boss and self.boss.x == i and self.boss.y == j:
                    print("B", end=" ")
                else:
                    print(self.map[i][j], end=" ")
            print()

    def move_player(self, direction):
        x, y = self.player_position
        if direction == "w" and x > 0:
            self.map[x][y] = "-"
            x -= 1
        elif direction == "s" and x < self.map_size - 1:
            self.map[x][y] = "-"
            x += 1
        elif direction == "a" and y > 0:
            self.map[x][y] = "-"
            y -= 1
        elif direction == "d" and y < self.map_size - 1:
            self.map[x][y] = "-"
            y += 1

        self.player_position = (x, y)
        self.map[x][y] = "P"

        self.check_encounter()

    def check_encounter(self):
        x, y = self.player_position

        for enemy in self.enemies:
            if enemy.x == x and enemy.y == y:
                print("Enemy encountered!")
                self.attack_enemy(enemy)

        if self.boss and self.boss.x == x and self.boss.y == y:
            print("Boss encountered!")
            self.attack_boss()

    def attack_enemy(self, enemy):
        while enemy.health > 0 and self.player.health > 0:
            command = input("Press space to attack: ")
            if command == " ":
                enemy.health -= self.player.attack_power
                if enemy.health > 0:
                    print("Enemy's health:", enemy.health)
                    self.player.health -= 1
                    print("Player's health:", self.player.health)
                else:
                    print("Enemy defeated!")
                    self.map[enemy.x][enemy.y] = "-"
                    self.enemies.remove(enemy)
                    self.player.level_up()
                    break
            else:
                print("Invalid command!")

        if self.player.health == 0:
            print("Game over!")

    def attack_boss(self):
        attack_count = 0
        while attack_count < 10 and self.boss and self.boss.health > 0 and self.player.health > 0:
            command = input("Press space to attack: ")
            if command == " ":
                self.boss.health -= self.player.attack_power
                attack_count += 1
                if self.boss.health > 0:
                    print("Boss's health:", self.boss.health)
                    self.player.health -= 1
                    print("Player's health:", self.player.health)
                else:
                    print("Boss defeated!")
                    self.map[self.boss.x][self.boss.y] = "-"
                    self.boss = None
                    print("Game cleared!")
                    break
            else:
                print("Invalid command!")

        if attack_count >= 10 and self.player.health > 0:
            print("Boss cannot be defeated!")

    def level_up(self):
        self.player.level += 1
        self.player.attack_power += 1
        print("Level up! Player's level is now", self.player.level)

map_size = 5  # マップサイズを設定
game = Game(map_size)

while game.player.health > 0 and game.boss:
    game.print_map()
    command = input("Press 'w' to move up, 's' to move down, 'a' to move left, 'd' to move right: ")
    if command in ["w", "s", "a", "d"]:
        game.move_player(command)
    else:
        print("Invalid command!")
