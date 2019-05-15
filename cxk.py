import  pygame
from pygame.sprite import Sprite

class Cxk(Sprite):
    '''表示一个蔡徐坤的类'''

    def __init__(self, ai_settings, screen):
        '''初始化蔡徐坤并设置起始位置'''
        super(Cxk, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        #加载蔡徐坤图像，设置rect属性
        self.image = pygame.image.load('images/cxk.bmp')
        self.rect = self.image.get_rect()

        #每个蔡徐坤最初都在屏幕左上角附近
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)

    def blitme(self):
        '''指定位置画出蔡徐坤'''
        self.screen.blit(self.image, self.rect)

    def update(self):
        self.x += (self.ai_settings.cxk_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x

    def check_edges(self):
        '''如果cxk位于边缘，就返回True'''
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True