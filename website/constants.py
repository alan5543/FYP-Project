# CONSTANTS PAGES For ALL py file

#__inti__py
DATABASE_SUCCESS_MSG = 'The Database is successfully created!'

# auth.py
LOGIN_SUCCESS_MSG = "Log in Successfully!"
LOGIN_WRONG_PW = 'Incorrect Password, Try Again...'
LOGIN_NOT_EXIST = 'Not Existed Account. Please register a new one'

EMAIL_EXIST_ERR = 'The Email Account is already existed'
EMAIL_SHORT_ERR = 'Email Account must be larger than 4 characters'
EMAIL_NAME_ERR = 'The name is too short for registration'
EMAIL_PW_ERR = 'The password setting should not be less than 7 characters'
EMAIL_MATCH_ERR = 'The password are not matched'
REGISTER_SUCCESS_MSG = 'Account Creation Success!'

# engine.py
DEFAULT_MEANING = "Let's read the news article together. Our Machine will help you to understand more."
EXT_ERROR_HANDLE = "No summary is Made. The number of extraction should be less than the total count of sentences. The default number of extraction is 5. Please find the article sentence is more than 5."
DEFAULT_ERROR_MESSAGE = "Sorry! The Summarizer Engine cannot do a summarical analysis on this News Article..."
ABS_ERROR_HANDLE = "No summary is made. The input length from the news article should be more than the DEFAULT MIN LENGTH, which is 80 characters."

# news.py
DEFAULT_PHOTO = "https://st4.depositphotos.com/14953852/24787/v/600/depositphotos_247872612-stock-illustration-no-image-available-icon-vector.jpg"
LOG_START_PROCESS = 'STAR PROCESS'
LOG_TRY_END = 'try end'
LOG_TRY_SKIP = 'try skip'
LOG_END_PROCESS = 'END PROCESS'
LOG_DB_FIND = "Finding the existing item in db"
LOG_DB_FINISHED = "Finding Finshed"
LOG_DB_STORE = "Store it in the db..."
LOG_DB_SUCCESS = "Successfully stored"
DEFAULT_NEW_ID = 1

# reports.py
DEFAULT_TITLE = "NOT DEFINED"
DEFAULT_DOC = "NOT DEFINED"
DEFAULT_INPUT_IMAGE = '../static/defaultImages/user_input_news.png'
DEFAULT_CLOUD_NAME = "wordcloud"

# views.py
INPUT_TITLE_ERROR = "Please Input the News Title for Extraction"
INPUT_TEXT_ERROR = "Please Input the News Article for Extraction"
INPUT_SUCCESS = "Success Process!"
NOT_SELECT_FILE = 'No selected file'
ONLY_SUPPORT_TEXT = 'Only Support Text File'
FILE_SAVED = "File saved"
FILE_ERROR = "File error happened. Check your file type"

URL_NO_NEWS = "No any news article is extracted here. Try the another URL please..."
URL_NO_TITLE = "No title extracted"
URL_NO_SUM = "Not Extracted Summary"
URL_DEFAULT_PUBLISHER = "Included in the Article"
DEFAULT_NEWS_IMAGE = "https://st4.depositphotos.com/14953852/24787/v/600/depositphotos_247872612-stock-illustration-no-image-available-icon-vector.jpg"
WEB_SCRAP_DENIED = "The web scraping request is denied. Try the articles in text input box..."

NO_EXPLORE_TITLE = "No Title is extracted in this news blog because the web scrapping is denied by other website. Please try another news blog."
NO_EXPLORE_TEXT = "No Article is extracted in this news blog because the web scrapping is denied by other website. Please try another news blog."