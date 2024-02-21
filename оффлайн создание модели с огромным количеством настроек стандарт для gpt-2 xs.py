from transformers import GPT2Tokenizer, GPT2Config, GPT2LMHeadModel

print("Загружаем предварительно созданный токенизатор")
tokenizer = GPT2Tokenizer.from_pretrained("C://Users//GpT//Desktop//GPT//token")

print("Создаем конфигурацию модели с нужными параметрами")
model_config = GPT2Config(
    vocab_size=tokenizer.vocab_size,
    n_layer=2, # Количество слоев (layers) в трансформере. Большее количество слоев может помочь модели улавливать более сложные зависимости в данных, но требует больше вычислительных ресурсов
    n_head=4, # Количество "голов" (heads) в механизме внимания (attention mechanism). Большее количество голов позволяет модели фокусироваться на разных аспектах данных одновременно и улучшает ее способность к обучению зависимостей
    n_embd=256, # Размерность вектора эмбеддинга для каждого токена. Определяет сколько информации может содержаться в представлении каждого слова
    intermediate_size=512, # Размер скрытого слоя промежуточного представления. Определяет размерность скрытого слоя между слоем внимания и слоем линейного преобразования
    hidden_size=256, # Размер скрытого состояния модели. Определяет размерность скрытого состояния каждого слоя трансформера
    max_position_embeddings=512, # Максимальная длина последовательности, которую модель может обрабатывать. В итоге и выводить не более задоной цыфры. Если последовательность превышает это значение, то она будет обрезана или заполнена специальными токенами
    gradient_checkpointing=True, # Флаг, указывающий, используется ли чекпоинтинг градиентов для оптимизации памяти и вычислений во время обучения
    bos_token_id=tokenizer.bos_token_id,
    eos_token_id=tokenizer.eos_token_id,    # False=Лож
    pad_token_id=tokenizer.pad_token_id,    # True=Истина
    sep_token_id=tokenizer.sep_token_id,
    use_cache=True, # Флаг, указывающий, используется ли кэширование в процессе генерации текста для ускорения работы модели
    layer_norm_epsilon=1e-5, # Эпсилон для Layer normalization, используемый для стабилизации обучения
    initializer_range=0.02, # Диапазон инициализации весов модели. Определяет начальные значения весов при инициализации модели
    output_attentions=True, # output_attentions, output_hidden_states: Флаги, указывающие, нужно ли выводить внимание и скрытые состояния модели во время прямого прохода
    output_hidden_states=True,
    tie_word_embeddings=True # Флаг, указывающий, нужно ли связывать веса слов в эмбеддингах с весами выходного слоя
)
 
print("Создаем модель на основе заданной конфигурации")
model = GPT2LMHeadModel(config=model_config)
model.set_input_embeddings(model.resize_token_embeddings(len(tokenizer)))
print("Модель создана.")

print("Сохраняем модель и токенизатор.")
model.save_pretrained("C://Users//GpT//Desktop//GPT//model")
tokenizer.save_pretrained("C://Users//GpT//Desktop//GPT//model")
print("Модель и токенизатор, сохранины.")
