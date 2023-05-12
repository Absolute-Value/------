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

    def move(self, player_position):
        dx = player_position[0] - self.x
        dy = player_position[1] - self.y

        if dx != 0:
            self.x += dx // abs(dx)
        if dy != 0:
            self.y += dy // abs(dy)

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
        self.place_entities()

    def generate_enemies(self):
        for _ in range(5):
            while True:
                x = random.randint(0, self.map_size - 1)
                y = random.randint(0, self.map_size - 1)
                if self.map[x][y] == "-" and (x, y) != self.player_position:
                    enemy = Enemy(x, y)
                    self.enemies.append(enemy)
                    break

    def generate_boss(self):
        while True:
            x = random.randint(0, self.map_size - 1)
            y = random.randint(0, self.map_size - 1)
            if self.map[x][y] == "-" and (x, y) != self.player_position:
                self.boss = Boss(x, y)
                break

    def place_entities(self):
        self.map[self.player_position[0]][self.player_position[1]] = "P"
        for enemy in self.enemies:
            self.map[enemy.x][enemy.y] = "E"
        if self.boss:
            self.map[self.boss.x][self.boss.y] = "B"

    def print_map(self):
        for i in range(self.map_size):
            for j in range(self.map_size):
                print(self.map[i][j], end=" ")
            print()
        print("Player HP:", self.player.health)
        print("Player Level:", self.player.level)

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

        # Check if the player encounters an enemy
        for enemy in self.enemies:
            if enemy.x == x and enemy.y == y:
                self.attack_enemy(enemy)
                break

        # Check if the player encounters the boss
        if self.boss and self.boss.x == x and self.boss.y == y:
            self.attack_boss()

    def attack_enemy(self, enemy):
        while True:
            print("Enemy encountered!")
            print("1. Physical Attack")
            print("2. Defend")
            print("3. Magic Attack")
            choice = input("Choose your action (1-3): ")
            if choice == "1":
                self.physical_attack(enemy)
                break
            elif choice == "2":
                self.defend()
                break
            elif choice == "3":
                self.magic_attack(enemy)
                break
            else:
                print("Invalid choice! Please try again.")

    def attack_boss(self):
        while True:
            print("Boss encountered!")
            print("1. Physical Attack")
            print("2. Defend")
            print("3. Magic Attack")
            choice = input("Choose your action (1-3): ")
            if choice == "1":
                self.physical_attack_boss()
                break
            elif choice == "2":
                self.defend()
                break
            elif choice == "3":
                self.magic_attack_boss()
                break
            else:
                print("Invalid choice! Please try again.")

    def physical_attack(self, enemy):
        enemy.health -= self.player.attack_power

        if enemy.health <= 0:
            self.enemies.remove(enemy)
            print("You defeated an enemy!")
            self.player.level_up()
        else:
            print("You attacked an enemy. Enemy's health:", enemy.health)

    def physical_attack_boss(self):
        self.boss.health -= self.player.attack_power

        if self.boss.health <= 0:
            print("Congratulations! You defeated the boss!")
            self.player.level_up()
        else:
            print("You attacked the boss. Boss's health:", self.boss.health)

    def defend(self):
        print("You defended against the enemy's attack!")
        # Apply any defensive effects or calculations here

    def magic_attack(self, enemy):
        # Implement the logic for magic attack against an enemy here
        print("Magic attack against an enemy is not implemented yet!")

    def magic_attack_boss(self):
        # Implement the logic for magic attack against the boss here
        print("Magic attack against the boss is not implemented yet!")

    def attack_boss(self):
        self.boss.health -= self.player.attack_power

        if self.boss.health <= 0:
            print("Congratulations! You defeated the boss!")
            self.player.level_up()
        else:
            print("You attacked the boss. Boss's health:", self.boss.health)

map_size = 5  # マップサイズを設定
game = Game(map_size)

while game.player.health > 0 and game.boss:
    game.print_map()
    command = input("Press 'w' to move up, 's' to move down, 'a' to move left, 'd' to move right: ")
    if command in ["w", "s", "a", "d"]:
        game.move_player(command)
    else:
        print("Invalid command!")
