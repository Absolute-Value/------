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
            x, y = self.get_random_empty_position()
            positions.append((x, y))
        return positions

    def generate_enemies(self):
        enemies = []
        for position in self.enemies_positions:
            x, y = position
            enemy = Enemy(x, y, 2, 1)  # 体力: 2, 攻撃力: 1
            enemies.append(enemy)
        return enemies

    def print_map(self):
        for row in self.map:
            print(" ".join(row))
        print("")

    def move_player(self, command):
        if command == "w":
            dx, dy = 0, -1
        elif command == "s":
            dx, dy = 0, 1
        elif command == "a":
            dx, dy = -1, 0
        elif command == "d":
            dx, dy = 1, 0
        else:
            print("Invalid command!")
            return

        new_x = self.player.x + dx
        new_y = self.player.y + dy

        # 移動先がマップ内かどうかをチェック
        if 0 <= new_x < self.map_size and 0 <= new_y < self.map_size:
            if self.map[new_y][new_x] == "-":
                # 移動先が空白の場合、プレイヤーを移動させる
                self.map[self.player.y][self.player.x] = "-"  # 元の位置を空白に戻す
                self.player.move(dx, dy)
                self.map[self.player.y][self.player.x] = "P"  # 移動後の位置にプレイヤーを表示
                self.encounter_enemy(self.player.x, self.player.y)  # 新しい位置に敵がいるかチェック
            elif self.map[new_y][new_x] == "E":
                # 移動先に敵がいる場合、バトルを開始する
                self.encounter_enemy(new_x, new_y)
            else:
                print("You can't move there. Try again.")
        else:
            print("You can't move there. Try again.")


    def encounter_enemy(self, x, y):
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
            self.encounter_enemy(self.player.x, self.player.y)

game = Game(5)  # 5x5のマップを作成
game.run_game()