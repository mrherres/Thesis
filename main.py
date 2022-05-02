from bs4 import BeautifulSoup
from urllib.request import urlopen
from os import listdir
from retrieve_xml import retrieve_xml


def webscraper():
    url = "https://www.gutenberg.org/files/42263/42263-0.txt"
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    print(soup)


def create_passages():
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


def write_article(articles, wd):
    name = wd[13:17] + "_"
    for i, text in enumerate(articles):
        ftext = open("passages\\newspaper\\" + name + str(i) + ".txt", "w", encoding="utf8")
        ftext.write(text)
        ftext.close()
        print("writing..")
    print("finished writing")



def main():
    # webscraper()
    # split()
    # Change the working directory accordingly to the files you want to convert
    wd = "E:\\Downloads\\1820"
    articles = retrieve_xml(wd)
    write_article(articles, wd)


if __name__ == "__main__":
    main()
