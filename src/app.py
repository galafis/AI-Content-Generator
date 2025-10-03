from flask import Flask, jsonify, render_template, request
from content_generator import ContentGenerator

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/generate', methods=['POST'])
def generate():
    data = request.get_json()
    topic = data.get('topic', 'Inteligência Artificial')
    length = data.get('length', 500)
    style = data.get('style', 'technical')

    generator = ContentGenerator()
    content = generator.generate_article(topic=topic, length=length, style=style)

    return jsonify({'content': content})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

