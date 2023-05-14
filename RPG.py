import random
import pygame
from pygame.locals import *
from entities import *
from player import Player
from define import *

class Game:
    def __init__(self):
        self.stage = INIT_STAGE
        self.map = MAP[self.stage]
        self.map_size = (len(self.map[0]), len(self.map))
        self.player = Player()
        self.init_entity_map()
        self.generate_enemies()
        self.game_over = False
        
        self.window_size = [m * CELL_SIZE for m in self.map_size]
        pygame.init()
        # ゲームウィンドウの作成
        self.window = pygame.display.set_mode((self.window_size[0], self.window_size[1]))
        pygame.display.set_caption('RPG Game')

        # 使用する画像を読み込んでおく
        self.heart_image = pygame.transform.scale(pygame.image.load("images/heart.png"), (CELL_SIZE, CELL_SIZE)) # 画像を読み込みリサイズ
        self.land_image = pygame.transform.scale(pygame.image.load("images/land.png"), (CELL_SIZE, CELL_SIZE)) # 画像を読み込みリサイズ
        self.tree_image = pygame.transform.scale(pygame.image.load("images/tree.png"), (CELL_SIZE, CELL_SIZE)) # 画像を読み込みリサイズ
        self.sea_image = pygame.transform.scale(pygame.image.load("images/sea.png"), (CELL_SIZE, CELL_SIZE)) # 画像を読み込みリサイズ
        self.player_image = pygame.transform.scale(pygame.image.load("images/player.png"), (CELL_SIZE, CELL_SIZE)) # 画像を読み込みリサイズ
        self.enemy_image = pygame.transform.scale(pygame.image.load("images/enemy.png"), (CELL_SIZE, CELL_SIZE)) # 画像を読み込みリサイズ
        self.boss_image = pygame.transform.scale(pygame.image.load("images/boss.png"), (CELL_SIZE, CELL_SIZE)) # 画像を読み込みリサイズ
        
    def init_entity_map(self):
        self.entity_map = [[0 for _ in range(self.map_size[0])] for _ in range(self.map_size[1])]
        self.entity_map[self.player.y][self.player.x] = 1
        
    def update_entity_map(self):
        for i, entity in enumerate(self.entities):
            self.entity_map[entity.y][entity.x] = i + 2
        
    def get_random_empty_position(self):
        while True:
            x = random.randint(0, self.map_size[0] - 1)
            y = random.randint(0, self.map_size[1] - 1)
            if self.entity_map[y][x] == 0 and self.map[y][x] == 0:
                return x, y
            
    def generate_enemies(self):
        self.entities = []
        for i in range(ENEMY_NUM):
            x, y = self.get_random_empty_position()
            self.entity_map[y][x] = i + 2
            if i == 0 and self.stage == (1,1):
                enemy = Enemy(x, y, "BoneKing", 5, 3, 30)  # BossのHP: 5, 攻撃力: 5
            else:
                enemy = Enemy(x, y, "Bone", 2, 1)  # 通常の敵のHP: 2, 攻撃力: 1
            self.entities.append(enemy)

    def print_map(self):
        for y, map_row in enumerate(self.map):
            for x, map_tile in enumerate(map_row):
                cell_rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                if map_tile == 4: # 海だったら
                    self.window.blit(self.sea_image, cell_rect) # 画像をブリット
                else:
                    self.window.blit(self.land_image, cell_rect) # 画像をブリット
                    if map_tile == 1: # 木だったら
                        self.window.blit(self.tree_image, cell_rect) # 画像をブリット
        
        cell_rect = pygame.Rect(self.player.x * CELL_SIZE, self.player.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        self.window.blit(self.player_image, cell_rect) # プレイヤー画像をブリット
        
        for entity in self.entities:
            cell_rect = pygame.Rect(entity.x * CELL_SIZE, entity.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if entity.name == "heart":
                self.window.blit(self.heart_image, cell_rect) # 画像をブリット
            elif entity.name == "BoneKing":
                self.window.blit(self.boss_image, cell_rect) # 画像をブリット
            else:
                self.window.blit(self.enemy_image, cell_rect) # 画像をブリット

    def player_move(self, dx, dy):
        new_x = self.player.x + dx
        new_y = self.player.y + dy

        if (new_x < 0 and self.stage[1] > 1): # 左ステージへの移動
            self.stage = (self.stage[0], self.stage[1]-1)
            self.map = MAP[self.stage]
            self.player.x = self.map_size[0] - 1
            self.init_entity_map()
            self.generate_enemies()
        elif (new_x == self.map_size[0] and self.stage[1] < 2): # 右ステージへの移動
            self.stage = (self.stage[0], self.stage[1]+1)
            self.map = MAP[self.stage]
            self.player.x = 0
            self.init_entity_map()
            self.generate_enemies()
        elif (new_x >= 0 and new_x < self.map_size[0] and new_y >= 0 and new_y < self.map_size[1] and (self.map[new_y][new_x] == 0)):
            target = self.entity_map[new_y][new_x]
            if target > 1:
                entity = self.entities[target-2]
                if entity.name == "heart":
                    self.player.heal()
                    self.entities.remove(entity)
                    self.states = ["Player healed ."]
                    
                    self.print_map()
                    self.print_status()
                    self.print_states()
                    self.wait_input()
                    
                    self.init_entity_map()
                    self.update_entity_map()
                else: # 移動先に敵がいる場合、バトルを開始する
                    self.battle(entity)
            else:
                self.entity_map[self.player.y][self.player.x] = 0
                self.player.x = new_x
                self.player.y = new_y
                self.entity_map[self.player.y][self.player.x] = 1
            
        else:
            print("You can't move there . Try again .")

    def battle(self, enemy):
        self.states = [f"{enemy.name} showed up !"]
        while self.player.health > 0 and enemy.health > 0:
            self.print_map()
            self.print_battle(enemy)

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

            if enemy.health > 0: # 敵のターン
                self.states.append(enemy.attack(self.player))

        if self.player.health == 0:
            self.game_over = True
            self.states.extend([f"Player was killed by {enemy.name}", "Game Over"])
            
            self.print_map()
            self.print_battle(enemy)
            self.wait_input()
                            
        else:
            self.entities.remove(enemy)
            self.states.append(f"Player killed {enemy.name}")
            self.states.extend(self.player.gain_experience(enemy.exp))
            if random.random() < 0.2:
                self.entities.append(Entity(enemy.x, enemy.y, "heart"))
                self.states.append(f"{enemy.name} droped heart .")

            self.print_map()
            self.print_battle(enemy)
            self.wait_input()
            
            self.init_entity_map()
            self.update_entity_map()
            
    def wait_input(self):
        pygame.display.update()
            
        command_entered = False
        while not command_entered:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_n or event.key == K_m:
                        command_entered = True
        

    def print_status(self):
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
            
    def print_states(self):
        state_pos = (self.window_size[0] // 6, self.window_size[1] // 5 * 3)
        state_size = (self.window_size[0] // 3 * 2, self.window_size[1] // 3)
        pygame.draw.rect(self.window, BLACK_COLOR, pygame.Rect(state_pos[0], state_pos[1], state_size[0], state_size[1]))
        pygame.draw.rect(self.window, WHITE_COLOR, pygame.Rect(state_pos[0], state_pos[1], state_size[0], state_size[1]), 4)
        pygame.draw.rect(self.window, BLACK_COLOR, pygame.Rect(state_pos[0], state_pos[1], state_size[0], state_size[1]), 2)
        for i, text in enumerate(self.states):
            self.draw_text(text, state_pos[0] + 15, state_pos[1] + 15 + i * 24, color=WHITE_COLOR)
        
    def print_battle(self, enemy):
        # icon
        icon_size =(self.window_size[0] // 4, self.window_size[0] // 4)
        icon_pos = (self.window_size[0] // 2 - icon_size[0] // 2, self.window_size[1] // 2 - icon_size[1] // 1.5)
        pygame.draw.rect(self.window, BLACK_COLOR, pygame.Rect(icon_pos[0], icon_pos[1], icon_size[0], icon_size[1]))
        pygame.draw.rect(self.window, WHITE_COLOR, pygame.Rect(icon_pos[0], icon_pos[1], icon_size[0], icon_size[1]), 4)
        pygame.draw.rect(self.window, BLACK_COLOR, pygame.Rect(icon_pos[0], icon_pos[1], icon_size[0], icon_size[1]), 2)
        cell_rect = pygame.Rect(icon_pos[0]+5, icon_pos[1]+5, icon_size[0], icon_size[1])
        if enemy.name == "BoneKing":
            image = pygame.transform.scale(self.boss_image, (icon_size[0]-10, icon_size[1]-10)) # 画像リサイズ
        else:
            image = pygame.transform.scale(self.enemy_image, (icon_size[0]-10, icon_size[1]-10)) # 画像リサイズ
            
        self.window.blit(image, cell_rect) # 画像をブリット
        
        self.print_status()

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
            
        self.print_states()


    def draw_text(self, text, x, y, font_size=36, color=BLACK_COLOR):
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
