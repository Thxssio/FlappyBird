import flappy
import pyxel

class FlappyConfig:
    largura_tela = 175
    altura_tela = 255
    abertura_cano = 200
    gravidade = 1
    pulo = 8
    velocidade_cano = 2

def desenhar():
    flappy.desenhar_fundo()
    flappy.desenhar_nuvens()
    flappy.desenhar_canos()
    flappy.desenhar_chao()
    flappy.desenhar_flappy()
    flappy.desenhar_instrucoes()

if __name__ == '__main__':
    flappy_game = flappy.FlappyBirdGame()
    
    flappy_game.width = FlappyConfig.largura_tela
    flappy_game.height = FlappyConfig.altura_tela
    flappy_game.pipe_gap = FlappyConfig.abertura_cano
    flappy_game.gravity = FlappyConfig.gravidade
    flappy_game.jump_power = FlappyConfig.pulo
    flappy_game.velocidade_cano = FlappyConfig.velocidade_cano
    
    flappy_game.start()
