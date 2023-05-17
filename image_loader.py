import pygame
from define import CELL_SIZE

# 使用する画像を読み込んでおく
def load_image(img_path, pos = None):
    image = pygame.image.load(img_path)
    if pos is not None:
        image = image.subsurface(pygame.Rect(pos))
    return pygame.transform.scale(image, (CELL_SIZE, CELL_SIZE)) # 画像を読み込みリサイズ
