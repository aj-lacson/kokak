import math
import pyxel
from random import Random

class ZumaTowerDefenceModel:
    def __init__(self, rng: Random, data):
        self._data = data["standard"]

        # game
        self._fps = 30
        self._return_game_frame = 0
        self._game_tile_coords = {}
        self._current_round: int = 0
        self._rounds: int = self._data["rounds"]
        self._score = 10
        self._rng = rng
        self._colors = self._data["colors-available"]
        
        # player
        self._player_lives: int = self._data["player-lives"]

        # enemy
        self._enemy_count: int = self._data["enemies-per-round"]
        self._enemies_spawned: int = 0
        self._enemy_path: list = self._data["map-sequence"]
        self._enemies: list[Enemy | None] = [None] * len(self._enemy_path) # physics of disconnected enemy in front not moving

        # tower
        self._towers: list[Tower | None] = []
        self._towered_tiles = {}
        self._unavailable_tower_tiles = self._enemy_path[:]
        self._tower_next_bullet_color = self._rng.randint(16 - self._colors, 15)

        # bullet
        self._bullets: list[Bullet] = []
        self._last_bullet_shot: int = 0
        self._next_bullet_color = self._rng.randint(16 - self._colors, 15)

        self.tile_number_generator()
    
    '''# game properties and methods'''

    @property
    def is_game_over(self) -> bool:
        return (self.rounds == self.current_round) or \
                (self._player_lives == 0)
    
    @property
    def is_round_over(self) -> bool:
        round_over = all(enemy is None for enemy in self._enemies)
        if round_over and self._enemies_spawned == self._enemy_count:
            self._enemies_spawned = 0
            self._current_round += 1
            self._return_game_frame = (pyxel.frame_count + 180) # 10 secs yung in between rounds
            return True
        return False
    
    @property
    def rounds(self) -> int:
        return self._rounds
    
    @property
    def round_ongoing(self):
        return pyxel.frame_count > self._return_game_frame
    
    @property
    def current_round(self) -> int:
        return self._current_round
    
    @property
    def score(self):
        return self._score
    
    def add_score(self):
        self._score += 1
    
    def tile_number_generator(self):
        tile_size = 16 # please change it to whatever max size screen (one side) you have divided by 16
        tile_number = 0

        for y in range(1, 384, tile_size):
            for x in range(1, 256, tile_size):
                self._game_tile_coords[tile_number] = (x, y)
                tile_number += 1
    
    def get_tile(self, mouse_pos):
        mouse_pos_x, mouse_pos_y = mouse_pos
        
        tile_col = (mouse_pos_x - 1) // 16
        tile_row = (mouse_pos_y - 1) // 16
        tile = (tile_row * 16) + tile_col

        return tile
    
    '''# player properties and methods'''

    @property
    def player_lives(self):
        return self._player_lives
    
    @property
    def next_bullet_color(self):
        return self._next_bullet_color

    def reduce_player_lives(self):
        for enemy in self._enemies:
            if enemy and self._enemy_path[enemy.path_idx] == self._enemy_path[-1]: # Once reach the last cell of the path, we lose a heart
                self._player_lives -= 1
                self._enemies[enemy.path_idx] = None
                break
              
    '''# tower properties and methods'''
    def add_tower(self, mouse_pos):
        
        if self._score < 5:
            return
        
        tile = self.get_tile(mouse_pos)

        if tile not in self._game_tile_coords:
            return

        coord_x, coord_y = self._game_tile_coords[tile]
        if tile not in self._unavailable_tower_tiles:
            
            self._towered_tiles[tile] = (coord_x, coord_y)
            self._unavailable_tower_tiles += [tile]
            
            self._score -= 5

            self._towers.append(Tower(tile, self._game_tile_coords))
    
    def upgrade_tower(self, mouse_pos): # upgrade tower
        if self._score < 5:
            return
        tile = self.get_tile(mouse_pos)

        tower = next((tower for tower in self._towers if tower and tower.tile == tile), None)
        if tower:
            tower.upgrade()
            self._score -= 5
        

    def tower_clicked(self, mouse_pos): # a upgrade button will pop up beside the tower
        tile = self.get_tile(mouse_pos)
        return tile in self._towered_tiles
    
    def tower_shoot(self):
        for tower in self._towers:
            if tower:
                tower.bullet_shot(self) if tower.level == 1 else tower.bullet_shot_two(self)

    @property
    def towers(self):
        return self._towers
    
    '''# enemy properties and methods'''
    
    @property
    def enemy_count(self) -> int:
        return self._enemy_count
    
    @property
    def enemies(self):
        return self._enemies
    
    @property
    def enemies_spawned(self):
        return self._enemies_spawned
    
    @property
    def enemy_path(self):
        return self._enemy_path
    
    @property
    def enemy_coords(self):
        return self._game_tile_coords
    
    def append_enemy(self):
        if self._enemies[0] is None and \
            self._enemies_spawned < self._enemy_count:

            self._enemies[0] = Enemy(self._game_tile_coords, self._enemy_path, self._rng.randint(16 - self._colors, 15))
            self._enemies_spawned += 1
    
    def kill_enemy(self):
        
        for enemy in self._enemies:
            if not enemy:
                continue
            enemy_x = enemy.x
            enemy_y = enemy.y
            
            for bullet in self._bullets:
                if (enemy_x <= bullet._current_x <= enemy_x + enemy.side) and \
                   (enemy_y <= bullet._current_y <= enemy_y + enemy.side): # update this so that yung hitbox ng bullet mismo yung tumatama, di lang center
                    
                    if bullet.color == enemy.color:
                        self.add_score()
                        self._enemies[enemy.path_idx] = None
                    self._bullets.remove(bullet)
    
    def update_enemies(self):
        new_enemies: list[Enemy | None] = [None] * len(self._enemies)
        for enemy in self._enemies:
            if enemy:
                enemy.update()
                if enemy.path_idx < len(self._enemy_path):
                    new_enemies[enemy.path_idx] = enemy
        self._enemies = new_enemies
    
    '''# bullet properties and methods'''

    @property
    def bullets(self):
        return self._bullets
        
    def bullet_shot(self, starting_x, starting_y, mouse_x, mouse_y, firerate):
        if (pyxel.frame_count - self._last_bullet_shot) > firerate: # 27 here is 0.9 of 30 frames, change to 50 once 60 fps
            self._bullets.append(
                    Bullet(starting_x, starting_y, mouse_x, mouse_y, self._next_bullet_color)
                )
            self._next_bullet_color = self._rng.randint(14, 15) # pede to isepartae function since dalwang beses kinall
            self._last_bullet_shot = pyxel.frame_count
    
    def update_bullets(self):
        for bullet in self._bullets:
            bullet.update()
        self._bullets = [bullet for bullet in self._bullets if bullet.is_alive()]
    

class Bullet:
    def __init__(self, current_x, current_y, target_x: int, target_y: int, color: int):
        self._current_x = current_x
        self._current_y = current_y
        self._speed = 10
        self._color = color
        

        dir_x = target_x - current_x
        dir_y = target_y - current_y
        length = math.hypot(dir_x, dir_y)

        if length == 0:
            self._dx = 0.0
            self._dy = -self._speed
        else:
            self._dx = dir_x / length * self._speed
            self._dy = dir_y / length * self._speed
        
        # color can be added here
    
    @property
    def bullet_x(self) -> float:
        return self._current_x
    
    @property
    def bullet_y(self) -> float:
        return self._current_y
    
    @property
    def color(self):
        return self._color
    
    def update(self):
        self._current_x += self._dx
        self._current_y += self._dy

    def is_alive(self) -> bool: # change the edge of the screen below for new screen sizes
        return 0 <= self._current_x <= 261 or 0 <= self._current_y <= 261 # 261 para off screen mawala

class Enemy:
    def __init__(self, game_tile_coords, enemy_path, color: int):       
        self._enemy_path_idx = 0
        self._side = 15
        self._enemy_coords = game_tile_coords
        self._enemy_path = enemy_path
        self._color = color
    
    @property
    def path_idx(self) -> int:
        return self._enemy_path_idx
    
    @property
    def x(self):
        tile_number = self._enemy_path[self._enemy_path_idx]
        return self._enemy_coords[tile_number][0]
    
    @property
    def y(self):
        tile_number = self._enemy_path[self._enemy_path_idx]
        return self._enemy_coords[tile_number][1]

    @property
    def side(self):
        return self._side
    
    @property
    def color(self):
        return self._color

    def update(self):
        if not pyxel.frame_count == 0 and pyxel.frame_count % 60 == 0:
            self._enemy_path_idx += 1

class Tower:
    def __init__(self, tile_pos, game_tile_coords):
        self._tile_pos = tile_pos
        self._tower_coords = game_tile_coords
        self._firerate = 60
        self._last_bullet_shot = 0
        self._level = 1
    
    @property
    def tile(self):
        return self._tile_pos

    @property
    def x(self):
        return self._tower_coords[self._tile_pos][0]
    
    @property
    def level(self):
        return self._level
    
    @property
    def y(self):
        return self._tower_coords[self._tile_pos][1]

    @property
    def firerate(self):
        return self._firerate
    
    @property
    def last_bullet_shot(self):
        return self._last_bullet_shot
    
    def upgrade(self):
        self._level = 2
    
    def set_last_bullet_shot(self, last_bullet_shot):
        self._last_bullet_shot = last_bullet_shot

    def bullet_shot(self, model):
        if (pyxel.frame_count - self._last_bullet_shot) > self._firerate:
            
            model._bullets.append(Bullet(self.x + 7, self.y + 7, self.x + 7, self.y, model._tower_next_bullet_color))

            model._tower_next_bullet_color = model._rng.randint(16 - model._colors, 15)
            self._last_bullet_shot = pyxel.frame_count
    
    def bullet_shot_two(self, model):
        if (pyxel.frame_count - self._last_bullet_shot) > self._firerate:
            for adjustment in range(4, 12, 7):
                model._bullets.append(Bullet(self.x + adjustment, self.y + adjustment, self.x + adjustment, self.y, model._tower_next_bullet_color))
                model._tower_next_bullet_color = model._rng.randint(16 - model._colors, 15)
            self._last_bullet_shot = pyxel.frame_count