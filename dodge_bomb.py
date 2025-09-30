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

    blackout_surface = pg.Surface(screen.get_size())
    blackout_surface.set_alpha(200)  # 透明度
    blackout_surface.fill((0, 0, 0)) # 黒

    font = pg.font.Font(None, 80)
    text_surface = font.render("Game Over", True, (255, 255, 255)) # 白文字
    text_rct = text_surface.get_rect(center=screen.get_rect().center)

    cry_kk_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 1)

    cry_kk_rct1 = cry_kk_img.get_rect(center=text_rct.center)
    cry_kk_rct1.right = text_rct.left # 左側
    cry_kk_rct2 = cry_kk_img.get_rect(center=text_rct.center)
    cry_kk_rct2.left = text_rct.right # 右側

    screen.blit(blackout_surface, (0, 0)) # ブラックアウト
    screen.blit(text_surface, text_rct) # "Game Over" を表示
    screen.blit(cry_kk_img, cry_kk_rct1) # 泣きこうかとん1
    screen.blit(cry_kk_img, cry_kk_rct2) # 泣きこうかとん2

    pg.display.update()
    time.sleep(5) #5秒待機


def init_bb_assets() -> tuple[list[pg.Surface], list[float]]:
    """
    爆弾のSurfaceリストと加速度リストを作成
    戻り値:異なる大きさの爆弾Surfaceリストとそれに対応する加速度リストのタプル
    """
    bb_surfs = []
    accelerations = [a for a in range(1, 11)] # 加速度のリスト
    for r in range(1, 11):
        bb_surface= pg.Surface((20*r, 20*r))# 爆弾のSurfaceを作成
        pg.draw.circle(bb_surface, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_surface.set_colorkey((0, 0, 0)) # 四隅の黒を透過
        bb_surfs.append(bb_surface)
    return bb_surfs, accelerations


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 1)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    bb_surfs, accelerations = init_bb_assets() # 爆弾アセット
    bb_surface = bb_surfs[0] # 最初の爆弾
    bb_rct = bb_surface.get_rect()
    bb_rct.centerx = random.randint(0, WIDTH) # 爆弾横座標
    bb_rct.centery = random.randint(0, HEIGHT) # 爆弾縦座標

    vx, vy = +5, +5 # 爆弾の速度
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
                sum_mv[0] += mv[0] # 横方向の移動量を加算
                sum_mv[1] += mv[1] # 縦方向の移動量を加算
        
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])

        index = min(tmr // 500, 9) #5秒ごと
        accel = accelerations[index]
        bb_surface = bb_surfs[index]
        center_pos = bb_rct.center
        bb_rct = bb_surface.get_rect()
        bb_rct.center = center_pos

        avx, avy = vx * accel, vy * accel # 加速後の速度
        bb_rct.move_ip(avx, avy) # 爆弾移動
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        
        screen.blit(kk_img, kk_rct)       # こうかとんを描画
        screen.blit(bb_surface, bb_rct)  # 現在の大きさの爆弾
        
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()