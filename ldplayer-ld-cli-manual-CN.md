# ld.exe 命令行工具說明文檔

`ld.exe` 是 **雷電模擬器 (LDPlayer)** 內建的 ADB Shell 快捷執行工具，用於直接對指定模擬器執行 Android Shell 命令，無需手動連接 ADB 或指定設備序列號。

---

## 概述

### 工具定位

| 工具 | 用途 | 複雜度 |
|------|------|--------|
| `dnconsole.exe` | 模擬器管理（啟動、關閉、配置等） | 高階管理 |
| `ld.exe` | 直接執行 Android Shell 命令 | 快速操作 |
| `adb.exe` | 標準 Android 調試橋 | 通用但繁瑣 |

### 優勢

- **簡化操作**：無需 `adb connect`、無需記憶設備序列號
- **索引定位**：直接使用模擬器索引號指定目標
- **自動 Shell**：命令直接在 Android Shell 環境執行，無需加 `shell` 前綴

---

## 基本語法

```
ld.exe -s <模擬器索引> <Android Shell 命令>
```

### 參數說明

| 參數 | 說明 |
|------|------|
| `-s <index>` | 指定模擬器索引（從 0 開始，與 `dnconsole --index` 相同） |
| `<命令>` | 要執行的 Android Shell 命令 |

### 與標準 ADB 對照

| ld.exe 命令 | 等效 ADB 命令 |
|-------------|---------------|
| `ld.exe -s 0 ls /sdcard` | `adb -s emulator-5554 shell ls /sdcard` |
| `ld.exe -s 1 pm list packages` | `adb -s emulator-5556 shell pm list packages` |
| `ld.exe -s 22 input tap 500 500` | `adb -s emulator-5598 shell input tap 500 500` |

### 索引與 ADB 端口對應關係

| 模擬器索引 | ADB 設備號 | ADB 端口 |
|------------|------------|----------|
| 0 | emulator-5554 | 127.0.0.1:5555 |
| 1 | emulator-5556 | 127.0.0.1:5557 |
| 2 | emulator-5558 | 127.0.0.1:5559 |
| n | emulator-(5554+2n) | 127.0.0.1:(5555+2n) |

---

## 常用命令分類

### 1. Activity Manager (am) - 活動管理

Activity Manager 用於啟動應用、服務、發送廣播等。

#### 1.1 啟動應用 / Activity

```bash
# 基本啟動（通過包名和 Activity）
ld.exe -s 0 am start -n <包名>/<Activity名>

# 範例：啟動設定
ld.exe -s 0 am start -n com.android.settings/.Settings

# 範例：啟動 Facebook
ld.exe -s 0 am start -n com.facebook.katana/.LoginActivity
```

#### 1.2 通過 Intent 啟動

```bash
# 通過 ACTION 啟動
ld.exe -s 0 am start -a <action>

# 通過 ACTION + DATA 啟動
ld.exe -s 0 am start -a android.intent.action.VIEW -d <URI>

# 範例：開啟網頁
ld.exe -s 0 am start -a android.intent.action.VIEW -d "https://www.google.com"

# 範例：開啟 Facebook 通知頁面
ld.exe -s 0 am start -a android.intent.action.VIEW -d "fb://notifications"

# 範例：撥打電話
ld.exe -s 0 am start -a android.intent.action.CALL -d "tel:123456789"

# 範例：發送簡訊
ld.exe -s 0 am start -a android.intent.action.SENDTO -d "sms:123456789" --es sms_body "Hello"

# 範例：開啟地圖定位
ld.exe -s 0 am start -a android.intent.action.VIEW -d "geo:25.0330,121.5654"

# 範例：開啟相機
ld.exe -s 0 am start -a android.media.action.IMAGE_CAPTURE

# 範例：開啟相簿
ld.exe -s 0 am start -t image/* -a android.intent.action.VIEW
```

#### 1.3 am start 完整參數

| 參數 | 說明 | 範例 |
|------|------|------|
| `-a <action>` | Intent Action | `-a android.intent.action.VIEW` |
| `-d <URI>` | Intent Data URI | `-d "https://example.com"` |
| `-t <MIME>` | MIME 類型 | `-t image/*` |
| `-c <category>` | Intent Category | `-c android.intent.category.LAUNCHER` |
| `-n <component>` | 指定組件 | `-n com.app/.MainActivity` |
| `-e <key> <value>` | 額外字串參數 | `-e name "John"` |
| `--es <key> <value>` | 額外字串參數 | `--es sms_body "Hello"` |
| `--ei <key> <value>` | 額外整數參數 | `--ei count 10` |
| `--ez <key> <value>` | 額外布林參數 | `--ez enabled true` |
| `-f <flags>` | Intent Flags | `-f 0x10000000` |
| `-W` | 等待啟動完成 | |
| `-S` | 啟動前先強制停止 | |

#### 1.4 啟動服務

```bash
# 啟動服務
ld.exe -s 0 am startservice -n <包名>/<服務名>

# 停止服務
ld.exe -s 0 am stopservice -n <包名>/<服務名>
```

#### 1.5 發送廣播

```bash
# 發送自定義廣播
ld.exe -s 0 am broadcast -a <action>

# 範例：發送開機完成廣播
ld.exe -s 0 am broadcast -a android.intent.action.BOOT_COMPLETED

# 範例：發送時間改變廣播
ld.exe -s 0 am broadcast -a android.intent.action.TIME_SET

# 範例：發送自定義廣播帶參數
ld.exe -s 0 am broadcast -a com.example.MY_ACTION --es message "Hello"
```

#### 1.6 強制停止應用

```bash
# 強制停止應用
ld.exe -s 0 am force-stop <包名>

# 範例
ld.exe -s 0 am force-stop com.facebook.katana
```

#### 1.7 殺死應用進程

```bash
# 殺死後台進程
ld.exe -s 0 am kill <包名>

# 殺死所有後台進程
ld.exe -s 0 am kill-all
```

---

### 2. Package Manager (pm) - 包管理

Package Manager 用於管理應用包。

#### 2.1 列出應用

```bash
# 列出所有已安裝應用
ld.exe -s 0 pm list packages

# 列出第三方應用
ld.exe -s 0 pm list packages -3

# 列出系統應用
ld.exe -s 0 pm list packages -s

# 列出已禁用的應用
ld.exe -s 0 pm list packages -d

# 列出已啟用的應用
ld.exe -s 0 pm list packages -e

# 搜索特定應用
ld.exe -s 0 pm list packages | grep facebook

# 顯示應用路徑
ld.exe -s 0 pm list packages -f

# 顯示安裝來源
ld.exe -s 0 pm list packages -i
```

#### 2.2 獲取應用信息

```bash
# 獲取應用 APK 路徑
ld.exe -s 0 pm path <包名>

# 範例
ld.exe -s 0 pm path com.facebook.katana

# 獲取應用詳細信息
ld.exe -s 0 pm dump <包名>

# 獲取應用版本信息
ld.exe -s 0 dumpsys package <包名> | grep versionName
```

#### 2.3 應用安裝與卸載

```bash
# 安裝應用（需先 push APK 到設備）
ld.exe -s 0 pm install /sdcard/app.apk

# 安裝並替換現有應用
ld.exe -s 0 pm install -r /sdcard/app.apk

# 安裝到 SD 卡
ld.exe -s 0 pm install -s /sdcard/app.apk

# 卸載應用
ld.exe -s 0 pm uninstall <包名>

# 卸載但保留數據
ld.exe -s 0 pm uninstall -k <包名>
```

#### 2.4 應用數據管理

```bash
# 清除應用數據
ld.exe -s 0 pm clear <包名>

# 範例：清除 Facebook 數據
ld.exe -s 0 pm clear com.facebook.katana
```

#### 2.5 應用啟用與禁用

```bash
# 禁用應用
ld.exe -s 0 pm disable-user <包名>

# 啟用應用
ld.exe -s 0 pm enable <包名>

# 隱藏應用
ld.exe -s 0 pm hide <包名>

# 取消隱藏
ld.exe -s 0 pm unhide <包名>
```

#### 2.6 權限管理

```bash
# 列出應用權限
ld.exe -s 0 pm list permissions

# 授予權限
ld.exe -s 0 pm grant <包名> <權限>

# 範例：授予存儲權限
ld.exe -s 0 pm grant com.example.app android.permission.WRITE_EXTERNAL_STORAGE

# 撤銷權限
ld.exe -s 0 pm revoke <包名> <權限>

# 重置所有權限
ld.exe -s 0 pm reset-permissions -p <包名>
```

---

### 3. Input - 輸入模擬

模擬各種輸入操作。

#### 3.1 點擊操作

```bash
# 單擊指定座標
ld.exe -s 0 input tap <X> <Y>

# 範例：點擊螢幕中央（假設 1080x1920）
ld.exe -s 0 input tap 540 960
```

#### 3.2 滑動操作

```bash
# 滑動
ld.exe -s 0 input swipe <起始X> <起始Y> <結束X> <結束Y> [持續時間ms]

# 範例：向上滑動
ld.exe -s 0 input swipe 540 1500 540 500 300

# 範例：向左滑動
ld.exe -s 0 input swipe 900 960 100 960 300

# 範例：長按（原地滑動）
ld.exe -s 0 input swipe 540 960 540 960 2000
```

#### 3.3 文字輸入

```bash
# 輸入文字（不支援中文和空格）
ld.exe -s 0 input text "hello"

# 空格用 %s 替代
ld.exe -s 0 input text "hello%sworld"
```

#### 3.4 按鍵模擬

```bash
# 發送按鍵事件
ld.exe -s 0 input keyevent <keycode>

# 常用按鍵
ld.exe -s 0 input keyevent 3      # Home 鍵
ld.exe -s 0 input keyevent 4      # 返回鍵
ld.exe -s 0 input keyevent 24     # 音量加
ld.exe -s 0 input keyevent 25     # 音量減
ld.exe -s 0 input keyevent 26     # 電源鍵
ld.exe -s 0 input keyevent 82     # 菜單鍵
ld.exe -s 0 input keyevent 187    # 最近任務
ld.exe -s 0 input keyevent 224    # 亮屏
ld.exe -s 0 input keyevent 223    # 熄屏
ld.exe -s 0 input keyevent 66     # Enter
ld.exe -s 0 input keyevent 67     # 刪除（Backspace）
ld.exe -s 0 input keyevent 61     # Tab
```

#### 3.5 常用 KeyCode 對照表

| KeyCode | 說明 | KeyCode | 說明 |
|---------|------|---------|------|
| 0 | UNKNOWN | 66 | ENTER |
| 1 | MENU (軟鍵盤) | 67 | DEL (刪除) |
| 3 | HOME | 82 | MENU |
| 4 | BACK | 84 | SEARCH |
| 5 | CALL | 85 | MEDIA_PLAY_PAUSE |
| 6 | ENDCALL | 86 | MEDIA_STOP |
| 24 | VOLUME_UP | 87 | MEDIA_NEXT |
| 25 | VOLUME_DOWN | 88 | MEDIA_PREVIOUS |
| 26 | POWER | 122 | MOVE_HOME |
| 27 | CAMERA | 123 | MOVE_END |
| 61 | TAB | 187 | APP_SWITCH (最近任務) |
| 62 | SPACE | 220 | BRIGHTNESS_DOWN |
| 64 | EXPLORER | 221 | BRIGHTNESS_UP |
| 65 | ENVELOPE | 223 | SLEEP |
|  |  | 224 | WAKEUP |

---

### 4. 檔案操作

#### 4.1 目錄與檔案操作

```bash
# 列出目錄
ld.exe -s 0 ls /sdcard

# 詳細列出
ld.exe -s 0 ls -la /sdcard

# 切換目錄
ld.exe -s 0 cd /sdcard/Download

# 查看當前目錄
ld.exe -s 0 pwd

# 創建目錄
ld.exe -s 0 mkdir /sdcard/NewFolder

# 創建檔案
ld.exe -s 0 touch /sdcard/test.txt

# 刪除檔案
ld.exe -s 0 rm /sdcard/test.txt

# 刪除目錄
ld.exe -s 0 rm -r /sdcard/NewFolder

# 複製檔案
ld.exe -s 0 cp /sdcard/a.txt /sdcard/b.txt

# 移動/重命名檔案
ld.exe -s 0 mv /sdcard/a.txt /sdcard/Download/a.txt

# 查看檔案內容
ld.exe -s 0 cat /sdcard/test.txt

# 修改檔案權限
ld.exe -s 0 chmod 777 /sdcard/test.txt
```

#### 4.2 檔案搜索

```bash
# 搜索檔案
ld.exe -s 0 find /sdcard -name "*.jpg"

# 搜索包含特定文字的檔案
ld.exe -s 0 grep -r "keyword" /sdcard/
```

---

### 5. 系統信息

#### 5.1 設備信息

```bash
# 獲取設備型號
ld.exe -s 0 getprop ro.product.model

# 獲取 Android 版本
ld.exe -s 0 getprop ro.build.version.release

# 獲取 SDK 版本
ld.exe -s 0 getprop ro.build.version.sdk

# 獲取設備序列號
ld.exe -s 0 getprop ro.serialno

# 獲取 IMEI
ld.exe -s 0 dumpsys iphonesubinfo

# 列出所有屬性
ld.exe -s 0 getprop
```

#### 5.2 系統狀態

```bash
# 電池狀態
ld.exe -s 0 dumpsys battery

# 記憶體信息
ld.exe -s 0 cat /proc/meminfo

# CPU 信息
ld.exe -s 0 cat /proc/cpuinfo

# 磁盤空間
ld.exe -s 0 df

# 運行中的進程
ld.exe -s 0 ps

# 查找特定進程
ld.exe -s 0 ps | grep facebook

# 獲取進程 PID
ld.exe -s 0 pidof com.facebook.katana
```

#### 5.3 螢幕信息

```bash
# 獲取螢幕解析度
ld.exe -s 0 wm size

# 獲取螢幕密度
ld.exe -s 0 wm density

# 修改解析度
ld.exe -s 0 wm size 1080x1920

# 修改密度
ld.exe -s 0 wm density 320

# 重置為預設
ld.exe -s 0 wm size reset
ld.exe -s 0 wm density reset
```

---

### 6. 網路操作

```bash
# 查看網路狀態
ld.exe -s 0 netstat

# Ping 測試
ld.exe -s 0 ping -c 4 www.google.com

# 獲取 IP 地址
ld.exe -s 0 ip addr

# 獲取 WiFi 信息
ld.exe -s 0 dumpsys wifi

# 啟用/禁用 WiFi
ld.exe -s 0 svc wifi enable
ld.exe -s 0 svc wifi disable

# 啟用/禁用移動數據
ld.exe -s 0 svc data enable
ld.exe -s 0 svc data disable
```

---

### 7. 截圖與錄屏

```bash
# 截圖
ld.exe -s 0 screencap -p /sdcard/screenshot.png

# 錄屏（最長 180 秒）
ld.exe -s 0 screenrecord /sdcard/video.mp4

# 錄屏（指定時長）
ld.exe -s 0 screenrecord --time-limit 30 /sdcard/video.mp4

# 錄屏（指定解析度）
ld.exe -s 0 screenrecord --size 720x1280 /sdcard/video.mp4

# 錄屏（指定碼率）
ld.exe -s 0 screenrecord --bit-rate 6000000 /sdcard/video.mp4
```

---

### 8. 日誌操作

```bash
# 查看系統日誌
ld.exe -s 0 logcat

# 過濾特定標籤
ld.exe -s 0 logcat -s TAG_NAME

# 過濾特定級別（V/D/I/W/E）
ld.exe -s 0 logcat *:E

# 清除日誌
ld.exe -s 0 logcat -c

# 輸出到檔案
ld.exe -s 0 logcat -d > log.txt
```

---

### 9. 設置操作

```bash
# 獲取設置值
ld.exe -s 0 settings get system <key>
ld.exe -s 0 settings get secure <key>
ld.exe -s 0 settings get global <key>

# 設置值
ld.exe -s 0 settings put system <key> <value>
ld.exe -s 0 settings put secure <key> <value>
ld.exe -s 0 settings put global <key> <value>

# 範例：調整螢幕亮度
ld.exe -s 0 settings put system screen_brightness 200

# 範例：開啟自動亮度
ld.exe -s 0 settings put system screen_brightness_mode 1

# 範例：設置螢幕超時時間（毫秒）
ld.exe -s 0 settings put system screen_off_timeout 300000
```

---

### 10. 進階操作

#### 10.1 模擬重啟

```bash
# 重啟設備
ld.exe -s 0 reboot

# 重啟到 Recovery
ld.exe -s 0 reboot recovery

# 重啟到 Bootloader
ld.exe -s 0 reboot bootloader
```

#### 10.2 設置日期時間

```bash
# 設置日期（格式：MMDDhhmm[[CC]YY][.ss]）
ld.exe -s 0 date 01011200

# 設置完整日期時間
ld.exe -s 0 date 010112002024.00
```

#### 10.3 Monkey 測試

```bash
# 對應用執行隨機操作
ld.exe -s 0 monkey -p <包名> -v <事件數>

# 範例：對 Facebook 執行 100 次隨機操作
ld.exe -s 0 monkey -p com.facebook.katana -v 100
```

---

## 實用範例集

### 自動化腳本範例

```batch
@echo off
REM 批量對多個模擬器執行操作

REM 啟動 Facebook 通知頁面（模擬器 0-5）
for /L %%i in (0,1,5) do (
    ld.exe -s %%i am start -a android.intent.action.VIEW -d "fb://notifications"
    timeout /t 1 >nul
)
```

### 常見操作組合

```bash
# 清除應用數據並重新啟動
ld.exe -s 0 pm clear com.example.app
ld.exe -s 0 am start -n com.example.app/.MainActivity

# 截圖並命名
ld.exe -s 0 screencap -p /sdcard/screenshot_%date%.png

# 模擬登入流程
ld.exe -s 0 input tap 540 800      # 點擊用戶名欄位
ld.exe -s 0 input text "username"  # 輸入用戶名
ld.exe -s 0 input tap 540 900      # 點擊密碼欄位
ld.exe -s 0 input text "password"  # 輸入密碼
ld.exe -s 0 input tap 540 1000     # 點擊登入按鈕
```

---

## 常見 Intent URI 協議

### 社交應用

| 應用 | URI | 說明 |
|------|-----|------|
| Facebook | `fb://notifications` | 通知頁面 |
| Facebook | `fb://profile/<user_id>` | 用戶個人頁面 |
| Facebook | `fb://page/<page_id>` | 粉絲專頁 |
| Facebook | `fb://messaging` | 訊息頁面 |
| Instagram | `instagram://user?username=<name>` | 用戶頁面 |
| Twitter | `twitter://user?screen_name=<name>` | 用戶頁面 |
| LINE | `line://msg/text/<message>` | 發送訊息 |
| WhatsApp | `whatsapp://send?phone=<number>` | 發送訊息 |

### 系統功能

| URI | 說明 |
|-----|------|
| `tel:<number>` | 撥打電話 |
| `sms:<number>` | 發送簡訊 |
| `mailto:<email>` | 發送郵件 |
| `geo:<lat>,<lng>` | 地圖定位 |
| `market://details?id=<package>` | Play 商店頁面 |
| `file://<path>` | 開啟檔案 |
| `content://<uri>` | 內容提供者 |

---

## 注意事項

1. **模擬器必須運行中**：`ld.exe` 只能對已啟動的模擬器執行命令
2. **路徑區分大小寫**：Android 檔案系統區分大小寫
3. **特殊字符需轉義**：在 Windows CMD 中，某些字符需要用引號包裹
4. **Root 權限**：部分命令需要模擬器開啟 Root 權限
5. **中文輸入限制**：`input text` 不支援直接輸入中文

---

## 疑難排解

### 常見錯誤

| 錯誤訊息 | 原因 | 解決方案 |
|----------|------|----------|
| `/system/bin/sh: xxx: not found` | 命令不存在 | 檢查命令拼寫或確認命令是否可用 |
| `Error: Activity not started` | Activity 不存在 | 檢查包名和 Activity 名稱 |
| `Failure [INSTALL_FAILED_xxx]` | 安裝失敗 | 根據具體錯誤碼排查 |
| `Permission denied` | 權限不足 | 開啟 Root 權限或使用 `su` |

### 獲取正確的包名和 Activity

```bash
# 列出所有包名
ld.exe -s 0 pm list packages

# 獲取應用的啟動 Activity
ld.exe -s 0 dumpsys package <包名> | grep -A 1 "android.intent.action.MAIN"

# 獲取當前前台 Activity
ld.exe -s 0 dumpsys window windows | grep mCurrentFocus
```

---

## 工具位置

`ld.exe` 位於雷電模擬器安裝目錄下，通常路徑為：

```
C:\LDPlayer\LDPlayer9\ld.exe
```

或

```
C:\leidian\LDPlayer9\ld.exe
```

建議將此目錄加入系統 PATH 環境變數，以便在任意位置使用。

---

## 相關工具

| 工具 | 說明 |
|------|------|
| `dnconsole.exe` | 模擬器管理工具（啟動、關閉、配置等） |
| `ldconsole.exe` | 與 `dnconsole.exe` 相同 |
| `adb.exe` | 標準 Android Debug Bridge |
| `dnmultiplayer.exe` | 雷電多開器 |

---

## 參考資料

- Android ADB Shell 官方文檔
- 雷電模擬器官方文檔
- Android Intent 參考
