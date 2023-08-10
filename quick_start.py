import copy
import random
import sys
from dataclasses import dataclass

import pygame as pg
import pygame_gui as gui

pg.init()
pg.display.set_caption('Main menu')
window_surface = pg.display.set_mode([500, 500])
MANAGER = gui.UIManager((500, 500), "data/themes/quick_theme.json")
background = pg.Surface([500, 500])
background.fill("#ffc0cb")
clock = pg.time.Clock()


def automa(field_width, cell_number, initual_conditions):
    res = field_width
    size = cell_number

    automa_background = pg.Surface([res, res])
    automa_background.fill("#ffc0cb")

    pink = pg.image.load("pink.png")
    white = pg.image.load("white.png")
    scale = res // size
    pink = pg.transform.scale(pink, [scale - 1, scale - 1])
    white = pg.transform.scale(white, [scale - 1, scale - 1])

    neighbors = [(0, 0), (0, 1), (0, -1), (-1, 0), (1, 0)]

    function = map(int, bin(372)[2:].zfill(32))
    list_function = list(function)[::-1]

    game_round = 0
    previous_rounds = []

    @dataclass
    class Cell:
        row: int
        col: int
        is_alive: bool = False
        f_count: int = 0

        def count_neighbors(self):
            n = 0
            for pos in range(len(neighbors)):
                self.row = self.row + neighbors[pos][0]
                self.col = self.col + neighbors[pos][1]
                if 0 <= row < size and 0 <= col < size:
                    cell = matrix[row * size + col]
                    if cell.is_alive:
                        n += pow(2, pos)
            self.f_count = n

        def show(self):
            pos = [self.row * scale, self.col * scale]
            if self.is_alive:
                automa_window_surface.blit(pink, pos)
            else:
                automa_window_surface.blit(white, pos)

    matrix = [Cell(i, j) for i in range(size) for j in range(size)]

    if initual_conditions:
        for cell in matrix:
            if (random.randint(0, 100)) % 2 == 0:
                cell.is_alive = False
            else:
                cell.is_alive = True

    automa_window_surface = pg.display.set_mode([res, res])
    automa_window_surface.blit(automa_background, [0, 0])
    pg.display.set_caption('Cellular automa')
    automa_manager = gui.UIManager((res, res))

    while True:

        time_delta = clock.tick(60) / 1000.0

        for cell in matrix:
            cell.show()
        pg.display.flip()

        for event in pg.event.get():

            if event.type == pg.QUIT:
                main_menu()

            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pg.mouse.get_pos()
                row = mouse_x // scale
                col = mouse_y // scale
                i = row * size + col
                cell = matrix[i]

                if pg.mouse.get_pressed()[0]:
                    cell.is_alive = True

                if pg.mouse.get_pressed()[2]:
                    cell.is_alive = False

            if event.type == pg.KEYDOWN:

                if event.key == pg.K_RIGHT:

                    game_round += 1
                    previous_rounds.append(copy.deepcopy(matrix))

                    for cell in matrix:
                        cell.count_neighbors()

                    for cell in matrix:
                        if list_function[cell.f_count] != 1:
                            cell.is_alive = False
                        else:
                            cell.is_alive = True

                if event.key == pg.K_LEFT:
                    if game_round > 0:
                        matrix = previous_rounds[-1]
                        del previous_rounds[-1]
                        game_round -= 1

                if event.key == pg.K_r:
                    for cell in matrix:
                        cell.is_alive = False
            automa_manager.process_events(event)
        automa_manager.update(time_delta)
        automa_manager.draw_ui(automa_window_surface)
        pg.display.update()


def start():
    is_running = True

    field_width = 300
    cn_number = 10
    initual_conditions = False

    ok_button = gui.elements.UIButton(relative_rect=pg.Rect(50, 400, 200, 50), text="OK")
    back_button = gui.elements.UIButton(relative_rect=pg.Rect(250, 400, 200, 50), text="BACK")

    fw_text = pg.font.Font("data/fonts/font.ttf", 20).render("Choose field width", True,
                                                             "White")
    fw_options = ["300", "400", "500", "600", "700"]
    cn_options = ["10", "15", "20", "25", "30", "40", "50"]
    ic_options = ["No", "Yes"]

    cn_text = pg.font.Font("data/fonts/font.ttf", 20).render("Choose number of cells", True,
                                                             "White")
    ic_text_1 = pg.font.Font("data/fonts/font.ttf", 20).render("Do you want random", True,
                                                               "White")
    ic_text_2 = pg.font.Font("data/fonts/font.ttf", 20).render("initial conditions?", True,
                                                               "White")

    field_width_menu = gui.elements.UIDropDownMenu(fw_options, "300", relative_rect=pg.Rect(150, 75, 200, 50))

    cell_number_menu = gui.elements.UIDropDownMenu(cn_options, "10", relative_rect=pg.Rect(150, 175, 200, 50))

    ic_menu = gui.elements.UIDropDownMenu(ic_options, "No", relative_rect=pg.Rect(150, 300, 200, 50))

    while is_running:

        time_delta = clock.tick(60) / 1000.0

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == gui.UI_BUTTON_PRESSED:
                if event.ui_element == ok_button:
                    for buttons in [ok_button, back_button, field_width_menu, cell_number_menu, ic_menu]:
                        buttons.hide()
                    automa(field_width, cn_number, initual_conditions)
                if event.ui_element == back_button:
                    for buttons in [ok_button, back_button, field_width_menu, cell_number_menu, ic_menu]:
                        buttons.hide()
                    main_menu()
            if event.type == gui.UI_DROP_DOWN_MENU_CHANGED:
                if event.ui_element == field_width_menu:
                    field_width = int(field_width_menu.selected_option)
                if event.ui_element == cell_number_menu:
                    cn_number = int(cell_number_menu.selected_option)
                if event.ui_element == ic_menu:
                    if ic_menu.selected_option == "Yes":
                        initual_conditions = True
            MANAGER.process_events(event)

        MANAGER.update(time_delta)

        window_surface.blit(background, [0, 0])
        window_surface.blit(fw_text, fw_text.get_rect(center=(250, 50)))
        window_surface.blit(cn_text, cn_text.get_rect(center=(250, 150)))
        window_surface.blit(ic_text_1, ic_text_1.get_rect(center=(250, 250)))
        window_surface.blit(ic_text_2, ic_text_2.get_rect(center=(250, 275)))
        MANAGER.draw_ui(window_surface)

        pg.display.update()


def main_menu():
    main_window_surface = pg.display.set_mode([500, 500])
    is_running = True

    text_2d = pg.font.Font('data/fonts/font.ttf', 50).render("2D", True, "White")
    text_cellular = pg.font.Font('data/fonts/font.ttf', 50).render("CELLULAR", True, "White")
    text_automata = pg.font.Font('data/fonts/font.ttf', 50).render("AUTOMATA", True, "White")

    start_button = gui.elements.UIButton(relative_rect=pg.Rect(100, 230, 300, 70), text="START")

    quit_button = gui.elements.UIButton(relative_rect=pg.Rect(100, 350, 300, 70), text="QUIT")

    while is_running:

        time_delta = clock.tick(60) / 1000.0

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == gui.UI_BUTTON_PRESSED:
                if event.ui_element == start_button:
                    for button in [start_button, quit_button]:
                        button.hide()
                    start()
                if event.ui_element == quit_button:
                    pg.quit()
                    sys.exit()
            MANAGER.process_events(event)

        MANAGER.update(time_delta)

        main_window_surface.blit(background, [0, 0])
        main_window_surface.blit(text_2d, text_2d.get_rect(center=(250, 50)))
        main_window_surface.blit(text_cellular, text_cellular.get_rect(center=(250, 100)))
        main_window_surface.blit(text_automata, text_automata.get_rect(center=(250, 150)))
        MANAGER.draw_ui(main_window_surface)

        pg.display.update()


main_menu()
