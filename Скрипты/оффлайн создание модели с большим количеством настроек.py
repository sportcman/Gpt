from transformers import GPT2Config, GPT2LMHeadModel, GPT2Tokenizer

# Создаем конфигурацию модели с малыми параметрами
model_config = GPT2Config(
    vocab_size=50257,   # Размер словаря модели
    n_positions=1024,   # Максимальное количество позиций в последовательности
    n_ctx=1024,         # Размер контекста (максимальная длина входной последовательности) 
    n_embd=1024,         # Размерность эмбеддинга
    n_layer=32,          # Количество слоев модели
    n_head=32,            # Количество голов в слоях AufioReg
    intermediate_size=3072,  # Размер промежуточного слоя в блоке
    hidden_size=1024,         # Размер скрытого состояния
    num_labels=2        # Количество меток задачи (в данном случае 2)
)

# Создаем модель на основе заданной конфигурации
model = GPT2LMHeadModel(config=model_config)

# Создаем русский токенизатор
tokenizer = GPT2Tokenizer.from_pretrained("C://token")

# Сохраняем модель и токенизатор
model.save_pretrained('C:/Novak/model')
tokenizer.save_pretrained('C:/Novak/model')
