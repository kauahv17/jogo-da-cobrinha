import pygame
from random import randint
from pygame.locals import *

tela_largura = 1000
tela_altura = 800

tela = pygame.display.set_mode((tela_largura, tela_altura))
pygame.display.set_caption("jogo da COBRA")
imagem_bg = pygame.image.load("campo.png")

cima = 1
baixo = -1
direita = 2
esquerda = -2

pygame.init()

class SNAKE:
    def __init__(self, snake, direcao):
        self.snake = snake
        self.altura_bg = imagem_bg.get_height()
        self.largura_bg = imagem_bg.get_width()
        self.direcao = direcao
        self.anti_direcao = 0
        self.pontos = 0

    def mudar_direcao(self):
        if self.direcao == cima:
            self.snake[0] = (self.snake[0][0], self.snake[0][1] - 20)
        if self.direcao == baixo:
            self.snake[0] = (self.snake[0][0], self.snake[0][1] + 20)
        if self.direcao == direita:
            self.snake[0] = (self.snake[0][0] + 20, self.snake[0][1])
        if self.direcao == esquerda:
            self.snake[0] = (self.snake[0][0] - 20, self.snake[0][1])

    def mover_snake(self):
        for i in range(len(self.snake)-1, 0, -1):
            self.snake[i] = (self.snake[i-1][0], self.snake[i-1][1])

    def colisao_parede(self):
        if self.snake[0][0] < (tela_largura - self.largura_bg)/2 + 20 - 1:#borda da esquerda
            return True
        if self.snake[0][0] > (tela_largura - self.largura_bg)/2 + self.largura_bg - 20 + 1:#borda da direita
            return True
        if self.snake[0][1] < (tela_altura - self.altura_bg)/2 + 20 - 1:#borda de cima
            return True
        if self.snake[0][1] > (tela_altura - self.altura_bg)/2 + self.altura_bg - 20 + 1:#borda de baixo
            return True
        
        return False
    
    def colisao_cauda(self):
        #print(self.snake[0],"==",corpo)
        if self.snake[0] in self.snake[3:]:
            del self.snake[0]
            return True
            
        return False

class APPLE:
    def __init__(self):
        self.x = (randint(120, 860) // 20) * 20
        self.y = (randint(120, 680) // 20) * 20

    def spawnar_maca(self):
        self.x = (randint(120, 860) // 20) * 20
        self.y = (randint(120, 680) // 20) * 20

    def colisao(self, pos_cobra):
        #print((self.x, self.y),"==",pos_cobra)
        return ((self.x, self.y) == pos_cobra)


def mostrar_mensagem():
    fonte_mensagem = pygame.font.SysFont("Arial", 50)
    mensagem = fonte_mensagem.render('APERTE "R" PARA REINICIAR', 1, (255, 255, 255))
    tela.blit(mensagem, (tela_largura/2 - imagem_bg.get_height()/2+35, tela_altura/2 - 50))

def main():
    COBRA = SNAKE([(360,360), (340,360), (320,360)], direita)
    COBRA_skin = pygame.Surface((20, 20))
    COBRA_skin.fill((0, 255, 0))

    MACA = APPLE()
    MACA_skin = pygame.Surface((20, 20))
    MACA_skin.fill((255, 0, 0))

    fonte_score = pygame.font.SysFont("Arial", 20)
    
    relogio = pygame.time.Clock()
    rodando = True

    while True:
        relogio.tick(10)
        #print(x_maca, y_maca)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()

            if event.type == KEYDOWN:
                if event.key == K_w or event.key == K_UP:
                    COBRA.anti_direcao = COBRA.direcao
                    COBRA.direcao = cima
                if event.key == K_s or event.key == K_DOWN:
                    COBRA.anti_direcao = COBRA.direcao
                    COBRA.direcao = baixo
                if event.key == K_d or event.key == K_RIGHT:
                    COBRA.anti_direcao = COBRA.direcao
                    COBRA.direcao = direita
                if event.key == K_a or event.key == K_LEFT:
                    COBRA.anti_direcao = COBRA.direcao
                    COBRA.direcao = esquerda

                if COBRA.anti_direcao + COBRA.direcao == 0:
                    aux = COBRA.anti_direcao
                    COBRA.anti_direcao = COBRA.direcao
                    COBRA.direcao = aux
                    

                if event.key == K_r:
                    main()
        
        if len(COBRA.snake) != 0:
            if MACA.colisao(COBRA.snake[0]):
                COBRA.pontos += 1
                COBRA.snake.append((0, 0))
                MACA.spawnar_maca()

            COBRA.mover_snake()
            COBRA.mudar_direcao()

            if rodando:
                if COBRA.colisao_cauda():
                    rodando = False
                    del COBRA.snake[0]

                if COBRA.colisao_parede():
                    rodando = False
                    del COBRA.snake[0]

            else:
                del COBRA.snake[0]

            tela.fill((0, 0, 0))
            tela.blit(imagem_bg, (99, 99))
            tela.blit(MACA_skin, (MACA.x, MACA.y))

            if not rodando:
                mostrar_mensagem()

            for pos in COBRA.snake:
                tela.blit(COBRA_skin, pos)
            
        score = fonte_score.render(f"PONTUAÇÃO: {COBRA.pontos}", 1, (255, 255, 255))
        tela.blit(score, (20, 20))    

        pygame.display.update()

if __name__ == '__main__':
    main()
