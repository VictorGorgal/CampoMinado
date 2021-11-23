import random
import pygame

pygame.init()
black = (0, 0, 0)
gray = (64, 64, 64)
blue = (0, 0, 255)
dark_blue = (0, 0, 153)
red = (255, 0, 0)
green = (0, 255, 0)
windowX = 719
windowY = 719
screen = pygame.display.set_mode((windowY, windowX), pygame.RESIZABLE)
screen.fill(black)

board = []
discovered = []
guess = []
boardLenght = 16
bombnumber = 35

font = pygame.font.Font('freesansbold.ttf', 14)


def Dtext(text, x, y):  # funcao que recebe o texto e as coordenadas e escreve na tela
    textRect = text.get_rect()
    textRect.center = (x + 22, y + 22)
    screen.blit(text, textRect)


def create():  # cria o tabuleiro do campo minado
    global board, discovered, guess
    linha = ''
    for y in range(boardLenght):  # gera o tabuleiro
        for x in range(boardLenght):
            discovered.append(0)
            guess.append(0)
            board.append(0)
    for bid in range(bombnumber):
        bomb = random.randint(0, 255)
        while board[bomb] == -1:
            bomb = random.randint(0, 255)
        board[bomb] = -1

    print('-' * 30)
    for tileID, tileV in enumerate(board):  # printa no console o tabuleiro (proposito de debugging)
        if tileV != -1:
            count = 0
            for ty in range(3):
                for tx in range(3):
                    x = tx - 1
                    y = ty - 1

                    tiley = tileID // 16
                    tilex = tileID % 16

                    if y + tiley > 15 or y + tiley < 0 or x + tilex > 15 or x + tilex < 0:
                        pass
                    else:
                        h = (y + tiley) * 16 + (x + tilex)
                        if board[h] == -1:
                            count += 1
            board[tileID] = count
    for y in range(boardLenght):
        for x in range(boardLenght):
            i = y * 16 + x
            if board[i] == -1:
                linha += " "
            else:
                linha += "  "
            linha += str(board[i])

        print(linha)
        linha = ""


def draw():  # renderiza o tabuleiro na tela
    for y in range(boardLenght):
        for x in range(boardLenght):
            pygame.draw.rect(screen, gray, [x * 45, y * 45, 44, 44])
            i = y * 16 + x
            value = board[i]
            cor = str(value)

            if value == -1:
                text = font.render(cor, True, red)
            elif value == 0:
                text = font.render('-', True, black)
            elif value == 1 or value == 5:
                text = font.render(cor, True, blue)
            elif value == 2 or value == 6:
                text = font.render(cor, True, green)
            elif value == 3 or value == 7:
                text = font.render(cor, True, red)
            elif value == 4 or value == 8:
                text = font.render(cor, True, dark_blue)

            if discovered[i] == 1:
                Dtext(text, x * 45, y * 45)

            if guess[i] == 1:
                drawFlag(x, y)


def drawFlag(x, y):  # funcao usada para desenhar a bandeira passando a coordenada
    pygame.draw.polygon(screen, red, [(x * 45 + 22, y * 45 + 4),
                                      (x * 45 + 22, y * 45 + 14),
                                      (x * 45 + 12, y * 45 + 9)])
    pygame.draw.line(screen, black, (x * 45 + 22, y * 45 + 15), (x * 45 + 22, y * 45 + 35), 1)


def drawCross(x, y):  # funcao usada para desenhar o X passando a coordenada
    pygame.draw.line(screen, red, (x * 45, y * 45), (x * 45 + 43, y * 45 + 43))
    pygame.draw.line(screen, red, (x * 45 + 43, y * 45), (x * 45, y * 45 + 43))


def path(start):
    # Algoritmo recursivo de pathfinding para achar todos os quadrados que nao sao adjacentes a uma bomba
    # Inicialmente comeca com o quadrado clicado, checa os 8 quadrados a sua volta e adiciona os
    # iguais a 0 de volta na lista toTest
    toTest = []
    if str(type(start)).find("list") != -1:
        toTest = start.copy()
    else:
        if board[start] == 0:
            discovered[start] = 1
            toTest.append(start)
        else:
            discovered[start] = 1

    for test in toTest:
        for Dy in range(3):
            for Dx in range(3):
                x = Dx - 1
                y = Dy - 1
                if x == 0 and y == 0:
                    pass
                else:
                    testy = test // 16
                    testx = test % 16

                    if y + testy > 15 or y + testy < 0:
                        y = 0
                    if x + testx > 15 or x + testx < 0:
                        x = 0

                    h = (testy + y) * 16 + (testx + x)
                    if board[h] == 0 and discovered[h] == 0:
                        toTest.append(h)
                        discovered[h] = 1
                    if board != -1 and discovered[h] == 0:
                        discovered[h] = 1

        toTest.remove(test)
    if len(toTest) != 0:
        path(toTest)


def status_check(idx):  # verifica se o jogador ganhou ou perdeu
    if board[idx] == -1:
        print("you lost!")
        return False

    if discovered.count(0) == board.count(-1):
        print("Voce ganhou!")

    return True


create()

game = True

while game:  # main loop
    screen.fill(black)
    draw()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mousex, mousey = event.pos
            print("click: ", mousex // 45, mousey // 45)
            mousex = mousex // 45
            mousey = mousey // 45
            id = mousey * 16 + mousex
            if event.button == 1:
                if guess[id] == 1:
                    guess[id] = 0
                path(id)
                game = status_check(id)
            elif event.button == 3 and discovered[id] == 0:
                guess[id] += 1
                if guess[id] == 2:
                    guess[id] = 0

        pygame.display.update()

while True:  # encerra o jogo e mostra a posicao das bombas
    screen.fill(black)

    draw()
    for i in range(256):
        discovered[i] = 1
        if guess[i] == 1 and board[i] != -1:
            drawFlag(i % 16, i // 16)
            drawCross(i % 16, i // 16)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        pygame.display.update()
