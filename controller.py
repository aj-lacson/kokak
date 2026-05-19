from model import ZumaTowerDefenceModel
from view import ZumaTowerDefenceView
import pyxel

class ZumaTowerDefenceController:
    def __init__(self, model: ZumaTowerDefenceModel, view: ZumaTowerDefenceView):
        self._model = model
        self._view = view
    
    def start_game(self):
        self._view.start_game(self.update, self.draw)
        
    def update(self):
        model = self._model
        view = self._view
        
        if not model.is_game_over:
            if view.shooting_click():
                model.bullet_shot(pyxel.mouse_x, pyxel.mouse_y)

            model.update_bullets()

            model.append_enemy()
            
            model.kill_enemy()
            
            model.reduce_player_lives()

            model.update_enemies()
        
    def draw(self):
        model = self._model
        view = self._view

        view.clear_screen()

        view.draw_paths(model.enemy_coords, model.enemy_path) # pathways

        view.draw_bullet(model.bullets)

        view.draw_player()

        view.draw_enemy(model.enemies)

        view.draw_score(str(model.score))

        view.draw_hearts(model.player_lives)

