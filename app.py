from flask import Flask, request, jsonify
from bot import answer

app = Flask(__name__)


history = []


@app.post('/chat')
def index():
    question = request.json['question']

    print(history)

    response = answer(question, history)

    history.append({ "role": "user", "content": question })
    history.append({ "role": "assistant", "content": response })

    return jsonify({ "answer": response })


if __name__ == '__main__':
   app.run()
