import pygame
from entities import *
from define import MAP, CELL_SIZE, IMAGES

class Map:
    def __init__(self, player):
        self.player = player
        self.map = MAP[self.player.stage]
        self.size = (len(self.map[0]), len(self.map))
        self.window_size = [m * CELL_SIZE for m in self.size]
 
        pygame.init()
        pygame.display.set_caption('RPG Game')
        
        # ゲームウィンドウの作成
        self.window = pygame.display.set_mode(self.window_size, pygame.DOUBLEBUF)
        self.generate_map_and_entities()
        pygame.display.update()
        
    def generate_map_and_entities(self, map_load:bool=False):
        if map_load:
            self.map = MAP[self.player.stage]
        self.window_bg = pygame.Surface(self.window_size)
        self.entities = []
        for y, map_row in enumerate(self.map):
            for x, map_tile in enumerate(map_row):
                cell_rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                self.window_bg.blit(IMAGES[0], cell_rect) # 画像をブリット
                if map_tile < 4:
                    self.window_bg.blit(IMAGES[map_tile], cell_rect) # 画像をブリット
                else:
                    if map_tile == 4:
                        self.entities.append(Enemy(x, y)) # 通常の敵のHP: 3, 攻撃力: 1
                    elif map_tile == 5:
                        self.entities.append(Boss(x, y)) # Boss
                    elif map_tile == 7:
                        self.entities.append(Entity(x,y,name="カギ"))
        self.draw_entities()

    def draw_entities(self):
        self.window.blit(self.window_bg, (0,0))
        for entity in self.entities:
            cell_rect = pygame.Rect(entity.x * CELL_SIZE, entity.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            self.window.blit(IMAGES[entity.name], cell_rect)
        self.player_cell = pygame.Rect(self.player.x * CELL_SIZE, self.player.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        self.window.blit(IMAGES["player"], self.player_cell)
        pygame.display.update()
        
    def change_map(self, new_stage):
        if self.player.stage != new_stage and new_stage in MAP.keys():
            self.player.stage = new_stage
            self.generate_map_and_entities(True)
        else:
            self.draw_entities()