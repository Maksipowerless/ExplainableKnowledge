import pygame
import os
from PIL import Image
import numpy as np
import pickle
from Config import *
import tkinter as tk
from tkinter import filedialog

# CONSTS
DISPLAY_WIDTH = 1920
DISPLAY_HEIGHT = 1080
SELECTED_PATCH_VIEW_RECT = (1732, 150)
QUIT_RECT = (1600, 840, 200, 50)
CHOOSE_FILE_RECT = (1520, 500, 350, 50)
CHOOSE_10_CLUSTER_RECT = (1550, 630, 100, 50)
CHOOSE_20_CLUSTER_RECT = (1720, 630, 100, 50)
CHOOSE_50_CLUSTER_RECT = (1550, 730, 100, 50)
CHOOSE_100_CLUSTER_RECT = (1720, 730, 100, 50)
Image.MAX_IMAGE_PIXELS = None


class ViewResult:

    def __init__(self):
        self.cluster_number = 20
        self.pic_number = 7
        self.init_display()
        self.draw_static()
        self.update_image(self.cluster_number)
        self.main_loop()

    def update_image(self, cluster_number):
        self.clear_image()
        self.cluster_number = cluster_number
        self.choose_image(self.pic_number)
        self.load_impact()
        self.load_re_impact()
        self.load_centroids()
        self.draw_dinamic()
        self.get_image_patches()
        self.draw_image()
        pygame.display.update()

    def clear_image(self):
        pygame.draw.rect(self.sc, (242, 242, 242), (0, 0, 1480, DISPLAY_HEIGHT))

    def load_impact(self):
        self.impacts = []
        with open(IMPACT_PATH + str(self.cluster_number) + "/impact.txt", 'rb') as f:
            self.impacts = pickle.load(f)

    def load_re_impact(self):
        with open(IMPACT_PATH + str(self.cluster_number) + "/re_impact.txt", 'rb') as f:
            self.re_impacts = pickle.load(f)

    def load_centroids(self):
        self.centroids = []
        with open(CENTROIDS_PATH + str(self.cluster_number) + '/' + str(self.pic_number) + '.txt', 'rb') as f:
            self.centroids = pickle.load(f)

    def init_display(self):
        pygame.init()
        self.sc = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT), pygame.FULLSCREEN)  # , pygame.FULLSCREEN
        self.sc.fill([242, 242, 242])

    def draw_static(self):

        # Текст "Количество кластеров"
        font = pygame.font.Font(None, 40)
        text_selected_patch = font.render('Количество кластеров:', 1, (0, 0, 0))
        self.sc.blit(text_selected_patch, (1500, 40))

        # Текст "Выбранный патч" + рамка патча
        font = pygame.font.Font(None, 36)
        text_selected_patch = font.render('Выбранный патч:', 1, (0, 0, 0))
        self.sc.blit(text_selected_patch, (1597, 100))
        pygame.draw.rect(self.sc, (0, 0, 0), (SELECTED_PATCH_VIEW_RECT[0] - 130, SELECTED_PATCH_VIEW_RECT[1] - 2, 131, 131), 2)

        # Текст "Выбрать количество центроидов" + рамка
        font = pygame.font.Font(None, 36)
        text_selected_patch = font.render('Выбрать кол-во центроидов', 1, (0, 0, 0))
        self.sc.blit(text_selected_patch, (1527, 570))
        pygame.draw.rect(self.sc, (0, 0, 0), (1480, 560, 410, 270), 2)

        # Кнопка "Выход"
        pygame.draw.rect(self.sc, (0, 0, 0), QUIT_RECT)
        font = pygame.font.Font(None, 36)
        text_selected_patch = font.render('Выход', 1, (250, 250, 250))
        self.sc.blit(text_selected_patch, (QUIT_RECT[0] + 55, QUIT_RECT[1] + 12))

        # Кнопка "Выбрать файл"
        pygame.draw.rect(self.sc, (0, 0, 0), CHOOSE_FILE_RECT)
        font = pygame.font.Font(None, 36)
        text_selected_patch = font.render('Выбрать изображение', 1, (250, 250, 250))
        self.sc.blit(text_selected_patch, (CHOOSE_FILE_RECT[0] + 55, CHOOSE_FILE_RECT[1] + 12))

        # Кнопка "Выбрать 10 кластеров"
        pygame.draw.rect(self.sc, (0, 0, 0), CHOOSE_10_CLUSTER_RECT)
        font = pygame.font.Font(None, 36)
        text_selected_patch = font.render('10', 1, (250, 250, 250))
        self.sc.blit(text_selected_patch, (CHOOSE_10_CLUSTER_RECT[0] + 35, CHOOSE_10_CLUSTER_RECT[1] + 12))

        # Кнопка "Выбрать 20 кластеров"
        pygame.draw.rect(self.sc, (0, 0, 0), CHOOSE_20_CLUSTER_RECT)
        font = pygame.font.Font(None, 36)
        text_selected_patch = font.render('20', 1, (250, 250, 250))
        self.sc.blit(text_selected_patch, (CHOOSE_20_CLUSTER_RECT[0] + 35, CHOOSE_20_CLUSTER_RECT[1] + 12))

        # Кнопка "Выбрать 50 кластеров"
        pygame.draw.rect(self.sc, (0, 0, 0), CHOOSE_50_CLUSTER_RECT)
        font = pygame.font.Font(None, 36)
        text_selected_patch = font.render('50', 1, (250, 250, 250))
        self.sc.blit(text_selected_patch, (CHOOSE_50_CLUSTER_RECT[0] + 35, CHOOSE_50_CLUSTER_RECT[1] + 12))

        # Кнопка "Выбрать 100 кластеров"
        pygame.draw.rect(self.sc, (0, 0, 0), CHOOSE_100_CLUSTER_RECT)
        font = pygame.font.Font(None, 36)
        text_selected_patch = font.render('100', 1, (250, 250, 250))
        self.sc.blit(text_selected_patch, (CHOOSE_100_CLUSTER_RECT[0] + 30, CHOOSE_100_CLUSTER_RECT[1] + 12))

        # Текст "Вероятность рака:"
        font = pygame.font.Font(None, 40)
        text_selected_patch = font.render('Вероятность рака:', 1, (0, 0, 0))
        self.sc.blit(text_selected_patch, (1500, 320))

        # Текст "Уточненная вероятность рака:"
        font = pygame.font.Font(None, 40)
        text_selected_patch = font.render('Уточненная вероятность', 1, (0, 0, 0))
        self.sc.blit(text_selected_patch, (1500, 370))
        text_selected_patch = font.render('рака:', 1, (0, 0, 0))
        self.sc.blit(text_selected_patch, (1685, 400))

        # Рамка вокруг информации
        pygame.draw.rect(self.sc, (0, 0, 0), (1480, 10, 410, 480), 2)

    def draw_dinamic(self, cluster=1):
        if cluster == None:
            cluster = 1

        #  Текст кол-во кластеров
        pygame.draw.rect(self.sc, (242, 242, 242), (1830, 40, 55, 30))
        font = pygame.font.Font(None, 40)
        text_selected_patch = font.render(str(self.impacts.__len__()), 1, (0, 0, 0))
        self.sc.blit(text_selected_patch, (1830, 40))

        # Текст "Вероятность рака:"
        pygame.draw.rect(self.sc, (242, 242, 242), (1770, 320, 80, 30))
        font = pygame.font.Font(None, 40)
        text_selected_patch = font.render("{:.3f}".format(self.impacts[cluster - 1]), 1, (0, 0, 0))
        self.sc.blit(text_selected_patch, (1770, 320))

        # Текст "Уточненная вероятность рака:"
        pygame.draw.rect(self.sc, (242, 242, 242), (1770, 400, 80, 30))
        font = pygame.font.Font(None, 40)
        text_selected_patch = font.render("{:.3f}".format(self.re_impacts[cluster - 1]), 1, (0, 0, 0))
        self.sc.blit(text_selected_patch, (1770, 400))

        # Текст номер кластера
        pygame.draw.rect(self.sc, (242, 242, 242), (1740, 147, 80, 30))
        font = pygame.font.Font(None, 40)
        text_selected_patch = font.render("#" + str(cluster), 1, (0, 0, 0))
        self.sc.blit(text_selected_patch, (1740, 147))

    def choose_image(self, pic_number=11):
        self.pic_number = pic_number
        self.path_split_images = SPLIT_IMAGES_PATH + str(self.pic_number) + "/"
        source_image = Image.open(SOURCE_IMAGES_PATH + str(self.pic_number) + ".tif")
        width, height = source_image.size
        scale_coeff_width = width //DISPLAY_WIDTH #(DISPLAY_WIDTH - 470)
        scale_coeff_height = height // DISPLAY_HEIGHT
        scale_coeff = max(scale_coeff_width, scale_coeff_height)
        self.patch_size = 128 // scale_coeff
        self.image_shift = width // scale_coeff

    def get_image_patches(self):
        try:
            with open(PATCH_MAP_PATH + str(self.cluster_number) + "/" + str(self.pic_number) + '.txt', 'rb') as f:
                self.patch_map = pickle.load(f)
            return
        except OSError as e:
            patch_map = {}
            entries = sorted(os.scandir(self.path_split_images), key=lambda x: (x.is_dir(), x.name))
            count = 0
            for entry in entries:
                tmp = entry.name.split('.')
                patch_name = tmp[0]
                tmp = patch_name.split('_')
                row = int(tmp[0])
                column = int(tmp[1])

                centroid = self.centroids[count]
                image = Image.open(self.path_split_images + entry.name).resize((self.patch_size, self.patch_size)).rotate(90)
                patch = np.asarray(image).copy()

                impact = self.re_impacts[centroid - 1]
                if impact < 0.5:
                    for j in range(self.patch_size):
                        for k in range(self.patch_size):
                            if j == 0 or k == 0 or j == self.patch_size - 1 or k == self.patch_size - 1:
                                patch[j, k, 0] = 0
                                patch[j, k, 1] = 0
                                patch[j, k, 2] = 255

                else:
                    for j in range(self.patch_size):
                        for k in range(self.patch_size):
                            if j == 0 or k == 0 or j == self.patch_size - 1 or k == self.patch_size - 1:
                                patch[j, k, 0] = 255
                                patch[j, k, 1] = 0
                                patch[j, k, 2] = 0

                rect = (self.image_shift - column * self.patch_size, row * self.patch_size)
                patch_map[rect] = {"patch": patch, "cluster": centroid, "name": entry.name}
                count += 1
            with open(PATCH_MAP_PATH + str(self.cluster_number) + "/" + str(self.pic_number) + '.txt', "wb") as fp:
                pickle.dump(patch_map, fp)
            self.patch_map = patch_map

    def draw_image(self):
        for key in self.patch_map.keys():
            patch = self.patch_map[key]["patch"].copy()
            patch_surf = pygame.surfarray.make_surface(patch)
            patch_rect = patch_surf.get_rect(topright=(key))
            self.sc.blit(patch_surf, patch_rect)

    def fill_cluster(self, cluster, selectet_patch_key):
        if selectet_patch_key == None:
            return
        for key in self.patch_map.keys():
            current_impact = self.re_impacts[self.patch_map[key]["cluster"] - 1]
            patch = self.patch_map[key]["patch"].copy()

            patch_size = self.patch_map[selectet_patch_key]["patch"].shape[0]  # сохраненные патчи и рассчитаные вновь мошут отличаться
            if self.patch_map[key]["cluster"] == cluster:
                if current_impact < 0.5:
                    for j in range(patch_size):
                        for k in range(patch_size):
                            patch[j, k, 0] = 0
                            patch[j, k, 1] = 0
                else:
                    for j in range(patch_size):
                        for k in range(patch_size):
                            patch[j, k, 1] = 0
                            patch[j, k, 2] = 0

            patch_surf = pygame.surfarray.make_surface(patch)
            patch_rect = patch_surf.get_rect(topright=(key))
            self.sc.blit(patch_surf, patch_rect)

        # Закраска выбранного патча на изображении
        if selectet_patch_key != None:
            patch = self.patch_map[selectet_patch_key]["patch"].copy()
            for i in range(patch.shape[0]):
                for j in range(patch.shape[1]):
                    patch[i][j] = [255, 255, 0]
            patch_surf = pygame.surfarray.make_surface(patch)
            patch_rect = patch_surf.get_rect(topright=(selectet_patch_key))
            self.sc.blit(patch_surf, patch_rect)

    def draw_selected_patch(self, coord):
        for key in self.patch_map.keys():
            x = key[0]
            y = key[1]
            if coord[0] in range(x - self.patch_size, x):
                if coord[1] in range(y, y + self.patch_size):
                    # Отрисовка патча 128x128
                    name = self.patch_map[key]["name"]
                    full_size_patch = np.asarray(Image.open(self.path_split_images + name).rotate(90))
                    patch_surf = pygame.surfarray.make_surface(full_size_patch)
                    patch_rect = patch_surf.get_rect(topright=(SELECTED_PATCH_VIEW_RECT))
                    self.sc.blit(patch_surf, patch_rect)
                    return key

    def select_file(self):
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename()
        splitted = file_path.split("/")[-1]
        self.pic_number = splitted.split(".")[0]

    def main_loop(self):
        cluster_for_lb = 1
        while 1:
            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    exit()
                if i.type == pygame.MOUSEBUTTONDOWN:
                    if i.button == 1:
                        coordinates = pygame.mouse.get_pos()
                        # нажата кнопка "Выход"
                        if coordinates[0] in range(QUIT_RECT[0], QUIT_RECT[0] + QUIT_RECT[2]) and \
                                coordinates[1] in range(QUIT_RECT[1], QUIT_RECT[1] + QUIT_RECT[3]):
                            exit()
                        # нажата кнопка "Выбрать изображение"
                        elif coordinates[0] in range(CHOOSE_FILE_RECT[0], CHOOSE_FILE_RECT[0] + CHOOSE_FILE_RECT[2]) and \
                                coordinates[1] in range(CHOOSE_FILE_RECT[1], CHOOSE_FILE_RECT[1] + CHOOSE_FILE_RECT[3]):
                            self.select_file()
                            self.update_image(self.cluster_number)
                                # нажата кнопка "10"
                        elif coordinates[0] in range(CHOOSE_10_CLUSTER_RECT[0], CHOOSE_10_CLUSTER_RECT[0] + CHOOSE_10_CLUSTER_RECT[2]) and \
                             coordinates[1] in range(CHOOSE_10_CLUSTER_RECT[1], CHOOSE_10_CLUSTER_RECT[1] + CHOOSE_10_CLUSTER_RECT[3]):
                            self.update_image(10)
                                # нажата кнопка "20"
                        elif coordinates[0] in range(CHOOSE_20_CLUSTER_RECT[0], CHOOSE_20_CLUSTER_RECT[0] + CHOOSE_20_CLUSTER_RECT[2]) and \
                             coordinates[1] in range(CHOOSE_20_CLUSTER_RECT[1], CHOOSE_20_CLUSTER_RECT[1] + CHOOSE_20_CLUSTER_RECT[3]):
                            self.update_image(20)
                                # нажата кнопка "50"
                        elif coordinates[0] in range(CHOOSE_50_CLUSTER_RECT[0], CHOOSE_50_CLUSTER_RECT[0] + CHOOSE_50_CLUSTER_RECT[2]) and \
                             coordinates[1] in range(CHOOSE_50_CLUSTER_RECT[1], CHOOSE_50_CLUSTER_RECT[1] + CHOOSE_50_CLUSTER_RECT[3]):
                            self.update_image(50)
                                # нажата кнопка "100"
                        elif coordinates[0] in range(CHOOSE_100_CLUSTER_RECT[0], CHOOSE_100_CLUSTER_RECT[0] + CHOOSE_100_CLUSTER_RECT[2]) and \
                             coordinates[1] in range(CHOOSE_100_CLUSTER_RECT[1], CHOOSE_100_CLUSTER_RECT[1] + CHOOSE_100_CLUSTER_RECT[3]):
                            self.update_image(100)
                        # выбран патч на изображении
                        else:
                            patch_key = self.draw_selected_patch(coordinates)
                            try:
                                cluster = self.patch_map[patch_key]["cluster"]
                            except KeyError:
                                cluster = None
                            self.fill_cluster(cluster, patch_key)
                            self.draw_dinamic(cluster)
                            pygame.display.update()
                    ##################################
                    elif i.button == 3:
                        if cluster_for_lb > self.cluster_number:
                            cluster_for_lb = 1
                        patch_key = list(self.patch_map.keys())[0]
                        self.fill_cluster(cluster_for_lb, patch_key)
                        self.draw_dinamic(cluster_for_lb)
                        pygame.display.update()
                        cluster_for_lb += 1

            pygame.time.delay(20)



vr = ViewResult()