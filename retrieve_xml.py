import os
from xml.etree import ElementTree as Et
from lxml import html
import re
from os import listdir


def retrieve_xml(wd):
    # This function will collect the texts from xml files from the Delpher dataset
    # It writes the texts to a list, which is then passed on to main.py
    article_list = []
    a = 0
    liist = os.listdir(wd)
    for month in liist:
        if month == "02":
            print(f"Ended {a}")
            break
        for i, day in enumerate(os.listdir(wd + "\\" + month)):
            for newspaper in os.listdir(wd + "\\" + month + "\\" + day):
                for article in os.listdir(wd + "\\" + month + "\\" + day + "\\" + newspaper):
                    ending = article[-15:]
                    if ending == "articletext.xml" and a <= 99:
                        a += 1
                        path = wd + "\\" + month + "\\" + day + "\\" + newspaper + "\\" + article
                        with open(path, encoding="utf8") as doc:
                            document = Et.parse(doc)
                            root = document.getroot()
                            text = root.find("p").text
                            article_list.append(text)
    return article_list


def dbnl_xml():
    # This is a test function to collect xml from the DBNL dataset
    # Sterre gave me the tip to use lxml instead of xml ElementTree, since that worked better
    # Change the path names accordingly
    path = "passages/jeugdliteratuur"
    files = [f for f in listdir(path)]
    for i in range(len(files)):
        print(i)
        with open("passages/jeugdliteratuur/" + files[i], encoding="utf-8") as a:
            text = ""
            tree = html.parse(a)
            # set this xpath to //div for jeugdliteratuur, //p for the rest
            paragraphs = tree.xpath('//p')
            for paragraph in paragraphs:
                text += "\n" + paragraph.text_content()
            filename = files[i][:-4]
            with open("passages/jeugdliteratuur/" + filename + ".txt", "w", encoding="utf8") as b:
                b.writelines(text)


def main():
    dbnl_xml()


if __name__ == "__main__":
    main()
