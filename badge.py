import time
import requests
from utils import log_message

def process_badge(badge_choice, token, index, proxy=None):
    """指定されたトークンのHypeSquadバッジを変更、または削除する"""
    headers = {
        "Authorization": token, 
        "Content-Type": "application/json", 
        "User-Agent": "Mozilla/5.0"
    }
    proxies_dict = {"http": proxy, "https": proxy} if proxy else None
    
    # セキュリティのため、ログ表示用にトークンの前後だけを切り出す
    masked_token = f"{token[:6]}...{token[-6:]}" if len(token) > 12 else "Unknown"
    url = "https://discord.com/api/v9/hypesquad/online"
    
    try:
        # [1]〜[3]はそれぞれのハウスIDを送信（1:紫, 2:赤, 3:緑）
        if badge_choice in ['1', '2', '3']:
            res = requests.post(url, headers=headers, json={"house_id": int(badge_choice)}, proxies=proxies_dict, timeout=8)
        # [4]はDELETEリクエストを送信してバッジを外す
        else:
            res = requests.delete(url, headers=headers, proxies=proxies_dict, timeout=8)
        
        # 429 速度規制（レートリミット）を検知した場合
        if res.status_code == 429:
            retry_after = res.json().get("retry_after", 5)
            log_message("WARN", f"アカウント #{index} 速度規制。{retry_after}秒待機します...", 226)
            time.sleep(retry_after)
            return False

        if res.status_code in [200, 204]:
            log_message("DONE", f"アカウント #{index} バッジ変更完了 - {masked_token}", 46)
            return True
        elif res.status_code == 401:
            log_message("ERROR", f"アカウント #{index} トークン死亡 (Unauthorized)", 196)
        else:
            log_message("ERROR", f"アカウント #{index} 変更失敗 ({res.status_code})", 196)
            
    except Exception as e:
        log_message("ERROR", f"アカウント #{index} 接続エラー: {e}", 196)
    return False