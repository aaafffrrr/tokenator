from flask import Flask, request, jsonify, render_template
import stripe
import os

app = Flask(__name__)

# Set your Stripe API key from the environment variable
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create-payment-intent', methods=['POST'])
def create_payment_intent():
    try:
        data = request.json
        amount = data['amount']
        currency = data['currency']
        payment_method_id = data['payment_method_id']
        
        # Create a payment intent with the tokenized payment method
        payment_intent = stripe.PaymentIntent.create(
            amount=amount,
            currency=currency,
            payment_method=payment_method_id,
            confirm=True  # Automatically confirm the payment intent
        )
        
        return jsonify({
            'payment_intent_id': payment_intent['id'],
            'status': payment_intent['status']
        })
    except Exception as e:
        return jsonify(error=str(e)), 403

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
