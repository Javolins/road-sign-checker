from App import app
import os

if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run(host="localhost", port=5000, debug=True)