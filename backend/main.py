from dotenv import load_dotenv
from app import app
import random, os

if __name__ == "__main__":
  load_dotenv('.env')
  if "True" in os.getenv('DEBUG_MODE'):
    app.run(host='0.0.0.0', port=random.randint(2000,9000), debug=os.environ['DEBUG_MODE'])
  else:
    from waitress import serve
    os.environ['FLASK_ENV']= 'Production'
    serve(app, host="0.0.0.0", port=5000)

