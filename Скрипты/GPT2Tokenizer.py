from transformers import GPT2Tokenizer

# Загрузка предварительно обученного токенизатора GPT-2
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

# Добавление специфичных для русского языка токенов
russian_special_tokens = {
    "additional_special_tokens": ["<USER>", "<SYSTEM>", "<SOMETHING_ELSE>", "<RUSSIAN_TOKEN>"]
}
tokenizer.add_special_tokens(russian_special_tokens)

# Добавление специфичных для английского языка токенов
english_special_tokens = {
    "additional_special_tokens": ["<ENGLISH_TOKEN>"]
}
tokenizer.add_special_tokens(english_special_tokens)

# Сохранение модифицированного токенизатора
tokenizer.save_pretrained("C://token")
