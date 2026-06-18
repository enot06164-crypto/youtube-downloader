"""
YouTube Downloader — Приложение для скачивания видео и аудио с YouTube
Версия БЕЗ FFmpeg (не требует дополнительных установок)

⚠️ Дисклеймер: Используйте только для скачивания контента, 
который вы имеете право загружать (личный архив, Creative Commons и т.д.)

⚠️ Ограничения этой версии:
- Видео 1080p/720p могут быть без звука (YouTube разделяет потоки)
- Для видео со звуком доступно максимум 480p
"""

import customtkinter as ctk
from tkinter import messagebox
import threading
import os
import re
import sys
from pathlib import Path
from typing import Optional, Callable

import yt_dlp
from PIL import Image, ImageDraw

# =============================================================================
# КОНФИГУРАЦИЯ
# =============================================================================

ICON_PATH = None
APP_TITLE = "YouTube Downloader Lite"
APP_VERSION = "0.1.0"

# FFmpeg не требуется для этой версии


# =============================================================================
# ИСКЛЮЧЕНИЯ
# =============================================================================


class DownloadCancelled(Exception):
    """Исключение, сигнализирующее об отмене загрузки пользователем."""
    pass


# =============================================================================
# ГЕНЕРАТОР ИКОНОК
# =============================================================================


class IconGenerator:
    """Генерирует иконки программно через PIL."""

    @staticmethod
    def create_download_icon(size: int = 24) -> ctk.CTkImage:
        """Создаёт иконку скачивания (стрелка вниз)."""
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        margin = size // 6
        arrow_width = size - 2 * margin
        center = size // 2
        
        points = [
            (center, margin + arrow_width),
            (margin, margin),
            (center, margin + arrow_width // 3),
            (size - margin, margin),
        ]
        draw.polygon(points, fill='#28a745')
        
        stem_width = arrow_width // 4
        stem_top = margin + arrow_width // 2
        stem_bottom = size - margin - 2
        draw.rectangle(
            [center - stem_width // 2, stem_top, center + stem_width // 2, stem_bottom],
            fill='#28a745'
        )
        
        return ctk.CTkImage(light_image=img, dark_image=img, size=(size, size))

    @staticmethod
    def create_paste_icon(size: int = 24) -> ctk.CTkImage:
        """Создаёт иконку буфера обмена."""
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        margin = size // 6
        
        draw.rounded_rectangle(
            [margin, margin + 4, size - margin, size - margin],
            radius=3,
            fill='#6c757d'
        )
        
        draw.rectangle(
            [margin + 4, margin, size - margin - 4, margin + 8],
            fill='#adb5bd'
        )
        
        inner_margin = margin + 5
        draw.rounded_rectangle(
            [inner_margin, margin + 10, size - inner_margin, size - margin - 2],
            radius=2,
            fill='#ffffff'
        )
        
        return ctk.CTkImage(light_image=img, dark_image=img, size=(size, size))

    @staticmethod
    def create_folder_icon(size: int = 24) -> ctk.CTkImage:
        """Создаёт иконку папки."""
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        margin = size // 6
        
        draw.rounded_rectangle(
            [margin, margin + 4, size - margin, size - margin],
            radius=3,
            fill='#007bff'
        )
        
        draw.rounded_rectangle(
            [margin, margin, size // 2 + 2, margin + 8],
            radius=2,
            fill='#0056b3'
        )
        
        return ctk.CTkImage(light_image=img, dark_image=img, size=(size, size))

    @staticmethod
    def create_cancel_icon(size: int = 24) -> ctk.CTkImage:
        """Создаёт иконку отмены (крестик)."""
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        margin = 2
        draw.ellipse([margin, margin, size - margin, size - margin], fill='#dc3545')
        
        line_width = 2
        center = size // 2
        offset = size // 4
        
        draw.line(
            [center - offset, center - offset, center + offset, center + offset],
            fill='#ffffff',
            width=line_width
        )
        draw.line(
            [center + offset, center - offset, center - offset, center + offset],
            fill='#ffffff',
            width=line_width
        )
        
        return ctk.CTkImage(light_image=img, dark_image=img, size=(size, size))

    @staticmethod
    def create_warning_icon(size: int = 20) -> ctk.CTkImage:
        """Создаёт иконку предупреждения."""
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Треугольник
        margin = 1
        points = [
            (size // 2, margin),
            (margin, size - margin),
            (size - margin, size - margin),
        ]
        draw.polygon(points, fill='#ffc107')
        
        # Восклицательный знак
        center = size // 2
        draw.rectangle([center - 1, margin + 6, center + 1, margin + 10], fill='#856404')
        draw.ellipse([center - 1, margin + 12, center + 1, margin + 15], fill='#856404')
        
        return ctk.CTkImage(light_image=img, dark_image=img, size=(size, size))

    @staticmethod
    def create_info_icon(size: int = 16) -> ctk.CTkImage:
        """Создаёт информационную иконку."""
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        margin = 1
        draw.ellipse([margin, margin, size - margin, size - margin], outline='#17a2b8', width=2)
        
        center = size // 2
        draw.rectangle([center - 1, margin + 5, center + 1, margin + 9], fill='#17a2b8')
        draw.ellipse([center - 1, margin + 10, center + 1, margin + 12], fill='#17a2b8')
        
        return ctk.CTkImage(light_image=img, dark_image=img, size=(size, size))

    @staticmethod
    def create_audio_icon(size: int = 20) -> ctk.CTkImage:
        """Создаёт иконку аудио (нота)."""
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Нота
        margin = 4
        draw.ellipse([margin, size - margin - 6, margin + 8, size - margin], fill='#9c27b0')
        draw.rectangle([margin + 3, margin, margin + 5, size - margin - 3], fill='#9c27b0')
        draw.ellipse([margin + 6, size - margin - 8, margin + 14, size - margin - 2], fill='#9c27b0')
        
        return ctk.CTkImage(light_image=img, dark_image=img, size=(size, size))


# =============================================================================
# КЛАСС DOWNLOADER
# =============================================================================


class Downloader:
    """Класс для управления загрузкой видео/аудио без FFmpeg."""

    def __init__(self, progress_callback: Optional[Callable] = None):
        self.progress_callback = progress_callback
        self.current_download: Optional[dict] = None
        self._cancelled = False
        self._ydl: Optional[yt_dlp.YoutubeDL] = None
        self._ydl_lock = threading.Lock()

    def _progress_hook(self, d: dict) -> None:
        """Хук для отслеживания прогресса."""
        if self._cancelled:
            raise DownloadCancelled("Загрузка отменена пользователем")

        if d['status'] == 'downloading':
            downloaded = d.get('downloaded_bytes', 0)
            total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
            speed = d.get('speed', 0)
            eta = d.get('eta', 0)

            percent = (downloaded / total) * 100 if total > 0 else 0

            if speed:
                if speed > 1024 * 1024:
                    speed_str = f"{speed / (1024 * 1024):.2f} MB/s"
                elif speed > 1024:
                    speed_str = f"{speed / 1024:.2f} KB/s"
                else:
                    speed_str = f"{speed:.2f} B/s"
            else:
                speed_str = "N/A"

            if self.progress_callback:
                self.progress_callback({
                    'status': 'downloading',
                    'percent': round(percent, 1),
                    'speed': speed_str,
                    'eta': f"{eta} сек" if eta else "N/A"
                })

        elif d['status'] == 'finished':
            if self.progress_callback:
                self.progress_callback({
                    'status': 'finished',
                    'percent': 100,
                    'speed': 'Готово!',
                    'eta': ''
                })

    def _postprocessor_hook(self, d: dict) -> None:
        """Хук для прерывания постпроцессинга при отмене."""
        if self._cancelled:
            raise DownloadCancelled("Загрузка отменена пользователем")

    @staticmethod
    def _collect_downloaded_files(info: dict) -> list[str]:
        """Собирает реальные пути скачанных файлов из результата yt-dlp."""
        files: list[str] = []
        for entry in info.get('requested_downloads', []) or []:
            filepath = entry.get('filepath')
            if filepath and os.path.exists(filepath):
                files.append(filepath)
        return files

    def download(self, url: str, quality: str, output_path: str) -> bool:
        """Загружает видео или аудио по URL. Возвращает True при успехе, False при отмене."""
        self._cancelled = False
        self._ydl = None

        ydl_opts = {
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'progress_hooks': [self._progress_hook],
            'postprocessor_hooks': [self._postprocessor_hook],
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
        }

        if quality == 'audio':
            ydl_opts.update({
                'format': 'bestaudio[ext=m4a]/bestaudio/best',
            })
        elif quality == '720p_best':
            ydl_opts.update({
                'format': 'bestvideo[height<=720]/best[height<=720]',
            })
        elif quality == '1080p_best':
            ydl_opts.update({
                'format': 'bestvideo[height<=1080]/best[height<=1080]',
            })
        elif quality == '480p':
            ydl_opts.update({
                'format': 'best[height<=480]/best',
            })
        else:
            ydl_opts.update({
                'format': 'best[height<=480]/best',
            })

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                with self._ydl_lock:
                    self._ydl = ydl
                try:
                    info = ydl.extract_info(url, download=True)
                finally:
                    with self._ydl_lock:
                        self._ydl = None

                if info is None:
                    raise Exception("Не удалось получить информацию о видео")

                downloaded_files = self._collect_downloaded_files(info)
                self.current_download = {
                    'title': info.get('title', 'Неизвестно'),
                    'uploader': info.get('uploader', 'Неизвестно'),
                    'duration': info.get('duration', 0),
                    'format': info.get('format_note', 'Unknown'),
                    'ext': info.get('ext', 'unknown'),
                    'filepath': downloaded_files[0] if downloaded_files else None,
                }
                return True
        except DownloadCancelled:
            return False
        except Exception:
            with self._ydl_lock:
                self._ydl = None
            raise

    def cancel(self) -> None:
        """Отменяет текущую загрузку."""
        self._cancelled = True
        with self._ydl_lock:
            if self._ydl is not None:
                try:
                    self._ydl.close()
                except Exception:
                    pass


# =============================================================================
# КЛАСС APP
# =============================================================================


class App(ctk.CTk):
    """Основной класс приложения YouTube Downloader Lite."""

    def __init__(self):
        super().__init__()

        self.title(APP_TITLE)
        self.geometry("650x750")
        self.minsize(550, 650)
        self.resizable(True, True)

        self._set_icon()
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(5, weight=1)

        self.downloader = Downloader(progress_callback=self._on_progress)

        self.url_var = ctk.StringVar()
        self.quality_var = ctk.StringVar(value="480p (со звуком)")
        self.is_downloading = False
        self.download_thread: Optional[threading.Thread] = None
        self._destroyed = False
        self._last_logged_percent: Optional[float] = None

        self.download_path = self._create_downloads_folder()
        self._create_widgets()
        self.protocol("WM_DELETE_WINDOW", self._on_closing)

    def destroy(self) -> None:
        """Перехватываем уничтожение, чтобы фоновый поток не дёргал after()."""
        self._destroyed = True
        super().destroy()

    def _set_icon(self) -> None:
        """Устанавливает иконку окна."""
        if ICON_PATH and os.path.exists(ICON_PATH):
            try:
                self.wm_iconbitmap(ICON_PATH)
            except Exception:
                pass
        else:
            # Пути поиска: рядом с .exe, рядом с исходником, в _MEIPASS
            search_dirs = []
            if getattr(sys, 'frozen', False):
                search_dirs.append(os.path.dirname(sys.executable))
                search_dirs.append(sys._MEIPASS)
            else:
                search_dirs.append(os.path.dirname(__file__))
            for d in search_dirs:
                icon_path = os.path.join(d, 'icon.ico')
                if os.path.exists(icon_path):
                    try:
                        self.wm_iconbitmap(icon_path)
                    except Exception:
                        pass
                    break

    def _create_downloads_folder(self) -> str:
        """Создает папку для загрузок в системной папке Загрузки."""
        # Получаем системную папку Загрузки
        downloads = Path.home() / "Downloads" / "YouTube Downloader"
        downloads.mkdir(parents=True, exist_ok=True)
        return str(downloads)

    def _create_widgets(self) -> None:
        """Создает все элементы интерфейса."""
        padding = 20

        # ===== ЗАГОЛОВОК =====
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid_columnconfigure(0, weight=1)
        header_frame.grid(row=0, column=0, padx=padding, pady=(padding, 5), sticky="ew")

        self.title_label = ctk.CTkLabel(
            header_frame,
            text="YouTube Downloader",
            font=ctk.CTkFont(size=26, weight="bold")
        )
        self.title_label.grid(row=0, column=0, sticky="w")

        self.version_badge = ctk.CTkLabel(
            header_frame,
            text="LITE",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#ffffff",
            fg_color="#6c757d",
            corner_radius=6
        )
        self.version_badge.grid(row=0, column=1, padx=(10, 0))

        self.subtitle_label = ctk.CTkLabel(
            self,
            text="Версия без FFmpeg • Для личного архива",
            font=ctk.CTkFont(size=13),
            text_color="gray"
        )
        self.subtitle_label.grid(row=1, column=0, padx=padding, pady=(0, 15))

        # ===== ПРЕДУПРЕЖДЕНИЕ =====
        warning_frame = ctk.CTkFrame(self, fg_color="#fff3cd", corner_radius=10)
        warning_frame.grid_columnconfigure(1, weight=1)
        warning_frame.grid(row=2, column=0, padx=padding, pady=10, sticky="ew")

        self.warning_icon = ctk.CTkLabel(
            warning_frame,
            image=IconGenerator.create_warning_icon(24),
            text=""
        )
        self.warning_icon.image = IconGenerator.create_warning_icon(24)
        self.warning_icon.grid(row=0, column=0, padx=12, pady=12)

        self.warning_label = ctk.CTkLabel(
            warning_frame,
            text="1080p/720p могут быть без звука. Для лучшего качества установите FFmpeg.",
            font=ctk.CTkFont(size=12),
            text_color="#856404",
            justify="left",
            wraplength=450
        )
        self.warning_label.grid(row=0, column=1, padx=(0, 12), pady=12, sticky="w")

        # ===== ПОЛЕ ВВОДА ССЫЛКИ =====
        url_frame = ctk.CTkFrame(self, fg_color="transparent")
        url_frame.grid_columnconfigure(0, weight=1)
        url_frame.grid(row=3, column=0, padx=padding, pady=10, sticky="ew")

        self.url_label = ctk.CTkLabel(
            url_frame,
            text="Ссылка на видео:",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self.url_label.grid(row=0, column=0, padx=(0, 10), sticky="w", pady=(0, 5))

        self.url_entry = ctk.CTkEntry(
            url_frame,
            textvariable=self.url_var,
            placeholder_text="https://www.youtube.com/watch?v=...",
            font=ctk.CTkFont(size=14),
            height=45
        )
        self.url_entry.grid(row=1, column=0, padx=(0, 10), sticky="ew")

        # Логируем только реальные вставки через виртуальное событие <<Paste>>
        self.url_entry._entry.bind("<<Paste>>", self._on_paste_event)
        # Единый обработчик Ctrl+V (работает на любой раскладке)
        # keycode 86 — это V в любой раскладке
        self.url_entry._entry.bind("<Control-KeyPress>", self._on_ctrl_key)

        self.paste_btn = ctk.CTkButton(
            url_frame,
            text="",
            width=48,
            height=45,
            command=self._paste_from_clipboard,
            fg_color="#6c757d",
            hover_color="#5a6268"
        )
        self.paste_btn.grid(row=1, column=1)

        paste_icon = IconGenerator.create_paste_icon(20)
        self.paste_icon_label = ctk.CTkLabel(self.paste_btn, image=paste_icon, text="")
        self.paste_icon_label.image = paste_icon
        self.paste_icon_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # Кнопка очистки
        self.clear_btn = ctk.CTkButton(
            url_frame,
            text="✕",
            width=48,
            height=45,
            command=self._clear_url,
            fg_color="#dc3545",
            hover_color="#c82333",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.clear_btn.grid(row=1, column=2, padx=(5, 0))

        # ===== ВЫБОР КАЧЕСТВА =====
        quality_frame = ctk.CTkFrame(self, fg_color="transparent")
        quality_frame.grid_columnconfigure(1, weight=1)
        quality_frame.grid(row=4, column=0, padx=padding, pady=10, sticky="ew")

        self.quality_label = ctk.CTkLabel(
            quality_frame,
            text="Качество:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.quality_label.grid(row=0, column=0, padx=(0, 10), sticky="w")

        self.quality_menu = ctk.CTkOptionMenu(
            quality_frame,
            variable=self.quality_var,
            values=[
                "480p (со звуком)",
                "720p (может быть без звука)",
                "1080p (может быть без звука)",
                "Аудио (M4A)",
            ],
            font=ctk.CTkFont(size=14),
            height=40,
            command=self._on_quality_change
        )
        self.quality_menu.grid(row=0, column=1, sticky="ew")

        # ===== ИНФОРМАЦИЯ О ФОРМАТАХ =====
        info_frame = ctk.CTkFrame(self, fg_color="transparent")
        info_frame.grid(row=5, column=0, padx=padding, pady=(0, 10), sticky="w")

        self.info_label = ctk.CTkLabel(
            info_frame,
            text="480p — лучший вариант со звуком | 720p/1080p — только видео",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        self.info_label.grid(row=0, column=0)

        # ===== ПРОГРЕСС БАР =====
        self.progress_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.progress_frame.grid_columnconfigure(0, weight=1)
        self.progress_frame.grid(row=6, column=0, padx=padding, pady=20, sticky="nsew")

        self.progress_bar = ctk.CTkProgressBar(self.progress_frame, height=24, corner_radius=12)
        self.progress_bar.grid(row=0, column=0, padx=0, pady=(0, 12), sticky="ew")
        self.progress_bar.set(0)

        self.progress_label = ctk.CTkLabel(
            self.progress_frame,
            text="Готов к загрузке",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="gray"
        )
        self.progress_label.grid(row=1, column=0, sticky="w")

        self.progress_details = ctk.CTkLabel(
            self.progress_frame,
            text="",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.progress_details.grid(row=2, column=0, sticky="w")

        # ===== КНОПКИ =====
        buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        buttons_frame.grid_columnconfigure(0, weight=2)
        buttons_frame.grid_columnconfigure(1, weight=1)
        buttons_frame.grid_columnconfigure(2, weight=1)
        buttons_frame.grid(row=7, column=0, padx=padding, pady=10, sticky="ew")

        self.download_btn = ctk.CTkButton(
            buttons_frame,
            text="Скачать",
            font=ctk.CTkFont(size=15, weight="bold"),
            height=48,
            command=self._start_download,
            fg_color="#28a745",
            hover_color="#218838",
            corner_radius=10
        )
        self.download_btn.grid(row=0, column=0, padx=(0, 8), sticky="ew")

        self.cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="Отмена",
            font=ctk.CTkFont(size=14),
            height=48,
            command=self._cancel_download,
            fg_color="#dc3545",
            hover_color="#c82333",
            state="disabled",
            corner_radius=10
        )
        self.cancel_btn.grid(row=0, column=1, padx=(0, 8))

        self.open_folder_btn = ctk.CTkButton(
            buttons_frame,
            text="Папка",
            font=ctk.CTkFont(size=14),
            height=48,
            command=self._open_downloads_folder,
            state="disabled",
            fg_color="#007bff",
            hover_color="#0056b3",
            corner_radius=10
        )
        self.open_folder_btn.grid(row=0, column=2)

        # ===== ЛОГ =====
        log_frame = ctk.CTkFrame(self, corner_radius=10)
        log_frame.grid_columnconfigure(0, weight=1)
        log_frame.grid_rowconfigure(1, weight=1)
        log_frame.grid(row=8, column=0, padx=padding, pady=(10, padding), sticky="nsew")

        log_header = ctk.CTkFrame(log_frame, fg_color="transparent")
        log_header.grid_columnconfigure(0, weight=1)
        log_header.grid(row=0, column=0, padx=12, pady=(10, 5), sticky="ew")

        self.log_icon = ctk.CTkLabel(log_header, image=IconGenerator.create_info_icon(16), text="")
        self.log_icon.image = IconGenerator.create_info_icon(16)
        self.log_icon.grid(row=0, column=0, sticky="w")

        self.log_label = ctk.CTkLabel(
            log_header,
            text="Журнал событий",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self.log_label.grid(row=0, column=1, padx=(8, 0), sticky="w")

        self.log_text = ctk.CTkTextbox(
            log_frame,
            font=ctk.CTkFont(size=11, family="Consolas"),
            state="disabled",
            corner_radius=8
        )
        self.log_text.grid(row=1, column=0, padx=12, pady=(0, 10), sticky="nsew")

        # ===== ПОДВАЛ =====
        self.footer_label = ctk.CTkLabel(
            self,
            text=f"Версия {APP_VERSION} | Только для личного использования",
            font=ctk.CTkFont(size=10),
            text_color="gray"
        )
        self.footer_label.grid(row=9, column=0, padx=padding, pady=(0, 10))

    def _on_ctrl_key(self, event) -> Optional[str]:
        """Обрабатывает Ctrl+V в любой раскладке (один биндинг — никакого двойного вызова)."""
        if event.keycode == 86 or event.keysym.lower() in ('v', 'м'):
            self._do_paste()
            return "break"
        return None

    def _on_paste_event(self, event=None) -> None:
        """Логирует факт вставки из буфера (срабатывает только при реальной вставке)."""
        self.after(50, lambda: self._log("Ссылка вставлена из буфера обмена"))

    def _do_paste(self) -> None:
        """Выполняет вставку из буфера обмена через виртуальное событие Tk."""
        try:
            self.url_entry._entry.event_generate("<<Paste>>")
        except Exception:
            self._log("Ошибка при вставке из буфера обмена")

    def _paste_from_clipboard(self) -> None:
        """Вставляет ссылку из буфера обмена (кнопка)."""
        self._do_paste()

    def _clear_url(self) -> None:
        """Очищает поле ввода ссылки."""
        self.url_var.set("")
        self._log("Поле ссылки очищено")
        self.url_entry.focus()

    def _on_quality_change(self, value: str) -> None:
        """Обработчик изменения качества."""
        self._log(f"Выбрано качество: {value}")

    def _validate_url(self, url: str) -> bool:
        """Проверяет валидность YouTube ссылки (включая Shorts)."""
        pattern = r'(https?://)?(www\.)?(youtube\.com/(watch|shorts|embed|live|playlist)|youtu\.be/).+'
        return bool(re.match(pattern, url))

    def _start_download(self) -> None:
        """Запускает загрузку в отдельном потоке."""
        url = self.url_var.get().strip()

        if not url:
            messagebox.showwarning("Предупреждение", "Пожалуйста, вставьте ссылку на видео!")
            return

        if not self._validate_url(url):
            messagebox.showerror("Ошибка", "Неверная ссылка! Пожалуйста, вставьте корректную ссылку на YouTube.")
            return

        if self.is_downloading:
            messagebox.showwarning("Предупреждение", "Загрузка уже выполняется!")
            return

        quality_map = {
            "480p (со звуком)": "480p",
            "720p (может быть без звука)": "720p_best",
            "1080p (может быть без звука)": "1080p_best",
            "Аудио (M4A)": "audio",
        }
        quality = quality_map.get(self.quality_var.get(), "480p")

        self.is_downloading = True
        self.download_thread = threading.Thread(
            target=self._download_thread,
            args=(url, quality),
            daemon=True
        )
        self.download_thread.start()

        self.download_btn.configure(state="disabled", text="Загрузка...")
        self.cancel_btn.configure(state="normal")
        self.open_folder_btn.configure(state="disabled")
        self.quality_menu.configure(state="disabled")
        self.url_entry.configure(state="disabled")

        self._log(f"Начало загрузки: {url[:50]}...")

    def _safe_after(self, ms: int, func: Callable) -> None:
        """Планирует callback, если окно ещё не разрушено."""
        if not self._destroyed:
            try:
                self.after(ms, func)
            except Exception:
                pass

    def _download_thread(self, url: str, quality: str) -> None:
        """Поток загрузки."""
        try:
            success = self.downloader.download(url, quality, self.download_path)
            self._safe_after(0, lambda: self._on_download_complete(success, url))
        except Exception as e:
            error_msg = str(e)
            self._safe_after(0, lambda: self._on_download_error(error_msg))

    def _on_download_complete(self, success: bool, url: str) -> None:
        """Обработчик завершения загрузки."""
        self.is_downloading = False

        if not success:
            self._on_download_cancelled()
            return

        self._log("Загрузка завершена успешно!")
        self.progress_label.configure(text="Загрузка завершена!")
        self.progress_details.configure(text="")

        if self.downloader.current_download:
            title = self.downloader.current_download.get('title', 'Файл')
            ext = self.downloader.current_download.get('ext', '')
            self.progress_details.configure(text=f"{title}.{ext}")

        self._reset_controls_after_download()
        messagebox.showinfo("Готово!", f"Файл успешно скачан!\n\nПапка: {self.download_path}")

    def _on_download_cancelled(self) -> None:
        """Обработчик отмены загрузки (без диалога ошибки)."""
        self._log("Загрузка отменена пользователем")
        self.progress_label.configure(text="Отменено")
        self.progress_details.configure(text="")
        self._reset_controls_after_download()

    def _reset_controls_after_download(self) -> None:
        """Восстанавливает состояние элементов UI после завершения/отмены/ошибки."""
        self.download_btn.configure(state="normal", text="Скачать")
        self.cancel_btn.configure(state="disabled")
        self.open_folder_btn.configure(state="normal")
        self.quality_menu.configure(state="normal")
        self.url_entry.configure(state="normal")

    def _on_download_error(self, error: str) -> None:
        """Обработчик ошибки загрузки."""
        self.is_downloading = False

        self._log(f"Ошибка: {error}")
        self.progress_label.configure(text="Ошибка загрузки")
        self.progress_details.configure(text=error)

        self._reset_controls_after_download()
        messagebox.showerror("Ошибка", f"Не удалось загрузить файл:\n{error}")

    def _cancel_download(self) -> None:
        """Отменяет текущую загрузку."""
        if self.is_downloading:
            self.downloader.cancel()
            self._log("Загрузка отменена пользователем")
            self.progress_label.configure(text="Отменено")

    def _open_downloads_folder(self) -> None:
        """Открывает папку с загрузками."""
        try:
            if os.path.exists(self.download_path):
                os.startfile(self.download_path)
                self._log("Открыта папка загрузок")
            else:
                messagebox.showwarning("Предупреждение", "Папка загрузок не найдена!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось открыть папку:\n{e}")

    def _on_progress(self, data: dict) -> None:
        """Callback для обновления прогресса (лог пишется не чаще раза в 5%)."""
        def update():
            if self._destroyed:
                return
            status = data.get('status', '')
            percent = data.get('percent', 0)
            speed = data.get('speed', '')
            eta = data.get('eta', '')

            self.progress_bar.set(percent / 100)

            if status == 'downloading':
                self.progress_label.configure(text=f"Загрузка: {percent}%")
                self.progress_details.configure(text=f"{speed} | {eta}")
            elif status == 'finished':
                self.progress_label.configure(text="Завершено!")
                self.progress_details.configure(text="Файл сохранён")

            if self._last_logged_percent is None or abs(percent - self._last_logged_percent) >= 5 or percent in (0, 100):
                self._log(f"Прогресс: {percent}% | {speed}")
                self._last_logged_percent = percent

        self._safe_after(0, update)

    def _log(self, message: str) -> None:
        """Добавляет сообщение в лог."""
        def add_log():
            if self._destroyed:
                return
            self.log_text.configure(state="normal")
            self.log_text.insert("end", f"{message}\n")
            self.log_text.see("end")
            self.log_text.configure(state="disabled")

        self._safe_after(0, add_log)

    def _on_closing(self) -> None:
        """Обработчик закрытия окна."""
        if self.is_downloading:
            if messagebox.askyesno("Подтверждение", "Загрузка выполняется. Вы действительно хотите выйти?"):
                self.downloader.cancel()
                if self.download_thread and self.download_thread.is_alive():
                    self.download_thread.join(timeout=3)
                self.destroy()
        else:
            self.destroy()


# =============================================================================
# ТОЧКА ВХОДА
# =============================================================================

if __name__ == "__main__":
    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("blue")

    messagebox.showinfo(
        "Дисклеймер",
        "Внимание!\n\n"
        "Это приложение предназначено ТОЛЬКО для личного использования.\n\n"
        "• Скачивайте только контент, который вы имеете право загружать\n"
        "• Уважайте авторские права создателей контента\n"
        "• Версия БЕЗ FFmpeg: 1080p/720p могут быть без звука\n\n"
        "Нажимая 'OK', вы подтверждаете согласие с этими условиями."
    )

    app = App()
    app.mainloop()
