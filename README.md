# Apex API 自动化测试项目

这是一个基于 Python 的 Apex API 自动化测试项目，使用 AoMaker 和 Allure 进行测试执行和报告生成。

## 项目特点

- 使用 AoMaker 框架进行 API 测试
- 支持 Allure 和 AoMaker 双重测试报告
- 通过 GitHub Actions 实现自动化测试
- 使用 GitHub Pages 托管测试报告
- 集成飞书机器人通知测试结果
- 支持任意分支推送自动触发测试

## 项目结构

```
.
├── .github/workflows/    # GitHub Actions 工作流配置
├── Tools/               # 工具类
│   └── feishu_bot.py   # 飞书机器人通知
├── testcases/          # 测试用例
│   ├── conftest.py     # 测试配置和fixtures
│   ├── test_create_order.py  # 订单相关测试
│   └── ...
├── reports/            # 测试报告
├── config.yaml         # AoMaker配置文件
├── requirements.txt    # 项目依赖
└── run.py             # 测试运行入口
```

## 环境要求

- Python 3.9+
- 依赖包：见 requirements.txt

## 配置说明

### AoMaker 配置

项目使用 `config.yaml` 进行 AoMaker 框架配置：

```yaml
env:
  test:  # 测试环境
    base_url: ${APEX_OMNI_HTTP_TEST}
    network_id: ${NETWORKID_TEST}
  prod:  # 生产环境
    base_url: ${APEX_OMNI_HTTP_MAIN}
    network_id: ${NETWORKID_MAIN}

default_env: prod  # 默认环境

report:
  title: "Apex API 自动化测试报告"
  description: "API自动化测试报告"
  language: zh-CN
```

### 环境变量

项目使用环境变量管理敏感信息，需要配置以下环境变量：

```bash
# API 认证信息
APEX_API_KEY=your_key
APEX_API_SECRET=your_secret
APEX_API_PASSPHRASE=your_passphrase

# 区块链信息
APEX_SEEDS=your_seeds
APEX_L2_KEY=your_l2_key

# 环境配置
APEX_OMNI_HTTP_TEST=test_api_url
APEX_OMNI_HTTP_MAIN=prod_api_url
NETWORKID_TEST=test_network_id
NETWORKID_MAIN=prod_network_id
```

### GitHub Actions 配置

在 GitHub 仓库的 Settings -> Secrets and variables -> Actions 中添加上述环境变量。

### 飞书机器人配置

在 GitHub Secrets 中配置：
- FEISHU_WEBHOOK_URL：飞书机器人的 Webhook 地址

## 运行测试

### 本地运行

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 运行测试：
```bash
python run.py
```

### GitHub Actions 运行

项目配置了以下自动触发条件：
- 推送到任意分支（自动触发测试）
- 创建 Pull Request 到 main 分支
- 每天 UTC 00:00 定时运行
- 手动触发

## 测试报告

测试完成后可通过以下方式查看报告：

1. GitHub Pages：
   - AoMaker报告：`https://<username>.github.io/<repo>/reports/aomaker-report.html`
   - Allure报告：`https://<username>.github.io/<repo>/allure/index.html`

2. 飞书通知：
   - 测试完成后会自动发送消息到飞书群
   - 包含测试结果统计和报告链接

## 主要功能

### 订单测试
- 创建市价买单
- 创建限价卖单
- 更多测试用例开发中...

## 注意事项

1. 本项目为公开仓库，注意不要提交敏感信息
2. 所有敏感信息通过环境变量管理
3. 测试报告通过 GitHub Pages 公开访问
4. 确保 config.yaml 中不包含敏感信息，使用环境变量引用

## 开发计划

- [ ] 添加更多 API 测试用例
- [ ] 优化测试报告展示
- [ ] 添加更多自动化测试场景

## 贡献指南

1. Fork 本仓库
2. 创建您的特性分支
3. 提交您的更改
4. 推送到分支
5. 创建新的 Pull Request