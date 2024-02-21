from transformers import GPT2Tokenizer, GPT2Config, GPT2LMHeadModel

# Загружаем предварительно созданный токенизатор
tokenizer = GPT2Tokenizer.from_pretrained("C://token")

# Создаем конфигурацию модели с нужными параметрами
model_config = GPT2Config(
    vocab_size=tokenizer.vocab_size,
    n_layer=16,
    n_head=32,
    n_embd=2048,
    intermediate_size=3072,
    hidden_size=1500,
    max_position_embeddings=3072,
    num_attention_heads=32,
    gradient_checkpointing=True,
    bos_token_id=tokenizer.bos_token_id,
    eos_token_id=tokenizer.eos_token_id,
    pad_token_id=tokenizer.pad_token_id,
    sep_token_id=tokenizer.sep_token_id
)

# Создаем модель на основе заданной конфигурации
model = GPT2LMHeadModel(config=model_config)
model.set_input_embeddings(model.resize_token_embeddings(len(tokenizer)))

# Сохраняем модель и токенизатор
model.save_pretrained('C://Novak//model')
tokenizer.save_pretrained('C://Novak//model')
