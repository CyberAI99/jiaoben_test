# pbc_monitor

监控中国人民银行公开市场公告页面并通过 PushPlus 发送通知。

说明：
- 将 PushPlus token 放到环境变量 `PUSH_TOKEN`（推荐）或暂时保留在脚本中（不安全）。
- 使用虚拟环境运行：
  ```powershell
  python -m venv .venv
  .\.venv\Scripts\Activate.ps1
  pip install -r requirements.txt
  ```
