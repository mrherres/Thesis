import os
from xml.etree import ElementTree as Et



def retrieve_xml(wd):
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


# def main():
#    working_directory = "/home/twan/Documents/Thesis/kranten_pd_voorbeeld/1618/06/14/DDD_ddd_010500649_mpeg21"
#    articles = retrieve_xml(working_directory)
#    return articles
