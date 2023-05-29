from flask import Flask, request, jsonify
from transformers import GPT2LMHeadModel, GPT2TokenizerFast
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Define the paths to the saved model and tokenizer
model_path = 'C:/Users/Nada/OneDrive/Desktop/gl3/2eme semestre/ppp/projet-final-ppp/back-ppp/poem/model'
tokenizer_path = 'C:/Users/Nada/OneDrive/Desktop/gl3/2eme semestre/ppp/projet-final-ppp/back-ppp/poem/tokens'

# Define the paths to the saved news model and tokenizer
news_model_tokenizer_path = 'C:/Users/Nada/OneDrive/Desktop/gl3/2eme semestre/ppp/projet-final-ppp/back-ppp/nouvelle/result'


# Load the pretrained model and tokenizer
tokenizer = GPT2TokenizerFast.from_pretrained(tokenizer_path)
model = GPT2LMHeadModel.from_pretrained(model_path)

# Load the pretrained news model and tokenizer
news_model = GPT2LMHeadModel.from_pretrained(news_model_tokenizer_path)
news_tokenizer = GPT2TokenizerFast.from_pretrained(news_model_tokenizer_path)

# API route for generating a poem
@app.route('/generate_poem', methods=['POST'])
def generate_poem():
    # Get the input text from the request body
    input_text = request.json['input_text']

    # Tokenize the input text
    input_ids = tokenizer.encode(input_text, return_tensors='pt')

    # Generate the poem
    output = model.generate(input_ids, max_length=60, num_beams=5, no_repeat_ngram_size=2, early_stopping=True)
    

    # Decode the generated output
    generated_poem = tokenizer.decode(output[0], skip_special_tokens=True)
    
    #generated_poem=generated_poem[:generated_poem.rfind('.')]
    

    # Return the generated poem as a JSON response
    return jsonify({'poem': generated_poem})

# API route for generating news
@app.route('/generate_news', methods=['POST'])
def generate_news():
    # Get the input text from the request body
    input_text = request.json['input_text']

    # Tokenize the input text
    input_ids = news_tokenizer.encode(input_text, return_tensors='pt')

    # Generate the news
    output = news_model.generate(input_ids, do_sample=True,
        max_length=50,
        pad_token_id=model.config.eos_token_id,
        top_k=50,
        top_p=0.95,)

    # Decode the generated output
    generated_news = news_tokenizer.decode(output[0], skip_special_tokens=True)

    # Return the generated news as a JSON response
    return jsonify({'news': generated_news})

if __name__ == '__main__':
    app.run()
