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

TOPIC_ERROR = "Sorry, we cannot find any relative news in this topic now."
TOPIC_LIMIT = 15
TOPIC_EXPLORE = 'explore'
TOPIC_WORLD = 'world'
TOPIC_HK = 'hongkong'
TOPIC_BUSINESS = 'business'
TOPIC_TECH = 'technology'
TOPIC_ENTERTAIN = 'entertainment'
TOPIC_SCIENCE = 'science'
TOPIC_SPORTS = 'sports'
TOPIC_HEALTH = 'health'

TOPIC_LABEL_EXPLORE = 'Explore News'
TOPIC_LABEL_WORLD = 'World News'
TOPIC_LABEL_HK = 'Hong Kong News'
TOPIC_LABEL_BUSINESS = 'Business News'
TOPIC_LABEL_TECH = 'Technology News'
TOPIC_LABEL_ENTERTAIN = 'Entertainment News'
TOPIC_LABEL_SCIENCE = 'Science News'
TOPIC_LABEL_SPORTS = 'Sports News'
TOPIC_LABEL_HEALTH = 'Health News'


# API Service
REJECT_TO_API = "The API service is in error"
NO_SUPPORRT_API = "The API service is not supported"


TWEET_DEMO = {
    "countries": [
        "us",
        "Not Found",
        "ru",
        "al",
        "gb"
    ],
    "hotWords": [
        "#fans",
        "#Giannis",
        "#shooting",
        "#Harden",
        "#They"
    ],
    "opinon": {
        "anger": 0,
        "disgust": 0,
        "fear": 4,
        "joy": 19,
        "negative": 6,
        "neutral": 14,
        "no_opinons": 15,
        "objective": 10,
        "positive": 10,
        "sadness": 4,
        "shame": 0,
        "subjective": 19,
        "support": 11,
        "surprise": 1,
        "unsuppoprt": 3
    },
    "timeline": [
        {
            "Neg": 0.0,
            "Polarity": 0.0,
            "Pos": 0.0,
            "Release": "2022-02-01 14:00:00+00:00"
        },
        {
            "Neg": 0.0,
            "Polarity": 0.2681818181818182,
            "Pos": 0.429,
            "Release": "2022-02-04 04:30:00+00:00"
        },
        {
            "Neg": 0.0,
            "Polarity": 0.35000000000000003,
            "Pos": 0.188,
            "Release": "2022-02-05 02:30:00+00:00"
        },
        {
            "Neg": 0.0,
            "Polarity": 0.0,
            "Pos": 0.0,
            "Release": "2022-02-06 00:30:00+00:00"
        },
        {
            "Neg": 0.277,
            "Polarity": -0.175,
            "Pos": 0.239,
            "Release": "2022-02-06 02:30:00+00:00"
        },
        {
            "Neg": 0.0,
            "Polarity": 0.0,
            "Pos": 0.0,
            "Release": "2022-02-06 04:30:00+00:00"
        },
        {
            "Neg": 0.05,
            "Polarity": 0.25,
            "Pos": 0.04,
            "Release": "2022-02-07 13:30:00+00:00"
        },
        {
            "Neg": 0.0,
            "Polarity": 0.0,
            "Pos": 0.0,
            "Release": "2022-02-07 16:00:00+00:00"
        },
        {
            "Neg": 0.11,
            "Polarity": 0.25,
            "Pos": 0.117,
            "Release": "2022-02-07 16:30:00+00:00"
        },
        {
            "Neg": 0.0925,
            "Polarity": -0.225,
            "Pos": 0.262,
            "Release": "2022-02-07 17:00:00+00:00"
        },
        {
            "Neg": 0.0,
            "Polarity": 0.0,
            "Pos": 0.0,
            "Release": "2022-02-07 18:00:00+00:00"
        },
        {
            "Neg": 0.057,
            "Polarity": -0.17500000000000002,
            "Pos": 0.0,
            "Release": "2022-02-07 19:00:00+00:00"
        },
        {
            "Neg": 0.0,
            "Polarity": 0.325,
            "Pos": 0.184,
            "Release": "2022-02-07 20:00:00+00:00"
        },
        {
            "Neg": 0.0,
            "Polarity": 0.0,
            "Pos": 0.0,
            "Release": "2022-02-07 20:30:00+00:00"
        },
        {
            "Neg": 0.0,
            "Polarity": 0.0,
            "Pos": 0.089,
            "Release": "2022-02-07 21:00:00+00:00"
        },
        {
            "Neg": 0.0,
            "Polarity": 0.5,
            "Pos": 0.213,
            "Release": "2022-02-08 03:30:00+00:00"
        },
        {
            "Neg": 0.0,
            "Polarity": 0.4,
            "Pos": 0.0,
            "Release": "2022-02-08 05:00:00+00:00"
        },
        {
            "Neg": 0.0,
            "Polarity": 0.0,
            "Pos": 0.0,
            "Release": "2022-02-08 15:30:00+00:00"
        },
        {
            "Neg": 0.0,
            "Polarity": 0.3,
            "Pos": 0.082,
            "Release": "2022-02-08 16:30:00+00:00"
        },
        {
            "Neg": 0.0,
            "Polarity": 0.0,
            "Pos": 0.0,
            "Release": "2022-02-08 22:00:00+00:00"
        },
        {
            "Neg": 0.0,
            "Polarity": 0.5,
            "Pos": 0.114,
            "Release": "2022-02-09 00:30:00+00:00"
        },
        {
            "Neg": 0.0,
            "Polarity": 0.0,
            "Pos": 0.0,
            "Release": "2022-02-09 02:30:00+00:00"
        },
        {
            "Neg": 0.0,
            "Polarity": 0.2,
            "Pos": 0.492,
            "Release": "2022-02-09 03:00:00+00:00"
        },
        {
            "Neg": 0.215,
            "Polarity": 0.0,
            "Pos": 0.169,
            "Release": "2022-02-09 03:30:00+00:00"
        },
        {
            "Neg": 0.0,
            "Polarity": -0.15555555555555559,
            "Pos": 0.0,
            "Release": "2022-02-09 04:30:00+00:00"
        },
        {
            "Neg": 0.0,
            "Polarity": -0.1,
            "Pos": 0.0,
            "Release": "2022-02-09 05:30:00+00:00"
        },
        {
            "Neg": 0.0,
            "Polarity": 0.0,
            "Pos": 0.0,
            "Release": "2022-02-09 06:30:00+00:00"
        }
    ],
    "tweets": [
        {
            "CleanText": "Lakers fans looking at Damian Lillard ",
            "Com": 0.0,
            "Country": "us",
            "Emotion": "joy",
            "Emotion_Score": 0.32617329853837107,
            "Location": "Not Found",
            "Neg": 0.0,
            "Neu": 1.0,
            "Polarity": 0.0,
            "Pos": 0.0,
            "Publisher": "@Complex Sports",
            "Release": "2022-02-08 15:41:11+00:00",
            "Subj": 0.0,
            "Tweets": "Lakers fans looking at Damian Lillard https://t.co/oercl6COTY",
            "Url": "https://twitter.com/twitter/statuses/1491074640810491906",
            "expression": "Objective",
            "opinion": "No Opinion",
            "sentiment": "Neutral"
        },
        {
            "CleanText": "Giannis vs the Lakers\n\n44 PTS\n15 REB\n8 AST\n17-20 FG\n\nHe joins Wilt Chamberlain and Kareem Abdul-Jabbar as the only players in NBA history with a 40/10/5 game on 85% shooting. ",
            "Com": 0.0,
            "Country": "us",
            "Emotion": "joy",
            "Emotion_Score": 0.9538206900416224,
            "Location": "Not Found",
            "Neg": 0.0,
            "Neu": 1.0,
            "Polarity": -0.2,
            "Pos": 0.0,
            "Publisher": "@StatMuse",
            "Release": "2022-02-09 05:31:42+00:00",
            "Subj": 0.7,
            "Tweets": "Giannis vs the Lakers:\n\n44 PTS\n15 REB\n8 AST\n17-20 FG\n\nHe joins Wilt Chamberlain and Kareem Abdul-Jabbar as the only players in NBA history with a 40/10/5 game on 85% shooting. https://t.co/fstikQ4Tz1",
            "Url": "https://twitter.com/twitter/statuses/1491283644144812032",
            "expression": "Subjective",
            "opinion": "No Opinion",
            "sentiment": "Negative"
        },
        {
            "CleanText": "LeBron answers a question asking if he thinks the Lakers can get to the Milwaukee Bucks’ level ",
            "Com": 0.0,
            "Country": "us",
            "Emotion": "fear",
            "Emotion_Score": 0.7723080812899443,
            "Location": "Los Angeles, CA",
            "Neg": 0.0,
            "Neu": 1.0,
            "Polarity": 0.0,
            "Pos": 0.0,
            "Publisher": "@Rob Perez",
            "Release": "2022-02-09 06:38:47+00:00",
            "Subj": 0.0,
            "Tweets": "LeBron answers a question asking if he thinks the Lakers can get to the Milwaukee Bucks’ level: https://t.co/B6djsSdoEN",
            "Url": "https://twitter.com/twitter/statuses/1491300527782596611",
            "expression": "Objective",
            "opinion": "No Opinion",
            "sentiment": "Neutral"
        },
        {
            "CleanText": "Giannis’ 2 games against the Lakers this season. ",
            "Com": 0.0,
            "Country": "us",
            "Emotion": "joy",
            "Emotion_Score": 0.7182348258410383,
            "Location": "Los Angeles, CA",
            "Neg": 0.0,
            "Neu": 1.0,
            "Polarity": 0.0,
            "Pos": 0.0,
            "Publisher": "@Rob Perez",
            "Release": "2022-02-09 05:43:33+00:00",
            "Subj": 0.0,
            "Tweets": "Giannis’ 2 games against the Lakers this season. https://t.co/i430AJpKso",
            "Url": "https://twitter.com/twitter/statuses/1491286629012901888",
            "expression": "Objective",
            "opinion": "No Opinion",
            "sentiment": "Neutral"
        },
        {
            "CleanText": "The Zen Master. Coach Riles. \n\nOfficially named among the top 15 coaches in NBA history. ",
            "Com": 0.2023,
            "Country": "us",
            "Emotion": "joy",
            "Emotion_Score": 0.989784582613685,
            "Location": "Los Angeles, CA",
            "Neg": 0.0,
            "Neu": 0.886,
            "Polarity": 0.5,
            "Pos": 0.114,
            "Publisher": "@Los Angeles Lakers",
            "Release": "2022-02-09 00:17:09+00:00",
            "Subj": 0.5,
            "Tweets": "The Zen Master. Coach Riles. \n\nOfficially named among the top 15 coaches in NBA history. https://t.co/Te8yxwVDwa",
            "Url": "https://twitter.com/twitter/statuses/1491204485234196480",
            "expression": "Subjective",
            "opinion": "Support",
            "sentiment": "Postive"
        },
        {
            "CleanText": "Lakers get more shooting, Blazers get to rebuild around two young stars, Sixers get their Harden-Morey reunion, and Nets get a point guard who can play in home games. ",
            "Com": 0.34,
            "Country": "Not Found",
            "Emotion": "joy",
            "Emotion_Score": 0.9452312602522673,
            "Location": "A roaming tower of giraffes",
            "Neg": 0.0,
            "Neu": 0.918,
            "Polarity": 0.3,
            "Pos": 0.082,
            "Publisher": "@Harrison Faigen",
            "Release": "2022-02-08 16:20:18+00:00",
            "Subj": 0.45,
            "Tweets": "Lakers get more shooting, Blazers get to rebuild around two young stars, Sixers get their Harden-Morey reunion, and Nets get a point guard who can play in home games. https://t.co/8qPMCcs6oT",
            "Url": "https://twitter.com/twitter/statuses/1491084482073415683",
            "expression": "Subjective",
            "opinion": "Support",
            "sentiment": "Postive"
        },
        {
            "CleanText": "Myles Turner to the Lakers confirmed ",
            "Com": 0.0,
            "Country": "Not Found",
            "Emotion": "joy",
            "Emotion_Score": 0.42482135553439804,
            "Location": "A roaming tower of giraffes",
            "Neg": 0.0,
            "Neu": 1.0,
            "Polarity": 0.4,
            "Pos": 0.0,
            "Publisher": "@Harrison Faigen",
            "Release": "2022-02-08 04:58:18+00:00",
            "Subj": 1.0,
            "Tweets": "Myles Turner to the Lakers confirmed https://t.co/G4ZdLnO9bM",
            "Url": "https://twitter.com/twitter/statuses/1490912851984220162",
            "expression": "Subjective",
            "opinion": "No Opinion",
            "sentiment": "Postive"
        },
        {
            "CleanText": "Ninth straight Warriors win. They're 41-13 with five games until the All-Star break at Utah, vs Knicks, vs Lakers, at Clippers, vs Nuggets.",
            "Com": 0.6908,
            "Country": "Not Found",
            "Emotion": "joy",
            "Emotion_Score": 0.9973621939107601,
            "Location": "NorCal - OKC - NorCal",
            "Neg": 0.0,
            "Neu": 0.787,
            "Polarity": 0.5,
            "Pos": 0.213,
            "Publisher": "@Anthony Slater",
            "Release": "2022-02-08 03:20:45+00:00",
            "Subj": 0.4,
            "Tweets": "Ninth straight Warriors win. They're 41-13 with five games until the All-Star break: at Utah, vs Knicks, vs Lakers, at Clippers, vs Nuggets.",
            "Url": "https://twitter.com/twitter/statuses/1490888305176903681",
            "expression": "Subjective",
            "opinion": "Support",
            "sentiment": "Postive"
        },
        {
            "CleanText": "Lakers 🏆 \nDodgers 🏆 \nRams ❓ ",
            "Com": 0.0,
            "Country": "us",
            "Emotion": "neutral",
            "Emotion_Score": 0.3936233030104749,
            "Location": "Cincinnati, OH",
            "Neg": 0.0,
            "Neu": 1.0,
            "Polarity": 0.0,
            "Pos": 0.0,
            "Publisher": "@PFF",
            "Release": "2022-02-08 22:00:14+00:00",
            "Subj": 0.0,
            "Tweets": "Lakers 🏆 \nDodgers 🏆 \nRams ❓ https://t.co/Z7GSxISDOK",
            "Url": "https://twitter.com/twitter/statuses/1491170031723597824",
            "expression": "Objective",
            "opinion": "No Opinion",
            "sentiment": "Neutral"
        },
        {
            "CleanText": "AD's averaging 29 points and 13 boards in his last five games ... but let's talk about his defense 🗜 ",
            "Com": 0.1901,
            "Country": "us",
            "Emotion": "joy",
            "Emotion_Score": 0.998441644142349,
            "Location": "Los Angeles, CA",
            "Neg": 0.0,
            "Neu": 0.911,
            "Polarity": 0.0,
            "Pos": 0.089,
            "Publisher": "@Los Angeles Lakers",
            "Release": "2022-02-07 21:00:01+00:00",
            "Subj": 0.06666666666666667,
            "Tweets": "AD's averaging 29 points and 13 boards in his last five games ... but let's talk about his defense 🗜 https://t.co/ur0APRDHtB",
            "Url": "https://twitter.com/twitter/statuses/1490792490256928771",
            "expression": "Subjective",
            "opinion": "Support",
            "sentiment": "Neutral"
        },
        {
            "CleanText": "The King. The Kicks. ",
            "Com": 0.0,
            "Country": "us",
            "Emotion": "joy",
            "Emotion_Score": 0.7135110681894582,
            "Location": "Los Angeles, CA",
            "Neg": 0.0,
            "Neu": 1.0,
            "Polarity": 0.0,
            "Pos": 0.0,
            "Publisher": "@Los Angeles Lakers",
            "Release": "2022-02-09 02:17:44+00:00",
            "Subj": 0.0,
            "Tweets": "The King. The Kicks. https://t.co/pkF64jISfU",
            "Url": "https://twitter.com/twitter/statuses/1491234830662598663",
            "expression": "Objective",
            "opinion": "No Opinion",
            "sentiment": "Neutral"
        },
        {
            "CleanText": "Lakers are just settling on offense and playing no defense. Recipe to get beat by 20.",
            "Com": -0.2263,
            "Country": "us",
            "Emotion": "joy",
            "Emotion_Score": 0.5967515664335751,
            "Location": "Not Found",
            "Neg": 0.215,
            "Neu": 0.615,
            "Polarity": 0.0,
            "Pos": 0.169,
            "Publisher": "@shannon sharpe",
            "Release": "2022-02-09 03:20:19+00:00",
            "Subj": 0.0,
            "Tweets": "Lakers are just settling on offense and playing no defense. Recipe to get beat by 20.",
            "Url": "https://twitter.com/twitter/statuses/1491250582208016386",
            "expression": "Objective",
            "opinion": "No Opinion",
            "sentiment": "Neutral"
        },
        {
            "CleanText": "thanks  for lakers tickets 😜 ",
            "Com": 0.4404,
            "Country": "us",
            "Emotion": "joy",
            "Emotion_Score": 0.7957911719420785,
            "Location": "Follow me  👉",
            "Neg": 0.0,
            "Neu": 0.508,
            "Polarity": 0.2,
            "Pos": 0.492,
            "Publisher": "@Clix",
            "Release": "2022-02-09 02:45:56+00:00",
            "Subj": 0.2,
            "Tweets": "thanks @bugha for lakers tickets 😜 https://t.co/thhfsx16TP",
            "Url": "https://twitter.com/twitter/statuses/1491241930654875649",
            "expression": "Subjective",
            "opinion": "Support",
            "sentiment": "Postive"
        },
        {
            "CleanText": "Lakers down 27 and the crowd is letting the Lakers hear it",
            "Com": 0.0,
            "Country": "Not Found",
            "Emotion": "joy",
            "Emotion_Score": 0.9310445939042472,
            "Location": "Behind the arc",
            "Neg": 0.0,
            "Neu": 1.0,
            "Polarity": -0.15555555555555559,
            "Pos": 0.0,
            "Publisher": "@Trevor Lane",
            "Release": "2022-02-09 04:32:53+00:00",
            "Subj": 0.2888888888888889,
            "Tweets": "Lakers down 27 and the crowd is letting the Lakers hear it",
            "Url": "https://twitter.com/twitter/statuses/1491268843464892416",
            "expression": "Subjective",
            "opinion": "No Opinion",
            "sentiment": "Negative"
        },
        {
            "CleanText": "Your Lakers basketball.\n\nLakeShow x  ",
            "Com": 0.0,
            "Country": "us",
            "Emotion": "joy",
            "Emotion_Score": 0.43546885004419766,
            "Location": "Los Angeles, CA",
            "Neg": 0.0,
            "Neu": 1.0,
            "Polarity": 0.0,
            "Pos": 0.0,
            "Publisher": "@Los Angeles Lakers",
            "Release": "2022-02-07 16:00:02+00:00",
            "Subj": 0.0,
            "Tweets": "Your Lakers basketball.\n\n#LakeShow x @Cincoro https://t.co/J9FY8g6Cfy",
            "Url": "https://twitter.com/twitter/statuses/1490716996605931522",
            "expression": "Objective",
            "opinion": "No Opinion",
            "sentiment": "Neutral"
        },
        {
            "CleanText": "A scenario told to me from someone whose identity I will protect Lakers trade Westbrook for Wall, Rockets buy Russ out, Russ signs w/ Wizards.\n\nTheir reasoning Beal/Rui/Gaff were good w/ Russ, Wiz had better win% last year. It's wild but I made a Photoshop to help visualize it. ",
            "Com": 0.8047,
            "Country": "us",
            "Emotion": "sadness",
            "Emotion_Score": 0.6953309064688552,
            "Location": "Washington, D.C.",
            "Neg": 0.0,
            "Neu": 0.816,
            "Polarity": 0.325,
            "Pos": 0.184,
            "Publisher": "@Chase Hughes",
            "Release": "2022-02-07 19:59:47+00:00",
            "Subj": 0.3916666666666667,
            "Tweets": "A scenario told to me from someone whose identity I will protect: Lakers trade Westbrook for Wall, Rockets buy Russ out, Russ signs w/ Wizards.\n\nTheir reasoning: Beal/Rui/Gaff were good w/ Russ, Wiz had better win% last year. It's wild but I made a Photoshop to help visualize it. https://t.co/j0kxcHkTmq",
            "Url": "https://twitter.com/twitter/statuses/1490777332038184962",
            "expression": "Subjective",
            "opinion": "Support",
            "sentiment": "Postive"
        },
        {
            "CleanText": "The Nets (+210) and Lakers (+450) were the championship favorites before the season started.\n\nThey both would be in the Play In Tournament if the season ended today.\n\nWho has the more disappointing season? ",
            "Com": 0.5584,
            "Country": "us",
            "Emotion": "joy",
            "Emotion_Score": 0.9999157202498071,
            "Location": "Not Found",
            "Neg": 0.084,
            "Neu": 0.721,
            "Polarity": -0.04999999999999999,
            "Pos": 0.195,
            "Publisher": "@StatMuse",
            "Release": "2022-02-07 16:48:50+00:00",
            "Subj": 0.6,
            "Tweets": "The Nets (+210) and Lakers (+450) were the championship favorites before the season started.\n\nThey both would be in the Play In Tournament if the season ended today.\n\nWho has the more disappointing season? https://t.co/oVUdtqW41H",
            "Url": "https://twitter.com/twitter/statuses/1490729277544751104",
            "expression": "Subjective",
            "opinion": "Support",
            "sentiment": "Negative"
        },
        {
            "CleanText": "A visibly confused Austin Reaves autographed a rice cooker for a fan, securing the 2022 NBA championship for the Lakers.  ",
            "Com": 0.6369,
            "Country": "ru",
            "Emotion": "joy",
            "Emotion_Score": 0.6743713364402298,
            "Location": "Southern California",
            "Neg": 0.101,
            "Neu": 0.57,
            "Polarity": -0.4,
            "Pos": 0.329,
            "Publisher": "@Silver Screen and Roll",
            "Release": "2022-02-07 17:11:54+00:00",
            "Subj": 0.7,
            "Tweets": "A visibly confused Austin Reaves autographed a rice cooker for a fan, securing the 2022 NBA championship for the Lakers. https://t.co/FBDpfAj2eL https://t.co/1cmFkUMT8l",
            "Url": "https://twitter.com/twitter/statuses/1490735082897915910",
            "expression": "Subjective",
            "opinion": "Support",
            "sentiment": "Negative"
        },
        {
            "CleanText": "Julius Randle and Knicks' video coordinator Scott King had to be separated during the Lakers game 😳\n\nRandle apparently didn't like what he was being shown, pushed King's laptop away, and then got in his face.\n\nThoughts? 🤔\n\n",
            "Com": -0.2755,
            "Country": "us",
            "Emotion": "sadness",
            "Emotion_Score": 0.7368369690476406,
            "Location": "Los Angeles, CA",
            "Neg": 0.057,
            "Neu": 0.943,
            "Polarity": -0.17500000000000002,
            "Pos": 0.0,
            "Publisher": "@ClutchPoints",
            "Release": "2022-02-07 19:09:01+00:00",
            "Subj": 0.375,
            "Tweets": "Julius Randle and Knicks' video coordinator Scott King had to be separated during the Lakers game 😳\n\nRandle apparently didn't like what he was being shown, pushed King's laptop away, and then got in his face.\n\nThoughts? 🤔\n\nhttps://t.co/VRPug4Tsjb",
            "Url": "https://twitter.com/twitter/statuses/1490764552866127873",
            "expression": "Subjective",
            "opinion": "Unsupport",
            "sentiment": "Negative"
        },
        {
            "CleanText": "The Nets with Kyrie Irving, James Harden and Kevin Durant vs. Lakers with LeBron, Anthony Davis and Russell Westbrook looked a solid bet for the NBA Finals before the season.\n\nNow we're not even sure they're making the playoffs 👀 ",
            "Com": -0.0931,
            "Country": "us",
            "Emotion": "joy",
            "Emotion_Score": 0.9940247083075047,
            "Location": "Los Angeles, CA",
            "Neg": 0.05,
            "Neu": 0.91,
            "Polarity": 0.25,
            "Pos": 0.04,
            "Publisher": "@ClutchPoints",
            "Release": "2022-02-07 13:31:28+00:00",
            "Subj": 0.4944444444444444,
            "Tweets": "The Nets with Kyrie Irving, James Harden and Kevin Durant vs. Lakers with LeBron, Anthony Davis and Russell Westbrook looked a solid bet for the NBA Finals before the season.\n\nNow we're not even sure they're making the playoffs 👀 https://t.co/NShXQN3ryW",
            "Url": "https://twitter.com/twitter/statuses/1490679607221182466",
            "expression": "Subjective",
            "opinion": "Unsupport",
            "sentiment": "Postive"
        },
        {
            "CleanText": "Since LeBron joined the Lakers in 2018, they are 127-76 when he plays.\n\nOnly three teams in the NBA have had a higher win percentage during that span 😳 ",
            "Com": 0.7003,
            "Country": "us",
            "Emotion": "fear",
            "Emotion_Score": 0.887663004205449,
            "Location": "Not Found",
            "Neg": 0.0,
            "Neu": 0.812,
            "Polarity": 0.35000000000000003,
            "Pos": 0.188,
            "Publisher": "@SportsCenter",
            "Release": "2022-02-05 02:22:36+00:00",
            "Subj": 0.6333333333333333,
            "Tweets": "Since LeBron joined the Lakers in 2018, they are 127-76 when he plays.\n\nOnly three teams in the NBA have had a higher win percentage during that span 😳 https://t.co/orWd7IdAlf",
            "Url": "https://twitter.com/twitter/statuses/1489786507342884864",
            "expression": "Subjective",
            "opinion": "Support",
            "sentiment": "Postive"
        },
        {
            "CleanText": "Lakers star Anthony Davis was among the nominees for Western Conference Player of the Week ",
            "Com": 0.0,
            "Country": "us",
            "Emotion": "fear",
            "Emotion_Score": 0.6335269494695112,
            "Location": "Los Angeles, California ",
            "Neg": 0.0,
            "Neu": 1.0,
            "Polarity": 0.0,
            "Pos": 0.0,
            "Publisher": "@Ryan Ward",
            "Release": "2022-02-07 20:35:20+00:00",
            "Subj": 0.0,
            "Tweets": "Lakers star Anthony Davis was among the nominees for Western Conference Player of the Week https://t.co/g4E2SwIao7",
            "Url": "https://twitter.com/twitter/statuses/1490786278241042432",
            "expression": "Objective",
            "opinion": "No Opinion",
            "sentiment": "Neutral"
        },
        {
            "CleanText": "Some big numbers LakeShow ",
            "Com": 0.0,
            "Country": "us",
            "Emotion": "joy",
            "Emotion_Score": 0.3271705306329551,
            "Location": "Los Angeles, CA",
            "Neg": 0.0,
            "Neu": 1.0,
            "Polarity": 0.0,
            "Pos": 0.0,
            "Publisher": "@Los Angeles Lakers",
            "Release": "2022-02-06 04:41:57+00:00",
            "Subj": 0.1,
            "Tweets": "Some big numbers #LakeShow https://t.co/Jd4Y1MjWbT",
            "Url": "https://twitter.com/twitter/statuses/1490183962139901958",
            "expression": "Subjective",
            "opinion": "No Opinion",
            "sentiment": "Neutral"
        },
        {
            "CleanText": "Russ is AWFUL. Anyone that thinks you can win a title with Russ playing a prominent role. Doesn’t know basketball. Lakers defensively are TERRIBLE",
            "Com": -0.3107,
            "Country": "us",
            "Emotion": "sadness",
            "Emotion_Score": 0.6630528632950871,
            "Location": "Not Found",
            "Neg": 0.277,
            "Neu": 0.484,
            "Polarity": -0.175,
            "Pos": 0.239,
            "Publisher": "@shannon sharpe",
            "Release": "2022-02-06 02:43:56+00:00",
            "Subj": 0.85,
            "Tweets": "Russ is AWFUL. Anyone that thinks you can win a title with Russ playing a prominent role. Doesn’t know basketball. Lakers defensively are TERRIBLE",
            "Url": "https://twitter.com/twitter/statuses/1490154262822719490",
            "expression": "Subjective",
            "opinion": "Unsupport",
            "sentiment": "Negative"
        },
        {
            "CleanText": "14 years ago today, the Lakers traded Kwame Brown, Javaris Crittenton, Aaron McKie, draft rights to Marc Gasol &amp; 2 future draft picks for Pau Gasol. \n\n😂 Stephen A. Smith...\n\n ",
            "Com": 0.0,
            "Country": "us",
            "Emotion": "fear",
            "Emotion_Score": 0.5727289646363342,
            "Location": "Los Angeles, Ca",
            "Neg": 0.0,
            "Neu": 1.0,
            "Polarity": 0.0,
            "Pos": 0.0,
            "Publisher": "@Ballislife.com",
            "Release": "2022-02-01 14:01:42+00:00",
            "Subj": 0.125,
            "Tweets": "14 years ago today, the Lakers traded Kwame Brown, Javaris Crittenton, Aaron McKie, draft rights to Marc Gasol &amp; 2 future draft picks for Pau Gasol. \n\n😂 Stephen A. Smith...\n\n https://t.co/CaboeSDINC",
            "Url": "https://twitter.com/twitter/statuses/1488512889036099584",
            "expression": "Subjective",
            "opinion": "No Opinion",
            "sentiment": "Neutral"
        },
        {
            "CleanText": "I'm not reading your trade idea if...\n- Jaylen or Jayson are involved\n- there are 3+ teams involved (not named the Thunder)\n- it involves the Lakers in any way",
            "Com": 0.0,
            "Country": "Not Found",
            "Emotion": "joy",
            "Emotion_Score": 0.8401727740658851,
            "Location": "CelticsBlog.com",
            "Neg": 0.0,
            "Neu": 1.0,
            "Polarity": 0.0,
            "Pos": 0.0,
            "Publisher": "@CelticsBlog",
            "Release": "2022-02-07 18:07:54+00:00",
            "Subj": 0.0,
            "Tweets": "I'm not reading your trade idea if...\n- Jaylen or Jayson are involved\n- there are 3+ teams involved (not named the Thunder)\n- it involves the Lakers in any way",
            "Url": "https://twitter.com/twitter/statuses/1490749174534578181",
            "expression": "Objective",
            "opinion": "No Opinion",
            "sentiment": "Neutral"
        },
        {
            "CleanText": "At No. 10 on our list of the NBA's Top 75 , I present...\n\nKobe...Bean...Bryant - through the eyes of Steph Curry, Devin Booker and DeMar DeRozan.\n\nThe Mamba Mentality. The mentor role. Memories of a fallen friend. His impact remains...\n\n",
            "Com": 0.0772,
            "Country": "al",
            "Emotion": "joy",
            "Emotion_Score": 0.9994587479396845,
            "Location": "Northern California",
            "Neg": 0.11,
            "Neu": 0.773,
            "Polarity": 0.25,
            "Pos": 0.117,
            "Publisher": "@Sam Amick",
            "Release": "2022-02-07 16:26:22+00:00",
            "Subj": 0.25,
            "Tweets": "At No. 10 on our list of the NBA's Top 75 @TheAthletic, I present...\n\nKobe...Bean...Bryant - through the eyes of Steph Curry, Devin Booker and DeMar DeRozan.\n\nThe Mamba Mentality. The mentor role. Memories of a fallen friend. His impact remains...\n\nhttps://t.co/XaY3DVWjB6",
            "Url": "https://twitter.com/twitter/statuses/1490723621517414400",
            "expression": "Subjective",
            "opinion": "Support",
            "sentiment": "Postive"
        },
        {
            "CleanText": "Nicki Minaj received a HUGE applause at Clippers-Lakers tonight. She made a surprise appearance to promote an exclusive look at her new song. ",
            "Com": 0.876,
            "Country": "us",
            "Emotion": "surprise",
            "Emotion_Score": 0.956022703326368,
            "Location": "Los Angeles, CA",
            "Neg": 0.0,
            "Neu": 0.571,
            "Polarity": 0.2681818181818182,
            "Pos": 0.429,
            "Publisher": "@Farbod Esnaashari",
            "Release": "2022-02-04 04:37:54+00:00",
            "Subj": 0.6772727272727272,
            "Tweets": "Nicki Minaj received a HUGE applause at Clippers-Lakers tonight. She made a surprise appearance to promote an exclusive look at her new song. https://t.co/jIGOddpdPf",
            "Url": "https://twitter.com/twitter/statuses/1489458165984862210",
            "expression": "Subjective",
            "opinion": "Support",
            "sentiment": "Postive"
        },
        {
            "CleanText": "“LeBron back!!!”\n\nLakers fans ",
            "Com": 0.0,
            "Country": "gb",
            "Emotion": "sadness",
            "Emotion_Score": 0.44284226701901397,
            "Location": "The Field",
            "Neg": 0.0,
            "Neu": 1.0,
            "Polarity": 0.0,
            "Pos": 0.0,
            "Publisher": "@Josiah Johnson",
            "Release": "2022-02-06 00:44:59+00:00",
            "Subj": 0.0,
            "Tweets": "“LeBron back!!!”\n\nLakers fans: https://t.co/InJLO1Et3Y",
            "Url": "https://twitter.com/twitter/statuses/1490124327500455944",
            "expression": "Objective",
            "opinion": "No Opinion",
            "sentiment": "Neutral"
        }
    ],
    "tweets_num": 29
}