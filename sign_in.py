#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
9090 社区每日签到脚本
使用 Playwright 进行浏览器自动化签到
用于 GitHub Actions 自动签到
"""

import sys
import os
from datetime import datetime
from playwright.sync_api import sync_playwright

def sign_in(cookie_str):
    """执行签到"""
    base_url = "https://qq9090.com"
    sign_url = f"{base_url}/sign.html"

    with sync_playwright() as p:
        # 启动浏览器
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080}
        )
        page = context.new_page()

        try:
            # 设置 cookie
            cookies = []
            for cookie_part in cookie_str.split('; '):
                if '=' in cookie_part:
                    name, value = cookie_part.split('=', 1)
                    cookies.append({
                        'name': name.strip(),
                        'value': value.strip(),
                        'domain': 'qq9090.com',
                        'path': '/'
                    })
            context.add_cookies(cookies)

            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 正在访问签到页面...")

            # 访问签到页面
            page.goto(sign_url, wait_until="networkidle", timeout=30000)

            # 等待页面加载
            page.wait_for_timeout(2000)

            # 检查页面状态
            page_content = page.content()

            # 检查是否已经签到过
            if '您今天还没有签到' not in page_content:
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✅ 您今天已经签到过了")
                browser.close()
                return True

            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 正在点击签到按钮...")

            # 查找签到按钮并点击
            sign_button = page.locator('#JD_sign')
            if sign_button.count() > 0:
                sign_button.click()
                page.wait_for_timeout(3000)

                # 检查签到结果
                new_content = page.content()

                if '您今天还没有签到' not in new_content:
                    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✅ 签到成功!")
                    browser.close()
                    return True
                else:
                    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ❌ 签到失败：页面状态未改变")
                    browser.close()
                    return False
            else:
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ❌ 未找到签到按钮")
                browser.close()
                return False

        except Exception as e:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ❌ 错误：{e}")
            browser.close()
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
