import sys
import re
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QAction, QShortcut, QMessageBox
from PyQt5.QtWidgets import QInputDialog

class CodeHighlighter:
    @staticmethod
    def highlight(code):
        # Список ключевых слов Python3
        keywords = ['False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await', 'break', 'class', 'continue',
                    'def', 'del', 'elif', 'else', 'except', 'finally', 'for', 'from', 'global', 'if', 'import',
                    'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try', 'while',
                    'with', 'yield']

        # Список встроенных функций Python3
        builtin_funcs = ['abs', 'all', 'any', 'ascii', 'bin', 'bool', 'bytearray', 'bytes', 'callable', 'chr',
                         'classmethod', 'compile', 'complex', 'delattr', 'dict', 'dir', 'divmod', 'enumerate',
                         'eval', 'exec', 'filter', 'float', 'format', 'frozenset', 'getattr', 'globals', 'hasattr',
                         'hash', 'help', 'hex', 'id', 'input', 'int', 'isinstance', 'issubclass', 'iter', 'len',
                         'list', 'locals', 'map', 'max', 'memoryview', 'min', 'next', 'object', 'oct', 'open',
                         'ord', 'pow', 'print', 'property', 'range', 'repr', 'reversed', 'round', 'set',
                         'setattr', 'slice', 'sorted', 'staticmethod', 'str', 'sum', 'super', 'tuple', 'type',
                         'vars', 'zip']

        # Стили текста
        styles = {
            'keyword': 'color: #0000FF;',  # Синий
            'builtin': 'color: #A020F0;',  # Фиолетовый
            'string': 'color: #008000;',  # Зеленый
            'comment': 'color: #808080;',  # Серый
        }

        # Регулярное выражение для поиска строковых литералов
        string_re = r'\'[^\']*\'|\"[^\"]*\"'

        # Регулярное выражение для поиска комментариев
        comment_re = r'#.*$'
        
        # Получаем список всех лексем
        all_tokens = code.split()

        # Проходимся по каждой лексеме и добавляем в ней тег <span> с нужным классом стиля
        highlighted_tokens = []
        for token in all_tokens:
            if token in keywords:
                highlighted_tokens.append('<span style="{}">{}</span>'.format(styles['keyword'], token))
            elif token in builtin_funcs:
                highlighted_tokens.append('<span style="{}">{}</span>'.format(styles['builtin'], token))
            elif token.startswith('#'):
                highlighted_tokens.append('<span style="{}">{}</span>'.format(styles['comment'], token))
            else:
                # Заменяем строковые литералы на плейсхолдеры, чтобы не выделять их дважды
                token = re.sub(string_re, '<span style="{}">\\g<0></span>'.format(styles['string']), token)
                highlighted_tokens.append(token)

        # Собираем выделенный текст с помощью тега <pre>
        highlighted_code = '<pre>{}</pre>'.format(' '.join(highlighted_tokens))

        return highlighted_code


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Code Highlighter")

        self.text_edit = QTextEdit()
        self.text_edit.setFont(QFont("Courier New", 11))
        self.setCentralWidget(self.text_edit)

        # Создание кнопки копирования
        copy_action = QAction("Копировать", self)
        copy_action.setShortcut("Ctrl+C")
        copy_action.triggered.connect(self.copy_text)

        # Добавление кнопки в меню
        menu_bar = self.menuBar()
        edit_menu = menu_bar.addMenu("Правка")
        edit_menu.addAction(copy_action)

        # Создание горячей клавиши для копирования
        copy_shortcut = QShortcut("Ctrl+C", self)
        copy_shortcut.activated.connect(self.copy_text)

    def copy_text(self):
        selected_text = self.text_edit.textCursor().selectedText()
        if selected_text != "":
            clipboard = QApplication.clipboard()
            clipboard.setText(selected_text)
        else:
            QMessageBox.warning(self, "Ошибка", "Не выделен текст для копирования.")

    def highlight_code(self):
        code = self.text_edit.toPlainText()
        highlighted_code = CodeHighlighter.highlight(code)
        self.text_edit.setHtml(highlighted_code)  # замените setPlainText на setHtml
        text_document = self.text_edit.document()  # получить объект QTextDocument
        text_document.setHtml(highlighted_code)  # задать тип контента

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    window.highlight_code()  # Вызываем метод для выделения синтаксиса кода
    sys.exit(app.exec_())
