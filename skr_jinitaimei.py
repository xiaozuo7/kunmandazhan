import  sys
from settings import Settings
import pygame
from  ship import Ship
import game_functions as gf
from pygame.sprite import Group
from cxk import Cxk
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

def run_game():
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("鳗鲲大战")
    #创建一个用于存储游戏统计信息的实例
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    ship = Ship(ai_settings, screen)
    #创建一个用于存储子弹的编组
    bullets = Group()
    cxks = Group()
    #创建坤群
    gf.create_fleet(ai_settings, screen, ship, cxks)
    #创建play按钮
    play_button = Button(ai_settings, screen, "Play")

    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, cxks, bullets)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship,   cxks, bullets)
            gf.update_cxks(ai_settings,screen, stats, sb, ship, cxks, bullets)

        gf.update_screen(ai_settings, screen, stats, sb, ship, cxks, bullets, play_button)
run_game()