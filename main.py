from app import app
import random

if __name__ == "__main__":
    app.run(host='0.0.0.0',
		port=random.randint(2000,9000))

