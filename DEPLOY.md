# 部署與更新指南 (Deployment Guide)

本指南說明如何將本地端的修改更新到伺服器上。

## 1. 本地端操作 (Local)

在您的電腦上，開啟終端機 (Terminal) 並執行以下指令，將修改提交到 Git：

```bash
# 1. 確認目前狀態
git status

# 2. 加入所有修改 (包含刪除的檔案)
git add .

# 3. 提交修改
git commit -m "Cleanup: Remove unused files and legacy code"

# 4. 推送到遠端倉庫 (GitHub/GitLab)
git push origin main
```

> **注意**: 如果您還沒有設定 Git 遠端倉庫，請先設定。

## 2. 伺服器端操作 (Server)

連線到您的伺服器，並執行以下步驟：

```bash
# 1. 進入專案目錄
cd /path/to/your/project/quiz_gui

# 2. 拉取最新程式碼
git pull origin main

# 3. (選擇性) 如果有安裝新的套件，請更新依賴
# pip install -r requirements.txt

# 4. 重新啟動 Streamlit 應用程式
# 如果您是使用 nohup 或 tmux 執行：
pkill -f "streamlit run quiz_app_gui.py"
nohup streamlit run quiz_app_gui.py --server.port 8501 &

# 或者如果您只是在測試，直接執行：
# streamlit run quiz_app_gui.py
```

## 3. 驗證

開啟瀏覽器訪問您的伺服器網址 (例如 `http://your-server-ip:8501`)，確認應用程式運作正常，且舊的功能 (如錯題複習) 依然可用。
