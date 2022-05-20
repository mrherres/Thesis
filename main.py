import spacy
import csv
import random
from spacy.lang.nl.examples import sentences

from bs4 import BeautifulSoup
from urllib.request import urlopen
from os import listdir, replace, system
from retrieve_xml import retrieve_xml, dbnl_xml


def collect_genres():
    # This function will divide files from the DBNL dataset according to their genre
    # It also rewrites two genres, since it makes it easier to refer to those
    file = open("files/meta_data.csv", encoding="ISO8859-1")
    csvreader = csv.reader(file, delimiter=";")
    rows = []
    for row in csvreader:
        rows.append(row)
    for row in rows:
        filename = row[0]
        year = row[7]
        genre = row[-1]
        if genre == "sec - letterkunde":
            genre = "letterkunde"
        elif genre == "sec - taalkunde":
            genre = "taalkunde"
        # print(listdir("E:\\Thesis_data"))
        filename += "_01.xml"
        # print(f'{filename}')
        if filename in listdir("E:\\Thesis_data"):
            replace("E:\\Thesis_data\\" + filename, "passages/" + genre + "/" + year + "_" + filename)


def webscraper(url):
    # This function can be ignored, since I won't be using it or my thesis
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    print(soup)


def create_passages():
    # This was a test function to divide txt files in to passages with a length of 100 words
    # However, this function was not used as it was easier to do it by hand,
    # because some files are smaller than 100 words.
    files = [f for f in listdir("annotations/newspaper")]
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
    # This function will write collected texts from the Delpher dataset to the right files
    # It adds the year and number of file in the title
    name = wd[13:17] + "_"
    for i, text in enumerate(articles):
        ftext = open("passages\\newspaper\\" + name + str(i) + ".txt", "w", encoding="utf8")
        ftext.write(text)
        ftext.close()
        print("writing..")
    print("finished writing")


def text_tokenizer():
    # Test function to try out the Spacy model
    with open("E:\\PycharmProjects\\Thesis\\passages\\newspaper\\1770_11.txt") as text:
        nlp = spacy.load("nl_core_news_sm")
        for word in text:
            doc = nlp(word)
            for i in doc:
                print(i.text, i.lemma)


def format_file(path):
    with open(path, "r") as file:
        s = ""
        for i in file:
            s += i.rstrip() + " "
    with open(path, "w") as newfile:
        newfile.write(s)


def fairy_tales():
    # This function can be ignored, since I won't be using it or my thesis
    a = 0
    with open("passages/test/pg22555.txt", "r") as f:
        for i in f.readlines():
            if len(i) <= 8 and i != "\n":
                print(i)
                a += 1
        print(a)


def generate_passages():
    # This function will copy 25 random seeded files to the annotation folder
    # Make sure to change the paths according to the files you want to copy
    files = [f for f in listdir("passages/taalkunde")]
    random.seed(420)
    size = len(files)
    for x in range(25):
        value = random.randint(0, size)
        file = files[value]
        system("copy E:\\PycharmProjects\\Thesis\\passages\\taalkunde\\" + file +
               " E:\\PycharmProjects\\Thesis\\annotations\\taalkunde\\" + file)


def divide_passages():
    # This function will divide the passages in the annotation's folder, and will divide them across the annotators.
    # Each passage will be annotated by three individual annotators.
    # Please set the genre accordingly.
    genre = "newspaper"
    genre_abbr = genre[:3]
    files = [f for f in listdir("annotations/" + genre)]
    annotator = 0
    for i in files:
        if i[-3:] == "txt":
            for x in range(3):
                if annotator == 0:
                    print("Sterre")
                    system("copy E:\\PycharmProjects\\Thesis\\annotations\\" + genre + "\\" + i +
                           " C:\\Users\\twant\\Desktop\\Annotations\\Sterre\\" + genre_abbr + "_" + i)
                    annotator += 1
                elif annotator == 1:
                    print("Julius")
                    system("copy E:\\PycharmProjects\\Thesis\\annotations\\" + genre + "\\" + i +
                           " C:\\Users\\twant\\Desktop\\Annotations\\Julius\\" + genre_abbr + "_" + i)
                    annotator += 1
                elif annotator == 2:
                    print("Max")
                    system("copy E:\\PycharmProjects\\Thesis\\annotations\\" + genre + "\\" + i +
                           " C:\\Users\\twant\\Desktop\\Annotations\\Max\\" + genre_abbr + "_" + i)
                    annotator += 1
                elif annotator == 3:
                    print("Karlo")
                    system("copy E:\\PycharmProjects\\Thesis\\annotations\\" + genre + "\\" + i +
                           " C:\\Users\\twant\\Desktop\\Annotations\\Karlo\\" + genre_abbr + "_" + i)
                    annotator += 1
                elif annotator == 4:
                    print("Twan")
                    system("copy E:\\PycharmProjects\\Thesis\\annotations\\" + genre + "\\" + i +
                           " C:\\Users\\twant\\Desktop\\Annotations\\Twan\\" + genre_abbr + "_" + i)
                    annotator = 0
            print("Moved to  3 annotators! Moving on to next passage")


def prepare_annotations():
    # This function will make all passages into one big string and add a header with seperations (the +)
    # so that spreadsheets can automatically load all the texts.
    # Make sure to adjust the path and file names according to the annotators.
    path = "C:\\Users\\twant\\Desktop\\Annotations\\Twan"
    files = [f for f in listdir(path)]
    somme_string = "Text+ Agency+ Event Sequencing+ World Making \n"
    for x in files:
        with open(path + "\\" + x, encoding="utf8") as let:
            for text in let:
                for char in text:
                    if char != "\n" and char != "\t":
                        somme_string += char
                somme_string += "+ + + \n"
    with open("annotations/twan.txt", "w", encoding="utf8") as newfile:
        newfile.write(somme_string)


def main():
    print("!")
    # These are all function that have to do with generating and preparing the annotations
    # generate_passages()
    # divide_passages()
    # create_passages()
    # prepare_annotations()
    # collect_genres()
    # --------------------------------------------------------------------------
    # These are all test functions and can be ignored
    # path = "passages\\biology\\1786_0.txt"
    # format_file(path)
    # webscraper(url)
    # split()
    # --------------------------------------------------------------------------
    # Change the working directory accordingly to the files you want to convert
    # wd = "E:\\Downloads\\1870"
    # articles = retrieve_xml(wd)
    # write_article(articles, wd)
    # --------------------------------------------------------------------------
    # Code for lemmatization etc. Is a wip
    # text_tokenizer()
    # --------------------------------------------------------------------------
    # Code for retrieving text from DBNL files
    # path = "passages/drama/1654_vond001luci01_01.xml"
    # dbnl_xml(path)
    # --------------------------------------------------------------------------
    # Test function, can be ignored
    # fairy_tales()


if __name__ == "__main__":
    main()
