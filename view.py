import pyxel
from typing import Protocol

class UpdateHandler(Protocol):
    def update(self): ...

class DrawHandler(Protocol):
    def draw(self): ...

class ZumaTowerDefenceView:
    def __init__(self):
        ...
    
    def start_game(self, update_fn, draw_fn):
        pyxel.init(256, 256)
        pyxel.mouse(True)
        pyxel.run(update_fn, draw_fn)
    
    def clear_screen(self):
        pyxel.cls(0)
    
    def shooting_click(self) -> bool:
        return pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT)
    
    '''# entities'''
    def draw_player(self):
        pyxel.circ(128, 128, 10, 1)
        
    def draw_bullet(self, bullets):
        for bullet in bullets:
            pyxel.circ(int(bullet.bullet_x), int(bullet.bullet_y), 5, 3)
    
    def draw_enemy(self, enemies):
        for enemy in enemies:
            if enemy:
                pyxel.rect(int(enemy.x), int(enemy.y), int(enemy.side), int(enemy.side), 3)
    
    '''# game environment'''
    def draw_score(self, score: str):
        pyxel.text(215, 240, f"EXP: {score}", 2)
        
    def draw_hearts(self, hearts):
        pyxel.text(215, 220, f"Hearts: {hearts}", 2)

    def draw_paths(self, enemy_coords, enemy_path):
        x_coord_extra = 0
        y_coord_extra = 0
        width = 0
        length = 0

        for idx, enemy_path_id in enumerate(enemy_path[1:]):

            curr_enemy_x = enemy_coords[enemy_path_id][0]
            curr_enemy_y = enemy_coords[enemy_path_id][1]
            
            tile_diff = enemy_path_id - enemy_path[idx]

            if abs(tile_diff) == 1:
                # horizontal paths
                x_coord_extra = -10 if tile_diff > 0 else 6
                y_coord_extra = 6
                width = 19
                length = 3
            else:
                # vertical paths
                x_coord_extra = 6
                y_coord_extra = -10 if tile_diff > 0 else 6
                width = 3
                length = 19
            
            pyxel.rect(curr_enemy_x + x_coord_extra, curr_enemy_y + y_coord_extra, width, length, 7)
        

             