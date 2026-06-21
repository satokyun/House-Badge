import sys
import asyncio

RESET     = "\033[0m"
BOLD      = "\033[1m"

YOATOOL_RAINBOW = [196, 202, 208, 214, 220, 226, 190, 154, 118, 82, 46, 47, 48, 49, 50, 51, 45, 39, 33, 27, 21, 57, 93, 129, 165, 201]

RAW_ASCII = r"""
███████╗████████╗ ██████╗ ███╗   ██╗
██╔════╝╚══██╔══╝██╔═══██╗████╗  ██║
╚█████╗    ██║   ██║   ██║██╔██╗ ██║
 ╚═══██╗   ██║   ██║   ██║██║╚██╗██║
██████╔╝   ██║   ╚██████╔╝██║ ╚████║
╚═════╝    ╚═╝    ╚═════╝ ╚═╝  ╚═══╝"""

# 外部ファイルからアニメーションを安全に停止させるためのフラグ
stop_animation = False

async def draw_moving_banner():
    """ASCIIアートのグラデーションを永久にうねうねと動かし続けるタスク"""
    global stop_animation
    lines = RAW_ASCII.strip("\n").split("\n")
    frame = 0
    
    while not stop_animation:
        # 画面のカーソルを左上に固定して上書き描画（画面のチラつきを完全に防止）
        sys.stdout.write("\033[H")
        
        for y, line in enumerate(lines):
            grad_line = ""
            for x, char in enumerate(line):
                # 横（x）と縦（y）、そしてフレーム（時間）を組み合わせてウェーブを表現
                color_index = (x + y * 2 + frame) % len(YOATOOL_RAINBOW)
                grad_line += f"\033[38;5;{YOATOOL_RAINBOW[color_index]}m{char}"
            sys.stdout.write(grad_line + RESET + "\n")
            
        sys.stdout.write(f"\033[38;5;39m{BOLD}============== STQN v8.0 [STABLE MODULE] =============={RESET}\n")
        sys.stdout.write("\n [1] House Badge\n\n")
        sys.stdout.write(f"\033[38;5;39m========================================================{RESET}\n")
        sys.stdout.write(f"\n{BOLD}メニューの番号を選択してください > {RESET}")
        sys.stdout.flush()
        
        frame += 1
        await asyncio.sleep(0.05)