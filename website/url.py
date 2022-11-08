
import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

def get_url(api):
    if os.getenv("DEBUG_MODE") == 'False':
        return os.getenv("CUSTOM_URL") + get_api(api)
    else:
        return os.getenv("LOCAL_URL") + get_api(api)



def get_api(api):
    return '/api/' + api