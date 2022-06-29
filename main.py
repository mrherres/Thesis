import spacy
import csv
import random
import pickle
import pandas as pd
import string
import matplotlib.pyplot as plt

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


def create_passages():
    # This was a test function to divide txt files in to passages with a length of 100 words
    # However, it was not used for my thesis
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
    # Test function to try out the Spacy model, eventually broadened to add POS and DEP tags for the passages
    #
    nlp = spacy.load("nl_core_news_sm")
    path = "passages/poezie"
    files = [f for f in listdir(path)]
    # stats = []
    for i in files:
        print(i)
        some_string = "Word\tPos\tDep\n"
        if i[-3:] == "txt":
            with open(path + "//" + i, encoding="utf8") as text:
                for word in text:
                    doc = nlp(word)
                    for stuff in doc:
                        pos_string = ""
                        dep_string = ""
                        word_string = ""
                        if stuff.text not in string.punctuation:
                            # print(stuff.text, stuff.pos_)
                            # pos_string += stuff.pos_ + " "
                            # dep_string += stuff.dep_ + " "
                            # word_string += stuff.text + " "
                            pos_string += stuff.pos_
                            dep_string += stuff.dep_
                            word_string += stuff.text
                        some_string += word_string + "\t" + pos_string + "\t" + dep_string + "\n"
                with open("dataframes/poezie/" + i[:-4] + ".tokens", "w", encoding="utf8") as some_to_csv:
                    some_to_csv.write(some_string)

            # data = [i[:-4], pos_string, dep_string, word_string]
            # stats.append(data)
    # df = pd.DataFrame(stats, columns=["Filename", "Pos", "Dep", "Word"])
    # df.to_pickle("dataframes/dataframe_newspaper")


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


def gather_scores1():
    # This function will create a pickle with all the scores of the annotations in them
    path = "C:\\Users\\twant\\Desktop\\Annotations\\Twan"
    files = [f for f in listdir(path)]
    genre = path[9:12]
    with open("scores//Twan - twan.csv", "r", encoding="utf8") as f:
        csvreader = csv.reader(f)
        header = next(csvreader)
        rows = []
        for row in csvreader:
            rows.append(row)
    # print(files)
    with open("scores/score_dict", "rb") as y:
        score_dict = pickle.loads(y.read())
    # score_dict = {}
    # print(rows[1][2])
    # print(score_dict)
    for i, row in enumerate(rows):
        agency = row[1]
        event_sequencing = row[2]
        world_making = row[3]
        if agency == "":
            agency = 1
            event_sequencing = 1
            world_making = 1
        # print(f"{agency} and {event_sequencing} and {world_making}, with {i+1}")
        file = files[i]
        file_name = file[:-4]
        if file_name not in score_dict:
            score_dict[file_name] = [agency, event_sequencing, world_making]
        else:
            score_dict[file_name] += [agency, event_sequencing, world_making]
        # score_dict[file_name] = [agency, event_sequencing, world_making]
    print(len(score_dict))

    with open("scores/score_dict", "wb") as x:
        pickle.dump(score_dict, x)


def gather_scores2():
    # This function will load all annotations per annotator into a pickled dictionary
    # These annotations originate from Sterre her round of annotations
    # Also here, adjust the path names accordingly
    path = "passages/poezie"
    genre = path[9:12]
    files = [f for f in listdir(path)]
    with open("scores//passages_Twan_5 - Sheet1.csv", "r", encoding="utf8") as f:
        csvreader = csv.reader(f)
        header = next(csvreader)
        rows = []
        for row in csvreader:
            rows.append(row)
    with open("scores/score_dict2", "rb") as a:
        score_dict2 = pickle.loads(a.read())
    # score_dict2 = {}
    # print(rows[1][2])
    for i in files:
        filename = genre + "_" + i[:-4]
        # print(filename)
        for row in rows:
            # print(row[2])
            agency = row[3]
            event_sequencing = row[4]
            world_making = row[5]
            if agency == "":
                agency = 1
                event_sequencing = 1
                world_making = 1
            # print(i[4:-7])
            if row[2] == i[5:-7] and i[-3:] == "txt":
                if filename not in score_dict2:
                    score_dict2[filename] = [agency, event_sequencing, world_making]
                else:
                    score_dict2[filename] += [agency, event_sequencing, world_making]
    print(score_dict2)
    print(len(score_dict2))
    with open("scores/score_dict2", "wb") as y:
        pickle.dump(score_dict2, y)


def average_scores():
    # This function needs to be run twice, with the paths set to the previous made score dictionaries
    # It then averages all scores and appends them to a new final dictionary
    with open("scores/score_dict2", "rb") as y:
        score_dict = pickle.loads(y.read())
    # some_string = "filename, avg_score\n"
    some_string = ""
    for key in score_dict.keys():
        scores = score_dict[key]
        filename = key[4:]
        print(filename)
        print(scores)
        if len(scores) > 6 < 10:
            agency = int(scores[0]) + int(scores[3]) + int(scores[6])
            event_sequencing = int(scores[1]) + int(scores[4]) + int(scores[7])
            world_making = int(scores[2]) + int(scores[5]) + int(scores[8])
            average_score = [agency / 3, event_sequencing / 3, world_making / 3]
            avg_score = (agency + event_sequencing + world_making) / 9
            some_string += filename + "," + str(avg_score) + "\n"
            new_values = [scores, average_score]
            score_dict[key] = new_values
        elif len(scores) > 3 < 6:
            agency = int(scores[0]) + int(scores[3])
            event_sequencing = int(scores[1]) + int(scores[4])
            world_making = int(scores[2]) + int(scores[5])
            average_score = [agency / 2, event_sequencing / 2, world_making / 2]
            avg_score = (agency + event_sequencing + world_making) / 6
            some_string += filename + "," + str(avg_score) + "\n"
            new_values = [scores, average_score]
            score_dict[key] = new_values
        else:
            pass

    # with open("scores/fin_score_dict2.txt", "wb") as x:
    #     pickle.dump(score_dict, x)
    with open("scores/avg_score.csv", "w") as y:
        y.write(some_string)


def remove_long_tags():
    # This function will remove some lines from the dataframes, because some of them contained more than 3 values,
    # which should not happen
    path = "dataframes/poezie"
    files = [f for f in listdir(path)]
    for file in files:
        new_some = ""
        print(file)
        with open(path + "/" + file, "r", encoding="utf8") as f:
            some = f.readlines()
            print(len(some))
            for index, line in enumerate(some):
                tag = line.split("\t")
                # print(f'Sentence{a} is {b}')
                if len(tag) > 3:
                    some.pop(index)
            for tag in some:
                new_some += tag
        with open(path + "/" + file, "w", encoding="utf8") as f:
            f.write(new_some)


def create_pandaframe():
    # This function can be ignored, since it was not used
    path = "passages/letterkunde"
    files = [f for f in listdir(path)]
    main_list = []
    for file in files:
        if file[-3:] == "txt":
            with open(path + "/" + file, "r", encoding="utf8") as f:
                some = f.read()
                some_list = ["NEG", "letterkunde", "5s", file[:-4], some]
                main_list.append(some_list)
    df = pd.DataFrame(main_list, columns=["narr", "genre", "kind", "fname", "text"])
    main_df = pd.read_pickle("dataframes/all.pickle")
    main_df = main_df.append(df)
    main_df.to_pickle("dataframes/all.pickle")


def copy_tsv():
    # In order to create a graph with pandas, the dates need to have days and months attached to them
    # This function will do just that so that the graph can be made
    path = "new_results/experimental-data"
    files = [f for f in listdir(path)]
    for tsv in files:
        with open(path + '/copy_' + tsv, 'a') as ntsv:
            ntsv.write("Date\tProbability\n")
        with open(path + '/' + tsv, "r") as ctsv:
            csvreader = csv.reader(ctsv, delimiter="\t")
            header = next(csvreader)
            rows = []
            for row in csvreader:
                rows.append(row)
            for row in rows:
                filename, prob = row
                # print(f'{filename[:4]} and {prob}')
                year = filename[:4]
                with open(path + '/copy_' + tsv, 'a') as ntsv:
                    ntsv.write(year + "-12-31\t" + prob + "\n")


def make_graph():
    # As the title suggests, create the graph for all predicted probabilities of narrative
    fic_df = pd.read_csv("new_results/graph_data/copy_within-401__fictie.tsv", delimiter="\t")
    fic_df['Date'] = pd.to_datetime(fic_df['Date'])
    five_annually_fic = fic_df.resample('5A', on='Date').mean()

    jeu_df = pd.read_csv("new_results/graph_data/copy_within-401__jeugdliteratuur.tsv", delimiter="\t")
    jeu_df['Date'] = pd.to_datetime(jeu_df['Date'])
    five_annually_jeu = jeu_df.resample('5A', on='Date').mean()

    let_df = pd.read_csv("new_results/graph_data/copy_within-401__letterkunde.tsv", delimiter="\t")
    let_df['Date'] = pd.to_datetime(let_df['Date'])
    five_annually_let = let_df.resample('5A', on='Date').mean()

    new_df = pd.read_csv("new_results/graph_data/copy_within-401__newspaper.csv", delimiter="\t")
    new_df['Date'] = pd.to_datetime(new_df['Date'])
    five_annually_new = new_df.resample('5A', on='Date').mean()

    non_df = pd.read_csv("new_results/graph_data/copy_within-401__non-fictie.tsv", delimiter="\t")
    non_df['Date'] = pd.to_datetime(non_df['Date'])
    five_annually_non = non_df.resample('5A', on='Date').mean()

    poe_df = pd.read_csv("new_results/graph_data/copy_within-401__poezie.tsv", delimiter="\t")
    poe_df['Date'] = pd.to_datetime(poe_df['Date'])
    five_annually_poe = poe_df.resample('5A', on='Date').mean()

    taa_df = pd.read_csv("new_results/graph_data/copy_within-401__taalkunde.tsv", delimiter="\t")
    taa_df['Date'] = pd.to_datetime(taa_df['Date'])
    five_annually_taa = taa_df.resample('5A', on='Date').mean()

    plt.plot(five_annually_fic.index, five_annually_fic['Probability'], label="Fiction")
    plt.plot(five_annually_jeu.index, five_annually_jeu['Probability'], label="Childen Literature")
    plt.plot(five_annually_let.index, five_annually_let['Probability'], label="Literature")
    plt.plot(five_annually_new.index, five_annually_new['Probability'], label="Newspaper")
    plt.plot(five_annually_non.index, five_annually_non['Probability'], label="Non-fiction")
    plt.plot(five_annually_poe.index, five_annually_poe['Probability'], label="Poetry")
    plt.plot(five_annually_taa.index, five_annually_taa['Probability'], label="Linguistics")
    plt.legend(loc=2)
    plt.xlabel("Year")
    plt.ylabel("Probability Narrative")
    plt.show()


def main():
    # Print out an exclamation mark to see that the program is running
    print("!")
    # These are all functions that have to do with collecting annotation scores and averaging them
    # gather_scores1()
    # gather_scores2()
    # average_scores()
    # -------------------------------------------------------------------------
    # These are all function that have to do with generating and preparing the annotations
    # generate_passages()
    # divide_passages()
    # create_passages()
    # prepare_annotations()
    # collect_genres()
    # --------------------------------------------------------------------------
    # Change the working directory accordingly to the files you want to convert
    # wd = "E:\\Downloads\\1870"
    # articles = retrieve_xml(wd)
    # write_article(articles, wd)
    # --------------------------------------------------------------------------
    # Code for POS and DEP tagging
    # text_tokenizer()
    # remove_long_tags()
    # create_pandaframe()
    # These are functions that have to do with preparing and making the graph
    # copy_tsv()
    # make_graph()
    # --------------------------------------------------------------------------
    # Code for retrieving text from DBNL files
    # path = "passages/drama/1654_vond001luci01_01.xml"
    # dbnl_xml()
    # --------------------------------------------------------------------------
    # These are all test functions and can be ignored
    # format_file(path)
    # split()


if __name__ == "__main__":
    main()
