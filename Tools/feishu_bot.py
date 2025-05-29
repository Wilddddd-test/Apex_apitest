import json
import re
import os
from typing import Dict
import requests
from datetime import datetime
from rich.console import Console

console = Console()

def get_test_results() -> Dict:
    """从aomaker-report.html中获取测试结果"""
    try:
        # 读取aomaker-report.html
        with open("reports/aomaker-report.html", "r", encoding="utf-8") as f:
            content = f.read()
            
        # 查找legend-value中的数字
        legend_pattern = r'<span class="legend-value">(\d+)</span>'
        stats = re.findall(legend_pattern, content)
        
        if len(stats) >= 4:
            passed = int(stats[0])  # 第一个是通过数
            failed = int(stats[1])  # 第二个是失败数
            broken = int(stats[2])  # 第三个是阻塞数
            skipped = int(stats[3])  # 第四个是跳过数
            total = passed + failed + broken + skipped
            
            # 获取时间信息
            start_time_pattern = r'开始时间:</span>\s*<span[^>]*>([^<]+)</span>'
            end_time_pattern = r'结束时间:</span>\s*<span[^>]*>([^<]+)</span>'
            duration_pattern = r'运行时长:</span>\s*<span[^>]*>([^<]+)</span>'
            
            start_time = re.search(start_time_pattern, content)
            end_time = re.search(end_time_pattern, content)
            duration = re.search(duration_pattern, content)
            
            return {
                "stats": {
                    "total": total,
                    "passed": passed,
                    "failed": failed,
                    "broken": broken,
                    "skipped": skipped
                },
                "time": {
                    "start": start_time.group(1) if start_time else "未知",
                    "end": end_time.group(1) if end_time else "未知",
                    "duration": duration.group(1) if duration else "未知"
                }
            }
    except Exception as e:
        console.print(f"[red]Error reading test results: {str(e)}[/red]")
        return {
            "stats": {
                "total": 0,
                "passed": 0,
                "failed": 0,
                "broken": 0,
                "skipped": 0
            },
            "time": {
                "start": "未知",
                "end": "未知",
                "duration": "未知"
            }
        }

def create_status_tag(count: int, type_name: str, color: str) -> Dict:
    """创建状态标签"""
    return {
        "tag": "div",
        "text": {
            "tag": "lark_md",
            "content": f"**{type_name}**\n{count}"
        },
        "extra": {
            "tag": "img",
            "img_key": "img_v2_041b28e3-5680-48c2-9af2-497ace79333g",
            "alt": {
                "tag": "plain_text",
                "content": f"{type_name} {count}"
            }
        }
    }

def send_feishu_report():
    """发送测试报告到飞书"""
    try:
        # 获取测试结果
        results = get_test_results()
        stats = results["stats"]
        times = results["time"]
        
        # 计算通过率
        total = stats["total"]
        passed = stats["passed"]
        failed = stats["failed"]
        broken = stats["broken"]
        skipped = stats["skipped"]
        
        pass_rate = (passed / total * 100) if total > 0 else 0
        
        # 获取 GitHub Pages URL
        report_url = os.getenv('GITHUB_PAGES_URL', '')
        if report_url:
            # 确保URL末尾没有斜杠
            report_url = report_url.rstrip('/')
            # 添加报告文件路径
            aomaker_report_url = f"{report_url}/reports/aomaker-report.html"
            allure_report_url = f"{report_url}/allure/index.html"
        
        # 构建消息卡片
        message = {
            "msg_type": "interactive",
            "card": {
                "header": {
                    "title": {
                        "tag": "plain_text",
                        "content": "🎯 自动化测试报告"
                    },
                    "template": "blue" if pass_rate == 100 else "orange" if pass_rate >= 80 else "red"
                },
                "elements": [
                    {
                        "tag": "div",
                        "text": {
                            "tag": "lark_md",
                            "content": f"**⏱️ 执行时间**\n开始：{times['start']}\n结束：{times['end']}\n耗时：{times['duration']}"
                        }
                    },
                    {
                        "tag": "hr"
                    },
                    {
                        "tag": "div",
                        "fields": [
                            {
                                "is_short": True,
                                "text": {
                                    "tag": "lark_md",
                                    "content": f"**📊 总用例数**\n{total}"
                                }
                            },
                            {
                                "is_short": True,
                                "text": {
                                    "tag": "lark_md",
                                    "content": f"**✨ 通过率**\n{pass_rate:.1f}%"
                                }
                            }
                        ]
                    },
                    {
                        "tag": "div",
                        "fields": [
                            {
                                "is_short": True,
                                "text": {
                                    "tag": "lark_md",
                                    "content": f"**✅ 通过**\n{passed}"
                                }
                            },
                            {
                                "is_short": True,
                                "text": {
                                    "tag": "lark_md",
                                    "content": f"**❌ 失败**\n{failed}"
                                }
                            }
                        ]
                    },
                    {
                        "tag": "div",
                        "fields": [
                            {
                                "is_short": True,
                                "text": {
                                    "tag": "lark_md",
                                    "content": f"**⚠️ 阻塞**\n{broken}"
                                }
                            },
                            {
                                "is_short": True,
                                "text": {
                                    "tag": "lark_md",
                                    "content": f"**⏭️ 跳过**\n{skipped}"
                                }
                            }
                        ]
                    }
                ]
            }
        }

        # 如果有报告链接，添加查看按钮
        if report_url:
            message["card"]["elements"].append({
                "tag": "action",
                "actions": [
                    {
                        "tag": "button",
                        "text": {
                            "tag": "plain_text",
                            "content": "📊 完整测试报告"
                        },
                        "type": "primary",
                        "url": aomaker_report_url
                    },
                    {
                        "tag": "button",
                        "text": {
                            "tag": "plain_text",
                            "content": "📈 Allure测试报告"
                        },
                        "type": "primary",
                        "url": allure_report_url
                    }
                ]
            })
        
        # 发送消息
        webhook_url = os.getenv('FEISHU_WEBHOOK_URL', 'https://open.feishu.cn/open-apis/bot/v2/hook/4184dbcd-2483-412e-9b88-330009114d69')
        headers = {'Content-Type': 'application/json'}
        
        response = requests.post(webhook_url, json=message, headers=headers, timeout=10)
        response_json = response.json()
        
        if response.status_code == 200 and response_json.get("code") == 0:
            console.print("[green]Successfully sent test report to Feishu[/green]")
        else:
            console.print(f"[red]Failed to send message to Feishu. Status: {response.status_code}, Response: {response.text}[/red]")
            
    except Exception as e:
        console.print(f"[red]Error sending message to Feishu: {str(e)}[/red]")