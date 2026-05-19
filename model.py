import math
import pyxel

class ZumaTowerDefenceModel:
    def __init__(self):
        # game
        self._current_round: int = 0
        self._rounds: int = 1
        self._score = 0
        
        # player
        self._player_lives: int = 2

        # enemy
        self._enemy_count: int = 5
        self._enemies_spawned: int = 0
        self._enemy_path: list = [0, 1, 17, 33] # 0 is reserved for -15, offscreen spawning
        self._enemies: list[Enemy | None] = [None] * len(self._enemy_path)
        self._enemy_coords = {}
        
        # bullet
        self._bullets: list[Bullet] = []
        self._bullet_speed = 5
        self._last_bullet_shot: int = 0

        self.tile_number_generator()
    
    '''# game properties and methods'''

    @property
    def is_game_over(self) -> bool:
        return (self.rounds == self.current_round) or \
                (self._player_lives == 0)
    
    @property
    def rounds(self) -> int:
        return self._rounds
    
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

        for y in range(1, 256, tile_size):
            for x in range(-15 if tile_number == 0 else 1, 256, tile_size):
                self._enemy_coords[tile_number] = (x, y)
                tile_number += 1
    
    '''# player properties and methods'''

    @property
    def player_lives(self):
        return self._player_lives

    def reduce_player_lives(self):
        for enemy in self._enemies:
            if enemy and self._enemy_path[enemy.path_idx] == self._enemy_path[-1]: # Once reach the last cell of the path, we lose a heart
                self._player_lives -= 1
                self._enemies[enemy.path_idx] = None
                break
    
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
        return self._enemy_coords
    
    def append_enemy(self):
        if self._enemies[0] is None and \
            self._enemies_spawned < self._enemy_count:

            self._enemies[0] = Enemy(self._enemy_coords, self._enemy_path)
            self._enemies_spawned += 1
    
    def kill_enemy(self):
        
        for enemy in self._enemies:
            if enemy:
                enemy_x = enemy.x
                enemy_y = enemy.y
                for bullet in self._bullets:
                    if (enemy_x <= bullet._current_x <= enemy_x + enemy.side) and \
                        (enemy_y <= bullet._current_y <= enemy_y + enemy.side): # update this so that yung hitbox ng bullet mismo yung tumatama, di lang center
                        
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
    
    @property
    def bullet_speed(self):
        return self._bullet_speed
        
    def bullet_shot(self, mouse_x, mouse_y):
        if (pyxel.frame_count - self._last_bullet_shot) > 27: # 27 here is 0.9 of 30 frames, change to 50 once 60 fps
            self._bullets.append(
                    Bullet(mouse_x, mouse_y, self._bullet_speed)
                )
            self._last_bullet_shot = pyxel.frame_count

    def update_bullets(self):
        for bullet in self._bullets:
            bullet.update()
        self._bullets = [bullet for bullet in self._bullets if bullet.is_alive()]
    

class Bullet:
    def __init__(self, target_x: int, target_y: int, speed: float):
        self._current_x = 128.0
        self._current_y = 128.0 # input the center here if binago size ng screen
        self._speed = speed

        dir_x = target_x - 128
        dir_y = target_y - 128 # input new center here if ever
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
    
    def update(self):
        self._current_x += self._dx
        self._current_y += self._dy

    def is_alive(self) -> bool: # change the edge of the screen below for new screen sizes
        return 0 <= self._current_x <= 261 or 0 <= self._current_y <= 261 # 261 para off screen mawala

class Enemy:
    def __init__(self, enemy_coords, enemy_path):       
        self._enemy_path_idx = 0
        self._side = 15
        self._enemy_coords = enemy_coords
        self._enemy_path = enemy_path

        # color can be added here
    
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

    def update(self):
        if not pyxel.frame_count == 0 and pyxel.frame_count % 60 == 0:
            self._enemy_path_idx += 1