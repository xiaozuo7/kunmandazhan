class Settings():
    '''存储游戏的所有设置的类'''

    def __init__(self):
        '''初始化游戏的静态设置'''
        #屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230 , 230)
        self.ship_speed_factor = 1.5
        self.ship_limit = 3
        #子弹设置
        self.bullet_speed_factor = 3
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 3
        self.cxk_speed_factor = 1
        self.fleet_drop_speed = 10
        #fleet_direction为1表示向右移，位-1表示向左移
        self.fleet_direction = 1
        #加快游戏节奏
        self.speedup_scale = 1.1
        #蔡徐坤点数的提高速度
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        '''初始化随游戏进行而变化的设置'''
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.cxk_speed_factor = 1

        #fleet_direction为1表示向右;为-1表示向左
        self.fleet_direction = 1
        #记分
        self.cxk_points = 50

    def increase_speed(self):
        '''提高速度和蔡徐坤的设置'''
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.cxk_speed_factor *= self.speedup_scale

        self.cxk_points = int(self.cxk_points * self.score_scale)
