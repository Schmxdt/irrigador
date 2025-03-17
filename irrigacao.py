import pygame
import time

# Inicializar pygame
pygame.init()

# Configurações da tela
tela_largura, tela_altura = 600, 600
tela = pygame.display.set_mode((tela_largura, tela_altura))
pygame.display.set_caption("Controle do Robô Irrigador")

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERDE = (0, 255, 0)  # Canteiros irrigados
VERMELHO = (255, 0, 0)  # Robô
AZUL = (0, 0, 255)  # Canteiros a serem irrigados
CINZA = (200, 200, 200)  # Caminho percorrido

# Fonte
fonte = pygame.font.Font(None, 30)

# Armazena os comandos executados
comandos_executados = ""
caminho_percorrido = []

def capturar_input(pergunta, tipo=int, validacao=None):
    input_text = ""
    rodando = True
    direcoes = ['N', 'L', 'S', 'O']
    while rodando:
        tela.fill(BRANCO)
        instrucao = fonte.render(pergunta, True, PRETO)
        tela.blit(instrucao, (20, 20))
        pygame.draw.rect(tela, PRETO, (20, 60, 500, 40), 2)
        texto_surface = fonte.render(input_text, True, PRETO)
        tela.blit(texto_surface, (30, 70))
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    try:
                        valor = tipo(input_text)
                        if validacao and not validacao(valor):
                            input_text = ""
                        else:
                            return valor
                    except ValueError:
                        input_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

def iniciar_nova_irrigacao():
    global tamanho_x, tamanho_y, posicao_x, posicao_y, direcao, canteiros, canteiros_irrigados, dir_index, comandos_executados, robot_x, robot_y, tam_celula, caminho_percorrido
    
    tamanho_x = capturar_input("Digite o tamanho da horta em X:", int, lambda v: v > 0)
    tamanho_y = capturar_input("Digite o tamanho da horta em Y:", int, lambda v: v > 0)
    posicao_x = capturar_input("Digite a posição inicial X do robô:", int, lambda v: 0 <= v < tamanho_x)
    posicao_y = capturar_input("Digite a posição inicial Y do robô:", int, lambda v: 0 <= v < tamanho_y)
    direcao = capturar_input("Digite a direção inicial do robô (N, S, L, O):", str, lambda v: v.upper() in ['N', 'S', 'L', 'O']).upper()
    
    canteiros = []
    n_canteiros = capturar_input("Quantos canteiros deseja irrigar?", int, lambda v: v > 0)
    for _ in range(n_canteiros):
        while True:
            cx = capturar_input("Digite a posição X do canteiro:", int, lambda v: 0 <= v < tamanho_x)
            cy = capturar_input("Digite a posição Y do canteiro:", int, lambda v: 0 <= v < tamanho_y)
            if (cx, cy) not in canteiros:
                canteiros.append((cx, cy))
                break
    
    # Validação da entrada
    direcoes = ['N', 'L', 'S', 'O']
    dir_index = direcoes.index(direcao)
    
    # Redefinir variáveis para nova irrigação
    canteiros_irrigados = set()
    comandos_executados = ""
    caminho_percorrido = []
    robot_x, robot_y = posicao_x, posicao_y
    tam_celula = min(tela_largura // tamanho_x, tela_altura // tamanho_y)

def mostrar_preview():
    global robot_x, robot_y, dir_index, caminho_percorrido
    robot_x, robot_y = posicao_x, posicao_y
    dir_index = direcoes.index(direcao)
    caminho_percorrido = [(robot_x, robot_y)]
    
    for comando in comandos_executados:
        if comando == 'D':
            dir_index = (dir_index + 1) % 4
        elif comando == 'E':
            dir_index = (dir_index - 1) % 4
        elif comando == 'M':
            if direcoes[dir_index] == 'N' and robot_y > 0:
                robot_y -= 1
            elif direcoes[dir_index] == 'S' and robot_y < tamanho_y - 1:
                robot_y += 1
            elif direcoes[dir_index] == 'L' and robot_x < tamanho_x - 1:
                robot_x += 1
            elif direcoes[dir_index] == 'O' and robot_x > 0:
                robot_x -= 1
            caminho_percorrido.append((robot_x, robot_y))
        elif comando == 'I':
            canteiros_irrigados.add((robot_x, robot_y))
        
        tela.fill(BRANCO)
        for x in range(tamanho_x):
            for y in range(tamanho_y):
                cor = VERDE if (x, y) in canteiros_irrigados else (AZUL if (x, y) in canteiros else BRANCO)
                pygame.draw.rect(tela, cor, (x * tam_celula, y * tam_celula, tam_celula, tam_celula), 0)
                pygame.draw.rect(tela, PRETO, (x * tam_celula, y * tam_celula, tam_celula, tam_celula), 1)
        
        for (px, py) in caminho_percorrido:
            pygame.draw.rect(tela, CINZA, (px * tam_celula, py * tam_celula, tam_celula, tam_celula), 1)
        
        if direcoes[dir_index] == 'N':
            pontos = [(robot_x * tam_celula + tam_celula // 2, robot_y * tam_celula), 
                      (robot_x * tam_celula, robot_y * tam_celula + tam_celula), 
                      (robot_x * tam_celula + tam_celula, robot_y * tam_celula + tam_celula)]
        elif direcoes[dir_index] == 'S':
            pontos = [(robot_x * tam_celula, robot_y * tam_celula), 
                      (robot_x * tam_celula + tam_celula, robot_y * tam_celula), 
                      (robot_x * tam_celula + tam_celula // 2, robot_y * tam_celula + tam_celula)]
        elif direcoes[dir_index] == 'L':
            pontos = [(robot_x * tam_celula, robot_y * tam_celula), 
                      (robot_x * tam_celula, robot_y * tam_celula + tam_celula), 
                      (robot_x * tam_celula + tam_celula, robot_y * tam_celula + tam_celula // 2)]
        elif direcoes[dir_index] == 'O':
            pontos = [(robot_x * tam_celula + tam_celula, robot_y * tam_celula), 
                      (robot_x * tam_celula + tam_celula, robot_y * tam_celula + tam_celula), 
                      (robot_x * tam_celula, robot_y * tam_celula + tam_celula // 2)]
        
        pygame.draw.polygon(tela, VERMELHO, pontos)
        
        status_texto = fonte.render(f"Irrigados: {len(canteiros_irrigados)}/{len(canteiros)}", True, PRETO)
        comandos_texto = fonte.render(f"Comandos: {comandos_executados}", True, PRETO)
        tela.blit(status_texto, (20, tela_altura - 40))
        tela.blit(comandos_texto, (20, tela_altura - 60))
        
        pygame.display.flip()
        time.sleep(0.5)

# Iniciar a primeira irrigação
iniciar_nova_irrigacao()

# Loop principal
direcoes = ['N', 'L', 'S', 'O']
rodando = True
while rodando:
    tela.fill(BRANCO)
    
    # Desenha a grade e os canteiros a serem irrigados
    for x in range(tamanho_x):
        for y in range(tamanho_y):
            cor = VERDE if (x, y) in canteiros_irrigados else (AZUL if (x, y) in canteiros else BRANCO)
            pygame.draw.rect(tela, cor, (x * tam_celula, y * tam_celula, tam_celula, tam_celula), 0)
            pygame.draw.rect(tela, PRETO, (x * tam_celula, y * tam_celula, tam_celula, tam_celula), 1)
    
   # Desenha o caminho percorrido
    for (px, py) in caminho_percorrido:
        # Desenha o contorno do bloco
        pygame.draw.rect(tela, CINZA, (px * tam_celula, py * tam_celula, tam_celula, tam_celula), 1)
        
        # Desenha uma linha no meio do bloco
        if len(caminho_percorrido) > 1:
            centro_x = (px * tam_celula) + tam_celula // 2
            centro_y = (py * tam_celula) + tam_celula // 2
            pygame.draw.line(tela, CINZA, (centro_x - tam_celula // 4, centro_y), (centro_x + tam_celula // 4, centro_y), 1)
            pygame.draw.line(tela, CINZA, (centro_x, centro_y - tam_celula // 4), (centro_x, centro_y + tam_celula // 4), 1)

    # Desenha o robô como um triângulo para indicar a direção
    if direcoes[dir_index] == 'N':
        pontos = [(robot_x * tam_celula + tam_celula // 2, robot_y * tam_celula), 
                  (robot_x * tam_celula, robot_y * tam_celula + tam_celula), 
                  (robot_x * tam_celula + tam_celula, robot_y * tam_celula + tam_celula)]
    elif direcoes[dir_index] == 'S':
        pontos = [(robot_x * tam_celula, robot_y * tam_celula), 
                  (robot_x * tam_celula + tam_celula, robot_y * tam_celula), 
                  (robot_x * tam_celula + tam_celula // 2, robot_y * tam_celula + tam_celula)]
    elif direcoes[dir_index] == 'L':
        pontos = [(robot_x * tam_celula, robot_y * tam_celula), 
                  (robot_x * tam_celula, robot_y * tam_celula + tam_celula), 
                  (robot_x * tam_celula + tam_celula, robot_y * tam_celula + tam_celula // 2)]
    elif direcoes[dir_index] == 'O':
        pontos = [(robot_x * tam_celula + tam_celula, robot_y * tam_celula), 
                  (robot_x * tam_celula + tam_celula, robot_y * tam_celula + tam_celula), 
                  (robot_x * tam_celula, robot_y * tam_celula + tam_celula // 2)]
    
    pygame.draw.polygon(tela, VERMELHO, pontos)
    
    # Exibe a lista de canteiros irrigados e comandos
    status_texto = fonte.render(f"Irrigados: {len(canteiros_irrigados)}/{len(canteiros)}", True, PRETO)
    comandos_texto = fonte.render(f"Comandos: {comandos_executados}", True, PRETO)
    tela.blit(status_texto, (20, tela_altura - 40))
    tela.blit(comandos_texto, (20, tela_altura - 60))
    
    pygame.display.flip()
    
    # Captura eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                dir_index = (dir_index + 1) % 4  # Direita
                comandos_executados += "D"
            elif event.key == pygame.K_LEFT:
                dir_index = (dir_index - 1) % 4  # Esquerda
                comandos_executados += "E"
            elif event.key == pygame.K_UP:
                if direcoes[dir_index] == 'N' and robot_y > 0:
                    robot_y -= 1
                elif direcoes[dir_index] == 'S' and robot_y < tamanho_y - 1:
                    robot_y += 1
                elif direcoes[dir_index] == 'L' and robot_x < tamanho_x - 1:
                    robot_x += 1
                elif direcoes[dir_index] == 'O' and robot_x > 0:
                    robot_x -= 1
                comandos_executados += "M"
                caminho_percorrido.append((robot_x, robot_y))
            elif event.key == pygame.K_SPACE:
                if (robot_x, robot_y) in canteiros:
                    canteiros_irrigados.add((robot_x, robot_y))  # Irrigar canteiro
                    comandos_executados += "I"  # Registrar irrigação
                    if set(canteiros) == canteiros_irrigados:
                        pygame.time.delay(500)
                        texto = fonte.render("Todos os canteiros foram irrigados!", True, PRETO)
                        tela.blit(texto, (20, 20))
                        pygame.display.flip()
                        mostrar_preview()
                        resposta = capturar_input("Deseja fazer uma nova irrigação? (S/N)", str, lambda v: v.upper() in ['S', 'N']).strip().upper()
                        if resposta == 'S' or resposta == 'Y':
                            iniciar_nova_irrigacao()
                        if resposta == 'N':
                            rodando = False
    
    time.sleep(0.1)

pygame.quit()