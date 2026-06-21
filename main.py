import os
import sys
import asyncio
import time
import random
import aioconsole

# 分割した自作ファイル（モジュール）から全機能をインポート
import config
import ui
import badge
from utils import log_message

RESET  = "\033[0m"
BOLD   = "\033[1m"
GREEN  = "\033[38;5;46m"
YELLOW = "\033[38;5;226m"
RED    = "\033[38;5;196m"

async def main():
    # WindowsのコマンドプロンプトやPowerShellでANSIカラーコードを有効化する魔法
    os.system('')  
    
    # フォルダや各種設定ファイルの準備
    config.setup_files()
    
    tokens = config.load_tokens()
    proxies = config.load_proxies()
    
    # トークンが空だった場合のガード
    if not tokens:
        print(f"{RED}[!] {config.TOKEN_FILE} にトークンを入れて再起動してください。{RESET}")
        return

    while True:
        # メイン画面のクリア
        os.system('cls' if os.name == 'nt' else 'clear')
        ui.stop_animation = False
        
        # UIモジュールからウネウネアニメーションを呼び出して、非同期で裏実行させる
        animation_task = asyncio.create_task(ui.draw_moving_banner())
        
        # ユーザーのキー入力を待つ
        choice = (await aioconsole.ainput()).strip()
        
        # 入力されたら即座にウネウネアニメーションのタスクを停止
        ui.stop_animation = True
        await animation_task
        
        if choice == '1':
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"\n{BOLD}📂 なんのバッジにしますか？{RESET}\n")
            print(" [1] House of Bravery    (紫のバッジ)")
            print(" [2] House of Brilliance (赤のバッジ)")
            print(" [3] House of Balance    (緑のバッジ)")
            print(" [4] バッジを削除する (Delete)\n")
            
            badge_choice = (await aioconsole.ainput(f"{BOLD}番号を選択してください > {RESET}")).strip()
            
            if badge_choice in ['1', '2', '3', '4']:
                os.system('cls' if os.name == 'nt' else 'clear')
                log_message("INFO", "順次安全同期処理を開始します...", 51)
                print("")
                
                # トークンファイルに入っているアカウントを1件ずつ順番に処理
                for index, token in enumerate(tokens, start=1):
                    # プロキシが設定されていれば順繰り（ループ）で割り当て、無ければNone
                    proxy = proxies[(index - 1) % len(proxies)] if proxies else None
                    
                    # バッジ処理の実行
                    badge.process_badge(badge_choice, token, index, proxy)
                    
                    # アカウントを安全に守るためのランダムなウェイト(ディレイ)を挟む
                    if index < len(tokens):
                        time.sleep(random.uniform(1.0, 2.0))
                        
                print(f"\n{GREEN}{BOLD}[✅] すべてのアカウントのバッジ処理が完了しました！{RESET}")
                await aioconsole.ainput("\nEnterキーを押してメニューに戻ります...")
            else:
                os.system('cls' if os.name == 'nt' else 'clear')
                log_message("ERROR", "1〜4の数値を入力してください。", 196)
                await asyncio.sleep(2)
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            log_message("ERROR", "無効な番号です。1を入力してください。", 196)
            await asyncio.sleep(2)

if __name__ == "__main__":
    try: 
        asyncio.run(main())
    except KeyboardInterrupt: 
        sys.exit()