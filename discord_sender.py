import requests
import random
import time
import logging
import json
from typing import List, Optional

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class DiscordSender:
    def __init__(self, min_interval: int = 21600, max_interval: int = 21600):  # 默认6小时 = 21600秒
        self.running = True
        self.accounts = self.load_accounts()  # 加载所有账号信息
        self.min_interval = min_interval  # 最小间隔时间（秒）
        self.max_interval = max_interval  # 最大间隔时间（秒）
        self.send_order = []  # 发送顺序列表

    def load_accounts(self) -> List[dict]:
        """从data.txt加载账号信息，包括token、钱包地址和代理"""
        accounts = []
        try:
            with open('data.txt', 'r') as f:
                for line in f:
                    if line.strip() and '----' in line:
                        parts = line.strip().split('----')
                        account = {
                            'token': parts[0],
                            'wallet': parts[1],
                        }
                        # 如果有代理信息，则添加代理
                        if len(parts) > 2:
                            account['proxy'] = parts[2]
                        accounts.append(account)
            return accounts
        except Exception as e:
            logging.error(f"加载账号信息失败: {e}")
            return []

    def shuffle_send_order(self):
        """生成新的随机发送顺序"""
        self.send_order = list(range(len(self.accounts)))
        random.shuffle(self.send_order)
        order_str = ", ".join([str(i+1) for i in self.send_order])
        logging.info(f"本轮发送顺序: {order_str}")

    def chat(self, channel_id: str):
        """发送消息到指定频道，每个账号使用自己的token"""
        round_count = 1
        while self.running:
            if not self.accounts:
                logging.error("没有可用的账号信息")
                return

            logging.info(f"\n开始第 {round_count} 轮发送")
            # 生成新的随机发送顺序
            self.shuffle_send_order()

            # 按随机顺序发送所有账号的消息
            for i, index in enumerate(self.send_order, 1):
                if not self.running:
                    return

                # 获取当前账号信息
                account = self.accounts[index]
                token = account['token']
                wallet = account['wallet']
                proxy = account.get('proxy')  # 获取代理信息，如果没有则为None

                headers = {
                    "Authorization": token,
                    "Content-Type": "application/json",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"
                }

                try:
                    msg = {
                        "content": f"!faucet {wallet}",
                        "nonce": str(random.randint(100000, 999999)),
                        "tts": False
                    }

                    # 准备请求参数
                    request_params = {
                        "url": f"https://discord.com/api/v10/channels/{channel_id}/messages",
                        "headers": headers,
                        "json": msg,
                        "timeout": 30
                    }

                    # 如果有代理，添加代理配置
                    if proxy:
                        request_params["proxies"] = {
                            "http": proxy,
                            "https": proxy
                        }
                        logging.info(f"使用代理: {proxy}")
                    else:
                        logging.info("不使用代理")

                    res = requests.post(**request_params)
                    
                    if res.status_code in [200, 201]:
                        logging.info(f"本轮第 {i}/{len(self.accounts)} 个账号发送成功 (账号序号: {index + 1})")
                        logging.info(f"Token: {token[:30]}...")
                        logging.info(f"钱包地址: {wallet}")
                    else:
                        logging.error(f"发送消息失败，状态码: {res.status_code}, 响应: {res.text}")
                    
                    # 在账号之间等待5-20秒
                    time.sleep(random.randint(5, 20))
                    
                except requests.exceptions.RequestException as e:
                    logging.error(f"请求失败: {str(e)}")
                    continue
                except Exception as e:
                    logging.error(f"发送消息时出错: {e}")
                    if not self.running:
                        return

            # 所有账号发送完成后，等待指定时间再开始下一轮
            sleep_time = random.randint(self.min_interval, self.max_interval)
            logging.info(f"第 {round_count} 轮发送完成，{sleep_time}秒后开始下一轮")
            round_count += 1
            time.sleep(sleep_time)

    def stop(self):
        """停止发送消息"""
        self.running = False

def main():
    # 使用示例
    sender = DiscordSender(
        min_interval=21666,  # 6小时
        max_interval=21688   # 6小时
    )
    
    channel_id = "1037811694564560966"  # Discord频道ID
    
    # 开始发送消息
    sender.chat(channel_id)

if __name__ == "__main__":
    main() 
