import pygame
import time

def obter_inteiro(mensagem):
    while True:
        try:
            return int(input(mensagem))
        except ValueError:
            print("Entrada inválida! Digite um número inteiro.")

def obter_direcao(mensagem):
    while True:
        direcao = input(mensagem).upper()
        if direcao in ['N', 'S', 'L', 'O']:
            return direcao
        print("Entrada inválida! Digite N, S, L ou O.")

# Solicitação de entrada do usuário
tamanho_x = obter_inteiro("Digite o tamanho da horta em X: ")
tamanho_y = obter_inteiro("Digite o tamanho da horta em Y: ")
posicao_x = obter_inteiro("Digite a posição inicial X do robô: ")
posicao_y = obter_inteiro("Digite a posição inicial Y do robô: ")
direcao = obter_direcao("Digite a direção inicial do robô (N, S, L, O): ")

# Solicitação dos canteiros a serem irrigados
canteiros = []
n_canteiros = obter_inteiro("Quantos canteiros deseja irrigar? ")
for _ in range(n_canteiros):
    while True:
        try:
            cx, cy = map(int, input("Digite a posição X e Y do canteiro separados por espaço: ").split())
            if 0 <= cx < tamanho_x and 0 <= cy < tamanho_y:
                canteiros.append((cx, cy))
                break
            else:
                print("Canteiro fora dos limites! Digite valores dentro da horta.")
        except ValueError:
            print("Entrada inválida! Digite dois números inteiros separados por espaço.")

direcoes = ['N', 'L', 'S', 'O']
dir_index = direcoes.index(direcao)

# Inicializar pygame
pygame.init()

# Configurações da tela
tela_largura, tela_altura = 500, 500
tela = pygame.display.set_mode((tela_largura, tela_altura))
pygame.display.set_caption("Controle do Robô Irrigador")

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERDE = (0, 255, 0)  # Canteiros irrigados
VERMELHO = (255, 0, 0)  # Robô
AZUL = (0, 0, 255)  # Canteiros a serem irrigados

# Tamanho da célula
tam_celula = min(tela_largura // tamanho_x, tela_altura // tamanho_y)

# Posição do robô
robot_x, robot_y = posicao_x, posicao_y
canteiros_irrigados = set()

# Loop principal
rodando = True
while rodando:
    tela.fill(BRANCO)
    
    # Desenha a grade e os canteiros a serem irrigados
    for x in range(tamanho_x):
        for y in range(tamanho_y):
            cor = VERDE if (x, y) in canteiros_irrigados else (AZUL if (x, y) in canteiros else BRANCO)
            pygame.draw.rect(tela, cor, (x * tam_celula, y * tam_celula, tam_celula, tam_celula), 0)
            pygame.draw.rect(tela, PRETO, (x * tam_celula, y * tam_celula, tam_celula, tam_celula), 1)
    
    # Desenha o robô e indica sua direção (seta para onde aponta)
    centro_x = robot_x * tam_celula + tam_celula // 2
    centro_y = robot_y * tam_celula + tam_celula // 2
    if direcoes[dir_index] == 'N':
        pontos = [(centro_x, centro_y - tam_celula // 2), (centro_x - tam_celula // 2, centro_y + tam_celula // 2), (centro_x + tam_celula // 2, centro_y + tam_celula // 2)]
    elif direcoes[dir_index] == 'S':
        pontos = [(centro_x, centro_y + tam_celula // 2), (centro_x - tam_celula // 2, centro_y - tam_celula // 2), (centro_x + tam_celula // 2, centro_y - tam_celula // 2)]
    elif direcoes[dir_index] == 'L':
        pontos = [(centro_x + tam_celula // 2, centro_y), (centro_x - tam_celula // 2, centro_y - tam_celula // 2), (centro_x - tam_celula // 2, centro_y + tam_celula // 2)]
    else:  # Oeste (O)
        pontos = [(centro_x - tam_celula // 2, centro_y), (centro_x + tam_celula // 2, centro_y - tam_celula // 2), (centro_x + tam_celula // 2, centro_y + tam_celula // 2)]
    
    pygame.draw.polygon(tela, VERMELHO, pontos)
    
    pygame.display.flip()
    
    # Captura eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                dir_index = (dir_index + 1) % 4  # Direita
            elif event.key == pygame.K_LEFT:
                dir_index = (dir_index - 1) % 4  # Esquerda
            elif event.key == pygame.K_UP:
                if direcoes[dir_index] == 'N' and robot_y > 0:
                    robot_y -= 1
                elif direcoes[dir_index] == 'S' and robot_y < tamanho_y - 1:
                    robot_y += 1
                elif direcoes[dir_index] == 'L' and robot_x < tamanho_x - 1:
                    robot_x += 1
                elif direcoes[dir_index] == 'O' and robot_x > 0:
                    robot_x -= 1
            elif event.key == pygame.K_SPACE:
                if (robot_x, robot_y) in canteiros:
                    canteiros_irrigados.add((robot_x, robot_y))  # Irrigar canteiro
    
    time.sleep(0.1)

pygame.quit()