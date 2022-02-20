from dotenv import load_dotenv
from time import sleep
import random, os

welcome = """
  __  __                 _                                      _                _____   _   _                   
 |  \/  |   __ _   ___  | |_    ___   _ __    ___    ___     __| |   ___        |  ___| (_) | |  _ __ ___    ___ 
 | |\/| |  / _` | / __| | __|  / _ \ | '__|  / __|  / _ \   / _` |  / _ \       | |_    | | | | | '_ ` _ \  / __|
 | |  | | | (_| | \__ \ | |_  |  __/ | |    | (__  | (_) | | (_| | |  __/       |  _|   | | | | | | | | | | \__ \\
 |_|  |_|  \__,_| |___/  \__|  \___| |_|     \___|  \___/   \__,_|  \___|       |_|     |_| |_| |_| |_| |_| |___/\n"""

if __name__ == "__main__":
  load_dotenv('.env')
  os.system('cls' if os.name == 'nt' else 'clear')
  print(welcome)
  from app import app
  if "True" in os.getenv('DEBUG_MODE'):
    app.run(host='0.0.0.0', port=random.randint(2000,9000), debug=os.environ['DEBUG_MODE'])
  else:
    from waitress import serve
    os.environ['FLASK_ENV']= 'Production'
    serve(app, host="0.0.0.0", port=5000, url_scheme='https')

from dotenv import load_dotenv
load_dotenv('.env')