from flask import Flask, request, jsonify
from nltk.corpus import words
from nltk.util import ngrams
from collections import Counter
import nltk
nltk.download('words')

app = Flask(__name__)
word_list = set(words.words())

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/suggest')
def suggest_words():
    sentence = request.args.get('sentence', '').lower()
    words_in_sentence = sentence.split()
    last_word = words_in_sentence[-1] if words_in_sentence else ''
    
    # Generate n-grams (up to 3-grams) for the sentence
    ngrams_list = []
    for n in range(1, 4):  # Consider 1-gram, 2-gram, and 3-gram
        ngrams_list.extend(list(ngrams(words_in_sentence[-n:], n)))

    suggestions = []
    for ngram in ngrams_list:
        prefix = ' '.join(ngram[:-1])
        suffix = ngram[-1]
        prefix_matches = [w for w in word_list if w.startswith(suffix)]
        suggestions.extend([f'{prefix} {match}' for match in prefix_matches])

    # Count the frequency of suggestions and sort them by word length in ascending order
    suggestion_counter = Counter(suggestions)
    sorted_suggestions = sorted(suggestion_counter.keys(), key=lambda x: (len(x), x))

    # Return the top 5 suggestions (simpler words first)
    top_suggestions = sorted_suggestions[:5]
    
    return jsonify(top_suggestions)

if __name__ == '__main__':
    app.run(debug=True)
