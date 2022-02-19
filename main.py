import threading
from website import create_app
import website.news

def main():
    if __name__ == '__main__':
        app.run(port=8001, debug = True)

app = create_app()

# for getting the exploreNews newlist
# by calling the funciton from new.py and app
# threading.Thread(target=website.news.toNewlist(app)).start()
# main()

