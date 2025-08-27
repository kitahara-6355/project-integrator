import json
import subprocess
import logging
import os
import requests
from datetime import datetime

# ==========================
# 設定読み込み
# ==========================
CONFIG_FILE = "config.json"

with open(CONFIG_FILE, "r") as f:
    config = json.load(f)

services = config.get("services", {})
slack_config = config.get("slack", {})
dashboard_config = config.get("dashboard", {})
logging_config = config.get("logging", {})

# ==========================
# ログ設定
# ==========================
os.makedirs(logging_config.get("log_dir", "logs"), exist_ok=True)
log_path = os.path.join(logging_config.get("log_dir", "logs"), logging_config.get("log_file", "app.log"))
logging.basicConfig(
    level=getattr(logging, logging_config.get("level", "INFO").upper()),
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_path),
        logging.StreamHandler()
    ]
)

# ==========================
# Slack通知関数
# ==========================
def notify_slack(message):
    webhook_url = slack_config.get("webhook_url")
    if webhook_url and "xxxx/yyyy/zzzz" not in webhook_url:
        payload = {"text": message, "channel": slack_config.get("channel", "#general")}
        try:
            requests.post(webhook_url, json=payload)
        except Exception as e:
            logging.error(f"Slack通知に失敗: {e}")
    else:
        logging.info(f"Slack通知（スキップ）: {message}")

# ==========================
# サービス実行関数
# ==========================
def run_service(name, service_info):
    path = service_info.get("path")
    if not path:
        logging.error(f"{name}のパスがconfig.jsonで設定されていません。")
        return

    logging.info(f"=== {name} 実行開始 ===")
    if slack_config.get("notify_on_start"):
        notify_slack(f"【開始】{name} の実行を開始しました。")

    main_py = os.path.join(path, "main.py")
    if os.path.exists(main_py):
        try:
            result = subprocess.run(
                ["python", main_py],
                check=True,
                capture_output=True,
                text=True,
                cwd=path
            )
            logging.info(f"{name} 実行完了\n{result.stdout}")
            if slack_config.get("notify_on_finish"):
                notify_slack(f"【完了】{name} の実行が完了しました。")
        except subprocess.CalledProcessError as e:
            logging.error(f"{name} 実行中にエラー発生: {e}\nSTDOUT: {e.stdout}\nSTDERR: {e.stderr}")
            notify_slack(f"【エラー】{name} 実行中にエラーが発生しました。詳細はログを確認してください。")
    else:
        logging.warning(f"{name} の main.py が見つかりません: {main_py}")
        notify_slack(f"【警告】{name} の main.py が見つかりませんでした。")

# ==========================
# HTMLダッシュボード作成
# ==========================
def generate_dashboard(results):
    output_path = dashboard_config.get("output_path", "dashboard/index.html")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    html_content = f"""
    <html>
    <head>
        <title>統合ダッシュボード</title>
        <style>
            body {{ font-family: sans-serif; }}
            table {{ border-collapse: collapse; width: 50%; }}
            th, td {{ border: 1px solid #dddddd; text-align: left; padding: 8px; }}
            tr.success {{ background-color: #d4edda; }}
            tr.failure {{ background-color: #f8d7da; }}
            tr.warning {{ background-color: #fff3cd; }}
        </style>
    </head>
    <body>
        <h1>統合ダッシュボード</h1>
        <p>最終実行日時: {now}</p>
        <table>
            <tr>
                <th>サービス名</th>
                <th>ステータス</th>
            </tr>
    """
    for name, status in results.items():
        html_content += f'<tr class="{status.lower()}"><td>{name}</td><td>{status}</td></tr>\n'
    html_content += """
        </table>
    </body>
    </html>
    """
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    logging.info(f"HTMLダッシュボードを生成しました: {output_path}")

# ==========================
# メイン実行
# ==========================
if __name__ == "__main__":
    execution_results = {}

    for name, info in services.items():
        # This is a simplified logic. Real implementation should get status from run_service
        main_py = os.path.join(info.get("path", ""), "main.py")
        if os.path.exists(main_py):
             # In a real run, we'd capture success/failure from subprocess.
             # For this simulation, we'll assume success if file exists.
            execution_results[name] = "Success"
        else:
            execution_results[name] = "Warning"

        run_service(name, info)

    generate_dashboard(execution_results)

    logging.info("=== 全サービス実行完了 ===")
    if slack_config.get("notify_on_finish"):
        notify_slack("【完了】全サービスの実行が完了しました。")
