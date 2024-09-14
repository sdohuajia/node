import json
import requests
import datetime
import urllib3
from loguru import logger
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

KeepAliveURL = "https://www.aeropres.in/chromeapi/dawn/v1/userreward/keepalive"
GetPointURL = "https://api.gradient.network/api/point/stats"
LoginURL = "https://www.aeropres.in//chromeapi/dawn/v1/user/login/v2"

# 创建一个请求会话
session = requests.Session()

# 设置通用请求头
headers = {
    "Content-Type": "application/json",
    "Origin": "chrome-extension://caacbgbklghmpodbdafajbgdnegacfmo",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.9",
    "Priority": "u=1, i",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
}

def login(USERNAME, PASSWORD):
    current_time = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='milliseconds').replace("+00:00", "Z")
    data = {
        "username": USERNAME,
        "password": PASSWORD,
        "logindata": {
            "_v": "1.0.7",
            "datetime": current_time
        }
    }
    login_data = json.dumps(data)
    logger.info(f'[2] 登录数据： {login_data}')
    try:
        r = session.post(LoginURL, login_data, headers=headers, verify=False).json()
        logger.debug(r)
        token = r['data']['token']
        logger.success(f'[√] 成功获取AuthToken {token}')
        return token
    except Exception as e:
        logger.error(f'[x] 登录失败，错误：{e}')

def KeepAlive(USERNAME, TOKEN):
    data = {"username": USERNAME, "extensionid": "caacbgbklghmpodbdafajbgdnegacfmo", "numberoftabs": 0, "_v": "1.0.1"}
    json_data = json.dumps(data)
    headers['authorization'] = "Bearer " + str(TOKEN)
    r = session.post(KeepAliveURL, data=json_data, headers=headers, verify=False).json()
    logger.info(f'[3] 保持链接中... {r}')

def GetPoint(TOKEN):
    headers['authorization'] = "Bearer " + str(TOKEN)
    r = session.get(GetPointURL, headers=headers, verify=False).json()
    logger.success(f'[√] 成功获取Point {r}')

def main(USERNAME, PASSWORD):
    TOKEN = login(USERNAME, PASSWORD)
    if TOKEN:
        while True:
            try:
                # 执行保持活动和获取点数的操作
                KeepAlive(USERNAME, TOKEN)
                GetPoint(TOKEN)
            except Exception as e:
                logger.error(e)

if __name__ == '__main__':
    with open('password.txt', 'r') as f:
        username, password = f.readline().strip().split(':')
    main(username, password)
