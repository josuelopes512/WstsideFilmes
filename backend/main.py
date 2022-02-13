from app import app
import random, os
from dotenv import load_dotenv

if __name__ == "__main__":
  load_dotenv('.env')
  # print(os.getenv('DEBUG_MODE'))
  if os.getenv('DEBUG_MODE') == True:
    app.run(host='0.0.0.0', port=random.randint(2000,9000), debug=os.environ['DEBUG_MODE'])
  else:
    app.run(host='0.0.0.0', port=5000, debug=os.environ['DEBUG_MODE'])

