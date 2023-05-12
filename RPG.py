import random

class Player:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.health = 5
        self.attack_power = 1

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def attack(self, enemy):
        enemy.take_damage(self.attack_power)

    def take_damage(self, damage):
        self.health -= damage

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.health = 2
        self.attack_power = 1

    def attack(self, player):
        player.take_damage(self.attack_power)

    def take_damage(self, damage):
        self.health -= damage

class Game:
    def __init__(self, map_size):
        self.map_size = map_size
        self.map = self.generate_map()
        self.player = Player()
        self.enemies = self.generate_enemies()
        self.game_over = False

    def generate_map(self):
        map = [["-" for _ in range(self.map_size)] for _ in range(self.map_size)]
        return map

    def print_map(self):
        for row in self.map:
            print(" ".join(row))

    def generate_enemies(self):
        enemies = []
        for _ in range(5):
            x = random.randint(0, self.map_size - 1)
            y = random.randint(0, self.map_size - 1)
            enemy = Enemy(x, y)
            enemies.append(enemy)
        return enemies

    def move_player(self, dx, dy):
        new_x = self.player.x + dx
        new_y = self.player.y + dy

        if self.is_valid_move(new_x, new_y):
            self.map[self.player.x][self.player.y] = "-"
            self.player.move(dx, dy)
            self.map[self.player.x][self.player.y] = "P"

    def is_valid_move(self, x, y):
        return 0 <= x < self.map_size and 0 <= y < self.map_size

    def encounter_enemy(self):
        for enemy in self.enemies:
            if enemy.x == self.player.x and enemy.y == self.player.y:
                self.battle(enemy)
                break

    def battle(self, enemy):
        print("Encountered an enemy!")
        print(f"Player HP: {self.player.health}")
        print(f"Enemy HP: {enemy.health}")

        while self.player.health > 0 and enemy.health > 0:
            command = input("Enter 'a' to attack or 'd' to defend: ")
            if command == "a":
                self.player.attack(enemy)
                if enemy.health > 0:
                    enemy.attack(self.player)
            elif command == "d":
                enemy.attack(self.player)
            else:
                print("Invalid command!")

            print(f"Player HP: {self.player.health}")
            print(f"Enemy HP: {enemy.health}")

        if self.player.health <= 0:
            self.game_over = True
            print("Game Over!")
        else:
            self.enemies.remove(enemy)
            print("Enemy defeated!")

    def run_game(self):
        while not self.game_over:
            self.print_map()
            self.encounter_enemy()
            command = input("Enter 'w' to move up, 's' to move down, 'a' to move left, 'd' to move right: ")
            if command == "w":
                self.move_player(-1, 0)
            elif command == "s":
                self.move_player(1, 0)
            elif command == "a":
                self.move_player(0, -1)
            elif command == "d":
                self.move_player(0, 1)
            else:
                print("Invalid command!")

            print()  # 改行

    def play_game(self):
        print("Game Start!")
        self.run_game()
        print("Game Over")


# ゲームの開始
map_size = 10  # マップサイズを設定
game = Game(map_size)
game.run_game()
