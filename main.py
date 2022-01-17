import pygame

# Изображение не получится загрузить
# без предварительной инициализации pygame
pygame.init()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Chacter(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.source = pygame.transform.scale(load_image("ship.png"), (200, 200))
        self.image = pygame.transform.scale(self.source, (200, 200))
        self.rect = self.image.get_rect()
        self.rect.centerx = 100
        self.rect.centery = 100
        self.angle = 0

    def rot(self, a):
        self.angle = (self.angle + a) % 360
        self.image = pygame.transform.rotate(self.source, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self, *args):
        if args[0] == pygame.K_DOWN:
            self.rect.centerx += 10
        if args[0] == pygame.K_UP:
            self.rect.centery -= 10
        if args[0] == pygame.K_RIGHT:
            self.angle -= 10

            print(self.image.get_rect())

            self.image = pygame.transform.rotate(self.source, self.angle)
            self.rect = self.image.get_rect(center=self.rect.center)

            # self.rect.center = self.rect.centerx, self.rect.centery
            # self.rect = self.image.get_rect(center=self.image.get_rect(center=(self.rect.x, self.rect.y)).center)
        if args[0] == pygame.K_LEFT:
            self.image = pygame.transform.rotate(self.image, math.pi / 36)
            self.rect = self.image.get_rect(center=self.image.get_rect(center=(self.rect.x, self.rect.y)).center)
v = 10
move = {pygame.K_LEFT: (-v, 0),
        pygame.K_RIGHT: (+v, 0),
        pygame.K_UP: (0, -v),
        pygame.K_DOWN: (0, +v)}

clock = pygame.time.Clock()

if __name__ == '__main__':
    running = True
    all_spr = pygame.sprite.Group()
    cur = Chacter(all_spr)
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
#            if event.type == pygame.KEYDOWN:
#                 v = event.type
#                 all_spr.update(event.key)
        for i in move:

            if pygame.key.get_pressed()[i] and (i == pygame.K_DOWN or i == pygame.K_UP):
                cur.rect.move_ip(move[i])
                screen.fill(pygame.Color("white"))
                screen.blit(cur.image, cur.rect)
            elif pygame.key.get_pressed()[i] and (i == pygame.K_LEFT or i == pygame.K_RIGHT):
                cur.rot(move[i][0])
                screen.fill(pygame.Color("white"))
                screen.blit(cur.image, cur.rect)

        screen.fill((255, 255, 255))
        all_spr.draw(screen)
        pygame.display.flip()
        clock.tick(100)
    pygame.quit()
