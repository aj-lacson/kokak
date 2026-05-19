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
        self._enemies: list[Enemy] = []
        self._enemies_spawned: int = 0
        
        # bullet
        self._bullets: list[Bullet] = []
        self._bullet_speed = 5
        self._last_bullet_shot: int = 0
    
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
    
    '''# player properties and methods'''

    @property
    def player_lives(self):
        return self._player_lives

    def reduce_player_lives(self):
        for enemy in self._enemies:
            if enemy.x >= 261: # pag lumabas sa screen enemy kasi wala pang way to approach yung enemy to center, 261 yung edge
                self._player_lives -= 1
                self._enemies.remove(enemy)
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
    
    def append_enemy(self):
        if (not self._enemies or self._enemies[-1].x > 0) and \
            self._enemies_spawned < self._enemy_count: # yung 15 rito sa taas is yung nagseset sa pagspawn ng next enemy
            
            self._enemies.append(Enemy())
            self._enemies_spawned += 1
    
    def kill_enemy(self):
        for enemy in self._enemies:
            for bullet in self._bullets:
                if (enemy.x <= bullet._current_x <= enemy.x + enemy.side) and \
                    (enemy.y <= bullet._current_y <= enemy.y + enemy.side): # update this so that yung hitbox ng bullet mismo yung tumatama, di lang center
                    
                    self.add_score()
                    
                    self._enemies.remove(enemy)
                    self._bullets.remove(bullet)
    
    def update_enemies(self):
        for enemy in self._enemies:
            enemy.update()
    
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
    def __init__(self):       
        self._current_x = -15 # offscreen tau spawn :))
        self._current_y = 5

        self._side = 15

        # color can be added here
    
    @property
    def x(self):
        return self._current_x
    
    @property
    def y(self):
        return self._current_y

    @property
    def side(self):
        return self._side

    def update(self):
        if pyxel.frame_count % 60 == 0:
            self._current_x += 16 # 16 muna pixel size nang tile, pede sya mabago