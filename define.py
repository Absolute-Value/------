import pygame

# 外観
CELL_SIZE = 60

# 色
BLACK_COLOR = (0, 0, 0)
WHITE_COLOR = (255, 255, 255)

# ゲーム設定
INIT_EXP = 2
EXP_RATE = 0.5
ENEMY_NUM = 5
INIT_STAGE = (1,2)
BATTLE_COMMAND = ["こうげき", "じゅもん", "にげる", "どうぐ"]

# マップ
# 0:陸 1:木 4:海
MAP = {
    (1,1):[
        [1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,0,0,0,0,0,0,0,0],
        [1,1,0,0,0,0,0,0,0,0,0,0],
        [1,1,0,0,0,0,0,0,0,0,0,0],
        [1,1,0,0,0,0,0,0,0,0,0,0],
        [1,0,0,0,0,0,0,0,0,0,0,0],
        [1,0,0,0,0,0,0,0,0,0,0,0],
        [1,0,0,0,0,0,0,0,0,0,4,4],
        [4,4,4,4,4,4,4,4,4,4,4,4],
    ],
    (1,2):[
        [1,1,1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,0,0,1,1,1,1,1,1],
        [0,0,0,0,0,0,0,0,1,1,1,1],
        [0,0,0,0,0,0,0,0,0,1,1,1],
        [0,0,0,0,0,0,0,0,0,0,1,1],
        [0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,4,4,4],
        [0,0,0,0,0,0,4,4,4,4,4,4],
        [4,4,4,4,4,4,4,4,4,4,4,4],
        [4,4,4,4,4,4,4,4,4,4,4,4],
    ],
    (1,3):[
        [1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,0,0,0,0,1,1,1,1],
        [1,1,0,0,0,0,0,0,0,1,1,1],
        [1,0,0,0,0,0,0,0,0,0,1,1],
        [1,0,0,0,0,0,0,0,0,0,1,1],
        [0,0,0,0,0,0,0,0,0,0,1,1],
        [4,4,0,0,0,0,0,0,0,4,4,4],
        [4,4,4,4,4,4,4,4,4,4,4,4],
        [4,4,4,4,4,4,4,4,4,4,4,4],
        [4,4,4,4,4,4,4,4,4,4,4,4],
    ]
}

# どうぐの説明
TOOL_INFO = {
    "やくそう":["HPを すこし かいふく"],
    "ポーション":["HPを かいふく"],
    "カギ":["どこかを あけることができる"],
}

HEAL_INFO = {
    "やくそう":2,
    "ポーション":8,
}

# 画像
# 使用する画像を読み込んでおく
def load_image(img_path):
    return pygame.transform.scale(pygame.image.load(img_path), (CELL_SIZE, CELL_SIZE))# 画像を読み込みリサイズ

IMAGES = {
    0: load_image("images/land.png"),
    1: load_image("images/tree.png"),
    4: load_image("images/sea.png"),
    "player": load_image("images/player.png"),
    "やくそう": load_image("images/herb.png"), 
    "ポーション": load_image("images/potion.png"), 
    "Bone": load_image("images/enemy.png"),
    "BoneKing": load_image("images/boss.png"),
    "カギ": load_image("images/key.png"),
}

