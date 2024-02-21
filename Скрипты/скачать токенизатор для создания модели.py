from transformers import GPT2Config, GPT2LMHeadModel, GPT2Tokenizer

# Загружаем предварительно обученный токенизатор GPT-2
tokenizer = GPT2Tokenizer.from_pretrained('ai-forever/ruGPT-3.5-13B')

# Загружаем предварительно обученные параметры модели и конфигурацию
model_config = GPT2Config.from_pretrained('ai-forever/ruGPT-3.5-13B')