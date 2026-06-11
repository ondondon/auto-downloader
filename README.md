# Auto-Downloader

全自動化本地下載器 — 一個基於 gallery-dl 的 Android App，支援 Twitter/X、Pixiv、Instagram、Reddit 等平台。

## 功能特色

- 🌐 支援多平台自動檢測 (Twitter/X, Pixiv, Instagram, Reddit, Danbooru...)
- 📁自動儲存至 Downloads/AutoDownloader 目錄
- 📊 即時下載狀態與日誌顯示
- 🔄佇列式下載管理
- 🤖 GitHub Actions 全自動 CI/CD APK 打包

## 技術架構

- **UI Framework**: Flet (Python)
- **下載核心**: gallery-dl
- **打包工具**: Buildozer (Python-for-Android)
- **CI/CD**: GitHub Actions

## 快速開始

### 本地開發

```bash
#執行 setup script
bash setup_project.sh

# 啟動 Flet UI (測試模式)
source venv/bin/activate
python -m flet run app/main.py
```

### GitHub Actions 自動編譯

1. 將代碼 push 到 GitHub Repo
2. GitHub Actions 自動下載 Android SDK、編譯 APK
3. 成功後 APK 作為 Artifact 上傳，並可通過 Telegram Bot 通知

## 支援平台

| Platform | 支援狀態 |
|----------|---------|
| Twitter/X | ✅ |
| Pixiv | ✅ |
| Instagram | ✅ |
| Reddit | ✅ |
| Danbooru | ✅ |
| Gelbooru | ✅ |
| Yande.re | ✅ |

## 檔案結構

```
auto-downloader/
├── app/
│   ├── __init__.py
│   ├── main.py              # Flet UI 主程式
│   ├── gallery_dl_wrapper.py # gallery-dl 包裝器
│   └── download_manager.py # 下載佇列管理
├── .github/workflows/
│   └── build.yml            # CI/CD 自動編譯腳本
├── requirements.txt          # Python 依賴
├── buildozer.spec           # Buildozer 打包配置
├── setup_project.sh         # 專案初始化腳本
└── README.md
```

## 環境變量 (GitHub Secrets)

| Secret |說明 |
|--------|------|
| TELEGRAM_BOT_TOKEN | Telegram Bot Token |
| TELEGRAM_CHAT_ID | Telegram Chat ID |

## License

MIT
