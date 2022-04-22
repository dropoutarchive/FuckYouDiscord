import os
import logging
import requests
from itertools import cycle
from base64 import b64decode
from concurrent.futures import ThreadPoolExecutor, as_completed

logging.basicConfig(
    level=logging.INFO,
    format="\x1b[38;5;63m[\x1b[0m%(asctime)s\x1b[38;5;63m]\x1b[0m %(message)s",
    datefmt="%H:%M:%S"
)

class FuckYouDiscord:

    def __init__(self):
        os.system("cls")

        with open("assets/tokens.txt", encoding="utf-8") as f:
            self.tokens = [i.strip() for i in f]
        with open("assets/proxies.txt", encoding="utf-8") as f:
            self.proxies = [i.strip() for i in f]

        self._oauth2_url = "https://discord.com/api/v9/oauth2/authorize?client_id=960237321482043424&response_type=code&redirect_uri=https%3A%2F%2Fthankyoudiscord.com%2Fcallback&scope=identify"
        self._oauth2_redirect = "https://thankyoudiscord.com/api/login"

        self.token = cycle(self.tokens)
        self.proxy = cycle(self.proxies)

        self.failed = 0
        self.success = 0

    def get_token_id(self, token):
        try:
            return b64decode(token.split(".")[0].encode()).decode()
        except:
            return "0" * 18

    def title_worker(self):
        while True:
            os.system("title [FuckYouDiscord] - Signed %s/%s" % (self.success, (self.failed + self.success)))

    def create_session(self, token: str):
        session = requests.Session()
        session.proxies.update({"https": "http://%s" % (next(self.proxy))})

        session.headers.update({
            "Authorization": token,
            "accept": "*/*",
            "accept-language": "en-US",
            "connection": "keep-alive",
            "cookie": "__cfduid=%s; __dcfduid=%s; locale=zh-CN; __stripe_mid=15964190-61b6-408f-a224-a1218d71991d77c46c; __stripe_sid=add771ce-9fd3-4ea9-9456-91f8f68defee203d29; __cf_bm=TK.KfKeAHAABcvneFA_2uiPQqqdZsAHwfTy7wBaoWEg-1650498920-0-AdCavSleyxAATvOZYoxgtEXOQ4qAo+II6wRIpEocfXdD1aRbchqCR7o0S3QYMOtY4INpJasHC9LYbq6KuDvKDSIaYngF1fARwW2HyGTGj/fYp9qa0lJD4KjivpchmjF99w==" % (os.urandom(43).hex(), os.urandom(32).hex()),
            "DNT": "1",
            "origin": "https://discord.com",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "referer": "https://discord.com/channels/@me",
            "TE": "Trailers",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9001 Chrome/83.0.4103.122 Electron/9.3.5 Safari/537.36",
            "X-Super-Properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC45MDAxIiwib3NfdmVyc2lvbiI6IjEwLjAuMTkwNDIiLCJvc19hcmNoIjoieDY0Iiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiY2xpZW50X2J1aWxkX251bWJlciI6ODMwNDAsImNsaWVudF9ldmVudF9zb3VyY2UiOm51bGx9"
        })

        return session

    def authenticate(self, session: requests.Session):
        response = session.post(self._oauth2_url, json={"permissions": "0","authorize": True})
        if response.status_code == 200:
            return response.json()["location"].split("=")[1]

    def login_with_code(self, session: requests.Session, code: str):
        response = session.post(self._oauth2_redirect, json={"code": code})
        if response.status_code == 200:
            return str(response.headers["set-cookie"]).split("session_id=")[1].split(";")[0]

    def signature(self, session: requests.Session):
        response = session.post("https://thankyoudiscord.com/api/banner/sign", json={"referrer": "https://github.com/dropout1337","captchaSolution": "captcha broke"})
        if response.status_code == 200:
            return True

    def create_task(self):
        token = next(self.token)
        session = self.create_session(token)

        code = self.authenticate(session)
        if code == None:
            logging.error("Failed to authenticate (\x1b[38;5;63m%s\x1b[0m)" % (self.get_token_id(token)))
            self.failed += 1
            return

        session_id = self.login_with_code(session, code)
        if session_id == None:
            logging.error("Failed to login with %s (\x1b[38;5;63m%s\x1b[0m)" % (code, self.get_token_id(token)))
            self.failed += 1
            return
        
        session.headers["cookie"] = "session_id=%s" % (session_id)
        if self.signature(session) == None:
            logging.error("Failed to sign banner %s (\x1b[38;5;63m%s\x1b[0m)" % (code, self.get_token_id(token)))
            self.failed += 1
            return

        logging.info("Successfully singed banner (\x1b[38;5;63m%s\x1b[0m)" % (self.get_token_id(token)))
        self.success += 1

    def run(self):
        with ThreadPoolExecutor(max_workers=5_000) as pool:
            pool.submit(self.title_worker)
            futures = [pool.submit(self.create_task) for x in range(len(self.tokens))]
            for x in as_completed(futures):
                x.result()

if __name__ == "__main__":
    fucker = FuckYouDiscord()
    fucker.run()