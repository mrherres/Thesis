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
                
                
def write_article(articles, wd):
    name = wd[49:53] + "_" + wd[54:56] + "_" + wd[57:59] + "_"
    for i, text in enumerate(articles):
        ftext = open("passages/" + name + str(i) + ".txt", "w")
        ftext.write(text)
        ftext.close()

def main():
    # webscraper()
    #split()
    wd = "/home/twan/Documents/Thesis/kranten_pd_voorbeeld/1618/06/14/DDD_ddd_010500649_mpeg21"
    articles = retrieve_xml(wd)
    write_article(articles, wd)


if __name__ == "__main__":
    main()
