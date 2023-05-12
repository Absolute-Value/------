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
                    self.enemies.append((x, y))
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
        self.attack_enemy(x, y)

    def attack_enemy(self, x, y):
        enemy_index = self.enemies.index((x, y))
        enemy = self.enemies.pop(enemy_index)

        while True:
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

    def physical_attack(self, enemy):
        self.map[enemy[0]][enemy[1]] = '-'
        print("You defeated an enemy!")
        self.player.level_up()

    def defend(self):
        print("You defended against the enemy's attack!")
        # Apply any defensive effects or calculations here

    def magic_attack(self, enemy):
        print("Magic attack against an enemy is not implemented yet!")

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

    def game_over(self):
        print("Game Over")
        self.game_over = True

# ゲームの開始
map_size = 10  # マップサイズを設定
game = Game(map_size)
game.run_game()
