import os
from xml.etree import ElementTree as ET



def retrieve_xml(wd):
    article_list = []
    liist = os.listdir(wd)
    for item in liist:
        ending = item[-15:]
        if ending == "articletext.xml":
            with open(wd + "/" + item) as doc:
                document = ET.parse(doc)
                root =  document.getroot()
                text = root.find("p").text
                article_list.append(text)
    return article_list

    
# def main():
#    working_directory = "/home/twan/Documents/Thesis/kranten_pd_voorbeeld/1618/06/14/DDD_ddd_010500649_mpeg21"
#    articles = retrieve_xml(working_directory)
#    return articles
    
    
    
if __name__ == "__main__":
    main()
