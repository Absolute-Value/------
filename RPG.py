import random
import pygame
from pygame.locals import *

# ウィンドウのサイズ
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600

# マップのセルのサイズと色
CELL_SIZE = 60
BLACK_COLOR = (0, 0, 0)
WHITE_COLOR = (255, 255, 255)

class Player:
    def __init__(self, x, y, game_map):
        self.x = x
        self.y = y
        self.health = 5
        self.max_health = 5
        self.attack_power = 1
        self.defense = False
        self.level = 1
        self.experience = 0
        self.experience_to_level_up = 20
        self.game_map = game_map
        self.game_map[self.y][self.x] = "P"

    def encounter_enemy(self, x, y):
        for enemy in self.enemies:
            if enemy.x == x and enemy.y == y:
                print("Encountered an enemy!")
                self.battle(enemy)

    def attack(self, enemy):
        enemy.health -= self.attack_power
        return f"Attacked {self.attack_power}"

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            print("Player defeated! Game over.")
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
        print(f"Player leveled up!({self.level-1}->{self.level}) ")
        print("HP increased and fully healed.")

class Enemy:
    def __init__(self, x, y, health=2, attack_power=1):
        self.x = x
        self.y = y
        self.health = health
        self.attack_power = attack_power

    def attack(self, player):
        if player.defense:
            return "Player defended the attack!"
        else:
            player.take_damage(self.attack_power)
            return f"Damaged {self.attack_power}"

    def take_damage(self, damage):
        self.health -= damage

class Boss(Enemy):
    def __init__(self, x, y, health=5, attack_power=3):
        super().__init__(x, y, health, attack_power)

class Game:
    def __init__(self, map_size):
        self.map_size = map_size
        self.map = self.generate_map()
        self.player = Player(0, 0, self.map)
        self.enemies_positions = self.generate_enemies_positions()
        self.boss_position = random.choice(self.enemies_positions)
        self.enemies = self.generate_enemies()
        self.game_over = False
        pygame.init()
        # ゲームウィンドウの作成
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Battle Game')

        self.map[self.player.y][self.player.x] = "P"
        for enemy in self.enemies:
            self.map[enemy.y][enemy.x] = "E"
        self.map[self.boss_position[1]][self.boss_position[0]] = "B"  # ボスの位置をマップに反映

        # 使用する画像を読み込んでおく
        self.bg_image = pygame.transform.scale(pygame.image.load("bg.png"), (CELL_SIZE, CELL_SIZE)) # 画像を読み込みリサイズ
        self.player_image = pygame.transform.scale(pygame.image.load("player.png"), (CELL_SIZE, CELL_SIZE)) # 画像を読み込みリサイズ
        self.enemy_image = pygame.transform.scale(pygame.image.load("enemy.png"), (CELL_SIZE, CELL_SIZE)) # 画像を読み込みリサイズ
        self.boss_image = pygame.transform.scale(pygame.image.load("boss.png"), (CELL_SIZE, CELL_SIZE)) # 画像を読み込みリサイズ
        
    def get_random_empty_position(self):
        while True:
            x = random.randint(0, self.map_size - 1)
            y = random.randint(0, self.map_size - 1)
            if self.map[y][x] == "-":
                return x, y

    def generate_enemies_positions(self):
        positions = []
        for _ in range(self.map_size):  # 敵の位置を生成
            x, y = self.get_random_empty_position()
            positions.append((x, y))
        return positions

    def generate_map(self):
        map = [["-" for _ in range(self.map_size)] for _ in range(self.map_size)]
        return map

    def generate_enemies(self):
        enemies = []
        for position in self.enemies_positions:
            x, y = position
            if position == self.boss_position:
                enemy = Boss(x, y, 5, 3)  # BossのHP: 5, 攻撃力: 5
            else:
                enemy = Enemy(x, y, 2, 1)  # 通常の敵のHP: 2, 攻撃力: 1
            enemies.append(enemy)
        return enemies

    def print_map(self):
        for y, map_row in enumerate(self.map):
            for x, map_tile in enumerate(map_row):
                cell_rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                self.window.blit(self.bg_image, cell_rect) # 画像をブリット
                if map_tile == "P":
                    self.window.blit(self.player_image, cell_rect) # プレイヤー画像をブリット
                elif map_tile == "E":
                    self.window.blit(self.enemy_image, cell_rect) # 画像をブリット
                elif map_tile == "B":
                    self.window.blit(self.boss_image, cell_rect) # 画像をブリット
                
        pygame.display.flip()

    def player_move(self, dx, dy):
        new_x = self.player.x + dx
        new_y = self.player.y + dy

        if (
            new_x >= 0
            and new_x < self.map_size
            and new_y >= 0
            and new_y < self.map_size
        ):
            if self.map[new_y][new_x] == "E" or self.map[new_y][new_x] == "B":
                # 敵がいる場合、バトルを開始する
                self.encounter_enemy(new_x, new_y)
            self.map[self.player.y][self.player.x] = "-"
            self.player.x = new_x
            self.player.y = new_y
            self.map[self.player.y][self.player.x] = "P"
        else:
            print("You can't move there. Try again.")


    def encounter_enemy(self, x, y):
        for enemy in self.enemies:
            if enemy.x == x and enemy.y == y:
                self.battle(enemy)

    def battle(self, enemy):
        self.current_enemy = enemy
        self.states = ["Battle start !"]
        while self.player.health > 0 and enemy.health > 0:
            self.print_map()
            self.print_battle()

            pygame.display.update()

            # プレイヤーのターン
            self.player.defense = False
            command_entered = False
            while not command_entered:
                for event in pygame.event.get():
                    if event.type == KEYDOWN:
                        pygame.event.clear()
                        self.states = []
                        if event.key == K_1:
                            self.states.append(self.player.attack(enemy))
                            command_entered = True
                        elif event.key == K_2:
                            self.player.defense = True
                            command_entered = True

            # 敵のターン
            self.states.append(enemy.attack(self.player))

        if self.player.health <= 0:
            pygame.display.update()
            self.game_over = True
        else:
            self.player.gain_experience(10)
            self.enemies.remove(enemy)
            self.map[enemy.y][enemy.x] = "-"  # マップ上から敵を削除
            self.states.append("Killed")
            # pygame.display.update()

    def print_battle(self):
        # status
        status_left = WINDOW_WIDTH // 10
        status_top = WINDOW_HEIGHT // 10
        status_width = WINDOW_WIDTH // 5
        status_height = WINDOW_WIDTH // 4
        pygame.draw.rect(self.window, BLACK_COLOR, pygame.Rect(status_left, status_top, status_width, status_height))
        pygame.draw.rect(self.window, WHITE_COLOR, pygame.Rect(status_left, status_top, status_width, status_height), 4)
        pygame.draw.rect(self.window, BLACK_COLOR, pygame.Rect(status_left, status_top, status_width, status_height), 2)
        status_text = [
            f"Lv: {self.player.level} ({self.player.experience}/{self.player.experience_to_level_up})",
            f"HP: {self.player.health}/{self.player.max_health}",
            f"E : {self.player.experience}"
        ]
        for i, text in enumerate(status_text):
            self.draw_text(text, status_left + 10, status_top + 10 + i * 20, color=WHITE_COLOR)

        # command
        command_left = WINDOW_WIDTH // 5 * 2
        command_top = WINDOW_HEIGHT // 12
        command_width = WINDOW_WIDTH // 2
        command_height = WINDOW_HEIGHT // 8
        pygame.draw.rect(self.window, BLACK_COLOR, pygame.Rect(command_left, command_top, command_width, command_height))
        pygame.draw.rect(self.window, WHITE_COLOR, pygame.Rect(command_left, command_top, command_width, command_height), 4)
        pygame.draw.rect(self.window, BLACK_COLOR, pygame.Rect(command_left, command_top, command_width, command_height), 2)
        status_text = [
            f"1 Attack",
            f"2 Defence"
        ]
        for i, text in enumerate(status_text):
            self.draw_text(text, command_left + 15, command_top + 15 + i * 20, color=WHITE_COLOR)

        # state
        state_left = WINDOW_WIDTH // 6
        state_top = WINDOW_HEIGHT // 5 * 3
        state_width = WINDOW_WIDTH // 3 * 2
        state_height = WINDOW_HEIGHT // 3
        pygame.draw.rect(self.window, BLACK_COLOR, pygame.Rect(state_left, state_top, state_width, state_height))
        pygame.draw.rect(self.window, WHITE_COLOR, pygame.Rect(state_left, state_top, state_width, state_height), 4)
        pygame.draw.rect(self.window, BLACK_COLOR, pygame.Rect(state_left, state_top, state_width, state_height), 2)
        for i, text in enumerate(self.states):
            self.draw_text(text, state_left + 15, state_top + 15 + i * 20, color=WHITE_COLOR)


    def draw_text(self, text, x, y, font_size=24, color=(0, 0, 0)):
        font = pygame.font.Font(None, font_size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y)
        self.window.blit(text_surface, text_rect)

    def run_game(self):
        while not self.game_over:
            self.handle_events()
            self.print_map()
            pygame.display.update()

        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.game_over = True

            if event.type == KEYDOWN:
                pygame.event.clear()
                if event.key == K_ESCAPE:
                    self.game_over = True
                if event.key == K_UP:
                    self.player_move(0, -1)
                if event.key == K_DOWN:
                    self.player_move(0, 1)
                if event.key == K_LEFT:
                    self.player_move(-1, 0)
                if event.key == K_RIGHT:
                    self.player_move(1, 0)

game = Game(10)  # 10x10のマップを作成
game.run_game()
