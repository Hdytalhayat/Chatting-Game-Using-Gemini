from flask import Flask, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

genai.configure(api_key="YOUR_API_KEY")
model = genai.GenerativeModel('gemini-1.5-flash')

conversation_history = []

@app.route('/chat', methods=['POST'])
def chat():
    input_data = request.json.get('message')
    if not input_data:
        return jsonify({"error": "No message provided"}), 400

    conversation_history.append("User: " + input_data)
    full_conversation = "\n".join(conversation_history)

    response = model.generate_content(full_conversation)
    response_text = response.text
    conversation_history.append("AI: " + response_text)

    return jsonify({"response": response_text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1209)
