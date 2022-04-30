from bs4 import BeautifulSoup
from urllib.request import urlopen
from os import listdir


def webscraper():
    url = "https://www.gutenberg.org/files/42263/42263-0.txt"
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    print(soup)


def split():
    files = [f for f in listdir("files")]
    counter = 0
    for f in files:
        passage = ""
        file = open("files/" + f, "r")
        text = file.read()
        for word in text.split():
            if len(passage.split()) >= 100 and word[-1] == ".":
                npassage = passage + " " + word
                passage = npassage
                fpassage = open("passages/p" + str(counter) + "_lorem.txt", "w")
                fpassage.write(passage)
                fpassage.close()
                counter += 1
                passage = ""
            else:
                npassage = passage + " " + word
                passage = npassage


def main():
    # webscraper()
    split()


if __name__ == "__main__":
    main()
