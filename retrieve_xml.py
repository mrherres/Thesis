import os
from xml.etree import ElementTree as Et


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
    # I have not got this working yet, though
    # ------------------------------------------------------------
    # with open("passages/drama/1654_vond001luci01_01.xml") as f:
    #     lines = f.readlines()
    #     text = ""
    #     for i in lines:
    #         text = i
    #         text = text.replace("&nbsp", "placeholder")
    #         with open("passages/test/a.xml", "a") as b:
    #             b.writelines(text)
    with open("passages/test/a.xml", encoding="utf-8") as a:
        document = Et.parse(a)
        print(document)
        root = document.getroot()
        print(root.tag)
        text = root.findall("./text/body/*/*/*")
        for i in text:
            if i.text is not None:
                print(i.text)


def main():
    dbnl_xml()
#    working_directory = "/home/twan/Documents/Thesis/kranten_pd_voorbeeld/1618/06/14/DDD_ddd_010500649_mpeg21"
#    articles = retrieve_xml(working_directory)
#    return articles


if __name__ == "__main__":
    main()
