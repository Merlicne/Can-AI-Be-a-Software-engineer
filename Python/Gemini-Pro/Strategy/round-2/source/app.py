from flask import Flask
from auth.strategies.basic_auth import BasicAuthenticator
# ... other imports

app = Flask(__name__)
app.secret_key = 'your_secret_key' # Required for sessions

# Set the desired authentication strategy
auth_strategy = BasicAuthenticator() 

@app.route('/protected')
def protected_route():
    try:
        user = auth_strategy.authenticate(request)
        return f"Welcome, {user['username']}!"
    except AuthenticationError as e:
        return f"Authentication Error: {e}", 401

if __name__ == "__main__":
    app.run(debug=True)