#!/usr/bin/env python3

if __name__ == "__main__":

    from math import pi
    from input_box import InputBox
    from draw_elephant_utils import PROPORTION_ORIGINAL_DRAWING
    from screen_utils import init_window, clear_screen
    from points_acquisition import get_points, sampling_points
    from decompositionEnSerieDeFourier import decompositions_en_serie_de_fourier
    from series_cercles import SeriesCercles
    from point import Point2D
    from constructed_rectangle import create_input_boxes

    from drawing_rectangle import DrawingRectangle

    import pygame as pg
    import time

    pg.init()

    screen = init_window()

    points = get_points(screen)

    clear_screen(screen)

    x_dimension, y_dimension = screen.get_size()

    ## Construction of the original drawing rectangle

    top_original_drawing_rect = 0
    left_original_drawing_rect = 0
    height_original_drawing_rect = y_dimension * PROPORTION_ORIGINAL_DRAWING
    width_original_drawing_rect = x_dimension * PROPORTION_ORIGINAL_DRAWING

    original_drawing_rectangle = DrawingRectangle(screen, left_original_drawing_rect,\
        top_original_drawing_rect, width_original_drawing_rect, height_original_drawing_rect)

    ## Construction of the reconstructed drawing rectangle

    top_reconstructed_drawing_rect = height_original_drawing_rect - 1
    left_reconstructed_drawing_rect = width_original_drawing_rect - 1
    width_reconstructed_drawing_rect = x_dimension - left_reconstructed_drawing_rect + 1
    height_reconstructed_drawing_rect = y_dimension - top_reconstructed_drawing_rect + 1

    reconstructed_drawing_rectangle = DrawingRectangle(screen, left_reconstructed_drawing_rect,\
     top_reconstructed_drawing_rect, width_reconstructed_drawing_rect, \
     height_reconstructed_drawing_rect)

    original_drawing_rectangle.draw()
    reconstructed_drawing_rectangle.draw()

    original_drawing_rectangle.draw_points(points)

    ## Construction of the input box
    sampling_box, number_circle_box, start_box = create_input_boxes(screen)

    not_done = True

    number_circle = 0
    sampled_points = points
    while not_done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                not_done = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    not_done = False

            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1: # If the button pressed is the left one
                    if sampling_box.collidepoint(event.pos):
                        number_points = sampling_box.get_number_input()

                        sampled_points = sampling_points(points, number_points)
                        original_drawing_rectangle.clear()
                        original_drawing_rectangle.draw_points(sampled_points)

                    elif number_circle_box.collidepoint(event.pos):
                        number_circle = number_circle_box.get_number_input()

                    elif start_box.collidepoint(event.pos):
                        not_done = False

            pg.display.update()

    sampled_points_complexe = [complex(point) for point in sampled_points]

    coeffCN = decompositions_en_serie_de_fourier(sampled_points_complexe, number_circle)

    centerReconstructedDrawing = Point2D(reconstructed_drawing_rectangle.centerx,\
        reconstructed_drawing_rectangle.centery)
    PAS = 2*pi/1024
    my_series_cercles = SeriesCercles(centerReconstructedDrawing, coeffCN,\
        1 - PROPORTION_ORIGINAL_DRAWING, PAS, screen)
    # print(coeffCN)
    not_done = True

    while not_done:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                not_done = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    not_done = False

        clear_screen(screen)

        my_series_cercles.dessiner_le_chemin()
        my_series_cercles.dessiner_les_cercles()
        original_drawing_rectangle.draw_points(sampled_points)

        original_drawing_rectangle.draw()
        reconstructed_drawing_rectangle.draw()

        pg.display.update()

        time.sleep(0.01)
