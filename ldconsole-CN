# ldconsole 命令行工具說明文檔

`ldconsole` 是 **雷電模擬器 (LDPlayer)** 的命令行控制工具，用於批量管理 Android 模擬器實例。

---

## 基本語法

```
ldconsole <命令> [參數]
```

**通用參數說明：**

- `--name mnq_name`：透過模擬器名稱指定
- `--index mnq_idx`：透過模擬器索引（從 0 開始）指定

---

## 命令分類

### 1. 模擬器生命週期管理

| 命令 | 說明 | 範例 |
|------|------|------|
| `launch` | 啟動模擬器 | `ldconsole launch --name MyPhone` |
| `launchex` | 啟動模擬器並運行應用 | `ldconsole launchex --index 0 --packagename com.example` |
| `quit` | 關閉模擬器 | `ldconsole quit --index 0` |
| `quitall` | 關閉所有模擬器 | `ldconsole quitall` |
| `reboot` | 重啟模擬器 | `ldconsole reboot --name MyPhone` |

---

### 2. 模擬器查詢

| 命令 | 說明 | 範例 |
|------|------|------|
| `list` | 列出所有模擬器 | `ldconsole list` |
| `list2` | 列出所有模擬器（詳細資訊） | `ldconsole list2` |
| `runninglist` | 列出正在運行的模擬器 | `ldconsole runninglist` |
| `isrunning` | 檢查指定模擬器是否運行中 | `ldconsole isrunning --index 0` |

---

### 3. 模擬器管理

| 命令 | 說明 | 範例 |
|------|------|------|
| `add` | 新增模擬器 | `ldconsole add --name NewPhone` |
| `copy` | 複製模擬器 | `ldconsole copy --name Clone1 --from 0` |
| `remove` | 刪除模擬器 | `ldconsole remove --name OldPhone` |
| `rename` | 重命名模擬器 | `ldconsole rename --index 0 --title NewName` |

---

### 4. 模擬器配置 (modify)

```bash
ldconsole modify <--name mnq_name | --index mnq_idx> [選項]
```

#### 硬體配置

| 選項 | 說明 | 可用值 |
|------|------|--------|
| `--resolution` | 解析度 | `寬,高,DPI`（如 `1280,720,240`） |
| `--cpu` | CPU 核心數 | `1`、`2`、`3`、`4` |
| `--memory` | 記憶體 (MB) | `256`、`512`、`768`、`1024`、`1536`、`2048`、`4096`、`8192` |

#### 設備資訊

| 選項 | 說明 | 可用值 |
|------|------|--------|
| `--manufacturer` | 製造商 | 如 `asus` |
| `--model` | 設備型號 | 如 `ASUS_Z00DUO` |
| `--pnumber` | 電話號碼 | 如 `13800000000` |

#### 設備識別碼

| 選項 | 說明 | 可用值 |
|------|------|--------|
| `--imei` | IMEI | `auto` 或具體值（如 `865166023949731`） |
| `--imsi` | IMSI | `auto` 或具體值（如 `460000000000000`） |
| `--simserial` | SIM 卡序號 | `auto` 或具體值（如 `89860000000000000000`） |
| `--androidid` | Android ID | `auto` 或 16 位十六進制（如 `0123456789abcdef`） |
| `--mac` | MAC 地址 | `auto` 或 12 位十六進制（如 `000000000000`） |

#### 顯示設定

| 選項 | 說明 | 可用值 |
|------|------|--------|
| `--autorotate` | 自動旋轉 | `1` 啟用 / `0` 禁用 |
| `--lockwindow` | 鎖定窗口 | `1` 啟用 / `0` 禁用 |

---

### 5. 應用管理

| 命令 | 說明 | 參數 |
|------|------|------|
| `installapp` | 安裝應用 | `--filename <apk路徑>` 或 `--packagename <包名>` |
| `uninstallapp` | 卸載應用 | `--packagename <包名>` |
| `runapp` | 啟動應用 | `--packagename <包名>` |
| `killapp` | 終止應用 | `--packagename <包名>` |

**範例：**

```bash
# 從本地 APK 安裝
ldconsole installapp --index 0 --filename "C:\Downloads\app.apk"

# 從應用商店安裝（透過包名）
ldconsole installapp --index 0 --packagename com.example.app

# 啟動應用
ldconsole runapp --index 0 --packagename com.example.app

# 卸載應用
ldconsole uninstallapp --index 0 --packagename com.example.app
```

---

### 6. 文件操作

| 命令 | 說明 | 參數 |
|------|------|------|
| `pull` | 從模擬器拉取文件到本地 | `--remote <模擬器路徑> --local <本地路徑>` |
| `push` | 推送本地文件到模擬器 | `--remote <模擬器路徑> --local <本地路徑>` |
| `backup` | 備份整個模擬器 | `--file <備份檔路徑>` |
| `restore` | 從備份恢復模擬器 | `--file <備份檔路徑>` |
| `backupapp` | 備份指定應用數據 | `--packagename <包名> --file <路徑>` |
| `restoreapp` | 恢復指定應用數據 | `--packagename <包名> --file <路徑>` |
| `scan` | 掃描文件到模擬器媒體庫 | `--file <路徑>` |

**範例：**

```bash
# 備份模擬器
ldconsole backup --index 0 --file "D:\backup\phone0.ldbk"

# 恢復模擬器
ldconsole restore --index 0 --file "D:\backup\phone0.ldbk"

# 從模擬器拉取截圖
ldconsole pull --index 0 --remote /sdcard/DCIM/screenshot.png --local "C:\screenshots\"

# 推送文件到模擬器
ldconsole push --index 0 --local "C:\files\data.txt" --remote /sdcard/Download/
```

---

### 7. 系統操作

| 命令 | 說明 | 參數 |
|------|------|------|
| `locate` | 設置虛擬 GPS 定位 | `--LLI <經度,緯度>` |
| `adb` | 執行 ADB 命令 | `--command <命令字串>` |
| `setprop` | 設置系統屬性 | `--key <屬性名> --value <值>` |
| `getprop` | 獲取系統屬性 | `--key <屬性名>`（可選） |
| `downcpu` | 限制 CPU 使用率 | `--rate <0~100>` |
| `action` | 執行模擬操作 | `--key <名稱> --value <值>` |

**範例：**

```bash
# 設置定位到東京
ldconsole locate --index 0 --LLI 139.6917,35.6895

# 執行 ADB shell 命令
ldconsole adb --index 0 --command "shell input tap 500 500"

# 模擬按鍵
ldconsole adb --index 0 --command "shell input keyevent 4"

# 獲取系統屬性
ldconsole getprop --index 0 --key ro.product.model

# 限制 CPU 使用率為 50%
ldconsole downcpu --index 0 --rate 50
```

---

### 8. 窗口管理

| 命令 | 說明 |
|------|------|
| `sortWnd` | 自動排列所有模擬器窗口 |
| `zoomIn` | 放大窗口 |
| `zoomOut` | 縮小窗口 |

---

### 9. 全局設置

```bash
ldconsole globalsetting [選項]
```

| 選項 | 說明 | 可用值 |
|------|------|--------|
| `--fps` | 幀率限制 | `0` ~ `60` |
| `--audio` | 音頻開關 | `1` 開啟 / `0` 關閉 |
| `--fastplay` | 快速播放 | `1` 開啟 / `0` 關閉 |
| `--cleanmode` | 清潔模式 | `1` 開啟 / `0` 關閉 |

---

## 常用操作範例

### 批量啟動模擬器

```bash
ldconsole launch --index 0
ldconsole launch --index 1
ldconsole launch --index 2
```

### 批量安裝應用

```bash
for /L %i in (0,1,5) do ldconsole installapp --index %i --filename "C:\app.apk"
```

### 自動化腳本範例

```bash
# 啟動模擬器 → 等待啟動 → 運行應用
ldconsole launch --index 0
timeout /t 30
ldconsole runapp --index 0 --packagename com.example.app
```

### 設置多開模擬器的不同定位

```bash
ldconsole locate --index 0 --LLI 121.4737,31.2304   # 上海
ldconsole locate --index 1 --LLI 116.4074,39.9042   # 北京
ldconsole locate --index 2 --LLI 114.1694,22.3193   # 香港
```

---

## 注意事項

1. **路徑包含空格時需用引號包裹**
2. **模擬器索引從 0 開始**
3. **部分命令需要模擬器處於運行狀態**
4. **ADB 命令需要模擬器完全啟動後才能執行**

---

## 參考資料

- 雷電模擬器官方文檔
- 命令行工具位置：`雷電安裝目錄\ldconsole.exe` 或 `ldconsole.exe`
