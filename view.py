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
            pyxel.rect(int(enemy.x), int(enemy.y), int(enemy.side), int(enemy.side), 3)
    
    '''# game environment'''
    def draw_score(self, score: str):
        pyxel.text(215, 240, f"EXP: {score}", 2)
    
    def draw_paths(self):
        pyxel.rect(0, 11, 271, 3, 7) 
        ...