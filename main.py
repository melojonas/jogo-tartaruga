import pygame
import random
import sys

# Inicialização do Pygame
pygame.init()

# Configurações do jogo
largura_tela = 750
altura_tela = 500
proporcao_tela = 4 / 3
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Jogo da Tartaruguinha")

# Cor de fundo azul
cor_de_fundo = (192,217,217)  # Azul

# Tartaruga
tartaruga_img = pygame.image.load("tartaruga.png")
tartaruga_largura = 100
tartaruga_altura = 75
tartaruga_x = largura_tela // 2 - tartaruga_largura // 2
tartaruga_y = altura_tela - tartaruga_altura
tartaruga_velocidade = 1
vidas = 3  # Inicialmente, a tartaruga tem 3 vidas

# Comida
comida_img = pygame.image.load("comida.png")
comida_largura = 60
comida_altura = 60
comida_x = random.randint(0, largura_tela - comida_largura)
comida_y = 0
comida_velocidade = 0.5

# Lixo
lixo_img = pygame.image.load("lixo.png")
lixo_largura = 60
lixo_altura = 60
lixo_x = random.randint(0, largura_tela - lixo_largura)
lixo_y = 0
lixo_velocidade = 0.5

# Pontuação
pontuacao = 0
fonte = pygame.font.Font(None, 36)

# Tempo limite em segundos
tempo_limite = 60
tempo_inicial = pygame.time.get_ticks()

def mostrar_pontuacao():
    texto = fonte.render(f'Pontuação: {pontuacao}', True, (255, 255, 255))  # Branco
    tela.blit(texto, (10, 10))

def mostrar_vidas():
    texto = fonte.render(f'Vidas: {vidas}', True, (0, 0, 0))  # Preto
    tela.blit(texto, (10, 50))

def mostrar_tempo_restante(tempo_restante):
    texto = fonte.render(f'Tempo Restante: {tempo_restante} s', True, (255, 255, 255))  # Branco
    # Posição proporcional
    texto_rect = texto.get_rect()
    texto_rect.right = largura_tela - 10
    texto_rect.top = 10
    tela.blit(texto, texto_rect)

# Telas de "perdeu" e "venceu"
def tela_perdeu():
    tela.fill((255, 0, 0))  # Fundo vermelho
    texto = fonte.render("QUE TISTREZA.... PERDEU!", True, (255, 255, 255))  # Texto branco
    tela.blit(texto, (largura_tela // 2 - texto.get_width() // 2, altura_tela // 2 - texto.get_height() // 2))
    pygame.display.update()
    esperar_tecla()

def tela_venceu():
    tela.fill((0, 255, 0))  # Fundo verde
    texto = fonte.render("PARABÉNS! SALVOU A TARTARUGUINIA", True, (255, 255, 255))  # Texto branco
    tela.blit(texto, (largura_tela // 2 - texto.get_width() // 2, altura_tela // 2 - texto.get_height() // 2))
    pygame.display.update()
    esperar_tecla()

def esperar_tecla():
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                esperando = False

# Loop principal do jogo
jogando = True
while jogando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jogando = False

    # Verifica o tempo decorrido
    tempo_atual = pygame.time.get_ticks()
    tempo_decorrido = (tempo_atual - tempo_inicial) // 1000  # Converte para segundos

    # Verifica se o tempo limite foi atingido
    if tempo_decorrido >= tempo_limite:
        jogando = False

    # Movimento da tartaruga
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT] and tartaruga_x > 0:
        tartaruga_x -= tartaruga_velocidade
    if teclas[pygame.K_RIGHT] and tartaruga_x < largura_tela - tartaruga_largura:
        tartaruga_x += tartaruga_velocidade

    # Movimento da comida
    comida_y += comida_velocidade

    # Colisão com a comida
    if tartaruga_x < comida_x + comida_largura and tartaruga_x + tartaruga_largura > comida_x and tartaruga_y < comida_y + comida_altura and tartaruga_y + tartaruga_altura > comida_y:
        pontuacao += 1
        comida_x = random.randint(0, largura_tela - comida_largura)
        comida_y = 0

    # Verifica se a comida atingiu o fundo da tela
    if comida_y > altura_tela:
        comida_x = random.randint(0, largura_tela - comida_largura)
        comida_y = 0

    # Movimento do lixo
    lixo_y += lixo_velocidade

    # Colisão com o lixo
    if tartaruga_x < lixo_x + lixo_largura and tartaruga_x + tartaruga_largura > lixo_x and tartaruga_y < lixo_y + lixo_altura and tartaruga_y + tartaruga_altura > lixo_y:
        vidas -= 1
        lixo_x = random.randint(0, largura_tela - lixo_largura)
        lixo_y = 0

    # Verifica se o lixo atingiu o fundo da tela
    if lixo_y > altura_tela:
        lixo_x = random.randint(0, largura_tela - lixo_largura)
        lixo_y = 0

    # Preenche a tela com a cor de fundo azul
    tela.fill(cor_de_fundo)

    # Desenha a tartaruga com as novas proporções
    tela.blit(pygame.transform.scale(tartaruga_img, (tartaruga_largura, tartaruga_altura)), (tartaruga_x, tartaruga_y))

    # Desenha a comida com as novas proporções
    tela.blit(pygame.transform.scale(comida_img, (comida_largura, comida_altura)), (comida_x, comida_y))

    # Desenha o lixo com as novas proporções
    tela.blit(pygame.transform.scale(lixo_img, (lixo_largura, lixo_altura)), (lixo_x, lixo_y))

    # Mostra a pontuação na tela
    mostrar_pontuacao()

    # Mostra o número de vidas na tela
    mostrar_vidas()

    # Mostra o tempo restante na tela
    tempo_restante = tempo_limite - tempo_decorrido
    mostrar_tempo_restante(tempo_restante)

    # Verifica se o jogador perdeu todas as vidas
    if vidas <= 0:
        jogando = False
        tela_perdeu()

    # Verifica se o jogador atingiu a pontuação desejada (por exemplo, 10 pontos)
    if tempo_decorrido >= tempo_limite:
        jogando = False
        tela_venceu()

    # Atualiza a tela
    pygame.display.update()

# Fim do jogo
pygame.quit()
sys.exit()
