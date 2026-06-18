# 📦 Создание дистрибутива YouTube Downloader

## ⚡ Быстрая инструкция

PyInstaller **НЕ создаёт установщик** — он создаёт только `.exe` файл.

Для распространения приложения используйте один из вариантов ниже.

---

## Вариант 1: ZIP-архив (рекомендуется)

### 1. Соберите .exe

```bash
# Lite версия
pyinstaller --onefile --windowed --name "YouTube Downloader Lite" --icon=icon.ico --clean main_no_ffmpeg.py

# Полная версия (с FFmpeg)
pyinstaller --onefile --windowed --name "YouTube Downloader" --icon=icon.ico --add-data "bin/ffmpeg.exe;." --clean main.py
```

### 2. Создайте папку для распространения

```bash
mkdir YouTube_Downloader_v1.0
copy dist\YouTube_Downloader.exe YouTube_Downloader_v1.0\
copy README_BUILD.md YouTube_Downloader_v1.0\ИНСТРУКЦИЯ.txt
```

### 3. Запакуйте в ZIP

**Через проводник Windows:**
1. ПКМ на папке `YouTube_Downloader_v1.0`
2. **Отправить** → **Сжатая ZIP-папка**

**Через 7-Zip:**
```bash
7z a YouTube_Downloader_v1.0.zip YouTube_Downloader_v1.0\
```

### 📁 Структура архива

```
YouTube_Downloader_v1.0.zip
└── YouTube_Downloader_v1.0/
    ├── YouTube Downloader.exe    ← Запустить
    └── ИНСТРУКЦИЯ.txt            ← Инструкция
```

---

## Вариант 2: Установщик (Inno Setup)

### 1. Скачайте Inno Setup

https://jrsoftware.org/isdl.php

### 2. Создайте скрипт `installer.iss`

```iss
#define MyAppName "YouTube Downloader"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Ваше имя"
#define MyAppExeName "YouTube Downloader.exe"

[Setup]
AppId={{12345678-1234-1234-1234-123456789012}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
OutputDir=installer_output
OutputBaseFilename=YouTube_Downloader_Setup
SetupIconFile=compiler:SetupClassicIcon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "russian"; MessagesFile: "compiler:Languages\Russian.isl"

[Files]
Source: "dist\{#MyAppExeName}"; DestDir: "{app}"
Source: "README_BUILD.md"; DestDir: "{app}"; DestName: "README.txt"; Flags: isreadme

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent
```

### 3. Скомпилируйте установщик

```bash
iscc installer.iss
```

### 📤 Результат

```
installer_output/YouTube_Downloader_Setup.exe  ← Готовый установщик
```

---

## Что входит в дистрибутив

| Файл | Входит? | Зачем |
|------|---------|-------|
| `YouTube Downloader.exe` | ✅ | Основное приложение |
| `README.txt` / `ИНСТРУКЦИЯ.txt` | ✅ | Инструкция для пользователя |
| `requirements.txt` | ❌ | Не нужен (только для разработки) |
| `main.py` | ❌ | Встроен в .exe |
| `main_no_ffmpeg.py` | ❌ | Не нужен пользователю |
| `bin/ffmpeg.exe` | ✅ (внутри .exe) | Встроен через `--add-data` |
| `icon.ico` | ❌ | Встроен в .exe |

---

## 📋 Инструкция для пользователя (ШАБЛОН)

Создайте файл `ИНСТРУКЦИЯ.txt`:

```
═══════════════════════════════════════════════════════
  YouTube Downloader — Инструкция по использованию
═══════════════════════════════════════════════════════

✅ ЗАПУСК ПРОГРАММЫ
   Просто дважды кликните на "YouTube Downloader.exe"

✅ КАК СКАЧАТЬ ВИДЕО
   1. Скопируйте ссылку на видео YouTube
   2. Вставьте в поле (Ctrl+V или кнопка 📋)
   3. Выберите качество
   4. Нажмите "Скачать"

✅ ГДЕ ФАЙЛЫ
   Файлы сохраняются в:
   C:\Users\<ВашеИмя>\Downloads\YouTube Downloader\

✅ ФОРМАТЫ
   • 1080p/720p — MKV (со звуком)
   • 480p — MP4 (со звуком)
   • Аудио — MP3

⚠️ ВАЖНО
   • Только для личного использования
   • Уважайте авторские права
   • Не для коммерческого использования

═══════════════════════════════════════════════════════
  Версия 1.0.0 | 2026
═══════════════════════════════════════════════════════
```

---

## 🚀 Публикация

### GitHub Releases
1. Создайте репозиторий на GitHub
2. Создайте Release с тегом `v1.0.0`
3. Прикрепите `YouTube_Downloader_v1.0.zip`

### Google Drive / Яндекс.Диск
1. Загрузите ZIP-архив
2. Получите ссылку для скачивания
3. Поделитесь с пользователями

### Telegram канал
1. Загрузите файл как документ
2. Добавьте описание с инструкцией

---

## 🔧 Обновление версии

При выпуске новой версии:

1. Обновите версию в `main.py`:
   ```python
   APP_VERSION = "1.0.1"
   ```

2. Пересоберите:
   ```bash
   pyinstaller --onefile --windowed --name "YouTube Downloader" --icon=icon.ico --add-data "bin/ffmpeg.exe;." --clean main.py
   ```

3. Создайте новый ZIP с новым именем:
   ```
   YouTube_Downloader_v1.0.1.zip
   ```

4. Обновите `ИНСТРУКЦИЯ.txt` с новой версией

---

## ⚠️ Важно для распространения

1. **Не включайте** `requirements.txt` в дистрибутив — он не нужен пользователям
2. **Не включайте** исходный код (`main.py`) — он встроен в .exe
3. **Включите** краткую инструкцию — пользователи оценят
4. **Проверьте** .exe на вирусы перед публикацией (VirusTotal)
5. **Протестируйте** на чистой системе (без Python)

---

## 📊 Размеры файлов

| Файл | Размер |
|------|--------|
| `YouTube Downloader Lite.exe` | ~35-40 МБ |
| `YouTube Downloader.exe` (с FFmpeg) | ~60-80 МБ |
| ZIP-архив (Lite) | ~35-40 МБ |
| ZIP-архив (Full) | ~60-80 МБ |
| Установщик (Full) | ~60-80 МБ |

---

## 🎯 Итог

**Для быстрого распространения:**
```bash
# 1. Сборка
pyinstaller --onefile --windowed --name "YouTube Downloader" --icon=icon.ico --add-data "bin/ffmpeg.exe;." --clean main.py

# 2. Копирование
mkdir Release
copy dist\YouTube_Downloader.exe Release\
copy ИНСТРУКЦИЯ.txt Release\

# 3. Упаковка
7z a YouTube_Downloader_v1.0.zip Release\
```

**Готово!** `YouTube_Downloader_v1.0.zip` можно распространять.
