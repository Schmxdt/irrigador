# Controle do Robô Irrigador

Este projeto simula o controle de um robô irrigador para uma horta. O robô pode mover-se por uma área de cultivo (representada como uma grade) e irrigar os canteiros selecionados. O sistema permite controlar o movimento do robô, visualizar os canteiros irrigados, e fornece uma interface para iniciar novas irrigação.

## Tecnologias

- **Python 3.x**
- **Pygame** - Biblioteca para criar jogos e simulações gráficas.

## Funcionalidades

1. **Entrada do Usuário:**
   - O usuário define o tamanho da horta (em X e Y).
   - O usuário define a posição inicial do robô e sua direção (Norte, Sul, Leste, Oeste).
   - O usuário escolhe a quantidade de canteiros a serem irrigados e suas posições.

2. **Movimento do Robô:**
   - O robô pode se mover usando os comandos:
     - **D**: Virar à direita.
     - **E**: Virar à esquerda.
     - **M**: Mover uma célula para frente.
     - **I**: Irrigar a célula atual.

3. **Visualização:**
   - O estado da horta é visualizado em uma tela gráfica.
   - A tela mostra a posição do robô, os canteiros irrigados e o caminho percorrido.

4. **Interação:**
   - O usuário pode enviar comandos usando as teclas do teclado:
     - **Setas Direcionais**: Controlam a direção do robô.
     - **Espaço**: Irriga a célula atual, caso seja um canteiro.
     - **Comandos D, E, M, I**: Definem a movimentação e ações do robô.

5. **Reinício:**
   - Após irrigar todos os canteiros, o usuário é questionado se deseja iniciar uma nova irrigação.

## Como Rodar o Projeto

1. **Instalar Dependências:**

   Antes de rodar o projeto, é necessário instalar a biblioteca **pygame**. Execute o seguinte comando:

   ```bash
   pip install pygame

Executar o Código:

Após a instalação, basta rodar o arquivo Python para iniciar a simulação.

bash
Copiar
python robo_irrigador.py
Interação:

Quando o programa for executado, o usuário verá uma janela gráfica com a simulação da horta.
O programa solicita as entradas do usuário para configurar a horta, a posição do robô, e os canteiros.
Use as setas para mover o robô e o espaço para irrigar os canteiros.
Explicação do Código
Pygame é utilizado para criar a interface gráfica, onde o estado da horta é mostrado em tempo real.
O robô é representado por um triângulo que aponta para a direção em que ele está se movendo.
O caminho percorrido é exibido ao longo do movimento do robô, além das linhas conectando os pontos que indicam por onde ele passou.
O controle do movimento é feito por comandos simples: virar à esquerda (E), virar à direita (D), mover-se para frente (M), e irrigar (I).
O usuário pode reiniciar o processo de irrigação a qualquer momento, permitindo simulações contínuas.
Licença
Este projeto é de código aberto e está licenciado sob a Licença MIT.

perl
Copiar

Você pode copiar e colar esse conteúdo no arquivo `README.md` do seu projeto.
