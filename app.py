from flask import Flask, request, jsonify, render_template
import stripe
import os

app = Flask(__name__)

# Set your secret key. Remember to switch to your live secret key in production!
stripe.api_key = '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'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/charge', methods=['POST'])
def charge():
    data = request.get_json()
    token = data.get('token')

    try:
        charge = stripe.Charge.create(
            amount=38790,  # Amount in cents
            currency='usd',
            source=token,
            description='Example charge'
        )
        return jsonify(success=True)
    except stripe.error.StripeError as e:
        return jsonify(error=str(e)), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)
