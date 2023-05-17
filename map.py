import pygame
from entities import *
from define import MAP, CELL_SIZE, IMAGE_PATHS
from image_loader import load_image

class Map:
    def __init__(self, player):
        self.player = player
        self.map = MAP[self.player.stage]
        self.size = (len(self.map[0]), len(self.map))
        self.window_size = [m * CELL_SIZE for m in self.size]
        self.image:dict = {k:load_image(v) for k, v in IMAGE_PATHS.items() if k != "player"}
        self.image.update({
            "DOWN":load_image(IMAGE_PATHS["player"], (32,0,32,32)),
            "LEFT":load_image(IMAGE_PATHS["player"], (32,32,32,32)),
            "RIGHT":load_image(IMAGE_PATHS["player"], (32,64,32,32)),
            "UP":load_image(IMAGE_PATHS["player"], (32,96,32,32)),
        })
 
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
                self.window_bg.blit(self.image[0], cell_rect) # 画像をブリット
                if map_tile < 4:
                    self.window_bg.blit(self.image[map_tile], cell_rect) # 画像をブリット
                else:
                    if map_tile == 4: # スライム
                        self.entities.append(Enemy(x, y, name="Slime", health=2, attack_power=1, exp=1, escape_rate=0.95, drop_items={"やくそう":0.2}))
                    if map_tile == 5:
                        self.entities.append(Enemy(x, y, name="Bone", health=6, attack_power=3, exp=4, escape_rate=0.8, drop_items={"やくそう":0.4}))
                    elif map_tile == 6:
                        self.entities.append(Enemy(x, y, name="BoneKing", health=20, attack_power=5, exp=8, escape_rate=0, drop_items={"ポーション":0.5}))
                    elif map_tile == 7:
                        self.entities.append(Entity(x,y,name="カギ"))
        self.draw_entities()

    def draw_entities(self):
        pygame.display.flip() # 画面をクリアする
        self.window.blit(self.window_bg, (0,0))
        
        for entity in self.entities:
            cell_rect = pygame.Rect(entity.x * CELL_SIZE, entity.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            self.window.blit(self.image[entity.name], cell_rect)
            
        player_cell = pygame.Rect(self.player.x * CELL_SIZE, self.player.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        if self.player.dx > 0:
            self.window.blit(self.image["RIGHT"], player_cell)
        else:
            if self.player.dy > 0:
                self.window.blit(self.image["DOWN"], player_cell)
            elif self.player.dy < 0:
                self.window.blit(self.image["UP"], player_cell)
            else:
                self.window.blit(self.image["LEFT"], player_cell)
        
        pygame.display.update()
        
    def change_map(self, new_stage):
        if self.player.stage != new_stage and new_stage in MAP.keys():
            self.player.stage = new_stage
            self.generate_map_and_entities(True)
        else:
            self.draw_entities()