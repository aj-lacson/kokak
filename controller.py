from model import ZumaTowerDefenceModel
from view import ZumaTowerDefenceView
import pyxel

class ZumaTowerDefenceController:
    def __init__(self, model: ZumaTowerDefenceModel, view: ZumaTowerDefenceView):
        self._model = model
        self._view = view
        self._tower_placement_mode = False
        self._upgrade_tower_mode = False
    
    def start_game(self):
        self._view.start_game(self.update, self.draw)
        
    def update(self):
        model = self._model
        view = self._view
        
        if not model.is_game_over:
            if model.round_ongoing:
                if view.shooting_click():
                    model.bullet_shot(384 //2, 256 // 2, pyxel.mouse_x, pyxel.mouse_y, 33)
                if model.towers:
                    model.tower_shoot()

                model.update_bullets()
                model.append_enemy() # spawns enemy
                model.update_enemies()
                model.kill_enemy()
                model.reduce_player_lives()
                model.is_round_over
            else:
                if self._tower_placement_mode:
                    if view.shooting_click():
                        model.add_tower(view.coords_pos())
                        self._tower_placement_mode = False
                elif self._upgrade_tower_mode:
                    if model.tower_clicked(view.coords_pos()):
                        model.upgrade_tower(view.coords_pos())
                        self._upgrade_tower_mode = False
                elif view.add_tower_click():
                    self._tower_placement_mode = True
                elif view.upgrade_tower_click():
                    self._upgrade_tower_mode = True
                    
        
    def draw(self):
        model = self._model
        view = self._view

        view.clear_screen()
        
        # game
        view.draw_score(str(model.score))
        view.draw_hearts(model.player_lives)
        view.draw_rounds(model.current_round)
        view.draw_paths(model.enemy_coords, model.enemy_path)
        view.draw_mouse_coords()

        # entities
        view.draw_bullet(model.bullets)
        view.draw_player(model.next_bullet_color)
        view.draw_enemy(model.enemies)
        view.draw_towers(model.towers)

        # buttons
        if not model.round_ongoing and not model.is_game_over:
            view.draw_add_tower_button()
            view.draw_upgrade_tower_button()

