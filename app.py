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
        name = data['name']
        email = data['email']
        amount = data['amount']
        currency = data['currency']
        payment_method_id = data['payment_method_id']
        address = data['address']
        city = data['city']
        state = data['state']
        zip = data['zip']
        country = data['country']
        
        # Create a customer with detailed billing information
        customer = stripe.Customer.create(
            name=name,
            email=email,
            payment_method=payment_method_id,
            address={
                'line1': address,
                'city': city,
                'state': state,
                'postal_code': zip,
                'country': country
            }
        )
        
        # Create a payment intent with the tokenized payment method and customer
        payment_intent = stripe.PaymentIntent.create(
            amount=amount,
            currency=currency,
            customer=customer.id,
            payment_method=payment_method_id,
            confirm=True,  # Automatically confirm the payment intent
            setup_future_usage='off_session',  # Disable 3DS for future off-session payments
            shipping={
                'name': name,
                'address': {
                    'line1': address,
                    'city': city,
                    'state': state,
                    'postal_code': zip,
                    'country': country
                }
            }
        )
        
        return jsonify({
            'payment_intent_id': payment_intent['id'],
            'status': payment_intent['status']
        })
    except Exception as e:
        return jsonify(error=str(e)), 403

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
