import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRect or ばくだんRect
    戻り値：判定結果タプル （横方向、縦方向）
    画面内ならTrue/画面外ならFalse
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right: #横
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom: #縦
        tate = False
    return yoko, tate


def game_over(screen: pg.Surface):
    """
    ゲームオーバー画面を表示し、5秒後にプログラムを終了する。
    """

    blackout_surf = pg.Surface(screen.get_size())
    blackout_surf.set_alpha(200)  # 透明度
    blackout_surf.fill((0, 0, 0)) # 黒

    font = pg.font.Font(None, 80)
    text_surf = font.render("Game Over", True, (255, 255, 255)) # 白文字
    text_rct = text_surf.get_rect(center=screen.get_rect().center)

    cry_kk_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)
    
    cry_kk_rct1 = cry_kk_img.get_rect(center=text_rct.center)
    cry_kk_rct1.right = text_rct.left # 左側
    cry_kk_rct2 = cry_kk_img.get_rect(center=text_rct.center)
    cry_kk_rct2.left = text_rct.right # 右側

    screen.blit(blackout_surf, (0, 0)) # ブラックアウト
    screen.blit(text_surf, text_rct) # "Game Over" を表示
    screen.blit(cry_kk_img, cry_kk_rct1) # 泣きこうかとん1
    screen.blit(cry_kk_img, cry_kk_rct2) # 泣きこうかとん2

    pg.display.update()
    time.sleep(5) #5秒待機


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20, 20))  # 爆弾用の空Surface
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # 赤い爆弾円
    bb_img.set_colorkey((0, 0, 0))  # 四隅の黒い部分を透過
    bb_rct = bb_img.get_rect()  # 爆弾Rect
    bb_rct.centerx = random.randint(0, WIDTH)  # 爆弾横座標
    bb_rct.centery = random.randint(0, HEIGHT)  # 爆弾縦座標
    vx, vy = +5, +5  # 爆弾の速度
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0])
        if kk_rct.colliderect(bb_rct):
            game_over(screen)
            return #ゲームオーバー

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]  # 横方向の移動量を加算
                sum_mv[1] += mv[1]  # 縦方向の移動量を加算
        
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx, vy)  # 爆弾移動
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bb_img, bb_rct)  # 爆弾描画
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()