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
        self.generate_entities()
        self.game_over = False
        
        self.window_size = [m * CELL_SIZE for m in self.map_size]
        pygame.init()
        # ゲームウィンドウの作成
        self.window = pygame.display.set_mode((self.window_size[0], self.window_size[1]))
        pygame.display.set_caption('RPG Game')

        # 使用する画像を読み込んでおく
        self.potion_image = pygame.transform.scale(pygame.image.load("images/potion.png"), (CELL_SIZE, CELL_SIZE)) # 画像を読み込みリサイズ
        self.land_image = pygame.transform.scale(pygame.image.load("images/land.png"), (CELL_SIZE, CELL_SIZE)) # 画像を読み込みリサイズ
        self.tree_image = pygame.transform.scale(pygame.image.load("images/tree.png"), (CELL_SIZE, CELL_SIZE)) # 画像を読み込みリサイズ
        self.sea_image = pygame.transform.scale(pygame.image.load("images/sea.png"), (CELL_SIZE, CELL_SIZE)) # 画像を読み込みリサイズ
        self.player_image = pygame.transform.scale(pygame.image.load("images/player.png"), (CELL_SIZE, CELL_SIZE)) # 画像を読み込みリサイズ
        self.enemy_image = pygame.transform.scale(pygame.image.load("images/enemy.png"), (CELL_SIZE, CELL_SIZE)) # 画像を読み込みリサイズ
        self.boss_image = pygame.transform.scale(pygame.image.load("images/boss.png"), (CELL_SIZE, CELL_SIZE)) # 画像を読み込みリサイズ
        self.key_image = pygame.transform.scale(pygame.image.load("images/key.png"), (CELL_SIZE, CELL_SIZE)) # 画像を読み込みリサイズ
        
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
            
    def generate_entities(self):
        self.entities = []
        bias = 2
        if self.stage == (1,2):
            self.entities.append(Enemy(10, 5, "BoneKing", 10, 3, 5, escape_rate=0)) # BossのHP: 5, 攻撃力: 3, 経験値: 5
            self.entity_map[5][10] = bias
            bias += 1
        if self.stage == (1,3):
            self.entities.append(Entity(5, 3, "カギ"))
            self.entity_map[3][5] = bias
            bias += 1
        for i in range(ENEMY_NUM):
            x, y = self.get_random_empty_position()
            self.entities.append(Enemy(x, y, "Bone")) # 通常の敵のHP: 3, 攻撃力: 1
            self.entity_map[y][x] = i + bias

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
            if entity.name == "ポーション":
                self.window.blit(self.potion_image, cell_rect) # 画像をブリット
            elif entity.name == "カギ":
                self.window.blit(self.key_image, cell_rect) # 画像をブリット
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
            self.generate_entities()
        elif (new_x == self.map_size[0] and self.stage[1] < len(MAP)): # 右ステージへの移動
            self.stage = (self.stage[0], self.stage[1]+1)
            self.map = MAP[self.stage]
            self.player.x = 0
            self.init_entity_map()
            self.generate_entities()
        elif (new_x >= 0 and new_x < self.map_size[0] and new_y >= 0 and new_y < self.map_size[1] and (self.map[new_y][new_x] == 0)):
            target = self.entity_map[new_y][new_x]
            if target > 1:
                entity = self.entities[target-2]
                if entity.name in ["ポーション", "カギ"]:
                    
                    self.states = [f"{entity.name}を てにいれた！"]
                    self.entities.remove(entity)
                    if entity.name == "カギ":
                        self.player.inventory["カギ"] = 1
                    else:
                        if "ポーション" in self.player.inventory.keys():
                            self.player.inventory["ポーション"] += 1
                        else:
                            self.player.inventory["ポーション"] = 1
                            
                    self.command = list(self.player.inventory.keys())
                    self.selected_command = 0
                    self.print_map()
                    self.print_stats_and_command()
                    self.wait_input()
                    
                    self.init_entity_map()
                    self.update_entity_map()
                    
                else: # 移動先に敵がいる場合、バトルを開始する
                    self.battle(entity)
            else:
                self.entity_map[self.player.y][self.player.x] = 0
                self.player.x, self.player.y = new_x, new_y
                self.entity_map[self.player.y][self.player.x] = 1
            
        else:
            print("You can't move there . Try again .")

    def battle(self, enemy):
        self.states = [f"{enemy.name}が あらわれた！", "どうする？"]
        while self.player.health > 0 and enemy.health > 0:
            self.command = BATTLE_COMMAND
            self.selected_command = 0
            self.print_battle(enemy)

            # プレイヤーのターン
            command_entered = False
            open_inventory = False
            while not command_entered:
                for event in pygame.event.get():
                    if event.type == KEYDOWN:
                        if event.key == K_n:
                            if open_inventory:
                                item_name = self.command[self.selected_command]
                                if item_name == "ポーション":
                                    command_entered = True
                                    self.player.inventory[item_name] -= 1
                                    if self.player.inventory[item_name] == 0:
                                        del self.player.inventory[item_name]
                                    self.states = [f"{item_name}を つかった！"] + self.player.heal(3)
                                else:
                                    self.states = [f"ここでは つかえない！", "どうする？"]
                            else:
                                if self.selected_command == 0:
                                    self.states = []
                                    self.states.extend(self.player.attack(enemy))
                                    command_entered = True
                                elif self.selected_command == 1:
                                    self.states = [f"じゅもんを おぼえていない！", "どうする？"]
                                elif self.selected_command == 2:
                                    command_entered = True
                                    if random.random() < enemy.escape_rate:
                                        self.states = ["うまくにげられた！"]
                                    else:
                                        self.states = ["にげられなかった！"]
                                else:
                                    if len(self.player.inventory) == 0:
                                        self.states = [f"どうぐを もっていない！", "どうする？"]
                                    else:
                                        self.command = list(self.player.inventory.keys())
                                        self.selected_command = 0
                                        self.states = [f"{self.player.inventory[self.command[self.selected_command]]}こ"]
                                        open_inventory = True
                        elif event.key == K_m:
                            self.command = BATTLE_COMMAND
                            self.states = ["どうする？"]
                            open_inventory = False
                        elif event.key == K_w:
                            self.selected_command = max(0, self.selected_command - 1)
                            if open_inventory : self.states = [f"{self.player.inventory[self.command[self.selected_command]]}こ"]
                        elif event.key == K_s:
                            self.selected_command = min(len(self.command)-1, self.selected_command + 1)
                            if open_inventory : self.states = [f"{self.player.inventory[self.command[self.selected_command]]}こ"]
                            
                        self.print_battle(enemy)
                            
            if self.states == ["うまくにげられた！"]:
                break
            if enemy.health > 0: # 敵のターン
                self.wait_input()
                self.states = enemy.attack(self.player)
                if self.player.health > 0:
                    self.print_battle(enemy)
                    self.wait_input()
                    self.states = ["どうする？"]

        if self.player.health <= 0:
            self.game_over = True
            self.states.extend([f"プレイヤーは しんでしまった！"])
            self.print_battle(enemy)
            self.wait_input()
        elif enemy.health > 0:
            self.print_battle(enemy)
            self.wait_input()
        else:
            self.entities.remove(enemy)
            self.states.append(f"{enemy.name}を たおした！")
            self.states.extend(self.player.gain_experience(enemy.exp))
            if self.player.experience >= self.player.experience_to_level_up:
                self.print_map()
                self.print_battle(enemy)
                self.wait_input()
                self.states = self.player.level_up()
            if random.random() < 0.2:
                self.entities.append(Entity(enemy.x, enemy.y, "ポーション"))
                self.states.append(f"{enemy.name}は ポーションを おとした")

            self.print_map()
            self.print_battle(enemy)
            self.wait_input()
            
            self.init_entity_map()
            self.update_entity_map()
            
    def wait_input(self):
        command_entered = False
        while not command_entered:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_n or event.key == K_m:
                        command_entered = True
        

    def print_status(self):
        status_pos = (self.window_size[0] // 12, self.window_size[1] // 10)
        status_size = (160, self.window_size[0] // 4)
        pygame.draw.rect(self.window, BLACK_COLOR, pygame.Rect(status_pos[0], status_pos[1], status_size[0], status_size[1]))
        pygame.draw.rect(self.window, WHITE_COLOR, pygame.Rect(status_pos[0], status_pos[1], status_size[0], status_size[1]), 4)
        pygame.draw.rect(self.window, BLACK_COLOR, pygame.Rect(status_pos[0], status_pos[1], status_size[0], status_size[1]), 2)
        status_text = [
            f"LV {self.player.level:3d}",
            f"HP {self.player.health:3d}/{self.player.max_health:3d}",
            f"MP {self.player.mp:3d}/{self.player.max_mp:3d}",
            f"E  {self.player.experience:3d}/{self.player.experience_to_level_up:3d}"
        ]
        for i, text in enumerate(status_text):
            self.draw_text(text, status_pos[0] + 12, status_pos[1] + 10 + i * 30, color=WHITE_COLOR)
            
    def print_states(self):
        state_pos = (self.window_size[0] // 6, self.window_size[1] // 5 * 3)
        state_size = (self.window_size[0] // 3 * 2, self.window_size[1] // 3)
        pygame.draw.rect(self.window, BLACK_COLOR, pygame.Rect(state_pos[0], state_pos[1], state_size[0], state_size[1]))
        pygame.draw.rect(self.window, WHITE_COLOR, pygame.Rect(state_pos[0], state_pos[1], state_size[0], state_size[1]), 4)
        pygame.draw.rect(self.window, BLACK_COLOR, pygame.Rect(state_pos[0], state_pos[1], state_size[0], state_size[1]), 2)
        for i, text in enumerate(self.states):
            self.draw_text(text, state_pos[0] + 12, state_pos[1] + 10 + i * 30, color=WHITE_COLOR)
            
    def print_command(self):
        command_pos = (self.window_size[0] // 3 * 2, self.window_size[1] // 10)
        command_size = (self.window_size[0] // 4.5, self.window_size[1] // 4)
        pygame.draw.rect(self.window, BLACK_COLOR, pygame.Rect(command_pos[0], command_pos[1], command_size[0], command_size[1]))
        pygame.draw.rect(self.window, WHITE_COLOR, pygame.Rect(command_pos[0], command_pos[1], command_size[0], command_size[1]), 4)
        pygame.draw.rect(self.window, BLACK_COLOR, pygame.Rect(command_pos[0], command_pos[1], command_size[0], command_size[1]), 2)
        for i, text in enumerate(self.command):
            self.draw_text(text, command_pos[0] + 30, command_pos[1] + 10 + i * 30, color=WHITE_COLOR)
        self.draw_text('>', command_pos[0] + 12, command_pos[1] + 10 + self.selected_command * 30, color=WHITE_COLOR)
        
    def print_battle(self, enemy):
        # icon
        icon_pos = (self.window_size[0] // 3, self.window_size[1] // 10)
        icon_size =(self.window_size[0] // 4, self.window_size[0] // 4)
        pygame.draw.rect(self.window, BLACK_COLOR, pygame.Rect(icon_pos[0], icon_pos[1], icon_size[0], icon_size[1]))
        pygame.draw.rect(self.window, WHITE_COLOR, pygame.Rect(icon_pos[0], icon_pos[1], icon_size[0], icon_size[1]), 4)
        pygame.draw.rect(self.window, BLACK_COLOR, pygame.Rect(icon_pos[0], icon_pos[1], icon_size[0], icon_size[1]), 2)
        cell_rect = pygame.Rect(icon_pos[0]+5, icon_pos[1]+5, icon_size[0], icon_size[1])
        if enemy.name == "BoneKing":
            image = pygame.transform.scale(self.boss_image, (icon_size[0]-10, icon_size[1]-10)) # 画像リサイズ
        else:
            image = pygame.transform.scale(self.enemy_image, (icon_size[0]-10, icon_size[1]-10)) # 画像リサイズ
            
        self.window.blit(image, cell_rect) # 画像をブリット
        
        self.print_stats_and_command()

    def draw_text(self, text, x, y, font_size=28, color=BLACK_COLOR):
        font = pygame.font.Font("Nosutaru-dotMPlusH-10-Regular.ttf", font_size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y)
        self.window.blit(text_surface, text_rect)

    def print_stats_and_command(self):
        self.print_status()
        self.print_command()
        self.print_states()
        pygame.display.update()
        
    def open_inventory(self):
        command_entered = False
        self.command = list(self.player.inventory.keys())
        self.selected_command = 0
        self.states = [f"{self.player.inventory[self.command[self.selected_command]]}こ"]
        self.print_stats_and_command()
        
        while not command_entered:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_n:
                        item_name = self.command[self.selected_command]
                        if item_name == "ポーション":
                            command_entered = True
                            self.player.inventory[item_name] -= 1
                            if self.player.inventory[item_name] == 0:
                                del self.player.inventory[item_name]
                            self.states = [f"{item_name}を つかった！"] + self.player.heal(3)
                        else:
                            self.states = [f"ここでは つかえない！"]
                    elif event.key == K_m:
                        command_entered = True
                    elif event.key == K_w:
                        self.selected_command = max(0, self.selected_command - 1)
                        self.states = [f"{self.player.inventory[self.command[self.selected_command]]}こ"]
                    elif event.key == K_s:
                        self.selected_command = min(len(self.command)-1, self.selected_command + 1)
                        self.states = [f"{self.player.inventory[self.command[self.selected_command]]}こ"]
                    self.print_stats_and_command()
                    if len(self.states) > 1:
                        self.wait_input()

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
                if event.key == K_i and len(self.player.inventory) > 0:
                    self.open_inventory()
                    
    def run_game(self):
        while not self.game_over:
            self.handle_events()
            self.print_map()
            pygame.display.update()

        pygame.quit()

game = Game()
game.run_game()
