import requests
import time
import json
import re


def get_ip():
    ip_content = "http://127.0.0.1:52526"

    ip_pattern = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}$'
    if re.match(ip_pattern, ip_content):
        proxies = {
            'http': f'http://{ip_content}',
            'https': f'http://{ip_content}'
        }
        return proxies
    else:
        print(f'获取的IP格式无效: {ip_content}')
        return None


def get_data(kw):
    post_url = 'https://fanyi.baidu.com/sug'
    data = {
        'kw': kw
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.51'
    }

    proxies = get_ip()

    max_retries = 3
    for attempt in range(max_retries):
        try:
            if proxies:
                print(f'使用代理: {list(proxies.values())[0]}')
                response = requests.post(url=post_url, data=data, headers=headers, proxies=proxies, timeout=10)
            else:
                print('未获取到代理，使用默认网络')
                response = requests.post(url=post_url, data=data, headers=headers, timeout=10)

            response.raise_for_status()

            data_json = response.json()

            if 'data' in data_json and len(data_json['data']) > 0:
                for item in data_json['data']:
                    for key, value in item.items():
                        print(f"{key}: {value}")
                    print('-' * 30)
                break
            else:
                print(f'返回数据格式异常: {data_json}')
                time.sleep(1)

        except requests.exceptions.RequestException as e:
            print(f'请求出错 (尝试 {attempt + 1}/{max_retries}): {e}')
            if proxies:
                print('将尝试下一个代理')
            time.sleep(2)
    else:
        print('所有尝试均失败')


def main():
    while True:
        kw = input("请输入需要翻译的单词（输入q退出）：")
        if kw.lower() == 'q':
            break
        get_data(kw)


if __name__ == '__main__':
    main()