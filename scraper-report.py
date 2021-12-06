# webscraper created for extracting text data from a website
# author: Johan van Eck

# import all neccessary modules
import pickle

from urllib.request import urlopen
from bs4 import BeautifulSoup


# object to store data obtained from company in a consistant format
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

    # method intended for static use to print information for a list of companies
    def print_list(com_list):
        for c in com_list:
            print(''.join(f'{c:3}' for c in c.listify()))

# store an object for later use
def save_object(obj, name):
    try:
        with open(name + ".pickle", "wb") as f:
            pickle.dump(obj, f, protocol=pickle.HIGHEST_PROTOCOL)
    except Exception as ex:
        print(ex)


### start ###        

# url for Software Advice
url = "https://www.softwareadvice.com/za/construction/p/all/"
# get HTML code from the website URLs
html = urlopen(url)
# create a new BeautifulSoup object containing data from the main page
soup = BeautifulSoup(html, "html.parser")
# extract all product titles from the main page
titles = soup.find_all("p", {"class": "product-title product-title-desktop ui"})
# extract all short descriptions from the main page
short_des = soup.find_all("p", {"class": "product-description small"})

# create an empty list for storing Company objects
companies = []
# create an empty list for storing names of companies that encounter errors
errors = []
# loop for the purpose of accessing elements at corresponding indices
for i in range(len(titles)):
    # enclose with try except statement to prevent program failure due to one company's url failure
    try:
        # get the url for the link to the page containing each company's info from the read more element
        read_more_url = short_des[i].a["href"]
        # create a new BeatifulSoup object with the HTML code from the company's url
        temp_soup = BeautifulSoup(urlopen(read_more_url), "html.parser")
        # get the product information from the temp_soup variable by using find() method
        product_content = temp_soup.find("p", {"class": "ui product-content"})
        # enclose with try except statement to prevent program failure due to one company's review url failure
        try:
            # create a url for each company accessing the "reviews" page
            review_url = read_more_url + "reviews/"
            # create a new BeautifulSoup object with the HTML from the company's "reviews" page
            review_soup = BeautifulSoup(urlopen(review_url), "html.parser")
            # collect all containers containing reviews for the current company
            review_containers = review_soup.find_all(
                "div", {"class": "review-copy-container"})
        except:
            # for companies with no "reviews" page, gather basic information from company page
            review_containers = temp_soup.find_all("div", {"class": "review-copy-container"})
        # create two variables to track the amount of pro and con comments from each container per company
        num_pros = 0
        num_cons = 0
        # create two empty lists to store comments for pros and cons
        pros = []
        cons = []
        # loop through each container of the current company
        for container in review_containers:
            # extract all p-tags from the container with contains data
            p_tags = container.findChildren("p", recursive=False)
            # loop through each p-tag to search for elements containing pro's or con's and store them
            for j in range(len(p_tags)):
                if p_tags[j].text == "Pros":
                    pros.append(p_tags[j + 1].text)
                    num_pros = num_pros + 1
                elif p_tags[j].text == "Cons":
                    cons.append(p_tags[j + 1].text)
                    num_cons = num_cons + 1
        # add current company's extracted data within a Company object to the list of companies
        companies.append(
            Company(titles[i].text, product_content.text, pros, cons))
        # print a status update after each company has been added
        print(titles[i].text + " added succesfully.")
        print("\tPros: " + str(num_pros))
        print("\tCons: " + str(num_cons))
        print("Current number of companies: " + str(len(companies)))
    except:
        # if the current company occurs any errors, add its title to the list of errors
        errors.append(str(titles[i].text))
        print("ERROR: " + str(titles[i].text))
# store the list of companies and errors into a pickle file for later access
save_object(errors, "errors")
save_object(companies, "companies")