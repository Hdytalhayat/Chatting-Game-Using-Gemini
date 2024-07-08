from flask import Flask, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

genai.configure(api_key="AIzaSyBRqw3Ozd7fNRmKAvzglsrtEPKrs2tAxOU")
model = genai.GenerativeModel('gemini-1.5-flash')

conversation_history = []

file_path = 'F:\PythonGAme\American Sign (2)\American Sign\CharInfo.txt'

with open(file_path, 'r') as file:
    char_info_string = file.read()

@app.route('/chat', methods=['POST'])
def chat():
    input_data = request.json.get('message')
    if not input_data:
        return jsonify({"error": "No message provided"}), 400

    conversation_history.append("char_info_string " + input_data)
    full_conversation = "\n".join(conversation_history)

    response = model.generate_content(full_conversation)
    response_text = response.text
    conversation_history.append("AI: " + response_text)

    return jsonify({"response": response_text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1209)
