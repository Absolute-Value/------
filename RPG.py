import random

class Player:
    def __init__(self, x, y, game_map):
        self.x = x
        self.y = y
        self.health = 5
        self.attack_power = 1
        self.defense_power = 1
        self.game_map = game_map

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def attack(self, enemy):
        enemy.health -= self.attack_power
        print(f"You attacked the enemy and dealt {self.attack_power} damage.")

    def defend(self):
        pass

    def take_damage(self, damage):
        self.health -= damage

class Enemy:
    def __init__(self, x, y, health=2, attack_power=1):
        self.x = x
        self.y = y
        self.health = health
        self.attack_power = attack_power

    def attack(self, player):
        player.take_damage(self.attack_power)

    def take_damage(self, damage):
        self.health -= damage

class Game:
    def __init__(self, map_size):
        self.map_size = map_size
        self.map = self.generate_map()
        self.player = Player(0, 0, self.map)  # プレイヤーの初期位置を設定
        self.enemies_positions = self.generate_enemies_positions()
        self.enemies = self.generate_enemies()
        self.game_over = False

        # プレイヤーと敵の位置をマップに反映する
        self.map[self.player.y][self.player.x] = "P"
        for enemy in self.enemies:
            self.map[enemy.y][enemy.x] = "E"

    def get_random_empty_position(self):
        while True:
            x = random.randint(0, self.map_size - 1)
            y = random.randint(0, self.map_size - 1)
            if self.map[x][y] == "-":
                return x, y

    def generate_map(self):
        map = [["-" for _ in range(self.map_size)] for _ in range(self.map_size)]
        return map

    def generate_enemies_positions(self):
        positions = []
        for _ in range(self.map_size):
            x = random.randint(0, self.map_size - 1)
            y = random.randint(0, self.map_size - 1)
            positions.append((x, y))
        return positions

    def generate_enemies(self):
        enemies = []
        for _ in range(len(self.enemies_positions)):
            x, y = self.enemies_positions[_]
            enemy = Enemy(x, y, 2, 1)  # 体力: 2, 攻撃力: 1
            enemies.append(enemy)
        return enemies

    def print_map(self):
        for row in self.map:
            print(" ".join(row))
        print("")

    def move_player(self, command):
        if command == "w":
            self.player.move(0, -1)
        elif command == "s":
            self.player.move(0, 1)
        elif command == "a":
            self.player.move(-1, 0)
        elif command == "d":
            self.player.move(1, 0)

    def encounter_enemy(self):
        x = self.player.x
        y = self.player.y

        for enemy in self.enemies:
            if enemy.x == x and enemy.y == y:
                print("Encountered an enemy!")
                self.battle(enemy)

    def battle(self, enemy):
        while self.player.health > 0 and enemy.health > 0:
            self.print_map()
            print("Player HP:", self.player.health)
            print("Enemy HP:", enemy.health)

            # プレイヤーのターン
            print("Player's turn:")
            command = input("Enter 'a' for attack or 'd' for defense: ")
            if command == "a":
                self.player.attack(enemy)
            elif command == "d":
                self.player.defend()
            else:
                print("Invalid command!")

            # 敵のターン
            print("Enemy's turn:")
            enemy.attack(self.player)

        if self.player.health <= 0:
            print("Player defeated! Game over.")
            self.game_over = True
        else:
            print("Enemy defeated!")
            self.enemies.remove(enemy)
            self.map[enemy.x][enemy.y] = "-"  # マップ上から敵を削除

    def run_game(self):
        while not self.game_over:
            self.print_map()
            command = input("Enter your command (w/a/s/d): ")
            self.move_player(command)
            self.encounter_enemy()


game = Game(5)  # 5x5のマップを作成
game.run_game()