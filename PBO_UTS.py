import pygame
import sys
import random

pygame.init()

WIDTH = 1280
HEIGHT = 720

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space War")

BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

class Pesawat:
    def __init__(self, x, y, width, height, asset, hp, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        file_gambar = 'asset/' + asset
        gambar_object = pygame.image.load(file_gambar)
        self.object = pygame.transform.scale(gambar_object, (self.width, self.height)). convert_alpha()

        self.hp = hp
        self.max_hp = hp
        self.speed = speed

    def tampilkan_layar(self, area_gambar):
        area_gambar.blit(self.object, (self.x, self.y))


class Player(Pesawat):
    def __init__(self, x, y):
        super().__init__(x, y, 75, 75, "player.png", 25, 5)


    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
        if keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.y += self.speed


    def batasan(self):
        if self.x < 0:
            self.x = 0
        if self.x > WIDTH - self.width:
            self.x = WIDTH - self.width
        if self.y < 350:
            self.y = 350
        if self.y > HEIGHT - self.height:
            self.y = HEIGHT - self.height


class Enemy(Pesawat):
    def __init__(self, x, y):
        super().__init__(x, y, 100, 100, "enemy.png", 25, 5)
        self.kecepatan_x = self.speed
        self.kecepatan_y = self.speed
        self.waktu_ganti_arah = 0
        self.waktu_nembak = 0

    def gerak_acak(self):
        self.waktu_ganti_arah += 1

        if self.waktu_ganti_arah > 90:
            self.kecepatan_x = random.choice([-self.speed, 0, self.speed])
            self.kecepatan_y = random.choice([-self.speed, 0, self.speed])
            self.waktu_ganti_arah = 0


        self.x += self.kecepatan_x
        self.y += self.kecepatan_y

        if self.x < 0 or self.x > WIDTH - self.width:
            self.kecepatan_x *= -1

        if self.y < 0 or self.y > 250:
            self.kecepatan_y *= -1

    def nembak(self, daftar_peluru_musuh):
        self.waktu_nembak += 1

        if self.waktu_nembak > 18:
            peluru_baru = PeluruEnemy(self.x + (self.width // 2) - 2, self.y + self.height)
            daftar_peluru_musuh.append(peluru_baru)
            self.waktu_nembak = 0

class PeluruPlayer:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 6
        self.height = 16
        self.speed = 7
        self.color = CYAN

    def gerak(self):
        self.y -= self.speed

    def tampilkan_layar(self, area_gambar):
        bentuk_peluru = (self.x, self.y, self.width, self.height)
        pygame.draw.rect(area_gambar, self.color, bentuk_peluru)

class PeluruEnemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 6
        self.height = 16
        self.speed = 7
        self.color = RED

    def gerak(self):
        self.y += self.speed

    def tampilkan_layar(self, area_gambar):
        bentuk_peluru = (self.x, self.y, self.width, self.height)
        pygame.draw.rect(area_gambar, self.color, bentuk_peluru)


bintang_bintang = []
for i in range(120):
    x = random.randrange(0, WIDTH)
    y = random.randrange(0, HEIGHT)
    ukuran = random.randrange(1, 3)
    kecepatan = random.randrange(1, 5)
    bintang_bintang.append([x, y, ukuran, kecepatan])


pesawat_player = Player(375, 500)
pesawat_enemy = Enemy(375, 50)
daftar_peluru_player = []
daftar_peluru_enemy = []

clock = pygame.time.Clock()
running = True
status_game = "BERMAIN"
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            if event.key == pygame.K_SPACE and status_game == "BERMAIN":
                peluru_baru = PeluruPlayer(pesawat_player.x + 35, pesawat_player.y)
                daftar_peluru_player.append(peluru_baru)

    screen.fill(BLACK)
    keys = pygame.key.get_pressed()
    font = pygame.font.SysFont(None, 36)


    for bintang in bintang_bintang:
        bintang[1] += bintang[3]
        if bintang[1] > HEIGHT:
            bintang[1] = random.randrange(-20, -5)
            bintang[0] = random.randrange(0, WIDTH)
        pygame.draw.circle(screen, WHITE, (bintang[0], bintang[1]), bintang[2])


    if status_game == "BERMAIN":
        pesawat_player.move(keys)
        pesawat_player.batasan()

        pesawat_enemy.gerak_acak()
        pesawat_enemy.nembak(daftar_peluru_enemy)

        rect_player = pygame.Rect(pesawat_player.x, pesawat_player.y, pesawat_player.width, pesawat_player.height)
        rect_enemy = pygame.Rect(pesawat_enemy.x, pesawat_enemy.y, pesawat_enemy.width, pesawat_enemy.height)

        for peluru in daftar_peluru_player[:]:
            peluru.gerak()
            rect_peluru = pygame.Rect(peluru.x, peluru.y, peluru.width, peluru.height)
            if rect_peluru.colliderect(rect_enemy):
                pesawat_enemy.hp -= 1
                daftar_peluru_player.remove(peluru)
            elif peluru.y < 0:
                daftar_peluru_player.remove(peluru)

        for peluru_m in daftar_peluru_enemy[:]:
            peluru_m.gerak()
            rect_peluru_m = pygame.Rect(peluru_m.x, peluru_m.y, peluru_m.width, peluru_m.height)
            if rect_peluru_m.colliderect(rect_player):
                pesawat_player.hp -= 1
                daftar_peluru_enemy.remove(peluru_m)
            elif peluru_m.y > HEIGHT:
                daftar_peluru_enemy.remove(peluru_m)

        if pesawat_player.hp <= 0:
            status_game = "KALAH"
            waktu_selesai = pygame.time.get_ticks()
        elif pesawat_enemy.hp <= 0:
            status_game = "MENANG"
            waktu_selesai = pygame.time.get_ticks()


    for peluru in daftar_peluru_player:
        peluru.tampilkan_layar(screen)
    for peluru_m in daftar_peluru_enemy:
        peluru_m.tampilkan_layar(screen)

    for peluru in daftar_peluru_player[:]:
        rect_peluru = pygame.Rect(peluru.x, peluru.y, peluru.width, peluru.height)

        for peluru_m in daftar_peluru_enemy[:]:
            rect_peluru_m = pygame.Rect(peluru_m.x, peluru_m.y, peluru_m.width, peluru_m.height)

            if rect_peluru.colliderect(rect_peluru_m):
                if peluru in daftar_peluru_player:
                    daftar_peluru_player.remove(peluru)
                if peluru_m in daftar_peluru_enemy:
                    daftar_peluru_enemy.remove(peluru_m)
                break

    if pesawat_player.hp > 0:
        pesawat_player.tampilkan_layar(screen)
    if pesawat_enemy.hp > 0:
        pesawat_enemy.tampilkan_layar(screen)


    rasio_hp_player = max(0, pesawat_player.hp) / pesawat_player.max_hp

    if rasio_hp_player > 0.5:
        warna_player = GREEN
    elif rasio_hp_player > 0.25:
        warna_player = YELLOW
    else:
        warna_player = RED


    pygame.draw.rect(screen, warna_player, (10, HEIGHT - 30, 200 * rasio_hp_player, 20))
    pygame.draw.rect(screen, WHITE, (10, HEIGHT - 30, 200, 20), 2)


    rasio_hp_enemy = max(0, pesawat_enemy.hp) / pesawat_enemy.max_hp


    if rasio_hp_enemy > 0.5:
        warna_enemy = GREEN
    elif rasio_hp_enemy > 0.25:
        warna_enemy = YELLOW
    else:
        warna_enemy = RED

    pygame.draw.rect(screen, warna_enemy, (10, 10, 200 * rasio_hp_enemy, 20))
    pygame.draw.rect(screen, WHITE, (10, 10, 200, 20), 2)

    if status_game == "KALAH":
        teks_kalah = font.render("GAME OVER! Kamu Kalah.", True, RED)
        screen.blit(teks_kalah, (WIDTH // 2 - 150, HEIGHT // 2 - 20))

        if pygame.time.get_ticks() - waktu_selesai > 4000:
            running = False

    elif status_game == "MENANG":
        teks_menang = font.render("YOU WIN! Musuh Hancur.", True, YELLOW)
        screen.blit(teks_menang, (WIDTH // 2 - 150, HEIGHT // 2 - 20))

        if pygame.time.get_ticks() - waktu_selesai > 4000:
            running = False


    pygame.display.flip()
    clock.tick(60)


pygame.quit()
sys.exit()