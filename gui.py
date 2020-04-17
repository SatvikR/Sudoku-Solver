import sys
import pygame
from pygame.locals import *
from colors import *
import solver

pygame.init()

fps = 120
fpsClock = pygame.time.Clock()
grid = solver.board
width, height = 800, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Sudoku Solver")
pygame.display.set_icon(pygame.image.load("icon.png"))
my_font = pygame.font.SysFont('Arial', 40)
button_font = pygame.font.SysFont('Consolas', 35)
button = button_font.render("Solve", False, BLACK)
title_font = pygame.font.SysFont('Consolas', 50)
title = title_font.render("Sudoku Solver", False, BLACK)
pos_font = pygame.font.SysFont("Arial", 25)
unsolved_cords = []


def draw_board():
    global screen
    for row in range(3):
        for col in range(3):
            pygame.draw.rect(screen, BLACK, (100 + (col * 200), 100 + (row * 200), 200, 200), 5)
    for row in range(9):
        for col in range(9):
            pygame.draw.rect(screen, BLACK, (100 + (col * 600 / 9), 100 + (row * 600 / 9), 66, 66), 2)


def draw_cells(board):
    for row in range(9):
        for col in range(9):
            if board[col][row] != 0:
                if (row, col) in unsolved_cords:
                    text_surface = my_font.render(str(board[col][row]), False, BLUE)
                    screen.blit(text_surface, (125 + (row * 600 / 9), 110 + (col * 600 / 9)))
                else:
                    text_surface = my_font.render(str(board[col][row]), False, BLACK)
                    screen.blit(text_surface, (125 + (row * 600 / 9), 110 + (col * 600 / 9)))
            else:
                unsolved_cords.append((row, col))
                possibles = ""
                if solver.finished:
                    for num in solver.cells[col][row].possible:
                        possibles += (" %d" % num)
                    for i, num in enumerate(solver.cells[col][row].possible):
                        y = int(i / 3)
                        x = i - (3 * y)
                        text = pos_font.render(str(num), False, RED)
                        screen.blit(text, (107 + (row * 600 / 9) + (x * 22), 100 + (col * 600 / 9) + (y * 22)))


while True:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            x, y = event.pos
            if 350 < x < 450 and 725 < y < 775:
                if not solver.finished:
                    solver.main()

    # Draw
    draw_board()
    draw_cells(grid)
    pygame.draw.rect(screen, TEAL, (350, 725, 100, 50))
    screen.blit(button, (352, 735))
    screen.blit(title, (230, 25))
    pygame.display.flip()
    fpsClock.tick(fps)
