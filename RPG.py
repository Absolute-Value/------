import random

class Player:
    def __init__(self):
        self.health = 5
        self.attack_power = 1
        self.level = 1

    def level_up(self):
        self.level += 1
        self.attack_power += 1
        print("Level Up! Your attack power increased to", self.attack_power)

    def attack(self, enemy):
        print("Player attacks the enemy!")
        enemy.health -= self.attack_power

    def is_defeated(self):
        return self.health <= 0


class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.health = 2

    def attack(self, player):
        print("Enemy attacks the player!")
        player.health -= 1

    def is_defeated(self):
        return self.health <= 0


class Game:
    def __init__(self, map_size):
        self.map_size = map_size
        self.map = [['-' for _ in range(self.map_size)] for _ in range(self.map_size)]
        self.player = Player()
        self.player_position = None
        self.enemies = []
        self.place_entities()
        self.game_over = False

    def place_entities(self):
        self.place_player()
        self.place_enemies()

    def place_player(self):
        x = random.randint(0, self.map_size - 1)
        y = random.randint(0, self.map_size - 1)
        self.player_position = (x, y)
        self.map[x][y] = 'P'

    def place_enemies(self):
        for _ in range(5):
            while True:
                x = random.randint(0, self.map_size - 1)
                y = random.randint(0, self.map_size - 1)
                if self.map[x][y] == '-':
                    self.map[x][y] = 'E'
                    self.enemies.append(Enemy(x, y))
                    break

    def print_map(self):
        for row in self.map:
            print(' '.join(row))

    def move_player(self, direction):
        x, y = self.player_position

        if direction == 'w' and x > 0:
            x -= 1
        elif direction == 's' and x < self.map_size - 1:
            x += 1
        elif direction == 'a' and y > 0:
            y -= 1
        elif direction == 'd' and y < self.map_size - 1:
            y += 1

        if self.map[x][y] == 'E':
            self.encounter_enemy(x, y)
        elif self.map[x][y] == '-':
            self.map[self.player_position[0]][self.player_position[1]] = '-'
            self.player_position = (x, y)
            self.map[x][y] = 'P'

    def encounter_enemy(self, x, y):
        print("Enemy encountered!")
        enemy = self.get_enemy_at(x, y)
        self.attack_enemy(enemy)
        if not enemy.is_defeated():
            self.attack_player(enemy)

    def get_enemy_at(self, x, y):
        for enemy in self.enemies:
            if enemy.x == x and enemy.y == y:
                return enemy
        return None

    def attack_enemy(self, enemy):
        self.player.attack(enemy)
        if enemy.is_defeated():
            self.defeat_enemy(enemy)

    def defeat_enemy(self, enemy):
        self.map[enemy.x][enemy.y] = '-'
        self.enemies.remove(enemy)
        print("You defeated an enemy!")
        if enemy.x == self.player_position[0] and enemy.y == self.player_position[1]:
            self.map[self.player_position[0]][self.player_position[1]] = '-'

    def attack_player(self, enemy):
        if enemy.x == self.player_position[0]:
            if enemy.y < self.player_position[1]:
                self.player.attack(enemy)
            else:
                self.attack_player_from_behind(enemy)
        elif enemy.y == self.player_position[1]:
            if enemy.x < self.player_position[0]:
                self.player.attack(enemy)
            else:
                self.attack_player_from_behind(enemy)

    def attack_player_from_behind(self, enemy):
        print("Enemy attacks the player from behind!")
        self.player.health -= 1

    def run_game(self):
        while not self.game_over:
            self.print_map()
            command = input("Press 'w' to move up, 's' to move down, 'a' to move left, 'd' to move right: ")
            if command in ["w", "s", "a", "d"]:
                self.move_player(command)
            else:
                print("Invalid command!")

            if not self.enemies:
                self.game_over = True
            elif self.player.is_defeated():
                self.game_over()

        if self.game_over:
            print("Congratulations! You cleared the game!")
        else:
            print("Game Over")

# ゲームの開始
map_size = 10  # マップサイズを設定
game = Game(map_size)
game.run_game()
