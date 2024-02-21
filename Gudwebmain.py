import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

class GPT2Generator:
    def __init__(self, model_path):
        self.tokenizer = GPT2Tokenizer.from_pretrained(model_path)
        self.model = GPT2LMHeadModel.from_pretrained(model_path)

    def generate_text(self, input_text, temperature_value, length_value, num_results, no_repeat_ngram_size):
        input_ids = self.tokenizer.encode(input_text, return_tensors='pt')
        attention_mask = torch.ones(input_ids.shape, dtype=torch.long, device=input_ids.device)

        outputs = self.model.generate(
            input_ids=input_ids,
            attention_mask=attention_mask,
            max_length=length_value,
            num_return_sequences=num_results,
            no_repeat_ngram_size=no_repeat_ngram_size,
            repetition_penalty=1.5,
            temperature=temperature_value,
            do_sample=True
        )

        result_text = []
        for i, output in enumerate(outputs):
            generated_text = self.tokenizer.decode(output, skip_special_tokens=True)
            generated_text = generated_text[len(input_text):]  # удаляем затравку из сгенерированного текста
            result_text.append(generated_text)

        return result_text

gpt2_generator = GPT2Generator("C://Users//GpT//Desktop//GPT//model")
temperature_value = 0.1
length_value = 200
num_results = 1
ngram_value = 1

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        input_text = request.get_json()['input_text']
        result_text = gpt2_generator.generate_text(input_text, temperature_value, length_value, num_results, ngram_value)
        return jsonify(result_text=result_text)

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
