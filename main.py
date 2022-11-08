
from website import create_app
import os

from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.

print("DEBUG MODE -----" + os.getenv("DEBUG_MODE"))


app = create_app()

if __name__ == '__main__':
    if os.getenv("DEBUG_MODE") == 'False':
        app.run(debug=False, port=int(os.environ.get("PORT", 5000)), host='0.0.0.0')
    else:
        app.run(port=8000, debug = True)





