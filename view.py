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
        self._width = 382
        self._height = 256
        pyxel.init(self._width, self._height)
        pyxel.mouse(True)
        pyxel.run(update_fn, draw_fn)
    
    def clear_screen(self):
        pyxel.cls(0)
    
    '''# buttons'''
    
    def shooting_click(self) -> bool:
        return pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT)
    
    def add_tower_click(self) -> bool:
        return (241 <= pyxel.mouse_x <= 255) and \
                (241 <= pyxel.mouse_y <= 255) and \
                pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT)
    
    def coords_pos(self) -> tuple[int, int]:
        return (pyxel.mouse_x, pyxel.mouse_y)
    
    def draw_add_tower_button(self):
        pyxel.rect(241, 241, 15, 15, 2)
    
    # pag pinindot tower, may upgrade button lalabs
    
    '''# entities'''
    def draw_player(self, bullet_color):
        pyxel.circ(self._width // 2, self._height // 2, 10, bullet_color)
        
    def draw_bullet(self, bullets):
        for bullet in bullets:
            pyxel.circ(int(bullet.bullet_x), int(bullet.bullet_y), 5, bullet.color)
    
    def draw_enemy(self, enemies):
        for enemy in enemies:
            if enemy:
                pyxel.rect(int(enemy.x), int(enemy.y), int(enemy.side), int(enemy.side), enemy.color)
    
    def draw_towers(self, towers):
        for tower in towers:
            pyxel.rect(int(tower.x), int(tower.y), 15, 15, 2)
    
    '''# game environment'''
    def draw_score(self, score: str):
        pyxel.text(15, 240, f"EXP: {score}", 2)
        
    def draw_hearts(self, hearts):
        pyxel.text(15, 230, f"Hearts: {hearts}", 2)
    
    def draw_rounds(self, round):
        pyxel.text(15, 220, f"Rounds: {round + 1}", 2)

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
        

             