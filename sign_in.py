#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
9090 社区每日签到脚本
用于 GitHub Actions 自动签到
"""

import requests
import re
import sys
import os
from datetime import datetime

def hex_encode(s):
    """JavaScript hexEncode 函数的 Python 实现"""
    return ''.join(format(ord(c), 'x') for c in s)

def generate_token():
    """生成签到所需的 token"""
    # 从页面的 JavaScript 代码中提取逻辑
    a = 'e5ded5d12fa410a5f9e9f10a88c7f3be'[8:16]  # 取第 8-16 位
    b = 'f9e9f10a'
    mix = b[::-1] + '~' + a  # b 反转后加~再加 a
    obf = ''
    for i in range(len(mix)):
        obf += chr(ord(mix[i]) ^ (i % 7 + 3))
    token = hex_encode(obf)
    return token

def sign_in(cookie_str):
    """执行签到"""
    base_url = "https://qq9090.com"
    sign_url = f"{base_url}/plugin.php?id=k_misign:sign&operation=qiandao&format=empty"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Referer": f"{base_url}/sign.html",
        "X-Requested-With": "XMLHttpRequest",
        "Cookie": cookie_str
    }

    session = requests.Session()
    session.headers.update(headers)

    try:
        # 第一步：获取签到页面以获得正确的 formhash
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 正在获取签到页面...")
        response = session.get(f"{base_url}/sign.html")

        # 从页面中提取 formhash
        formhash_match = re.search(r'formhash=([a-f0-9]+)', response.text)
        if formhash_match:
            formhash = formhash_match.group(1)
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 获取到 formhash: {formhash}")
        else:
            # 如果无法获取 formhash，使用一个默认值
            formhash = "b9e03173"
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 未找到 formhash，使用默认值")

        # 生成 token
        token = generate_token()
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 生成 token: {token}")

        # 第二步：执行签到
        sign_url_with_hash = f"{sign_url}&formhash={formhash}&token={token}"
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 正在提交签到请求...")

        response = session.get(sign_url_with_hash)

        # 检查签到结果
        content = response.text

        # 检查是否已经签到过
        if '已经签到' in content or '已签到' in content or '您已经签到' in content:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✅ 您今天已经签到过了")
            return True

        # 检查签到成功
        if '签到成功' in content or 'qiandao_success' in content:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✅ 签到成功!")
            return True

        # 检查错误信息
        error_match = re.search(r'<p>([^<]+)</p>', content)
        if error_match:
            error_msg = error_match.group(1)
            if error_msg and error_msg != '点击这里返回上一页':
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ❌ 签到失败：{error_msg}")
                return False

        # 如果返回了签到页面，可能是签到成功了
        if '您今天还没有签到' not in content:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✅ 签到可能成功 (页面状态已改变)")
            return True
        else:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ❌ 签到失败：页面状态未改变")
            return False

    except requests.exceptions.RequestException as e:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ❌ 网络错误：{e}")
        return False
    except Exception as e:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ❌ 未知错误：{e}")
        return False

def main():
    # 从环境变量获取 cookie
    cookie = os.environ.get('SIGN_IN_COOKIE')

    if not cookie:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ❌ 错误：未找到 SIGN_IN_COOKIE 环境变量")
        sys.exit(1)

    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 🚀 开始执行 9090 社区签到...")
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Cookie: {cookie[:20]}...")

    success = sign_in(cookie)

    if success:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 🎉 签到流程完成!")
        sys.exit(0)
    else:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 💔 签到失败，请检查日志")
        sys.exit(1)

if __name__ == "__main__":
    main()
