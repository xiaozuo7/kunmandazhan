import  sys
from  bullet import Bullet
import pygame
from cxk import Cxk
from time import sleep

def check_keydown_events(event, ai_settings, screen, ship, bullets):
    '''响应按键'''
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, stats, sb, play_button, ship, cxks, bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, cxks, bullets, mouse_x, mouse_y)

def check_play_button(ai_settings, screen, stats, sb, play_button, ship, cxks, bullets, mouse_x, mouse_y):
    '''在玩家单价Play按钮时开始新游戏'''
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        #重置游戏设置
        ai_settings.initialize_dynamic_settings()
        #隐藏光标
        pygame.mouse.set_visible(False)
        #重置游戏统计信息
        stats.reset_stats()
        stats.game_active = True

        #重置记分牌图像
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        #清空外星人列表和子弹列表
        cxks.empty()
        bullets.empty()

        #创建一群新的外星人, 并让飞船居中
        create_fleet(ai_settings, screen, ship , cxks)
        ship.center_ship()


def update_screen(ai_settings, screen, stats, sb, ship, cxks, bullets, play_button):
    '''更新屏幕上的图像，并切换到新屏幕'''
    #每次循环时都重绘屏幕
    screen.fill(ai_settings.bg_color)
    #在飞船和外星人后面重绘所有子弹
    for bullets in bullets.sprites():
        bullets.draw_bullet()
    ship.blitme()
    cxks.draw(screen)
    #显示得分
    sb.show_score()
    #如果游戏处于非活动状态，就绘制play按钮
    if not stats.game_active:
        play_button.draw_button()
    pygame.display.flip()

def update_bullets(ai_settings, screen, stats, sb, ship, cxks, bullets):
    '''更新子弹的位置， 并删除已消失的子弹'''

    #删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_cxk_collisions(ai_settings, screen, stats, sb, ship, cxks, bullets)

def check_bullet_cxk_collisions(ai_settings, screen, stats, sb, ship, cxks, bullets):
    #更新子弹的位置
    bullets.update()
    collisions = pygame.sprite.groupcollide(bullets, cxks, True, True)
    if collisions:
        for cxks in collisions.values():
            stats.score += ai_settings.cxk_points * len(cxks)
            sb.prep_score()
        check_high_score(stats, sb)
    if len(cxks) == 0:
        bullets.empty()
        ai_settings.increase_speed()

        #提高等级
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, ship, cxks)




def fire_bullet(ai_settings, screen, ship, bullets):
    '''如果没有到达限制， 就发射一颗子弹'''
    #创建一个子弹， 并将其加入到编组bullet中
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def create_fleet(ai_settings, screen, ship, cxks):
    '''创建坤群'''
    cxk = Cxk(ai_settings, screen)
    number_cxks_x = get_number_cxks_x(ai_settings, cxk.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,cxk.rect.height)
    for row_number in range(number_rows):
        for cxk_number in range(number_cxks_x):
            create_cxk(ai_settings, screen, cxks, cxk_number, row_number)

def create_cxk(ai_settings, screen, cxks, cxk_number, row_number):
    '''创建一个cxk并放在首行'''
    cxk = Cxk(ai_settings, screen)
    cxk_width = cxk.rect.width
    cxk.x = cxk_width + 2 * cxk_width * cxk_number
    cxk.rect.x = cxk.x
    cxk.rect.y = cxk.rect.height + 2 * cxk.rect.height * row_number
    cxks.add(cxk)

def get_number_cxks_x(ai_settings, cxk_width):
    '''计算每行可以容纳多少个cxk'''
    available_space_x = ai_settings.screen_width - 2 * cxk_width
    number_cxks_x = int(available_space_x / (2 * cxk_width))
    return number_cxks_x

def get_number_rows(ai_settings, ship_height, cxk_height):
    '''计算可以容纳多少个cxk'''
    available_space_y = (ai_settings.screen_height - (3 * cxk_height) - ship_height)
    number_rows = int(available_space_y / (2 * cxk_height))
    return number_rows

def update_cxks(ai_settings, screen,stats, sb, ship, cxks, bullets):
    check_fleet_edges(ai_settings, cxks)
    check_cxks_bottom(ai_settings, screen, stats, sb, ship, cxks, bullets)
    cxks.update()


    #检测碰撞
    if pygame.sprite.spritecollideany(ship, cxks):
        ship_hit(ai_settings, screen, stats, sb, ship, cxks, bullets)
    check_cxks_bottom(ai_settings, screen, stats, sb, ship, cxks, bullets)

def check_fleet_edges(ai_settings, cxks):
    for cxk in cxks.sprites():
        if cxk.check_edges():
            change_fleet_direction(ai_settings, cxks)
            break

def change_fleet_direction(ai_settings, cxks):
    for cxk in cxks.sprites():
        cxk.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def ship_hit(ai_settings, screen,stats, sb, ship, cxks, bullets):
    '''响应被cxk撞到的吴亦凡'''
    if stats.ships_left > 0:
        #将ships_left减1
        stats.ships_left -= 1

        #更新记分牌
        sb.prep_ships()

        #清空cxk列表和子弹列表
        cxks.empty()
        bullets.empty()

        #创建一群新的cxk，并将吴亦凡放到屏幕地段中央
        create_fleet(ai_settings, screen, ship, cxks)
        ship.center_ship()

        #暂停
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_cxks_bottom(ai_settings, screen, stats, sb, ship, cxks, bullets):
    '''检查是否有cxk到达了屏幕低端'''
    screen_rect = screen.get_rect()
    for cxk in cxks.sprites():
        if cxk.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, screen, stats, sb, ship, cxks, bullets)
            break

def check_high_score(stats, sb):
    '''检查是否诞生了新的最高分'''
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()