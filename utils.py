from datetime import datetime

RESET     = "\033[0m"
BOLD      = "\033[1m"

def get_timestamp():
    """写真仕様のピンク赤枠付きの美しいタイムスタンプを生成"""
    current_time = datetime.now().strftime("%H:%M:%S")
    return f"\033[38;5;203m[\033[38;5;250m{current_time}\033[38;5;203m]{RESET}"

def log_message(status_type, message, color_code):
    """写真のログ画面（・区切り、太字、右矢印記号）を完全に再現"""
    time_str = get_timestamp()
    print(f"{time_str} ・ \033[38;5;{color_code}m{BOLD}{status_type:<5}{RESET} » {message}")