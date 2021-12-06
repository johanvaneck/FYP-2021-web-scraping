# script to prepare data for analysis
# author: Johan van Eck

# import all neccessary modules
import pickle
import matplotlib.pyplot as plt

from collections import Counter
from wordcloud import WordCloud, STOPWORDS


class Company:
    # each Company object has four attributes
    def __init__(self, name: str, description: str, pros=[], cons=[]):
        self.name = name
        self.description = description
        self.pros = pros
        self.cons = cons

    # method to easily print data for an instance of a Company
    def print_info(self):
        print("Name: " + str(self.name))
        print("Description: " + str(self.description))
        print("Pros: " + str(self.pros))
        print("Cons: " + str(self.cons))

    # method to obtain a list of useful information from a Company
    def listify(self):
        return [self.name,
                len(self.pros),
                len(self.cons),
                self.description] 


# function to load an object from a pickle file
def load_object(filename):
    try:
        with open(filename + ".pickle", "rb") as f:
            return pickle.load(f)
    except Exception as ex:
        print(ex)


### start ###

# load list of Companies from pickle file and store in companies variable
companies = load_object("companies")

# print total companies
print("Total number of comapanies: " + str(len(companies)))

# count total comments extracted from website
total_pro_count = 0
total_con_count = 0
for company in companies:
    total_pro_count = total_pro_count + len(company.pros)
    total_con_count = total_con_count + len(company.cons)

print("Total number of pro comments: {}\nTotal number of con comments: {}".format(total_pro_count, total_con_count))

# concatenate all strings into one large string
des_string = ""
pro_string = ""
con_string = ""
for company in companies:
    des_string += company.description.replace(",", "")
    for pro in company.pros:
        pro_string += pro
    for con in company.cons:
        con_string += con

# split each long string into a list of words
des_words = des_string.split()
pro_words = pro_string.split()
con_words = con_string.split()

print("\nTotal words in all descriptions: {}".format(len(des_words)))
print("Total words in all pro comments: {}".format(len(pro_words)))
print("Total words in all con comments: {}".format(len(con_words)))

STOPWORDS.add('-')
print("\nNumber of stopwords: " + str(len(STOPWORDS)))

des_words = [w for w in des_words if not w.lower() in STOPWORDS]
pro_words = [w for w in pro_words if not w.lower() in STOPWORDS]
con_words = [w for w in con_words if not w.lower() in STOPWORDS]


print("\nTotal useful words in all descriptions: {}".format(len(des_words)))
print("Total useful words in all pro comments: {}".format(len(pro_words)))
print("Total useful words in all con comments: {}".format(len(con_words)))

# count number of occurences of words in each string
des_counter = Counter(des_words)
pro_counter = Counter(pro_words)
con_counter = Counter(con_words)

# function to print data for top_num words in a Counter object
def print_top_counter(counter: Counter, top_num):
    for word in counter.most_common(top_num):
        print("{} & {} \\\\ \\hline".format(word[0], word[1]))


# print information
top_n = 10
print("\nMost common words in descriptions: ")
print_top_counter(des_counter, top_n)
print("\nMost common words in pro comments: ")
print_top_counter(pro_counter, top_n)
print("\nMost common words in con comments: ")
print_top_counter(con_counter, top_n)

# concatenate a list of words
def concat_list(list_words: list):
    big_string = ''
    for word in list_words:
        big_string += word
    return big_string


# function to create a basic bar plot using a Counter object
def bar_plot(counter: Counter, top_num=10):
    x = []
    y = []
    # fig = plt.figure()
    for element in counter.most_common(top_num):
        x.append(element[0])
        y.append(element[1])
    plt.barh(x, y)
    # plt.savefig(name)
    plt.show()

# create bar plots
# bar_plot(des_counter)
# bar_plot(pro_counter)
# bar_plot(con_counter)


# function to generate standard Wordcloud object
def wordcloud(words):
    return WordCloud(width=800,
                     height=800,
                     background_color='white',
                     stopwords=STOPWORDS,
                     min_font_size=10).generate(words)

# plot wordcloud
# wordcloud(des_string).to_file('wc-description.png')
# wordcloud(pro_string).to_file('wc-pros.png')
# wordcloud(con_string).to_file('wc-cons.png')
