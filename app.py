from flask import Flask, render_template, request, jsonify
from semanitc_search import get_best_response
from collections import deque

app = Flask(__name__)

conversation_history = deque(maxlen=3)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_query = request.form['user_query']

    if user_query.lower() == "exit":
        return jsonify({'response': "Thank you! Have a great day! 😊", 'end_conversation': True})

   
    product_details = get_best_response(user_query)

   
    conversation_history.append(user_query)

    
    confidence = product_details.get('Confidence', 0)
    response_text = product_details.get('Response', '')

    if confidence > 0.3:
        response = f"Intent detected - {product_details['Intent']} <br>Here are the most relevant product details:<br>"
        for key, value in product_details.items():
            if key not in ["Intent", "Confidence"]: 
                response += f"<strong>{key}</strong>: {value}<br>"
        response += f"Confidence: {confidence:.2f}"
    else:
        response = response_text  

    return jsonify({'response': response, 'end_conversation': False})

if __name__ == '__main__':
    app.run(debug=True)
