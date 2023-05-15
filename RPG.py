import random
import pygame
import pickle
from pygame.locals import *
from map import Map
from player import Player
from define import *

class Game:
    def __init__(self):
        self.game_over:bool = False
        self.player = Player()
        self.map = Map(self.player)
        self.window_size = self.map.window_size
        self.window = self.map.window
    
    def player_move(self, dx, dy):
        new_x, new_y = self.player.x + dx, self.player.y + dy
        new_stage = self.map.stage
        
        if new_x < 0: # 左ステージへの移動
            new_stage = (self.map.stage[0], self.map.stage[1]-1)
            new_x = self.map.size[0] - 1
        elif new_x == self.map.size[0]: # 右ステージへの移動
            new_stage = (self.map.stage[0], self.map.stage[1]+1)
            new_x = 0
        elif (new_y < 0): # 上ステージへの移動
            new_stage = (self.map.stage[0]-1, self.map.stage[1])
            new_y = self.map.size[1] - 1
        elif (new_y == self.map.size[1]): # 下ステージへの移動
            new_stage = (self.map.stage[0]+1, self.map.stage[1])
            new_y = 0
        elif (self.map.map[new_y][new_x] > 0 and self.map.map[new_y][new_x] < 4):
            return
        for entity in self.map.entities:
            if entity.x == new_x and entity.y == new_y:
                if entity.name in TOOL_INFO.keys():
                    self.states = [f"{entity.name}を てにいれた！"]
                    self.map.entities.remove(entity)
                    if entity.name == "カギ":
                        self.player.inventory["カギ"] = 1
                    else:
                        if entity.name in self.player.inventory.keys():
                            self.player.inventory[entity.name] += 1
                        else:
                            self.player.inventory[entity.name] = 1
                            
                    self.command = list(self.player.inventory.keys())
                    self.selected_command = 0
                    self.print_stats_and_command()
                    self.wait_input()
                    self.map.draw_entities()
                    return
                    
                else: # 移動先に敵がいる場合、バトルを開始する
                    self.battle(entity)
                    return
        self.player.x, self.player.y = new_x, new_y
        self.map.change_map(new_stage)

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
                                if item_name in ["やくそう", "ポーション"]:
                                    command_entered = True
                                    self.player.inventory[item_name] -= 1
                                    if self.player.inventory[item_name] == 0:
                                        del self.player.inventory[item_name]
                                    self.states = [f"{item_name}を つかった！"] + self.player.heal(HEAL_INFO[item_name])
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
                                        self.states = [f"しょじ {self.player.inventory[self.command[self.selected_command]]:3d}こ"] + TOOL_INFO[self.command[self.selected_command]]
                                        open_inventory = True
                        elif event.key == K_m:
                            self.command = BATTLE_COMMAND
                            self.states = ["どうする？"]
                            open_inventory = False
                        elif event.key == K_w:
                            self.selected_command = max(0, self.selected_command - 1)
                            if open_inventory : self.states = [f"しょじ {self.player.inventory[self.command[self.selected_command]]:3d}こ"] + TOOL_INFO[self.command[self.selected_command]]
                        elif event.key == K_s:
                            self.selected_command = min(len(self.command)-1, self.selected_command + 1)
                            if open_inventory : self.states = [f"しょじ {self.player.inventory[self.command[self.selected_command]]:3d}こ"] + TOOL_INFO[self.command[self.selected_command]]
                            
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
            print("GAME OVER")
            self.print_battle(enemy)
            self.wait_input()
        elif enemy.health > 0:
            self.print_battle(enemy)
            self.wait_input()
        else:
            self.map.entities.remove(enemy)
            self.states.append(f"{enemy.name}を たおした！")
            self.states.extend(self.player.gain_experience(enemy.exp))
            if self.player.experience >= self.player.experience_to_level_up:
                self.print_battle(enemy)
                self.wait_input()
                self.states = self.player.level_up()
            
            entity = enemy.drop()
            if entity:
                self.map.entities.append(entity)
                self.states.append(f"{enemy.name}は {entity.name}を おとした")
                self.map.draw_entities()
            self.print_battle(enemy)
            self.wait_input()
        self.map.draw_entities()
            
    def wait_input(self):
        command_entered = False
        while not command_entered:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_n or event.key == K_m:
                        command_entered = True
        
    def draw_bg_rect(self, pos=(0,0), size=(1,1), texts=None, text_bias=(12,10)):
        pygame.draw.rect(self.window, BLACK_COLOR, pygame.Rect(pos[0], pos[1], size[0], size[1]))
        pygame.draw.rect(self.window, WHITE_COLOR, pygame.Rect(pos[0], pos[1], size[0], size[1]), 4)
        pygame.draw.rect(self.window, BLACK_COLOR, pygame.Rect(pos[0], pos[1], size[0], size[1]), 2)
        if texts:
            for i, text in enumerate(texts):
                self.draw_text(text, pos[0] + text_bias[0], pos[1] + text_bias[1] + i * 30, color=WHITE_COLOR)

    def print_status(self):
        status_text = [
            f"LV {self.player.level:3d}",
            f"HP {self.player.health:3d}/{self.player.max_health:3d}",
            f"MP {self.player.mp:3d}/{self.player.max_mp:3d}",
            f"E  {self.player.experience:3d}/{self.player.experience_to_level_up:3d}"
        ]
        self.draw_bg_rect(pos=(self.window_size[0] // 12, self.window_size[1] // 10), size=(160, self.window_size[0] // 4), texts=status_text)
            
    def print_states(self):
        self.draw_bg_rect(pos=(self.window_size[0] // 6, self.window_size[1] // 5 * 3),size=(self.window_size[0] // 3 * 2, self.window_size[1] // 3),texts=self.states)
            
    def print_command(self):
        command_pos = (self.window_size[0] // 3 * 2, self.window_size[1] // 10)
        self.draw_bg_rect(pos=command_pos,size=(self.window_size[0] // 4.5, self.window_size[1] // 4),texts=self.command,text_bias=(30,10))
        self.draw_text('>', command_pos[0] + 12, command_pos[1] + 10 + self.selected_command * 30, color=WHITE_COLOR)
        
    def print_battle(self, enemy):
        # icon
        icon_pos = (self.window_size[0] // 3, self.window_size[1] // 10)
        icon_size =(self.window_size[0] // 4, self.window_size[0] // 4)
        self.draw_bg_rect(pos=icon_pos,size=icon_size)
        
        cell_rect = pygame.Rect(icon_pos[0]+5, icon_pos[1]+5, icon_size[0], icon_size[1])
        image = pygame.transform.scale(IMAGES[enemy.name], (icon_size[0]-10, icon_size[1]-10)) # 画像リサイズ
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
        if len(self.player.inventory) > 0:
            self.states = [f"しょじ {self.player.inventory[self.command[self.selected_command]]:3d}こ"] + TOOL_INFO[self.command[self.selected_command]]
        else:
            self.states = ["どうぐを もっていない！"]
        self.print_stats_and_command()
        
        while not command_entered:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_n and len(self.player.inventory) > 0:
                        item_name = self.command[self.selected_command]
                        if item_name in ["やくそう", "ポーション"]:
                            command_entered = True
                            self.player.inventory[item_name] -= 1
                            if self.player.inventory[item_name] == 0:
                                del self.player.inventory[item_name]
                            self.states = [f"{item_name}を つかった！"] + self.player.heal(HEAL_INFO[item_name])
                            self.print_stats_and_command()
                            self.wait_input()
                            self.map.draw_entities()
                        else:
                            self.states = [f"ここでは つかえない！"]
                            self.print_stats_and_command()
                            self.wait_input()
                        
                    elif event.key == K_m:
                        command_entered = True
                        self.map.draw_entities()
                    elif event.key == K_w and len(self.player.inventory) > 0:
                        self.selected_command = max(0, self.selected_command - 1)
                        self.states = [f"しょじ {self.player.inventory[self.command[self.selected_command]]:3d}こ"] + TOOL_INFO[self.command[self.selected_command]]
                        self.print_stats_and_command()
                    elif event.key == K_s and len(self.player.inventory) > 0:
                        self.selected_command = min(len(self.command)-1, self.selected_command + 1)
                        self.states = [f"しょじ {self.player.inventory[self.command[self.selected_command]]:3d}こ"] + TOOL_INFO[self.command[self.selected_command]]
                        self.print_stats_and_command()

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
                if event.key == K_i:
                    self.open_inventory()
                if event.key == K_F1:
                    with open("player.save", "wb") as f:
                        pickle.dump(self.player, f)
                    print("saved")
                if event.key == K_F2:
                    with open("player.save", "rb") as f:
                        self.player = pickle.load(f)
                    self.player_move(0, 0)
                    print("loaded")
                    
    def run_game(self):
        while not self.game_over:
            self.handle_events()

        pygame.quit()

game = Game()
game.run_game()
