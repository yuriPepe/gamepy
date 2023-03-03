import pygame
import os
import random
from neat import NEAT

ai_jogando = True
geracao = 0

TELA_LARGURA = 500
TELA_ALTURA = 800

IMAGEM_CHAO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'chao.png')))
IMAGEM_CANO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'pipe.png')))
IMAGEM_BACKGROUND = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'background.png')))
IMAGENS_PASSARO = [
    
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird.png'))),
     pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'birdUp.png'))),
     pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'birdDown.png')))
]

pygame.font.init()
FONTE_PONTOS = pygame.font.SysFont('arial', 50)

class Passaro:
    IMGS = IMAGENS_PASSARO
    #ANIMAÇÕES
    ROTACAO_MAXIMA = 25
    VELOCIDADE_ROTACAO = 20
    TEMPO_ANIMACAO = 5

    #posição inicial
    def __init__(self, x, y):
        self.x=x
        self.y=y
        self.angulo = 0
        self.velocidade = 0
        self.altura = self.y
        self.tempo = 0
        self.contagem_imagens = 0
        self.imagem = self.IMGS[0]


    def pular(self):
        self.velocidade = -10.5
        self.tempo = 0
        self.altura = self.y

    #deslocamento
    def mover(self):
        #distância deslocada em um periodo de tempo
        self.tempo += 1
        deslocamento = 1.5 * (self.tempo*2) + self.velocidade * self.tempo

    #restrição do deslocamento

        if deslocamento > 16:
            deslocamento = 16
        elif deslocamento < 0:
            deslocamento -= 2


        self.y += deslocamento
        return self.y

    #angulo passaro

        if deslocamento < 0 or self.y < (self.altura + 50):
            if self.angulo < self.ROTACAO_MAXIMA:
                self.angulo = self.ROTACAO_MAXIMA
        else:
            if self.angulo > -90:
                self.angulo -= self.VELOCIDADE_ROTACAO



    def desenhar(self, tela):
        #definir imagem do passaro voando
        self.contagem_imagens += 1

        if self.contagem_imagens<self.TEMPO_ANIMACAO:
            self.imagem = self.IMGS[0]

        elif self.contagem_imagens < self.TEMPO_ANIMACAO*2:
            self.imagem = self.IMGS[1]

        elif self.contagem_imagens < self.TEMPO_ANIMACAO*3:
            self.imagem = self.IMGS[2]

        elif self.contagem_imagens < self.TEMPO_ANIMACAO*4:
            self.imagem = self.IMGS[1]

        elif self.contagem_imagens >= self.TEMPO_ANIMACAO*4 +1:
            self.imagem = self.IMGS[0]
            self.contagem_imagens = 0


    #quando o passaro estiver caindo
        if self.angulo <= -80:
            self.imagem = self.IMGS[1]
            self.contagem_imagem = self.TEMPO_ANIMACAO*2

    #desenhar imagem
        imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)
        pos_centro_imagem = self.imagem.get_rect(topleft=(self.x, self.y)).center
        retangulo = imagem_rotacionada.get_rect(center=pos_centro_imagem)
        tela.blit(imagem_rotacionada, retangulo.topleft)

def get_mask(self):
        return pygame.mask.from_surface(self.imagem)

    




class Cano:
    DISTANCIA = 200
    VELOCIDADE = 5

    def __init__(self, x):
        self.x = x
        self.altura = 0
        self.pos_topo = 0
        self.pos_base = 0
        self.CANO_TOPO = pygame.transform.flip(IMAGEM_CANO, False, True )
        self.CANO_BASE = IMAGEM_CANO
        self.passou = False
        self.definir_altura()

def definir_altura(self):
        self.altura = random.range(50, 450)
        self.pos_base = self.altura - self.CANO_TOPO.get_height()
        self.pos_topo = self.altura + self.DISTANCIA

def mover(self):
        self.x -= self.VELOCIDADE

def desenhar(self, tela):
        tela.blit(self.CANO_TOPO, (self.x, self.pos_topo))
        tela.blit(self.CANO_BASE, (self.x, self.pos_base))

def colidir(self, passaro):
        passaro_mask = pygame.mask.from_surface(self.passaro)
        topo_mask =  pygame.mask.from_surface(self.CANO_TOPO)
        base_mask =  pygame.mask.from_surface(self.CANO_BASE)

        distancia_topo = (self.x - passaro.x, self.pos_topo - round(passaro.y))
        distancia_base = (self.x - passaro.x, self.pos_base - round(passaro.x))

        base_ponto = passaro_mask.overlap(base_mask, distancia_base)
        topo_ponto = passaro_mask.overlap(topo_mask, distancia_topo)

        if base_ponto or topo_ponto:
            return True
        else:
            return False



class Chao:
    VELOCIDADE = 5
    LARGURA = IMAGEM_CHAO.get_width()
    IMAGEM = IMAGEM_CHAO

    def __init__(self, y):
        self.y = y 
        self.x0 = 0
        self.x1 = self.LARGURA


def mover(self):
        self.x0 -= self.VELOCIDADE
        self.x1 -= self.VELOCIDADE

        if self.x0 + self.LARGURA < 0:
                self.x0 = self.x1 + self.LARGURA

        if self.x1 + self.LARGURA < 0:
                self.x1 = self.x0 + self.LARGURA

def desenhar(self, tela):
         tela.blit(self.IMAGEM, (self.x0, self.y))
         tela.blit(self.IMAGEM, (self.x1, self.y))



def desenhar_tela(tela, passaros, chao, canos, pontuacao):
        tela.blit(IMAGEM_BACKGROUND, (0, 0))
        for passaro in passaros:
            passaro.desenhar(tela)

        for cano in canos:
            cano.desenhar(tela)

        texto = FONTE_PONTOS.render(f"Pontuação: {pontos}", 1, (255, 255, 255))
        tela.blit(texto, (TELA_LARGURA - 10 - texto.get_width(), 10))

        if ai_jogando:
            texto = FONTE_PONTOS.render(f"Geração: {geracao}", 1, (255, 255, 255))
            tela.blit(texto, (10, 10))


        chao.desenhar(tela)
        pygame.display.update()

def main(genomas, config):
    global geracao
    geracao += 1

    if ai_jogando:
        redes=[]
        lista_genomas=[]
        passaros=[]
    for _, genoma in genomas:
        rede = neat.nn.FeedForwardNetwork.create(genoma, config)
        redes.append(rede)
        genoma.fitness=0
        lista_genomas.append(genoma)
        passaros.append(Passaro(230, 350))
        

    else:
        

        passaros = [Passaro(230, 350)]
        chao = Chao(730)
        canos = [Cano(700)]
        tela = pygame.pygame.set_mode(TELA_LARGURA, TELA_ALTURA)
        pontos = 0
        relogio = pygame.time_Clock()

    jogoRodando = True

    while jogoRodando:
        relogio.tick(30)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                jogoRodando = False
                pygame.quit()
                quit()

            if not ai_jogando:

                if evento.pygame.event.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_SPACE:
                     for passaro in passaros:
                        passaro.pular()

        indice_cano=0
        if len(passaros)>0:
            if len(canos)>1 and passaros[0].x > (canos[0].x + canos[0].CANOS_TOPO.get_width()):
                indice_cano=1

        else:
            jogoRodando=False
            break

        for i, passaro in enumerate(passaros):
            passaro.mover()
            chao.mover()
            lista_genomas[i].fitness+=0.1
            output=redes[i].activate()
            
            if output[0]>0:
                passaro.pular((passaro.y, abs(passaro.y-canos[indice_cano].altura), 
                                          abs(passaro.y-canos[indice_cano].pos_base)))

        
        
        add_canos = False

        for cano in canos:
            remover_canos=[]
            for i, passaros in enumerate(passaros):
                if cano.colidir(passaro):
                    passaros.pop(i)
                    if ai_jogando:
                        lista_genomas[i].fitness-=1
                        lista_genomas.pop(i)
                        redes.pop(i)
                

                if not cano.passou and passaro.x > cano.x:
                    cano.passou = True
                    add_canos = True
            cano.mover()
            if cano.x == cano.CANO_TOPO.get_width()<0:
                    remover_canos.append(cano)

            if add_canos:
                pontos+=1
                canos.append(Cano(600))
                for genoma in lista_genomas:
                    genomas.fitness+=5
            for canos in remover_canos:
                cano.ramover(cano)


            for i, passaro in enumerate(passaros):
                if (passaro.y + passaro.imagem.get_height())>chao.y or passaro.y<0:
                    passaros.pop(1)
                    if ai_jogando:
                        lista_genomas.pop(i)
                        redes.pop(i)
        
            desenhar_tela(tela, passaros, canos, chao, pontos)

def rodar(caminho_config):
    config=neat.config.Config(neat.DefaultGenome,
                              neat.DefaultReproduction,
                              neat.DefaultSpeciesSet,
                              neat.DefaultStagnation,
                              caminho_config)

    populacao = neat.Population(config)
    populacao.add_reporter(neat.StdOutReporter(True))
    populacao.add_reporter(neat.StatisticReporter())

    if ai_jogando:
        populacao.run(main, 50)
    else:
        main(None, None)


if __name__ == '__main__':
    caminho=os.path.dirname(__file__)
    caminho_config=os.path.join(caminho,'config.txt')
    rodar(caminho_config)






    