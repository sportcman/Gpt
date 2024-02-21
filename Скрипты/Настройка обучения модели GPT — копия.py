import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QProgressBar, QFileDialog, QLineEdit
from PyQt5.QtCore import QThread, pyqtSignal
from transformers import GPT2Tokenizer, TextDataset, DataCollatorForLanguageModeling, Trainer, TrainingArguments, GPT2LMHeadModel


class TrainingThread(QThread):
    updateProgress = pyqtSignal(int)

    def __init__(self, dataset_path, num_epochs):
        super().__init__()
        self.dataset_path = dataset_path
        self.num_epochs = num_epochs

    def run(self):
        model_path = "C:/gpt/model"
        batch_size = 4

        tokenizer = GPT2Tokenizer.from_pretrained(model_path)
        model = GPT2LMHeadModel.from_pretrained(model_path)

        dataset = TextDataset(
            tokenizer=tokenizer,
            file_path=self.dataset_path,
            block_size=128
        )

        data_collator = DataCollatorForLanguageModeling(
            tokenizer=tokenizer,
            mlm=False
        )

        training_args = TrainingArguments(
            output_dir=model_path,
            overwrite_output_dir=True,
            num_train_epochs=self.num_epochs,
            per_device_train_batch_size=batch_size,
            save_total_limit=1,
        )

        trainer = Trainer(
            model=model,
            args=training_args,
            data_collator=data_collator,
            train_dataset=dataset,
        )

        for epoch in range(self.num_epochs):
            trainer.train()
            progress_value = int((epoch + 1) / self.num_epochs * 100)
            self.updateProgress.emit(progress_value)

        model.save_pretrained(model_path)
        tokenizer.save_pretrained(model_path)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Настройка обучения модели GPT")
        self.setGeometry(100, 100, 600, 200)

        self.dataset_path_label = QLabel(self)
        self.dataset_path_label.setText("Путь к датасету:")
        self.dataset_path_label.adjustSize()
        self.dataset_path_label.setGeometry(20, 20, 100, 30)

        self.dataset_path_button = QPushButton(self)
        self.dataset_path_button.setText("Выбрать файл")
        self.dataset_path_button.setGeometry(120, 20, 120, 30)
        self.dataset_path_button.clicked.connect(self.select_dataset_path)

        self.num_epochs_label = QLabel(self)
        self.num_epochs_label.setText("Количество эпох:")
        self.num_epochs_label.setGeometry(20, 60, 100, 30)

        self.num_epochs_input = QLineEdit(self)  # Добавлено поле ввода для количества эпох
        self.num_epochs_input.setGeometry(120, 60, 100, 30)

        self.start_training_button = QPushButton(self)  # Изменено название кнопки
        self.start_training_button.setText("Запустить обучение")
        self.start_training_button.setGeometry(120, 100, 150, 30)  # Изменены координаты и размер
        self.start_training_button.clicked.connect(self.start_training)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setGeometry(20, 140, 360, 30)  # Изменены координаты
        self.progress_bar.setValue(0)

    def select_dataset_path(self):
        filename, _ = QFileDialog.getOpenFileName(
            parent=self,
            caption="Выберите файл с датасетом",
            filter="Text Files (*.txt)"
        )
        if filename != "":
            self.dataset_path = filename

    def start_training(self):
        num_epochs_str = self.num_epochs_input.text()
        if not num_epochs_str.isdigit():
            # Вывести сообщение об ошибке и прервать обучение
            return
        num_epochs = int(num_epochs_str)
        dataset_path = self.dataset_path

        self.training_thread = TrainingThread(dataset_path, num_epochs)
        self.training_thread.updateProgress.connect(self.update_progress_bar)
        self.training_thread.finished.connect(self.training_finished)
        self.training_thread.start()

    def update_progress_bar(self, value):
        self.progress_bar.setValue(value)

    def training_finished(self):
        self.progress_bar.setValue(100)
        # Добавьте код для сообщения о завершении обучения


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
