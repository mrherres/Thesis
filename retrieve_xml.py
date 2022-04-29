import os
from xml.etree import ElementTree as ET



def retrieve_xml(wd):
    liist = os.listdir(wd)
    for item in liist:
        ending = item[-15:]
        if ending == "articletext.xml":
            with open(wd + "/" + item) as doc:
                document = ET.parse(doc)
                root =  document.getroot()
                text = root.find("p").text
                convert_text(text)
                
def convert_text(text):
    print(text)
    print("\n")
    
    
    
    
    
    
def main():
    working_directory = "/home/twan/Documents/Thesis/kranten_pd_voorbeeld/1618/06/14/DDD_ddd_010500649_mpeg21"
    retrieve_xml(working_directory)
    
    
    
if __name__ == "__main__":
    main()
