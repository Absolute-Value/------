import random
import pygame
from pygame.locals import *
from enemies import *
from player import Player

# マップのセルのサイズと色
BLACK_COLOR = (0, 0, 0)
WHITE_COLOR = (255, 255, 255)

class Game:
    def __init__(self, map_size=(12,10), cell_size=60, enemy_num=16): # 12x10のマップを作成
        self.map_size = map_size
        self.map = self.generate_map()
        self.player = Player(0, 0, self.map)
        self.enemies_positions = self.generate_enemies_positions(enemy_num=enemy_num)
        self.boss_position = random.choice(self.enemies_positions)
        self.enemies = self.generate_enemies()
        self.game_over = False
        
        self.cell_size = cell_size
        self.window_size = [m * cell_size for m in map_size]
        pygame.init()
        # ゲームウィンドウの作成
        self.window = pygame.display.set_mode((self.window_size[0], self.window_size[1]))
        pygame.display.set_caption('RPG Game')

        self.map[self.player.y][self.player.x] = "P"
        for enemy in self.enemies:
            self.map[enemy.y][enemy.x] = "E"
        self.map[self.boss_position[1]][self.boss_position[0]] = "B"  # ボスの位置をマップに反映

        # 使用する画像を読み込んでおく
        self.bg_image = pygame.transform.scale(pygame.image.load("images/bg.png"), (cell_size, cell_size)) # 画像を読み込みリサイズ
        self.player_image = pygame.transform.scale(pygame.image.load("images/player.png"), (cell_size, cell_size)) # 画像を読み込みリサイズ
        self.enemy_image = pygame.transform.scale(pygame.image.load("images/enemy.png"), (cell_size, cell_size)) # 画像を読み込みリサイズ
        self.boss_image = pygame.transform.scale(pygame.image.load("images/boss.png"), (cell_size, cell_size)) # 画像を読み込みリサイズ
        
    def get_random_empty_position(self):
        while True:
            x = random.randint(0, self.map_size[0] - 1)
            y = random.randint(0, self.map_size[1] - 1)
            if self.map[y][x] == "-":
                return x, y

    def generate_enemies_positions(self, enemy_num=16):
        positions = []
        for _ in range(enemy_num):  # 敵の位置を生成
            x, y = self.get_random_empty_position()
            positions.append((x, y))
        return positions

    def generate_map(self):
        map = [["-" for _ in range(self.map_size[0])] for _ in range(self.map_size[1])]
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
                cell_rect = pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
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

        if (new_x >= 0 and new_x < self.map_size[0] and new_y >= 0 and new_y < self.map_size[1]):
            if self.map[new_y][new_x] == "E" or self.map[new_y][new_x] == "B":
                # 敵がいる場合、バトルを開始する
                self.encounter_enemy(new_x, new_y)
            self.map[self.player.y][self.player.x] = "-"
            self.player.x = new_x
            self.player.y = new_y
            self.map[self.player.y][self.player.x] = "P"
        else:
            print("You can't move there . Try again .")


    def encounter_enemy(self, x, y):
        for enemy in self.enemies:
            if enemy.x == x and enemy.y == y:
                self.battle(enemy)

    def battle(self, enemy):
        self.current_enemy = enemy
        self.states = [f"{enemy.name} showed up !"]
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
                        if event.key == K_n:
                            self.states.append(self.player.attack(enemy))
                            command_entered = True
                        elif event.key == K_m:
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
            self.states.append(f"Player killed {enemy.name} .")
            # pygame.display.update()

    def print_battle(self):
        # status
        status_pos = (self.window_size[0] // 10, self.window_size[1] // 10)
        status_size = (self.window_size[0] // 5, self.window_size[0] // 4)
        pygame.draw.rect(self.window, BLACK_COLOR, pygame.Rect(status_pos[0], status_pos[1], status_size[0], status_size[1]))
        pygame.draw.rect(self.window, WHITE_COLOR, pygame.Rect(status_pos[0], status_pos[1], status_size[0], status_size[1]), 4)
        pygame.draw.rect(self.window, BLACK_COLOR, pygame.Rect(status_pos[0], status_pos[1], status_size[0], status_size[1]), 2)
        status_text = [
            f"Lv.: {self.player.level}",
            f"HP : {self.player.health}/{self.player.max_health}",
            f"Exp: {self.player.experience}/{self.player.experience_to_level_up}"
        ]
        for i, text in enumerate(status_text):
            self.draw_text(text, status_pos[0] + 10, status_pos[1] + 10 + i * 24, color=WHITE_COLOR)

        # command
        command_pos = (self.window_size[0] // 5 * 2, self.window_size[1] // 12)
        command_size = (self.window_size[0] // 2, self.window_size[1] // 8)
        pygame.draw.rect(self.window, BLACK_COLOR, pygame.Rect(command_pos[0], command_pos[1], command_size[0], command_size[1]))
        pygame.draw.rect(self.window, WHITE_COLOR, pygame.Rect(command_pos[0], command_pos[1], command_size[0], command_size[1]), 4)
        pygame.draw.rect(self.window, BLACK_COLOR, pygame.Rect(command_pos[0], command_pos[1], command_size[0], command_size[1]), 2)
        status_text = [
            f"n Attack",
            f"m Defence"
        ]
        for i, text in enumerate(status_text):
            self.draw_text(text, command_pos[0] + 15, command_pos[1] + 15 + i * 24, color=WHITE_COLOR)

        # state
        state_pos = (self.window_size[0] // 6, self.window_size[1] // 5 * 3)
        state_size = (self.window_size[0] // 3 * 2, self.window_size[1] // 3)
        pygame.draw.rect(self.window, BLACK_COLOR, pygame.Rect(state_pos[0], state_pos[1], state_size[0], state_size[1]))
        pygame.draw.rect(self.window, WHITE_COLOR, pygame.Rect(state_pos[0], state_pos[1], state_size[0], state_size[1]), 4)
        pygame.draw.rect(self.window, BLACK_COLOR, pygame.Rect(state_pos[0], state_pos[1], state_size[0], state_size[1]), 2)
        for i, text in enumerate(self.states):
            self.draw_text(text, state_pos[0] + 15, state_pos[1] + 15 + i * 24, color=WHITE_COLOR)


    def draw_text(self, text, x, y, font_size=36, color=(0, 0, 0)):
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
                if event.key == K_w:
                    self.player_move(0, -1)
                if event.key == K_s:
                    self.player_move(0, 1)
                if event.key == K_a:
                    self.player_move(-1, 0)
                if event.key == K_d:
                    self.player_move(1, 0)

game = Game()
game.run_game()
