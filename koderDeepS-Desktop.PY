"""
koderDeepS Desktop - AI IDE для работы с DeepSeek
Установка зависимостей для Python 3.13:
    pip install PySide6
"""

import sys
import os
import re
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Tuple
import time
import subprocess
import html
import shutil

# Сначала импортируем сам PySide6 для проверки версии
try:
    import PySide6
    PYSIDE_VERSION = PySide6.__version__
    print(f"PySide6 версия: {PYSIDE_VERSION}")
    
    # Затем импортируем все необходимые компоненты
    from PySide6.QtCore import (
        Qt, QUrl, QTimer, Signal, Slot, QObject, 
        QThread, QSize, QByteArray, QPoint
    )
    from PySide6.QtGui import (
        QAction, QIcon, QFont, QTextCursor, 
        QColor, QPalette, QSyntaxHighlighter, QTextCharFormat,
        QPixmap, QCursor
    )
    from PySide6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, 
        QHBoxLayout, QSplitter, QTreeView, QTextEdit, 
        QToolBar, QPushButton, QLabel, QMessageBox,
        QFileSystemModel, QStatusBar, QMenu, QMenuBar,
        QPlainTextEdit, QFrame, QLineEdit, QInputDialog,
        QFileDialog, QDialog, QDialogButtonBox, QGroupBox,
        QGridLayout, QButtonGroup, QCheckBox
    )
    from PySide6.QtWebEngineWidgets import QWebEngineView
    from PySide6.QtWebEngineCore import QWebEnginePage, QWebEngineProfile, QWebEngineSettings
    PYSIDE_INSTALLED = True
except ImportError as e:
    PYSIDE_INSTALLED = False
    print("=" * 60)
    print("ОШИБКА: Библиотека PySide6 не установлена или установлена некорректно!")
    print("=" * 60)
    print(f"\nДетали ошибки: {e}")
    print("\nДля установки выполните команду:")
    print("  pip install PySide6")
    print("\nИли если используете pip3:")
    print("  pip3 install PySide6")
    print("=" * 60)
    sys.exit(1)


def setup_dark_theme(app):
    """Устанавливает темную тему для всего приложения"""
    app.setStyle('Fusion')
    
    # Создаем темную палитру
    dark_palette = QPalette()
    
    # Цвета для темной темы
    dark_palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
    dark_palette.setColor(QPalette.ColorRole.Base, QColor(35, 35, 35))
    dark_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(25, 25, 25))
    dark_palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
    dark_palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
    dark_palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
    dark_palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
    dark_palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)
    
    # Цвета для disabled состояния
    dark_palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, Qt.GlobalColor.gray)
    dark_palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, Qt.GlobalColor.gray)
    dark_palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, Qt.GlobalColor.gray)
    
    app.setPalette(dark_palette)
    
    # Дополнительные стили для виджетов
    app.setStyleSheet("""
        QToolBar {
            background-color: #353535;
            border: none;
            spacing: 3px;
            padding: 5px;
        }
        
        QToolBar QPushButton {
            background-color: #454545;
            color: white;
            border: 1px solid #555555;
            border-radius: 3px;
            padding: 5px 10px;
            min-width: 80px;
        }
        
        QToolBar QPushButton:hover {
            background-color: #555555;
        }
        
        QToolBar QPushButton:pressed {
            background-color: #656565;
        }
        
        QTreeView {
            background-color: #2d2d2d;
            color: white;
            border: 1px solid #555555;
        }
        
        QTreeView::item:hover {
            background-color: #3d3d3d;
        }
        
        QTreeView::item:selected {
            background-color: #0d7377;
        }
        
        QTextEdit, QPlainTextEdit {
            background-color: #1e1e1e;
            color: #d4d4d4;
            border: 1px solid #555555;
            font-family: 'Consolas', 'Monaco', monospace;
        }
        
        QLabel {
            color: white;
        }
        
        QMenuBar {
            background-color: #353535;
            color: white;
        }
        
        QMenuBar::item {
            background-color: #353535;
            color: white;
        }
        
        QMenuBar::item:selected {
            background-color: #454545;
        }
        
        QMenu {
            background-color: #353535;
            color: white;
            border: 1px solid #555555;
        }
        
        QMenu::item:selected {
            background-color: #454545;
        }
        
        QStatusBar {
            background-color: #353535;
            color: white;
        }
        
        QFrame {
            color: white;
        }
        
        QSplitter::handle {
            background-color: #555555;
        }
        
        QSplitter::handle:hover {
            background-color: #666666;
        }
        
        QScrollBar:vertical {
            background-color: #353535;
            width: 14px;
            border-radius: 7px;
        }
        
        QScrollBar::handle:vertical {
            background-color: #555555;
            min-height: 20px;
            border-radius: 7px;
        }
        
        QScrollBar::handle:vertical:hover {
            background-color: #666666;
        }
        
        QScrollBar:horizontal {
            background-color: #353535;
            height: 14px;
            border-radius: 7px;
        }
        
        QScrollBar::handle:horizontal {
            background-color: #555555;
            min-width: 20px;
            border-radius: 7px;
        }
        
        QScrollBar::handle:horizontal:hover {
            background-color: #666666;
        }
        
        QDialog {
            background-color: #353535;
            color: white;
        }
        
        QLineEdit {
            background-color: #2d2d2d;
            color: white;
            border: 1px solid #555555;
            border-radius: 3px;
            padding: 5px;
        }
        
        QDialogButtonBox QPushButton {
            background-color: #454545;
            color: white;
            border: 1px solid #555555;
            border-radius: 3px;
            padding: 5px 15px;
        }
        
        QDialogButtonBox QPushButton:hover {
            background-color: #555555;
        }
        
        QGroupBox {
            border: 2px solid #555555;
            border-radius: 5px;
            margin-top: 10px;
            padding-top: 10px;
            color: white;
            font-weight: bold;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px 0 5px;
            color: #0d7377;
        }
        
        QCheckBox {
            color: white;
            spacing: 5px;
        }
        
        QCheckBox::indicator {
            width: 18px;
            height: 18px;
            border: 1px solid #555555;
            border-radius: 3px;
            background-color: #2d2d2d;
        }
        
        QCheckBox::indicator:checked {
            background-color: #0d7377;
            border-color: #0d7377;
        }
        
        QCheckBox::indicator:hover {
            border-color: #0d7377;
        }
        
        .format-button {
            background-color: #3d3d3d;
            color: white;
            border: 1px solid #555555;
            border-radius: 3px;
            padding: 8px;
            font-size: 12px;
            min-width: 60px;
        }
        
        .format-button:hover {
            background-color: #4d4d4d;
            border-color: #0d7377;
        }
        
        .format-button:checked {
            background-color: #0d7377;
            border-color: #0d7377;
        }
    """)


class Logger(QObject):
    """Система логирования действий программы"""
    log_updated = Signal(str)
    
    def __init__(self):
        super().__init__()
        self.logs = []
        
    def info(self, message: str):
        """Логирование информационного сообщения"""
        log_entry = f"[{datetime.now().strftime('%H:%M:%S')}] [ИНФО] {message}"
        self.logs.append(log_entry)
        self.log_updated.emit(log_entry)
        print(log_entry)  # Для отладки
        
    def warning(self, message: str):
        """Логирование предупреждения"""
        log_entry = f"[{datetime.now().strftime('%H:%M:%S')}] [ПРЕДУПРЕЖДЕНИЕ] {message}"
        self.logs.append(log_entry)
        self.log_updated.emit(log_entry)
        print(log_entry)
        
    def error(self, message: str):
        """Логирование ошибки"""
        log_entry = f"[{datetime.now().strftime('%H:%M:%S')}] [ОШИБКА] {message}"
        self.logs.append(log_entry)
        self.log_updated.emit(log_entry)
        print(log_entry)


class PrePromptDialog(QDialog):
    """Диалог настройки пред промпта"""
    
    def __init__(self, current_pre_prompt: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Настройка пред промпта")
        self.setModal(True)
        self.resize(600, 500)
        
        # Устанавливаем иконку для диалога
        icon_path = Path("koderDeepS-Desktop.ico")
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))
        
        layout = QVBoxLayout()
        
        # Заголовок
        title_label = QLabel("⚙️ Настройка пред промпта")
        title_font = QFont()
        title_font.setBold(True)
        title_font.setPointSize(12)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #0d7377; padding: 10px;")
        layout.addWidget(title_label)
        
        # Пояснение
        info_label = QLabel(
            "Текст пред промпта будет автоматически добавляться "
            "к каждому вашему сообщению перед отправкой в DeepSeek."
        )
        info_label.setWordWrap(True)
        info_label.setStyleSheet("color: #888888; padding: 5px;")
        layout.addWidget(info_label)
        
        # Группа с кнопками форматов файлов
        formats_group = QGroupBox("📁 Форматы файлов для пред промпта")
        formats_group.setStyleSheet("""
            QGroupBox {
                color: #0d7377;
                font-size: 11pt;
                margin-top: 10px;
            }
        """)
        
        formats_layout = QGridLayout()
        
        # Создаем кнопки для разных форматов
        self.format_buttons = []
        formats = [
            ("🐍 Python", ".py", "Создай файл Python с именем"),
            ("📜 JavaScript", ".js", "Создай файл JavaScript с именем"),
            ("🌐 HTML", ".html", "Создай HTML файл с именем"),
            ("🎨 CSS", ".css", "Создай CSS файл с именем"),
            ("🗄️ SQL", ".sql", "Создай SQL файл с именем"),
            ("📦 JSON", ".json", "Создай JSON файл с именем"),
            ("📝 Text", ".txt", "Создай текстовый файл с именем"),
            ("📘 Markdown", ".md", "Создай Markdown файл с именем"),
        ]
        
        row, col = 0, 0
        for i, (label, ext, prompt) in enumerate(formats):
            btn = QPushButton(label)
            btn.setProperty("ext", ext)
            btn.setProperty("prompt", prompt)
            btn.setCheckable(True)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #3d3d3d;
                    color: white;
                    border: 1px solid #555555;
                    border-radius: 3px;
                    padding: 8px;
                    font-size: 11px;
                    min-width: 100px;
                }
                QPushButton:hover {
                    background-color: #4d4d4d;
                    border-color: #0d7377;
                }
                QPushButton:checked {
                    background-color: #0d7377;
                    border-color: #0d7377;
                }
            """)
            btn.clicked.connect(lambda checked, b=btn, p=prompt, e=ext: self.on_format_selected(b, p, e))
            formats_layout.addWidget(btn, row, col)
            self.format_buttons.append(btn)
            
            col += 1
            if col > 3:
                col = 0
                row += 1
        
        formats_group.setLayout(formats_layout)
        layout.addWidget(formats_group)
        
        # Поле ввода
        self.prompt_edit = QTextEdit()
        self.prompt_edit.setPlaceholderText("Введите текст пред промпта...")
        self.prompt_edit.setPlainText(current_pre_prompt)
        self.prompt_edit.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                border: 1px solid #555555;
                border-radius: 3px;
                font-family: 'Consolas', monospace;
                font-size: 11pt;
                min-height: 150px;
            }
        """)
        layout.addWidget(self.prompt_edit)
        
        # Кнопки
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | 
            QDialogButtonBox.StandardButton.Cancel
        )
        button_box.button(QDialogButtonBox.StandardButton.Save).setText("Сохранить")
        button_box.button(QDialogButtonBox.StandardButton.Cancel).setText("Отмена")
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
        self.setLayout(layout)
    
    def on_format_selected(self, button: QPushButton, prompt: str, ext: str):
        """Обработчик выбора формата файла"""
        # Снимаем выделение с других кнопок
        for btn in self.format_buttons:
            if btn != button:
                btn.setChecked(False)
        
        # Добавляем текст в поле ввода
        current_text = self.prompt_edit.toPlainText()
        new_text = f"{prompt} [имя_файла{ext}]\n\n"
        
        if button.isChecked():
            if current_text:
                self.prompt_edit.setPlainText(current_text + "\n" + new_text)
            else:
                self.prompt_edit.setPlainText(new_text)
        else:
            # Если кнопка снята, ничего не делаем
            pass
    
    def get_pre_prompt(self) -> str:
        """Возвращает введенный пред промпт"""
        return self.prompt_edit.toPlainText().strip()


class CodeParser(QObject):
    """Парсер кода для обнаружения файловых блоков"""
    
    def __init__(self, logger: Logger):
        super().__init__()
        self.logger = logger
        self.project_path = Path("projects/current")
        self.project_path.mkdir(parents=True, exist_ok=True)
        
        # Паттерны для поиска имени файла в разных форматах
        self.file_patterns = [
            r'file:\s*([\w\/\\\-\.]+\.\w+)',  # file: main.py
            r'файл:\s*([\w\/\\\-\.]+\.\w+)',  # файл: main.py
            r'\/\/\s*file:\s*([\w\/\\\-\.]+\.\w+)',  # // file: app.js
            r'--\s*file:\s*([\w\/\\\-\.]+\.\w+)',  # -- file: database.sql
            r'#\s*file:\s*([\w\/\\\-\.]+\.\w+)',  # # file: config.py
            r'/\*\s*file:\s*([\w\/\\\-\.]+\.\w+)\s*\*/',  # /* file: styles.css */
        ]
        
        # Паттерн для поиска кодовых блоков
        self.code_block_pattern = r'```(\w*)\n(.*?)```'
        
    def parse_content(self, html_content: str) -> List[Tuple[str, str]]:
        """
        Анализирует HTML-контент страницы и извлекает кодовые блоки с именами файлов
        Возвращает список кортежей (имя_файла, содержимое_кода)
        """
        results = []
        
        # Декодируем HTML сущности
        text_content = html.unescape(html_content)
        
        # Извлекаем все кодовые блоки
        code_blocks = re.findall(self.code_block_pattern, text_content, re.DOTALL | re.IGNORECASE)
        
        for lang, code in code_blocks:
            code = code.strip()
            if not code:
                continue
                
            # Ищем имя файла в коде или в комментариях перед блоком
            filename = self._extract_filename(code)
            
            if filename:
                # Очищаем код от строки с именем файла
                clean_code = self._remove_filename_line(code, filename)
                results.append((filename, clean_code))
                self.logger.info(f"Обнаружен файл: {filename}")
            else:
                # Если имя файла не найдено, используем имя по умолчанию
                default_name = self._get_default_filename(lang)
                if default_name:
                    results.append((default_name, code))
                    self.logger.info(f"Создан файл по умолчанию: {default_name}")
                    
        return results
    
    def _extract_filename(self, code: str) -> Optional[str]:
        """Извлекает имя файла из кода"""
        # Проверяем первые несколько строк на наличие имени файла
        lines = code.split('\n')[:5]
        
        for line in lines:
            line = line.strip()
            for pattern in self.file_patterns:
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    return match.group(1).strip()
        return None
    
    def _remove_filename_line(self, code: str, filename: str) -> str:
        """Удаляет строку с именем файла из кода"""
        lines = code.split('\n')
        
        # Удаляем строки, содержащие имя файла
        cleaned_lines = []
        for line in lines:
            # Проверяем содержит ли строка имя файла и индикатор файла
            if filename in line and any(indicator in line.lower() for indicator in ['file:', 'файл:', '//', '--', '#', '/*']):
                continue
            cleaned_lines.append(line)
                
        return '\n'.join(cleaned_lines)
    
    def _get_default_filename(self, language: str) -> str:
        """Возвращает имя файла по умолчанию для языка"""
        defaults = {
            'python': 'main.py',
            'javascript': 'script.js',
            'html': 'index.html',
            'css': 'styles.css',
            'sql': 'query.sql',
            'json': 'data.json',
            '': 'code.txt'
        }
        return defaults.get(language.lower(), 'code.txt')
    
    def save_file(self, filename: str, content: str) -> bool:
        """Сохраняет файл в папку проекта"""
        try:
            filepath = self.project_path / filename
            
            # Создаем поддиректории если нужно
            filepath.parent.mkdir(parents=True, exist_ok=True)
            
            # Проверяем существование файла
            if filepath.exists():
                # Читаем существующий контент
                existing_content = filepath.read_text(encoding='utf-8')
                if existing_content != content:
                    filepath.write_text(content, encoding='utf-8')
                    self.logger.info(f"Файл обновлён: {filename}")
                    return True
                else:
                    self.logger.warning(f"Файл уже существует и не изменился: {filename}")
                    return False
            else:
                filepath.write_text(content, encoding='utf-8')
                self.logger.info(f"Создан файл: {filename}")
                return True
                
        except Exception as e:
            self.logger.error(f"Ошибка при сохранении файла {filename}: {str(e)}")
            return False


class FileManager(QObject):
    """Менеджер файлов проекта"""
    file_saved = Signal(str)
    file_updated = Signal(str)
    file_deleted = Signal(str)
    file_created = Signal(str)
    file_renamed = Signal(str, str)
    
    def __init__(self, logger: Logger):
        super().__init__()
        self.logger = logger
        self.project_path = Path("projects/current")
        self.project_path.mkdir(parents=True, exist_ok=True)
        
    def get_project_files(self) -> List[Path]:
        """Возвращает список всех файлов в проекте"""
        if not self.project_path.exists():
            return []
        return list(self.project_path.rglob('*'))
    
    def read_file(self, filepath: Path) -> str:
        """Читает содержимое файла"""
        try:
            if filepath.is_file():
                return filepath.read_text(encoding='utf-8')
        except Exception as e:
            self.logger.error(f"Ошибка чтения файла {filepath}: {str(e)}")
        return ""
    
    def delete_file(self, filepath: Path) -> bool:
        """Удаляет файл"""
        try:
            if filepath.is_file():
                filepath.unlink()
                self.logger.info(f"Файл удалён: {filepath.name}")
                self.file_deleted.emit(filepath.name)
                return True
            elif filepath.is_dir():
                # Удаляем папку со всем содержимым
                shutil.rmtree(filepath)
                self.logger.info(f"Папка удалена: {filepath.name}")
                self.file_deleted.emit(filepath.name)
                return True
        except Exception as e:
            self.logger.error(f"Ошибка удаления файла {filepath}: {str(e)}")
        return False
    
    def create_file(self, filename: str, content: str = "") -> bool:
        """Создает новый файл"""
        try:
            filepath = self.project_path / filename
            filepath.parent.mkdir(parents=True, exist_ok=True)
            
            if filepath.exists():
                self.logger.warning(f"Файл уже существует: {filename}")
                return False
            else:
                filepath.write_text(content, encoding='utf-8')
                self.logger.info(f"Создан новый файл: {filename}")
                self.file_created.emit(filename)
                return True
        except Exception as e:
            self.logger.error(f"Ошибка создания файла {filename}: {str(e)}")
            return False
    
    def create_folder(self, foldername: str) -> bool:
        """Создает новую папку"""
        try:
            folderpath = self.project_path / foldername
            folderpath.mkdir(parents=True, exist_ok=True)
            self.logger.info(f"Создана новая папка: {foldername}")
            return True
        except Exception as e:
            self.logger.error(f"Ошибка создания папки {foldername}: {str(e)}")
            return False
    
    def rename_file(self, old_path: Path, new_name: str) -> bool:
        """Переименовывает файл или папку"""
        try:
            new_path = old_path.parent / new_name
            old_path.rename(new_path)
            self.logger.info(f"Переименован: {old_path.name} -> {new_name}")
            self.file_renamed.emit(old_path.name, new_name)
            return True
        except Exception as e:
            self.logger.error(f"Ошибка переименования: {str(e)}")
            return False
    
    def duplicate_file(self, filepath: Path) -> bool:
        """Создает копию файла"""
        try:
            if filepath.is_file():
                stem = filepath.stem
                suffix = filepath.suffix
                new_name = f"{stem}_копия{suffix}"
                new_path = filepath.parent / new_name
                
                # Если файл уже существует, добавляем номер
                counter = 1
                while new_path.exists():
                    new_name = f"{stem}_копия_{counter}{suffix}"
                    new_path = filepath.parent / new_name
                    counter += 1
                
                shutil.copy2(filepath, new_path)
                self.logger.info(f"Создана копия: {new_name}")
                self.file_created.emit(new_name)
                return True
        except Exception as e:
            self.logger.error(f"Ошибка создания копии: {str(e)}")
            return False


class BrowserPanel(QWidget):
    """Панель браузера с элементами управления"""
    
    def __init__(self, logger: Logger, parent=None):
        super().__init__(parent)
        self.logger = logger
        self.setup_ui()
        
    def setup_ui(self):
        """Настройка интерфейса панели браузера"""
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Панель инструментов браузера
        toolbar = QToolBar()
        toolbar.setStyleSheet("""
            QToolBar {
                background-color: #2d2d2d;
                border: none;
                border-bottom: 1px solid #555555;
                padding: 5px;
                spacing: 5px;
            }
        """)
        
        # Кнопки навигации
        self.back_btn = QPushButton("←")
        self.forward_btn = QPushButton("→")
        self.refresh_btn = QPushButton("↻")
        self.zoom_in_btn = QPushButton("+")
        self.zoom_out_btn = QPushButton("-")
        self.home_btn = QPushButton("🏠")
        
        # Добавляем подписи для кнопок
        self.back_btn.setToolTip("Назад")
        self.forward_btn.setToolTip("Вперёд")
        self.refresh_btn.setToolTip("Обновить")
        self.zoom_in_btn.setToolTip("Увеличить масштаб")
        self.zoom_out_btn.setToolTip("Уменьшить масштаб")
        self.home_btn.setToolTip("DeepSeek")
        
        # Стилизация кнопок
        button_style = """
            QPushButton {
                background-color: #3d3d3d;
                color: white;
                border: 1px solid #555555;
                border-radius: 3px;
                padding: 5px 10px;
                font-size: 12px;
                min-width: 30px;
            }
            QPushButton:hover {
                background-color: #4d4d4d;
            }
            QPushButton:pressed {
                background-color: #5d5d5d;
            }
        """
        for btn in [self.back_btn, self.forward_btn, self.refresh_btn,
                   self.zoom_in_btn, self.zoom_out_btn, self.home_btn]:
            btn.setStyleSheet(button_style)
            toolbar.addWidget(btn)
            
        layout.addWidget(toolbar)
        
        # Браузер
        self.browser = QWebEngineView()
        
        # Настройки браузера
        settings = self.browser.settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, True)
        
        # Загружаем DeepSeek
        self.browser.setUrl(QUrl("https://chat.deepseek.com"))
        
        # Подключаем сигналы
        self.back_btn.clicked.connect(self.browser.back)
        self.forward_btn.clicked.connect(self.browser.forward)
        self.refresh_btn.clicked.connect(self.browser.reload)
        self.zoom_in_btn.clicked.connect(lambda: self.browser.setZoomFactor(self.browser.zoomFactor() + 0.1))
        self.zoom_out_btn.clicked.connect(lambda: self.browser.setZoomFactor(max(0.1, self.browser.zoomFactor() - 0.1)))
        self.home_btn.clicked.connect(lambda: self.browser.setUrl(QUrl("https://chat.deepseek.com")))
        
        # Подключаем сигнал загрузки страницы
        self.browser.loadFinished.connect(self.on_page_loaded)
        
        layout.addWidget(self.browser)
        self.setLayout(layout)
        
    def on_page_loaded(self, ok: bool):
        """Обработчик завершения загрузки страницы"""
        if ok:
            self.logger.info("Страница DeepSeek загружена")
        else:
            self.logger.error("Ошибка загрузки страницы DeepSeek")
        
    def get_page_content(self, callback):
        """Получает HTML-содержимое текущей страницы через callback"""
        self.browser.page().toHtml(callback)
        
    def inject_pre_prompt(self, pre_prompt: str, user_message: str):
        """Внедряет пред промпт в сообщение пользователя"""
        if pre_prompt:
            final_message = f"{pre_prompt}\n\n{user_message}"
            # Здесь должен быть код для внедрения в поле ввода DeepSeek
            # Это сложная часть, требующая JavaScript инъекции
            js_code = f"""
            (function() {{
                const textarea = document.querySelector('textarea[placeholder*="сообщение"]') || 
                                 document.querySelector('textarea');
                if (textarea) {{
                    textarea.value = `{final_message}`;
                    textarea.dispatchEvent(new Event('input', {{ bubbles: true }}));
                }}
            }})();
            """
            self.browser.page().runJavaScript(js_code)


class LogPanel(QPlainTextEdit):
    """Панель отображения логов"""
    
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)
        self.setMaximumBlockCount(1000)
        self.setStyleSheet("""
            QPlainTextEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 10pt;
                border: 1px solid #555555;
                border-radius: 3px;
            }
        """)
        
    def add_log(self, message: str):
        """Добавляет сообщение в лог"""
        self.appendPlainText(message)
        # Автопрокрутка
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.setTextCursor(cursor)


class FilePreviewPanel(QTextEdit):
    """Панель предпросмотра файлов"""
    
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)
        self.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 11pt;
                border: 1px solid #555555;
                border-radius: 3px;
            }
        """)
        
        self.current_file = None
        
    def show_file_content(self, content: str, filename: str = ""):
        """Отображает содержимое файла"""
        self.current_file = filename
        if filename:
            header = f"// Файл: {filename}\n// Размер: {len(content)} символов\n// {'=' * 50}\n\n"
            self.setPlainText(header + content)
        else:
            self.clear()
            self.setPlainText("// Выберите файл для просмотра")


class ProjectTreeView(QTreeView):
    """Дерево файлов проекта с контекстным меню"""
    
    def __init__(self, file_manager: FileManager, logger: Logger, parent=None):
        super().__init__(parent)
        self.file_manager = file_manager
        self.logger = logger
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
        
    def show_context_menu(self, position: QPoint):
        """Показывает контекстное меню"""
        index = self.indexAt(position)
        
        menu = QMenu()
        
        if index.isValid():
            # Контекстное меню для выбранного элемента
            filepath = self.model().filePath(index)
            path = Path(filepath)
            
            if path.is_file():
                # Меню для файла
                open_action = menu.addAction("📂 Открыть файл")
                open_action.triggered.connect(lambda: self.open_file(path))
                
                menu.addSeparator()
                
                rename_action = menu.addAction("✏️ Переименовать")
                rename_action.triggered.connect(lambda: self.rename_file(index, path))
                
                duplicate_action = menu.addAction("📄 Создать копию")
                duplicate_action.triggered.connect(lambda: self.duplicate_file(path))
                
                delete_action = menu.addAction("🗑️ Удалить файл")
                delete_action.triggered.connect(lambda: self.delete_file(path))
                
                menu.addSeparator()
                
                copy_name_action = menu.addAction("📋 Копировать имя")
                copy_name_action.triggered.connect(lambda: self.copy_name(path))
                
                copy_path_action = menu.addAction("📋 Копировать путь")
                copy_path_action.triggered.connect(lambda: self.copy_path(path))
                
            else:
                # Меню для папки
                open_action = menu.addAction("📂 Открыть папку")
                open_action.triggered.connect(lambda: self.open_folder(path))
                
                menu.addSeparator()
                
                rename_action = menu.addAction("✏️ Переименовать папку")
                rename_action.triggered.connect(lambda: self.rename_file(index, path))
                
                delete_action = menu.addAction("🗑️ Удалить папку")
                delete_action.triggered.connect(lambda: self.delete_file(path))
                
                menu.addSeparator()
                
                new_file_action = menu.addAction("📄 Новый файл в папке")
                new_file_action.triggered.connect(lambda: self.create_file_in_folder(path))
                
                new_folder_action = menu.addAction("📁 Новая подпапка")
                new_folder_action.triggered.connect(lambda: self.create_subfolder(path))
        else:
            # Контекстное меню для пустой области
            new_file_action = menu.addAction("📄 Создать новый файл")
            new_file_action.triggered.connect(self.create_new_file)
            
            new_folder_action = menu.addAction("📁 Создать новую папку")
            new_folder_action.triggered.connect(self.create_new_folder)
            
            menu.addSeparator()
            
            import_file_action = menu.addAction("📂 Импортировать файл")
            import_file_action.triggered.connect(self.import_file)
            
            refresh_action = menu.addAction("🔄 Обновить")
            refresh_action.triggered.connect(self.refresh)
        
        menu.exec(QCursor.pos())
    
    def open_file(self, path: Path):
        """Открывает файл в системе"""
        try:
            os.startfile(str(path))
        except Exception as e:
            self.logger.error(f"Не удалось открыть файл: {str(e)}")
    
    def open_folder(self, path: Path):
        """Открывает папку в проводнике"""
        try:
            os.startfile(str(path))
        except Exception as e:
            self.logger.error(f"Не удалось открыть папку: {str(e)}")
    
    def delete_file(self, path: Path):
        """Удаляет файл с подтверждением"""
        reply = QMessageBox.question(
            self, 
            "Подтверждение удаления",
            f"Вы уверены, что хотите удалить '{path.name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            if self.file_manager.delete_file(path):
                self.refresh()
    
    def rename_file(self, index, path: Path):
        """Переименовывает файл"""
        new_name, ok = QInputDialog.getText(
            self, 
            "Переименование",
            "Введите новое имя:",
            QLineEdit.EchoMode.Normal,
            path.name
        )
        
        if ok and new_name and new_name != path.name:
            if self.file_manager.rename_file(path, new_name):
                self.refresh()
    
    def duplicate_file(self, path: Path):
        """Создает копию файла"""
        if self.file_manager.duplicate_file(path):
            self.refresh()
    
    def copy_name(self, path: Path):
        """Копирует имя файла в буфер обмена"""
        clipboard = QApplication.clipboard()
        clipboard.setText(path.name)
        self.logger.info(f"Имя скопировано: {path.name}")
    
    def copy_path(self, path: Path):
        """Копирует путь к файлу в буфер обмена"""
        clipboard = QApplication.clipboard()
        clipboard.setText(str(path.absolute()))
        self.logger.info(f"Путь скопирован: {path.absolute()}")
    
    def create_new_file(self):
        """Создает новый файл в корне проекта"""
        filename, ok = QInputDialog.getText(
            self, 
            "Создание файла",
            "Введите имя файла (с расширением):",
            QLineEdit.EchoMode.Normal,
            "новый_файл.txt"
        )
        
        if ok and filename:
            content, ok = QInputDialog.getMultiLineText(
                self,
                "Содержимое файла",
                "Введите содержимое файла (необязательно):"
            )
            
            if self.file_manager.create_file(filename, content if content else ""):
                self.refresh()
    
    def create_new_folder(self):
        """Создает новую папку в корне проекта"""
        foldername, ok = QInputDialog.getText(
            self, 
            "Создание папки",
            "Введите имя папки:",
            QLineEdit.EchoMode.Normal,
            "новая_папка"
        )
        
        if ok and foldername:
            if self.file_manager.create_folder(foldername):
                self.refresh()
    
    def create_file_in_folder(self, folder_path: Path):
        """Создает новый файл в указанной папке"""
        filename, ok = QInputDialog.getText(
            self, 
            "Создание файла",
            f"Введите имя файла в папке {folder_path.name}:",
            QLineEdit.EchoMode.Normal,
            "новый_файл.txt"
        )
        
        if ok and filename:
            filepath = folder_path / filename
            if self.file_manager.create_file(str(filepath.relative_to(self.file_manager.project_path)), ""):
                self.refresh()
    
    def create_subfolder(self, parent_path: Path):
        """Создает подпапку в указанной папке"""
        foldername, ok = QInputDialog.getText(
            self, 
            "Создание подпапки",
            f"Введите имя подпапки в {parent_path.name}:",
            QLineEdit.EchoMode.Normal,
            "новая_папка"
        )
        
        if ok and foldername:
            folderpath = parent_path / foldername
            folderpath.mkdir(parents=True, exist_ok=True)
            self.logger.info(f"Создана подпапка: {foldername}")
            self.refresh()
    
    def import_file(self):
        """Импортирует файл из файловой системы"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите файл для импорта",
            "",
            "Все файлы (*.*)"
        )
        
        if file_path:
            source = Path(file_path)
            dest = self.file_manager.project_path / source.name
            
            # Проверяем, существует ли уже файл
            if dest.exists():
                reply = QMessageBox.question(
                    self,
                    "Файл уже существует",
                    f"Файл {source.name} уже существует. Перезаписать?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )
                if reply != QMessageBox.StandardButton.Yes:
                    return
            
            # Копируем файл
            shutil.copy2(source, dest)
            self.logger.info(f"Файл импортирован: {source.name}")
            self.refresh()
    
    def refresh(self):
        """Обновляет дерево файлов"""
        self.parent().update_file_tree()


class ProjectPanel(QWidget):
    """Панель проекта с деревом файлов и предпросмотром"""
    
    def __init__(self, file_manager: FileManager, logger: Logger):
        super().__init__()
        self.file_manager = file_manager
        self.logger = logger
        self.setup_ui()
        
        # Подключаем сигналы
        self.file_manager.file_deleted.connect(self.on_file_changed)
        self.file_manager.file_created.connect(self.on_file_changed)
        self.file_manager.file_renamed.connect(self.on_file_renamed)
        
    def setup_ui(self):
        """Настройка интерфейса панели проекта"""
        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(10)
        
        # Заголовок "Файлы проекта" с кнопками
        header_layout = QHBoxLayout()
        
        title_label = QLabel("📁 Файлы проекта")
        title_font = QFont()
        title_font.setBold(True)
        title_font.setPointSize(11)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: white; padding: 5px;")
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        # Кнопки управления файлами
        self.new_file_btn = QPushButton("📄 Новый файл")
        self.new_file_btn.setToolTip("Создать новый файл")
        self.new_file_btn.setStyleSheet("""
            QPushButton {
                background-color: #3d3d3d;
                color: white;
                border: 1px solid #555555;
                border-radius: 3px;
                padding: 5px 10px;
                font-size: 10px;
            }
            QPushButton:hover {
                background-color: #4d4d4d;
            }
        """)
        
        self.new_folder_btn = QPushButton("📁 Новая папка")
        self.new_folder_btn.setToolTip("Создать новую папку")
        self.new_folder_btn.setStyleSheet("""
            QPushButton {
                background-color: #3d3d3d;
                color: white;
                border: 1px solid #555555;
                border-radius: 3px;
                padding: 5px 10px;
                font-size: 10px;
            }
            QPushButton:hover {
                background-color: #4d4d4d;
            }
        """)
        
        self.import_btn = QPushButton("📂 Импорт")
        self.import_btn.setToolTip("Импортировать файл")
        self.import_btn.setStyleSheet("""
            QPushButton {
                background-color: #3d3d3d;
                color: white;
                border: 1px solid #555555;
                border-radius: 3px;
                padding: 5px 10px;
                font-size: 10px;
            }
            QPushButton:hover {
                background-color: #4d4d4d;
            }
        """)
        
        header_layout.addWidget(self.new_file_btn)
        header_layout.addWidget(self.new_folder_btn)
        header_layout.addWidget(self.import_btn)
        
        layout.addLayout(header_layout)
        
        # Дерево файлов с контекстным меню
        self.tree_view = ProjectTreeView(self.file_manager, self.logger, self)
        self.tree_view.setStyleSheet("""
            QTreeView {
                background-color: #2d2d2d;
                color: white;
                border: 1px solid #555555;
                border-radius: 3px;
            }
            QTreeView::item {
                padding: 3px;
            }
            QTreeView::item:hover {
                background-color: #3d3d3d;
            }
            QTreeView::item:selected {
                background-color: #0d7377;
            }
        """)
        
        self.model = QFileSystemModel()
        self.model.setRootPath(str(self.file_manager.project_path))
        self.tree_view.setModel(self.model)
        self.tree_view.setRootIndex(self.model.index(str(self.file_manager.project_path)))
        self.tree_view.setColumnHidden(1, True)  # Скрыть колонку размера
        self.tree_view.setColumnHidden(2, True)  # Скрыть колонку типа
        self.tree_view.setColumnWidth(0, 200)    # Ширина колонки имени
        
        layout.addWidget(self.tree_view)
        
        # Разделитель
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("background-color: #555555; max-height: 1px;")
        layout.addWidget(line)
        
        # Заголовок "Просмотр файла"
        preview_label = QLabel("👁️ Просмотр файла")
        preview_label.setFont(title_font)
        preview_label.setStyleSheet("color: white; padding: 5px;")
        layout.addWidget(preview_label)
        
        # Панель предпросмотра
        self.preview = FilePreviewPanel()
        layout.addWidget(self.preview)
        
        # Разделитель
        line2 = QFrame()
        line2.setFrameShape(QFrame.Shape.HLine)
        line2.setStyleSheet("background-color: #555555; max-height: 1px;")
        layout.addWidget(line2)
        
        # Заголовок "Лог системы"
        log_label = QLabel("📋 Лог системы")
        log_label.setFont(title_font)
        log_label.setStyleSheet("color: white; padding: 5px;")
        layout.addWidget(log_label)
        
        # Панель логов
        self.log_panel = LogPanel()
        layout.addWidget(self.log_panel)
        
        self.setLayout(layout)
        
        # Подключаем сигналы
        self.tree_view.clicked.connect(self.on_file_selected)
        self.new_file_btn.clicked.connect(self.on_new_file)
        self.new_folder_btn.clicked.connect(self.on_new_folder)
        self.import_btn.clicked.connect(self.on_import_file)
        
    def on_file_selected(self, index):
        """Обработчик выбора файла в дереве"""
        filepath = self.model.filePath(index)
        if os.path.isfile(filepath):
            content = self.file_manager.read_file(Path(filepath))
            filename = os.path.basename(filepath)
            self.preview.show_file_content(content, filename)
            
    def update_file_tree(self):
        """Обновляет дерево файлов"""
        self.model.setRootPath(str(self.file_manager.project_path))
        self.tree_view.setRootIndex(self.model.index(str(self.file_manager.project_path)))
        
    def on_file_changed(self, filename):
        """Обработчик изменения файлов"""
        self.update_file_tree()
        
    def on_file_renamed(self, old_name, new_name):
        """Обработчик переименования файла"""
        self.update_file_tree()
        self.logger.info(f"Файл переименован: {old_name} -> {new_name}")
        
    def on_new_file(self):
        """Обработчик кнопки создания нового файла"""
        self.tree_view.create_new_file()
        
    def on_new_folder(self):
        """Обработчик кнопки создания новой папки"""
        self.tree_view.create_new_folder()
        
    def on_import_file(self):
        """Обработчик кнопки импорта файла"""
        self.tree_view.import_file()


class MainWindow(QMainWindow):
    """Главное окно приложения"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("koderDeepS Desktop - AI IDE для DeepSeek")
        self.setGeometry(100, 100, 1400, 900)
        
        # Устанавливаем иконку для главного окна
        icon_path = Path("koderDeepS-Desktop.ico")
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))
        
        # Загружаем пред промпт из конфига
        self.pre_prompt = self.load_pre_prompt()
        
        # Устанавливаем темный фон для главного окна
        self.setStyleSheet("""
            QMainWindow {
                background-color: #353535;
            }
            QStatusBar {
                background-color: #2d2d2d;
                color: white;
                border-top: 1px solid #555555;
            }
            QMenuBar {
                background-color: #2d2d2d;
                color: white;
                border-bottom: 1px solid #555555;
            }
            QMenuBar::item {
                background-color: #2d2d2d;
                color: white;
                padding: 5px 10px;
            }
            QMenuBar::item:selected {
                background-color: #3d3d3d;
            }
            QMenu {
                background-color: #2d2d2d;
                color: white;
                border: 1px solid #555555;
            }
            QMenu::item {
                padding: 5px 20px;
            }
            QMenu::item:selected {
                background-color: #3d3d3d;
            }
            QMenu::separator {
                background-color: #555555;
                height: 1px;
                margin: 5px 0px;
            }
        """)
        
        # Инициализация компонентов
        self.logger = Logger()
        self.file_manager = FileManager(self.logger)
        self.code_parser = CodeParser(self.logger)
        
        # Настройка интерфейса
        self.setup_menu()
        self.setup_ui()
        self.setup_connections()
        
        # Таймер для периодической проверки кода
        self.scan_timer = QTimer()
        self.scan_timer.timeout.connect(self.scan_for_code)
        self.scan_timer.start(3000)  # Проверка каждые 3 секунды
        
        # Кэш последнего сканирования
        self.last_content = ""
        
        self.logger.info("=" * 50)
        self.logger.info("Программа запущена")
        if self.pre_prompt:
            self.logger.info(f"Пред промпт загружен: {self.pre_prompt[:50]}...")
        self.logger.info(f"Папка проекта: {self.file_manager.project_path.absolute()}")
        self.logger.info("=" * 50)
        
    def load_pre_prompt(self) -> str:
        """Загружает пред промпт из config.json"""
        config_path = Path("config.json")
        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    return config.get("pre_prompt", "")
            except Exception as e:
                print(f"Ошибка загрузки config.json: {e}")
        return ""
    
    def save_pre_prompt(self, pre_prompt: str):
        """Сохраняет пред промпт в config.json"""
        config_path = Path("config.json")
        try:
            config = {}
            if config_path.exists():
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
            
            config["pre_prompt"] = pre_prompt
            
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            
            self.pre_prompt = pre_prompt
            self.logger.info("Пред промпт сохранён")
            if pre_prompt:
                self.logger.info(f"Текст: {pre_prompt[:50]}...")
                
            # Обновляем статус бар
            if pre_prompt:
                self.pre_prompt_label.setText("🤖 Пред промпт активен")
            else:
                self.pre_prompt_label.setText("🤖 Пред промпт не задан")
                
        except Exception as e:
            self.logger.error(f"Ошибка сохранения config.json: {e}")
    
    def show_pre_prompt_dialog(self):
        """Показывает диалог настройки пред промпта"""
        dialog = PrePromptDialog(self.pre_prompt, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_pre_prompt = dialog.get_pre_prompt()
            self.save_pre_prompt(new_pre_prompt)
            
    def setup_menu(self):
        """Настройка меню приложения"""
        menubar = self.menuBar()
        
        # Меню Файл
        file_menu = menubar.addMenu("Файл")
        
        new_file_action = QAction("📄 Новый файл", self)
        new_file_action.triggered.connect(lambda: self.project_panel.on_new_file())
        file_menu.addAction(new_file_action)
        
        new_folder_action = QAction("📁 Новая папка", self)
        new_folder_action.triggered.connect(lambda: self.project_panel.on_new_folder())
        file_menu.addAction(new_folder_action)
        
        import_action = QAction("📂 Импортировать файл", self)
        import_action.triggered.connect(lambda: self.project_panel.on_import_file())
        file_menu.addAction(import_action)
        
        file_menu.addSeparator()
        
        open_project_action = QAction("📂 Открыть папку проекта", self)
        open_project_action.triggered.connect(self.open_project_folder)
        file_menu.addAction(open_project_action)
        
        refresh_action = QAction("🔄 Обновить файлы", self)
        refresh_action.triggered.connect(self.refresh_files)
        file_menu.addAction(refresh_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("❌ Выход", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Меню Инструменты
        tools_menu = menubar.addMenu("Инструменты")
        
        pre_prompt_action = QAction("🤖 Пред промпт", self)
        pre_prompt_action.triggered.connect(self.show_pre_prompt_dialog)
        tools_menu.addAction(pre_prompt_action)
        
        # Меню Вид
        view_menu = menubar.addMenu("Вид")
        
        zoom_in_action = QAction("➕ Увеличить", self)
        zoom_in_action.triggered.connect(self.zoom_in)
        view_menu.addAction(zoom_in_action)
        
        zoom_out_action = QAction("➖ Уменьшить", self)
        zoom_out_action.triggered.connect(self.zoom_out)
        view_menu.addAction(zoom_out_action)
        
        # Меню Помощь
        help_menu = menubar.addMenu("Помощь")
        
        about_action = QAction("ℹ️ О программе", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
    def setup_ui(self):
        """Настройка основного интерфейса"""
        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Главный layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(5)
        
        # Левая панель (браузер)
        self.browser_panel = BrowserPanel(self.logger, self)
        
        # Правая панель (проект)
        self.project_panel = ProjectPanel(self.file_manager, self.logger)
        
        # Создаем сплиттер для разделения окна
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setStyleSheet("""
            QSplitter::handle {
                background-color: #555555;
                width: 2px;
            }
            QSplitter::handle:hover {
                background-color: #666666;
            }
        """)
        
        splitter.addWidget(self.browser_panel)
        splitter.addWidget(self.project_panel)
        
        # Устанавливаем пропорции
        total_width = self.width()
        splitter.setSizes([int(total_width * 0.67), int(total_width * 0.33)])
        
        main_layout.addWidget(splitter)
        
        # Статус бар
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Готов к работе")
        
        # Добавляем информацию о проекте в статус бар
        self.project_label = QLabel(f"📁 {self.file_manager.project_path.name}")
        self.status_bar.addPermanentWidget(self.project_label)
        
        # Добавляем информацию о пред промпте в статус бар
        if self.pre_prompt:
            self.pre_prompt_label = QLabel("🤖 Пред промпт активен")
        else:
            self.pre_prompt_label = QLabel("🤖 Пред промпт не задан")
        self.pre_prompt_label.setStyleSheet("color: #0d7377;")
        self.status_bar.addPermanentWidget(self.pre_prompt_label)
        
        # Подключаем логгер к панели логов
        self.logger.log_updated.connect(self.project_panel.log_panel.add_log)
        
    def setup_connections(self):
        """Настройка соединений сигналов и слотов"""
        pass
        
    def scan_for_code(self):
        """Сканирует страницу на наличие кодовых блоков"""
        self.browser_panel.get_page_content(self.process_page_content)
        
    def process_page_content(self, content: str):
        """Обрабатывает HTML-контент страницы"""
        if not content or content == self.last_content:
            return
            
        self.last_content = content
        files_to_save = self.code_parser.parse_content(content)
        
        files_saved = 0
        for filename, code_content in files_to_save:
            if self.code_parser.save_file(filename, code_content):
                files_saved += 1
                
        if files_saved > 0:
            self.project_panel.update_file_tree()
            self.status_bar.showMessage(f"💾 Сохранено файлов: {files_saved}", 3000)
                
    def open_project_folder(self):
        """Открывает папку проекта в проводнике"""
        try:
            project_path = str(self.file_manager.project_path.absolute())
            if sys.platform == "win32":
                os.startfile(project_path)
            elif sys.platform == "darwin":
                subprocess.run(["open", project_path])
            else:
                subprocess.run(["xdg-open", project_path])
            self.logger.info(f"Открыта папка проекта: {project_path}")
        except Exception as e:
            self.logger.error(f"Не удалось открыть папку проекта: {str(e)}")
            
    def refresh_files(self):
        """Обновляет список файлов"""
        self.project_panel.update_file_tree()
        self.logger.info("Список файлов обновлён")
        
    def zoom_in(self):
        """Увеличивает масштаб"""
        current_zoom = self.browser_panel.browser.zoomFactor()
        self.browser_panel.browser.setZoomFactor(current_zoom + 0.1)
        self.logger.info(f"Масштаб: {int(current_zoom * 100 + 10)}%")
        
    def zoom_out(self):
        """Уменьшает масштаб"""
        current_zoom = self.browser_panel.browser.zoomFactor()
        new_zoom = max(0.1, current_zoom - 0.1)
        self.browser_panel.browser.setZoomFactor(new_zoom)
        self.logger.info(f"Масштаб: {int(new_zoom * 100)}%")
        
    def show_about(self):
        """Показывает окно 'О программе'"""
        QMessageBox.about(
            self,
            "О программе koderDeepS Desktop",
            f"<h2 style='color: #0d7377;'>koderDeepS Desktop v2.0</h2>"
            f"<p>Специализированная AI-IDE программа для работы с сайтом DeepSeek</p>"
            f"<p><b style='color: #0d7377;'>Возможности:</b></p>"
            f"<ul>"
            f"<li>Встроенный браузер DeepSeek</li>"
            f"<li>Автоматическое создание файлов из кода</li>"
            f"<li>Управление файлами проекта</li>"
            f"<li>Контекстное меню для файлов</li>"
            f"<li>Создание и импорт файлов</li>"
            f"<li>Система логирования</li>"
            f"<li>Пред промпт с кнопками форматов файлов</li>"
            f"</ul>"
            f"<p><b style='color: #0d7377;'>Технологии:</b> Python 3.13, PySide6 {PYSIDE_VERSION}</p>"
            f"<p><b style='color: #0d7377;'>Папка проекта:</b> projects/current/</p>"
        )
        
    def resizeEvent(self, event):
        """Обработчик изменения размера окна"""
        super().resizeEvent(event)
        # Обновляем пропорции сплиттера при изменении размера окна
        if hasattr(self, 'browser_panel') and hasattr(self, 'project_panel'):
            splitter = self.centralWidget().findChild(QSplitter)
            if splitter:
                total_width = self.width()
                splitter.setSizes([int(total_width * 0.67), int(total_width * 0.33)])
        
    def closeEvent(self, event):
        """Обработчик закрытия окна"""
        self.logger.info("=" * 50)
        self.logger.info("Программа завершена")
        self.logger.info("=" * 50)
        event.accept()


def check_dependencies():
    """Проверяет наличие всех необходимых зависимостей"""
    try:
        import PySide6
        print(f"PySide6 версия: {PySide6.__version__}")
        
        # Проверяем возможность импорта WebEngine компонентов
        from PySide6.QtWebEngineWidgets import QWebEngineView
        from PySide6.QtWebEngineCore import QWebEngineSettings, QWebEnginePage
        print("✓ WebEngine компоненты доступны")
        return True
    except ImportError as e:
        print("\n" + "="*60)
        print("ОШИБКА: Не удалось импортировать PySide6")
        print("="*60)
        print(f"\nДетали: {e}")
        print("\nДля установки выполните команду:")
        print("  pip install PySide6")
        print("="*60)
        return False


def main():
    """Точка входа в программу"""
    # Создаем необходимые директории
    Path("projects/current").mkdir(parents=True, exist_ok=True)
    
    # Проверяем зависимости
    if not check_dependencies():
        input("\nНажмите Enter для выхода...")
        return 1
    
    # Создаем приложение
    app = QApplication(sys.argv)
    
    # Устанавливаем иконку для приложения
    icon_path = Path("koderDeepS-Desktop.ico")
    if icon_path.exists():
        app.setWindowIcon(QIcon(str(icon_path)))
    
    # Устанавливаем темную тему
    setup_dark_theme(app)
    
    # Создание главного окна
    window = MainWindow()
    window.show()
    
    # Запуск цикла обработки событий
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())