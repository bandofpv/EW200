import pygame


class Button:
    def __init__(self, center, title, font_size, font_color, screen):
        self.center = center
        self.title = title
        self.font_size = font_size
        self.font_color = font_color
        self.screen = screen
        self.font = pygame.font.Font('assets/fonts/rush.otf', self.font_size)
        self.text = self.font.render(title, 1, self.font_color)
        self.rect = self.text.get_rect(center=center)
        self.collision_rect = pygame.Rect(0, 0, 0, 0)

    def calc_collision(self):
        calc_rect = pygame.Rect((0, 0), (self.rect.width, self.rect.height))
        glyph_rect = pygame.mask.from_surface(self.text).get_bounding_rects()[0]
        offset = glyph_rect.top - calc_rect.top
        self.collision_rect = pygame.Rect(0, 0, self.rect.width, glyph_rect.height)
        self.collision_rect.center = self.center
        self.rect.midtop = (self.collision_rect.centerx, self.collision_rect.top)
        self.rect.top -= offset

    def click(self, game_events, scale=1.0, font_color='white'):
        if self.collision_rect.collidepoint(pygame.mouse.get_pos()):
            self.font = pygame.font.Font('assets/fonts/rush.otf', int(self.font_size * scale))
            self.text = self.font.render(self.title, 1, font_color)
            self.rect = self.text.get_rect(center=self.center)
            self.calc_collision()
            for e in game_events:
                if e.type == pygame.MOUSEBUTTONDOWN:  # If mouse click, return True
                    return True
        else:
            self.font = pygame.font.Font('assets/fonts/rush.otf', self.font_size)
            self.text = self.font.render(self.title, 1, self.font_color)
            self.rect = self.text.get_rect(center=self.center)
            self.calc_collision()
        self.screen.blit(self.text, self.rect)
