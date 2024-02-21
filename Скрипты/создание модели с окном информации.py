import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton
from PyQt5.QtCore import QThread, pyqtSignal
from transformers import GPT2Tokenizer, GPT2Config, GPT2LMHeadModel

class ModelThread(QThread):
    update_text_signal = pyqtSignal(str)
    model_saved_signal = pyqtSignal()
    
    def run(self):
        self.update_text_signal.emit("Загружаем предварительно созданный токенизатор")
        tokenizer = GPT2Tokenizer.from_pretrained("C://gpt//token")

        self.update_text_signal.emit("Создаем конфигурацию модели с нужными параметрами")
        model_config = GPT2Config(
            vocab_size=tokenizer.vocab_size,
            n_layer=22,
            n_head=32,
            n_embd=2048,
            intermediate_size=3072,
            hidden_size=1536,
            max_position_embeddings=3072,
            num_attention_heads=32,
            gradient_checkpointing=True,
            bos_token_id=tokenizer.bos_token_id,
            eos_token_id=tokenizer.eos_token_id,
            pad_token_id=tokenizer.pad_token_id,
            sep_token_id=tokenizer.sep_token_id
        )

        self.update_text_signal.emit("Создаем модель на основе заданной конфигурации")
        model = GPT2LMHeadModel(config=model_config)
        model.set_input_embeddings(model.resize_token_embeddings(len(tokenizer)))
        self.update_text_signal.emit("Модель создана.")

        self.update_text_signal.emit("Сохраняем модель и токенизатор.")
        model.save_pretrained("C://gpt//model")
        tokenizer.save_pretrained("C://gpt//model")
        self.update_text_signal.emit("Модель и токенизатор сохранены.")
        self.model_saved_signal.emit()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Создание модель GPT")
        self.setGeometry(100, 100, 600, 200)
        
        self.text_edit = QTextEdit(self)
        self.text_edit.setGeometry(10, 10, 580, 320)
        self.text_edit.setReadOnly(True)
        
        self.exit_button = QPushButton("Выход", self)
        self.exit_button.setGeometry(10, 340, 580, 50)
        self.exit_button.setEnabled(False)
        self.exit_button.clicked.connect(self.close)
        
        self.model_thread = ModelThread()
        self.model_thread.update_text_signal.connect(self.update_text)
        self.model_thread.model_saved_signal.connect(self.enable_exit_button)
    
    def start_model_creation(self):
        self.model_thread.start()
    
    def update_text(self, text):
        self.text_edit.append(text)
    
    def enable_exit_button(self):
        self.exit_button.setEnabled(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    window.start_model_creation()
    sys.exit(app.exec_())
