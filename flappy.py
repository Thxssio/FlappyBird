import sys
from random import randrange, randint
import pyxel

class FlappyBirdGame:
    def __init__(self):
        self.pyxel = pyxel
        self.width = 150
        self.height = 255
        self.pipe_gap = 200
        self.gravity = 1
        self.jump_power = 8
        self.active = False
        self.dead = False
        self.flappy_x = self.width // 3
        self.flappy_y = self.height // 2
        self.velocity = 0
        self.pipes = []
        self.score = 0

    def run(self):
        self.pyxel.init(width=self.width, height=self.height, title="Flappy Bird", fps=35)
        self.pyxel.load('data.pyxres')
        self.pyxel.run(self.update, self.draw)

    def start(self):
        self.reset()
        draw_func = self.draw if self.draw else self.noop
        update_func = self.update if self.update else self.noop

        self.pyxel.init(width=self.width, height=self.height, title="Flappy Bird", fps=35)
        self.pyxel.load('data.pyxres')
        self.pyxel.run(update_func, draw_func)

    def reset(self):
        self.active = False
        self.dead = False
        self.flappy_x = self.width // 3
        self.flappy_y = self.height // 2
        self.velocity = 0
        pipe_distance = 80
        pipe1 = self.width + pipe_distance * 0, -10 * randint(1, 8)
        pipe2 = self.width + pipe_distance * 1, -10 * randint(1, 8)
        pipe3 = self.width + pipe_distance * 2, -10 * randint(1, 8)
        pipe4 = self.width + pipe_distance * 3, -10 * randint(1, 8)
        self.pipes = [pipe1, pipe2, pipe3, pipe4]
        self.score = 0

    def update(self):
        if self.pyxel.btnp(self.pyxel.KEY_Q):
            self.pyxel.quit()
        elif self.active and self.pyxel.btnp(self.pyxel.KEY_R):
            self.reset()
        elif self.active:
            self.update_game()
        elif self.pyxel.btnp(self.pyxel.KEY_SPACE) or self.pyxel.btnp(self.pyxel.KEY_UP):
            self.active = True

    def update_game(self):
        self.update_flappy()
        self.update_pipes()
        self.check_collisions()
        self.update_score()

    def update_flappy(self):
        self.velocity += self.gravity
        if not self.dead and (self.pyxel.btnp(self.pyxel.KEY_SPACE) or self.pyxel.btnp(self.pyxel.KEY_UP)):
            self.velocity = -self.jump_power
        self.flappy_y += self.velocity
        self.flappy_y = min(self.flappy_y, self.height - 29)
        if self.dead:
            self.flappy_x -= 1

    def update_pipes(self):
        for i, (x, y) in enumerate(self.pipes):
            x -= 1
            if x < -80:
                xmax = max(x for (x, _) in self.pipes)
                x += xmax + 160
                y = randrange(-100, 0, 10)
            self.pipes[i] = (x, y)

    def check_collisions(self):
        if self.flappy_y > self.height - 30:
            self.dead = True

        for i, (x, y) in enumerate(self.pipes):
            colide_x = self.flappy_x + 17 > x and self.flappy_x < x + 25
            colide_y = self.flappy_y < y + 135 or self.flappy_y + 13 > y + self.pipe_gap
            if colide_x and colide_y:
                self.dead = True

    def update_score(self):
        for (x, y) in self.pipes:
            if self.flappy_x == x:
                self.score += 1

    def draw(self):
        self.draw_background()
        self.draw_clouds()
        self.draw_pipes()
        self.draw_ground()
        self.draw_flappy()
        self.draw_instructions()

    def draw_background(self):
        self.pyxel.cls(12)

    def draw_clouds(self):
        offset = -self.pyxel.frame_count // 2
        self.pyxel.blt(offset % (self.width + 32) - 32, self.height // 2, 2, 0, 16, 32, 32, 12)
        self.pyxel.blt((offset + 96) % (self.width + 32) - 32, self.height // 4, 2, 0, 48, 32, 32, 12)
        self.pyxel.blt(offset % (self.width + 32) - 64, int(self.height / 1.5), 2, 0, 80, 32, 32, 12)

    def draw_pipes(self):
        for (x, y) in self.pipes:
            self.pyxel.blt(x, y, 1, 0, 0, 25, 135, 0)
            self.pyxel.blt(x, y + self.pipe_gap, 1, 0, 0, 25, -135, 0)

    def draw_ground(self):
        offset = -self.pyxel.frame_count % self.width
        self.pyxel.bltm(offset, self.height - 16, 0, 0, 0, 32, 3)
        self.pyxel.bltm(offset - self.width, self.height - 16, 0, 0, 0, 32, 3)

    def draw_flappy(self):
        frame = (self.pyxel.frame_count // 4) % 3
        self.pyxel.blt(self.flappy_x, self.flappy_y, 0, 0, frame * 16, 17, 13, 0)

    def draw_instructions(self):
        if not self.active:
            msg = "Espaco ou seta para cima para comecar"
            self.pyxel.text(self.width // 2 - len(msg) * 2, self.height // 3, msg, 7)
        else:
            self.pyxel.text(self.width // 2, self.height // 3, str(self.score), 7)

        if self.dead:
            msg = "Aperte R para reiniciar"
            self.pyxel.text(self.width // 2 - len(msg) * 2, self.height // 2, msg, 7)

    def noop(self, *args, **kwargs):
        pass

if __name__ == '__main__':
    game = FlappyBirdGame()
    game.start()
