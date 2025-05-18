import sys
import json
import time
import requests
import websocket
from colorama import init, Fore, Back, Style

init()  # colorama 초기화

# ASCII 아트로 타이틀 표시
title = """
╔══════════════════════════════════════════╗
║          제작자: sorin_wo               ║
╚══════════════════════════════════════════╝
"""

print(Fore.CYAN + title + Style.RESET_ALL)

status = "online"
custom_status = input(Fore.YELLOW + "상태 메시지를 입력하세요: " + Style.RESET_ALL)
usertoken = input(Fore.YELLOW + "토큰을 입력하세요: " + Style.RESET_ALL)

headers = {"Authorization": usertoken, "Content-Type": "application/json"}

print(Fore.YELLOW + "토큰 검증 중..." + Style.RESET_ALL)

validate = requests.get("https://discordapp.com/api/v9/users/@me", headers=headers)
if validate.status_code != 200:
    print(Fore.RED + "[오류] 토큰이 유효하지 않을 수 있습니다. 다시 확인해주세요." + Style.RESET_ALL)
    sys.exit()

userinfo = validate.json()
username = userinfo["username"]
discriminator = userinfo["discriminator"]
userid = userinfo["id"]


def onliner(token, status):
    ws = websocket.WebSocket()
    ws.connect("wss://gateway.discord.gg/?v=9&encoding=json")
    start = json.loads(ws.recv())
    heartbeat = start["d"]["heartbeat_interval"]
    
    auth = {
        "op": 2,
        "d": {
            "token": token,
            "properties": {
                "$os": "Windows 10",
                "$browser": "Google Chrome",
                "$device": "Windows",
            },
            "presence": {
                "status": status,
                "since": 0,
                "activities": [{
                    "type": 0,
                    "name": custom_status,
                    "created_at": int(time.time() * 1000)
                }],
                "afk": False
            }
        },
        "s": None,
        "t": None
    }
    
    ws.send(json.dumps(auth))
    
    while True:
        try:
            msg = json.loads(ws.recv())
            if msg["op"] == 10:
                heartbeat = msg["d"]["heartbeat_interval"]
            elif msg["op"] == 1:
                ws.send(json.dumps({"op": 1, "d": None}))
        except:
            break
        
        time.sleep(heartbeat / 1000)
        ws.send(json.dumps({"op": 1, "d": None}))


def run_onliner():
    print(Fore.GREEN + "✓ 토큰이 유효합니다!" + Style.RESET_ALL)
    print(Fore.CYAN + f"\n► 계정 정보:" + Style.RESET_ALL)
    print(f"• 사용자: {Fore.YELLOW}{username}#{discriminator}{Style.RESET_ALL}")
    print(f"• 아이디: {Fore.YELLOW}{userid}{Style.RESET_ALL}")
    print(f"\n{Fore.MAGENTA}24/7 온라인 상태 유지를 시작합니다...{Style.RESET_ALL}")
    
    while True:
        try:
            onliner(usertoken, status)
            print(Fore.GREEN + "♥ 온라인 상태 유지 중..." + Style.RESET_ALL)
            time.sleep(30)
        except Exception as e:
            print(Fore.RED + f"[오류 발생] {e}" + Style.RESET_ALL)
            time.sleep(5)


run_onliner()
