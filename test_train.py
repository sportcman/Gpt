import sys
import os
import torch
from torch.utils.data import DataLoader, Dataset
from transformers import GPT2Tokenizer, GPT2LMHeadModel
from torch.optim import AdamW
from torch.optim.lr_scheduler import StepLR
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QProgressBar, QLabel, QLineEdit
from PyQt6.QtCore import QThread, pyqtSignal, QObject

class CustomTextDataset(Dataset):
    def __init__(self, tokenizer, file_path, block_size):
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = [line for line in f.read().splitlines() if (len(line) > 0 and not line.isspace())]

        self.examples = tokenizer.batch_encode_plus(lines, add_special_tokens=True, max_length=block_size, truncation=True, padding="max_length")["input_ids"]

    def __len__(self):
        return len(self.examples)

    def __getitem__(self, i):
        return torch.tensor(self.examples[i], dtype=torch.long)

class TrainingWorker(QObject):
    update_progress = pyqtSignal(int)
    update_log = pyqtSignal(str)
    training_finished = pyqtSignal()

    def __init__(self, model, dataset, tokenizer, device, batch_size, epochs, model_path):
        super().__init__()
        self.model = model
        self.dataset = dataset
        self.tokenizer = tokenizer
        self.device = device
        self.batch_size = batch_size
        self.epochs = epochs
        self.model_path = model_path
        self.is_running = True

    def run(self):
        data_loader = DataLoader(self.dataset, batch_size=self.batch_size, shuffle=True)
        optimizer = AdamW(self.model.parameters(), lr=5e-5)
        scheduler = StepLR(optimizer, step_size=1, gamma=0.95)

        self.model.train()
        self.model.to(self.device)

        total_steps = len(data_loader) * self.epochs

        for epoch in range(self.epochs):
            if not self.is_running:
                break

            for i, batch in enumerate(data_loader):
                if not self.is_running:
                    break

                inputs = batch.to(self.device)
                labels = batch.to(self.device)

                optimizer.zero_grad()
                outputs = self.model(inputs, labels=labels)
                loss = outputs.loss
                loss.backward()
                optimizer.step()

                current_step = epoch * len(data_loader) + i + 1
                self.update_progress.emit(int((current_step / total_steps) * 100))
                self.update_log.emit(f"Эпоха {epoch+1}/{self.epochs}, Партия {i+1}/{len(data_loader)}, Потеря: {loss.item()}")

            scheduler.step()
            self.update_log.emit(f"Эпоха {epoch+1}/{self.epochs} завершена.")

        if self.is_running:
            self.model.save_pretrained(self.model_path)
            self.tokenizer.save_pretrained(self.model_path)
            self.update_log.emit("Обучение завершено. Модель сохранена.")
            self.update_progress.emit(100)

        self.training_finished.emit()

    def stop(self):
        self.is_running = False

class MainWindow(QWidget):
    def __init__(self, model, dataset, tokenizer, device, batch_size, epochs, model_path):
        super().__init__()
        self.thread = QThread()
        self.worker = TrainingWorker(model, dataset, tokenizer, device, batch_size, epochs, model_path)
        self.worker.moveToThread(self.thread)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Обучение Gpt")
        self.setGeometry(100, 100, 400, 150)

        layout = QVBoxLayout()

        self.startButton = QPushButton("Начать обучение")
        self.stopButton = QPushButton("Остановить обучение")
        self.logText = QTextEdit()
        self.progressBar = QProgressBar()
        self.epochsLabel = QLabel("Количество эпох:")
        self.epochsInput = QLineEdit(str(self.worker.epochs))

        layout.addWidget(self.startButton)
        layout.addWidget(self.stopButton)
        layout.addWidget(self.epochsLabel)
        layout.addWidget(self.epochsInput)
        layout.addWidget(self.logText)
        layout.addWidget(self.progressBar)

        self.setLayout(layout)

        self.startButton.clicked.connect(self.startTraining)
        self.stopButton.clicked.connect(self.stopTraining)
        self.worker.update_progress.connect(self.progressBar.setValue)
        self.worker.update_log.connect(self.logText.append)
        self.worker.training_finished.connect(self.onTrainingFinished)

    def startTraining(self):
        self.worker.epochs = int(self.epochsInput.text())  # Получаем количество эпох из поля ввода
        if not self.thread.isRunning():
            self.thread.started.connect(self.worker.run)
            self.thread.start()
        self.startButton.setEnabled(False)
        self.stopButton.setEnabled(True)

    def stopTraining(self):
        self.worker.stop()

    def onTrainingFinished(self):
        self.startButton.setEnabled(True)
        self.stopButton.setEnabled(False)
        if self.thread.isRunning():
            self.thread.quit()

def prepare_model_and_dataset(model_path, dataset_path, device):
    try:
        tokenizer = GPT2Tokenizer.from_pretrained(model_path)
        model = GPT2LMHeadModel.from_pretrained(model_path)
    except Exception as e:
        print(f"Error loading model from {model_path}, loading GPT-2 base model instead. Error: {e}")
        tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
        model = GPT2LMHeadModel.from_pretrained('gpt2')

    model.to(device)

    dataset = CustomTextDataset(tokenizer, dataset_path, block_size=64) #  Учитывает среднюю длину текстовых фрагментов, которые модель будет обрабатывать.
    return model, dataset, tokenizer

def main():
    app = QApplication(sys.argv)

    model_path = "C://Users//GpT//Desktop//GPT//model"
    dataset_path = "C://Users//GpT//Desktop//GPT//dataset.txt"
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    batch_size = 4 #  Параметр должен учитывать количество ядер процессора и доступную оперативную память
    epochs = 1

    model, dataset, tokenizer = prepare_model_and_dataset(model_path, dataset_path, device)
    window = MainWindow(model, dataset, tokenizer, device, batch_size, epochs, model_path)
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
