# 9090 社区自动签到

用于 9090 社区 (https://qq9090.com) 的每日自动签到脚本。

## ✅ 测试状态

- **首次测试**: 已成功签到 (2026-02-19)
- **签到结果**: 成功完成今日签到

## 文件结构

```
.
├── .github/
│   └── workflows/
│       └── sign-in.yml      # GitHub Actions 工作流配置
├── sign_in.py               # Python 签到脚本
├── requirements.txt         # Python 依赖
└── README.md               # 本文件
```

## 设置步骤

### 1. Fork 或克隆此仓库

### 2. 配置 GitHub Secrets

1. 进入你的 GitHub 仓库
2. 点击 **Settings** → **Secrets and variables** → **Actions**
3. 点击 **New repository secret**
4. 添加以下 secret:
   - **Name**: `SIGN_IN_COOKIE`
   - **Value**: 你的 9090 社区 cookie(完整的 cookie 字符串)

### 3. 获取 Cookie 的方法

1. 在浏览器中访问 https://qq9090.com 并登录
2. 按 F12 打开开发者工具
3. 进入 **Network** (网络) 标签
4. 刷新页面
5. 点击任意请求，查看 **Request Headers** 中的 **Cookie** 字段
6. 复制完整的 cookie 字符串

### 4. 启用 GitHub Actions

1. 进入你的 GitHub 仓库的 **Actions** 标签
2. 找到 **9090 Community Daily Sign-in** 工作流
3. 点击 **Enable workflow**

### 5. 手动测试

1. 进入 **Actions** → **9090 Community Daily Sign-in**
2. 点击 **Run workflow**
3. 选择分支并点击 **Run workflow**
4. 查看运行日志确认签到结果

## 定时任务说明

- 默认每天 UTC 时间 00:00 运行 (北京时间 08:00)
- 如需修改时间，编辑 `.github/workflows/sign-in.yml` 中的 cron 表达式

## 本地测试

```bash
# 安装依赖
pip install -r requirements.txt

# 设置 cookie 环境变量 (Windows PowerShell)
$env:SIGN_IN_COOKIE="你的 cookie"
python sign_in.py

# 或者 (Linux/Mac)
export SIGN_IN_COOKIE="你的 cookie"
python sign_in.py
```

## 工作原理

脚本模拟了网站的签到流程:

1. 访问签到页面获取 `formhash` (安全令牌)
2. 根据网站的 JavaScript 逻辑生成 `token`
3. 发送签到请求，包含 `formhash` 和 `token`
4. 检查响应确认签到结果

## 注意事项

- Cookie 可能会过期，如果签到失败请更新 cookie
- 请确保 cookie 包含完整的认证信息
- 此脚本仅供个人学习使用
