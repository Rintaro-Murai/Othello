import pygame
import random


pygame.init()


#関数-------------------------------------------------------------------------------------
def draw_grid():#グリッド線を各描く関数
    for i in range(square_num):
        #横線
        pygame.draw.line(screen,BLACK,(0,i*square_size) , (screen_width,i*square_size),2)#pygameでは左上が原点，どこに，色，始点，終点，太さ
        #縦線
        pygame.draw.line(screen,BLACK,(i*square_size,0) , (i*square_size,screen_height),2)

def draw_board():#盤面を描く関数
    for row_index,row in enumerate(board):#盤面のどこに石を置いているのか取得する
        for col_index,col in enumerate(row):
            if col == 1:
                #黒石
                pygame.draw.circle(screen,BLACK,(col_index*square_size + 25,row_index*square_size +25),20)#どこに，色，位置座標（x,y），半径
            elif col == -1:
                #白石
                pygame.draw.circle(screen,WHITE,(col_index*square_size +25,row_index*square_size + 25),20)#どこに，色，位置座標（x,y），半径

def get_valid_position():
    valid_position_list = []
    for row in range(square_num):
        for col in range(square_num):#8x8の盤面の状態をチェック
            if board[row][col] == 0:#何も置かれていないマスのみチェック
                for vx , vy in vec_table:
                    x = vx + col #周囲のマスは(vx+col,vy+row)で表せる
                    y = vy + row
                    #マスの範囲内，かつプレイヤーの石と異なる石がある場合，その方向は引き続きチェック
                    if 0 <= x < square_num and 0 <= y < square_num and board[y][x] == -player:#盤面の範囲内であり，かつ相手の石があるかどうか
                        while True:
                            x += vx#相手の石のある方向へ自分の石があるかチェックを続ける
                            y += vy
                            #プレイヤーの石と異なる石がある場合，その方向は引き続きチェック
                            if 0 <= x < square_num and 0 <= y < square_num and board[y][x] == -player:
                                continue
                            #対象のマスに自分と同じ色の石がある場合，そのチェックしたマスには石が置けるので，そのインデックスを保存
                            elif 0 <= x < square_num and 0 <= y < square_num and board[y][x] == player:
                                valid_position_list.append((col,row))#石が置ける位置を保存
                                break
                            else:
                                break
    return valid_position_list

#石をひっくり返す関数
def flip_pieces(col , row):
    for vx , vy in vec_table:
        flip_list = []#ひっくり返セル可能性のある石をリストに一時保存
        x = vx + col
        y = vy + row
        while 0 <= x < square_num and 0 <= y < square_num and board[y][x] == -player:#周囲のマスの範囲内かつ相手の意志が置いてある場合
            flip_list.append((x, y))
            x += vx
            y += vy
            if 0 <= x < square_num and 0 <= y < square_num and board[y][x] == player:#引き続きチェックを続けて自分の石があればひっくり返す
                for flip_x , flip_y in flip_list:
                    board[flip_y][flip_x] = player#メインループでプレイヤーチェンジしているため，ターン中のplayerの石が置かれる


def get_computer_move(valid_positions):
    return random.choice(valid_positions)


#-----------------------------------------------------------------------------------------

#ウインドウの作成
screen_width=400
screen_height=400
screen=pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("オセロ")

square_num=8
square_size=screen_width//square_num

#fpsの設定
FPS=60
clock = pygame.time.Clock()

#色設定
BLACK = (0,0,0)
WHITE = (255,255,255)   
RED = (255,0,0)
GREEN = (0,128,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)

#盤面(黒：1，白:-1)
board = [
    [0,0,0,0,0,0,0,0,],
    [0,0,0,0,0,0,0,0,],
    [0,0,0,0,0,0,0,0,],
    [0,0,0,1,-1,0,0,0,],
    [0,0,0,-1,1,0,0,0,],
    [0,0,0,0,0,0,0,0,],
    [0,0,0,0,0,0,0,0,],
    [0,0,0,0,0,0,0,0,]]


#プレイヤー
player = 1

#チェック用のベクトル
vec_table = [
    (-1, -1),   #左上
    (0, -1),    #上
    (1, -1),    #右上
    (-1, 0),    #左
    (1, 0),     #右
    (-1, 1),    #左下
    (0, 1),     #下
    (1, 1)]     #右下

game_over = False
pass_num = 0

#ゲーム以外のGUI

#フォントの設定
font = pygame.font.SysFont(None , 50 , bold=False , italic=False)

balack_win_surface = font.render('You Win!', False,BLACK,RED)
white_win_surface = font.render('You Lose..', False,WHITE,RED)
draw_surface = font.render('Draw...', False,BLUE,RED)
reset_surface = font.render('Click here to reset!',False,BLACK,RED)
balack_win_surface = font.render('You Win!', False,BLACK,RED)


#メインループ--------------------------------------------------------------------------------
run = True
while run:

    #背景の色設定
    screen.fill(GREEN)

    #グリッド線の作成
    draw_grid()

    #盤面の作成
    draw_board()

    #石が置ける場所の取得
    valid_position_list = get_valid_position()
    #print(valid_position_list)


    #石を置ける場所に黄色で目印をつける
    for x , y in valid_position_list:
        pygame.draw.circle(screen,YELLOW,(x * square_size + 25,y * square_size +25),20,2)#どこに，色，位置座標（x,y），半径
       
    #石が置ける場所がない場合，パスをする(playerのチェンジ)
    if len(valid_position_list) < 1:#石の置ける場所の座標が入ったリストが0のとき，playerチェンジ
        player *= -1
        pass_num +=1 

    #両者とも石を置けなくなったら終了（ゲームオーバー判定）
    if pass_num > 1:
        pass_num = 2
        game_over = True

    #勝敗判定とリセット
    black_num = 0
    white_num = 0
    if game_over:
        black_num = sum(row.count(1) for row in board)
        white_num = sum(row.count(-1) for row in board)

        if black_num > white_num:
            screen.blit(balack_win_surface,(80,100))

        elif black_num < white_num:
            screen.blit(white_win_surface,(80,100),)    
        else :
            screen.blit(draw_surface,(80,100))
        screen.blit(reset_surface,(80,200))
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN :  
                board = [
                            [0,0,0,0,0,0,0,0,],     #盤面のリセット
                            [0,0,0,0,0,0,0,0,],
                            [0,0,0,0,0,0,0,0,],
                            [0,0,0,1,-1,0,0,0,],
                            [0,0,0,-1,1,0,0,0,],
                            [0,0,0,0,0,0,0,0,],
                            [0,0,0,0,0,0,0,0,],
                            [0,0,0,0,0,0,0,0,]]
                player = 1
                game_over = False
                pass_num = 0


    if game_over == False and player == -1:#COMの処理
        if valid_position_list:
            com_x,com_y = random.choice(valid_position_list)
            x = com_x
            y = com_y
            flip_pieces(x, y)
            board[y][x] = player
            player *= -1
            pass_num = 0
        else:
            print('valid_position_listが空です')

        

    #イベント取得
    for event in pygame.event.get():
        if event.type == pygame.QUIT:#×ボタンで終了
            run = False
        if event.type == pygame.KEYDOWN:#escボタンで終了
            if event.key == pygame.K_ESCAPE:
                run = False        #マウスクリック
        if event.type == pygame.MOUSEBUTTONDOWN :#プレイヤーの動き
            if game_over == False:
                mx , my = pygame.mouse.get_pos()#クリックした位置の座標を取得
                x = mx // square_size#枠ごとに座標を決定する
                y = my // square_size
                #print(x,y)#座標確認
                
                if board[y][x] == 0 and (x , y) in valid_position_list:#石を置けるところをクリックした場合のみ，石を置く
                                                #クリックした場所がvalid_posision_list内に存在するかチェックする
                    #石をひっくり返す
                    flip_pieces(x , y)                  
                    board[y][x] = player  
                    player *= -1#ターン交代
                    pass_num = 0
       


    #更新
    pygame.display.update()
    clock.tick(FPS)
#--------------------------------------------------------------------------------------------

pygame.quit()