# 📘 Инструкция по сборке YouTube Downloader

> **Две версии приложения:** полная (с FFmpeg) и лёгкая (без FFmpeg)

---

## 📋 Содержание

1. [Установка зависимостей](#1-установка-зависимостей)
2. [Создание иконки](#2-создание-иконки)
3. [Сборка версии без FFmpeg](#3-сборка-версии-без-ffmpeg)
4. [Сборка полной версии](#4-сборка-полной-версии)
5. [Сравнение версий](#5-сравнение-версий)
6. [Решение проблем](#6-решение-проблем)

---

## 1. Установка зависимостей

### ▶️ Шаг 1.1: Проверка Python

```bash
python --version
```

Требуется **Python 3.9 или выше**. Если не установлен — скачайте с [python.org](https://www.python.org/downloads/)

### ▶️ Шаг 1.2: Установка библиотек

```bash
pip install -r requirements.txt
```

Или вручную:

```bash
pip install customtkinter yt-dlp Pillow packaging pyinstaller
```

---

## 2. Создание иконки

### 🖼️ Вариант 1: Онлайн-конвертер (рекомендуется)

1. Подготовьте изображение **256×256 px** (PNG с прозрачным фоном)
2. Конвертируйте на одном из сервисов:

| Сервис | Ссылка |
|--------|--------|
| Convertio | https://convertio.co/ru/png-ico/ |
| ICO Converter | https://www.icoconverter.com/ |
| CloudConvert | https://cloudconvert.com/png-to-ico |

3. Сохраните как `icon.ico` в папку с проектом

### 🐍 Вариант 2: Через Python

```python
from PIL import Image

img = Image.open('logo.png')
img.save('icon.ico', format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])
```

### 📁 Вариант 3: Готовая иконка

Положите файл `icon.ico` в папку с проектом.

---

## 3. Сборка версии без FFmpeg

### 🎯 Для кого

Для пользователей, которые хотят **быстро начать** без установки дополнительного ПО.

### ⚙️ Команда сборки

```bash
pyinstaller --onefile --windowed --name "YouTube Downloader Lite" --icon=icon.ico --clean main_no_ffmpeg.py
```

### 📦 Параметры

| Параметр | Описание |
|----------|----------|
| `--onefile` | Один EXE-файл |
| `--windowed` | Без консольного окна |
| `--name` | Имя приложения |
| `--icon` | Путь к иконке |
| `--clean` | Очистка временных файлов |

### 📤 Результат

```
dist/YouTube Downloader Lite.exe  ← готовый файл
```

---

## 4. Сборка полной версии

### 🎯 Для кого

Для пользователей, которым нужно **максимальное качество** (1080p+ со звуком).

### ⚙️ Предварительные требования

Установите **FFmpeg** одним из способов:

```bash
# Через winget (Windows)
winget install ffmpeg

# Через Chocolatey
choco install ffmpeg

# Через Scoop
scoop install ffmpeg
```

### ⚙️ Команда сборки

```bash
pyinstaller --onefile --windowed --name "YouTube Downloader" --icon=icon.ico --clean main.py
```

### 📤 Результат

```
dist/YouTube Downloader.exe  ← готовый файл
```

---

## 5. Сравнение версий

### 📊 Таблица сравнения

| Характеристика | Lite (без FFmpeg) | Full (с FFmpeg) |
|----------------|-------------------|-----------------|
| **Файл** | `main_no_ffmpeg.py` | `main.py` |
| **EXE имя** | YouTube Downloader Lite | YouTube Downloader |
| **Размер EXE** | ~35 МБ | ~50 МБ |
| **1080p + звук** | ❌ | ✅ |
| **720p + звук** | ❌ | ✅ |
| **480p + звук** | ✅ | ✅ |
| **Аудио** | M4A | MP3 |
| **Установка** | Не требуется | Требуется FFmpeg |
| **Скорость** | Быстрее | Медленнее (конвертация) |

### 🎬 Форматы видео

| Версия | 1080p | 720p | 480p | Аудио |
|--------|-------|------|------|-------|
| **Lite** | Без звука | Без звука | Со звуком | M4A |
| **Full** | Со звуком | Со звуком | Со звуком | MP3 |

### 🎨 Визуальные отличия

| Элемент | Lite | Full |
|---------|------|------|
| Заголовок | YouTube Downloader (No FFmpeg) | YouTube Downloader |
| Предупреждение | ⚠️ О возможных ограничениях | Отсутствует |
| Выбор качества | 4 варианта | 4 варианта |

---

## 6. Решение проблем

### ❌ ModuleNotFoundError: No module named 'yt_dlp'

```bash
pip install yt-dlp
```

Или добавьте скрытый импорт:

```bash
pyinstaller --onefile --windowed --hidden-import=yt_dlp --icon=icon.ico main.py
```

---

### ❌ Большой размер EXE (>100 МБ)

Это нормально для yt-dlp. Для уменьшения:

```bash
# С использованием UPX-сжатия
pyinstaller --onefile --windowed --upx-dir=upx --icon=icon.ico main.py
```

---

### ❌ Антивирус блокирует EXE

1. Добавьте папку в исключения
2. Подпишите файл цифровой подписью (для распространения)
3. Отправьте на ложное срабатывание в поддержку антивируса

---

### ❌ Ошибка "FFmpeg not found" (Full версия)

Установите FFmpeg:

```bash
winget install ffmpeg
```

Или скачайте вручную с [gyan.dev/ffmpeg](https://www.gyan.dev/ffmpeg/)

---

### ❌ Видео без звука (Lite версия)

Это ограничение YouTube — высокие качества разделяются на потоки.

**Решение:** Используйте версию Full с FFmpeg или выберите 480p.

---

### ❌ Чёрный экран при запуске

Удалите папку `%APPDATA%\customtkinter` и запустите снова.

---

## 📁 Структура проекта

```
youtube downloader/
├── main.py                    # Полная версия (с FFmpeg)
├── main_no_ffmpeg.py          # Лёгкая версия (без FFmpeg)
├── requirements.txt           # Зависимости
├── icon.ico                   # Иконка приложения
├── README_BUILD.md            # Эта инструкция
├── Downloads/                 # Папка загрузок (создаётся)
├── dist/
│   ├── YouTube Downloader.exe         # Полная версия
│   └── YouTube Downloader Lite.exe    # Лёгкая версия
└── build/                     # Временные файлы (можно удалить)
```

---

## 🚀 Быстрый старт

### Для Lite версии:

```bash
pip install -r requirements.txt
pyinstaller --onefile --windowed --name "YouTube Downloader Lite" --icon=icon.ico main_no_ffmpeg.py
start dist
```

### Для Full версии:

```bash
winget install ffmpeg
pip install -r requirements.txt
pyinstaller --onefile --windowed --name "YouTube Downloader" --icon=icon.ico main.py
start dist
```

---

## 📊 Какой файл запускать?

| Ситуация | Выбор |
|----------|-------|
| Нужно быстро и просто | **Lite** |
| Нужно 1080p со звуком | **Full** + FFmpeg |
| Только аудио | **Lite** (M4A) или **Full** (MP3) |
| Для друзей без FFmpeg | **Lite** |

---

## 🎨 Советы по дизайну иконки

### 📐 Технические требования

| Параметр | Значение |
|----------|----------|
| Размер исходника | 256×256 px |
| Формат | PNG с прозрачностью |
| Глубина цвета | 32 бит (RGBA) |

### 🎨 Рекомендации

- **Контрастность** — иконка должна быть заметна на любом фоне
- **Минимализм** — без мелких деталей
- **Узнаваемость** — используйте ассоциации с YouTube/видео

### 💡 Идеи для иконки

```
┌─────────────────────────────────────────────────────┐
│  🎬 Красная кнопка Play + стрелка вниз             │
│  📺 Телевизор с символом загрузки                  │
│  🔴 Логотип YouTube + Download                     │
│  📦 Коробка с видео-символом                       │
└─────────────────────────────────────────────────────┘
```

### 🛠️ Инструменты

| Инструмент | Тип | Ссылка |
|------------|-----|--------|
| Figma | Онлайн | https://figma.com/ |
| Canva | Онлайн | https://canva.com/ |
| GIMP | Десктоп | https://gimp.org/ |
| Inkscape | Вектор | https://inkscape.org/ |

---

## 📬 Распространение

### Упаковка для публикации

```
YouTube Downloader Lite/
├── YouTube Downloader Lite.exe
└── README.txt (инструкция для пользователя)
```

### README.txt для пользователей

```
═══════════════════════════════════════════════════════
  YouTube Downloader Lite — Инструкция
═══════════════════════════════════════════════════════

1. Запустите "YouTube Downloader Lite.exe"
2. Вставьте ссылку на видео YouTube
3. Выберите качество (480p — лучший вариант со звуком)
4. Нажмите "Скачать"

⚠️ 1080p/720p могут быть без звука — это ограничение
   YouTube, а не программы. Для лучшего качества
   установите FFmpeg и используйте полную версию.

Папка загрузок: Downloads/ (в той же папке)
═══════════════════════════════════════════════════════
```

---

## 🔗 Полезные ссылки

| Ресурс | Назначение |
|--------|------------|
| [yt-dlp документация](https://github.com/yt-dlp/yt-dlp) | Форматы, опции |
| [customtkinter документация](https://customtkinter.tomsimulation.de/) | GUI компоненты |
| [PyInstaller руководство](https://pyinstaller.org/en/stable/) | Сборка EXE |
| [FFmpeg загрузки](https://www.gyan.dev/ffmpeg/) | FFmpeg для Windows |

---

> **⚖️ Лицензия:** Только для личного использования. Уважайте авторские права.
