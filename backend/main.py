from app import app
import random
from dotenv import load_dotenv

if __name__ == "__main__":
  load_dotenv('.env')
  app.run(host='0.0.0.0', port=random.randint(2000,9000), debug=True)

