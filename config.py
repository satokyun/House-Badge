import os

INPUT_DIR = "input"
TOKEN_FILE = os.path.join(INPUT_DIR, "token.txt")
PROXY_FILE = os.path.join(INPUT_DIR, "proxy.txt")

def setup_files():
    """必要なフォルダとテキストファイルを自動生成する"""
    if not os.path.exists(INPUT_DIR): 
        os.makedirs(INPUT_DIR)
    if not os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "w", encoding="utf-8") as f: 
            f.write("# ここに1行ずつトークンを貼り付けてください\n")
    if not os.path.exists(PROXY_FILE):
        with open(PROXY_FILE, "w", encoding="utf-8") as f: 
            f.write("# ここに1行ずつプロキシを貼り付けてください\n")

def load_tokens():
    """token.txt から重複を除外してトークンを読み込む"""
    if not os.path.exists(TOKEN_FILE): 
        return []
    with open(TOKEN_FILE, "r", encoding="utf-8") as f:
        return list(dict.fromkeys([line.strip() for line in f if line.strip() and not line.strip().startswith("#")]))

def load_proxies():
    """proxy.txt から重複を除外してプロキシを読み込む"""
    if not os.path.exists(PROXY_FILE): 
        return []
    proxies = []
    with open(PROXY_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"): 
                continue
            if not (line.startswith("http://") or line.startswith("https://") or line.startswith("socks")): 
                line = "http://" + line
            proxies.append(line)
    return list(dict.fromkeys(proxies))