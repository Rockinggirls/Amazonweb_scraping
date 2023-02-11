from bs4 import BeautifulSoup
import requests
import csv


# Function to extract Product Title


def get_title(soup):

    try:
        # Outer Tag Object
        title = soup.find("span", attrs={'id': 'productTitle'})

        # Inner NavigatableString Object
        title_value = title.string

        # Title as a string value
        title_string = title_value.strip()

    except AttributeError:
        title_string = ""

    return title_string

# Function to extract Product Price


def get_price(soup):

    try:
        price = soup.find(
            "span", attrs={'class': 'a-offscreen'}).string.strip()

    except AttributeError:

        try:
            # If there is some deal price
            price = soup.find(
                "span", attrs={'class': 'a-price-whole'}).string.strip()

        except:
            price = ""

    return price

# Function to extract Product Rating


def get_rating(soup):

    try:
        rating = soup.find(
            "i", attrs={'class': 'a-icon a-icon-star a-star-4-5'}).string.strip()

    except AttributeError:

        try:
            rating = soup.find(
                "span", attrs={'class': 'a-icon-alt'}).string.strip()
        except:
            rating = ""

    return rating

# Function to extract Number of User Reviews


def get_review_count(soup):
    try:
        review_count = soup.find(
            "span", attrs={'id': 'acrCustomerReviewText'}).string.strip()

    except AttributeError:
        review_count = ""

    return review_count


titles = []
prices = []
ratings = []
reviews = []

if __name__ == '__main__':

    # Headers for request
    HEADERS = ({'User-Agent':
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
                'Accept-Language': 'en-US'})

    # The webpage URL
    URL = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"

    # HTTP Request
    webpage = requests.get(URL, headers=HEADERS)
    print(webpage)

    # Soup Object containing all data
    soup = BeautifulSoup(webpage.content, "lxml")

    # Fetch links as List of Tag Objects
    links = soup.find_all("a", attrs={
                          'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style'})

    # Store the links
    links_list = []

    # Loop for extracting links from Tag Objects
    for link in links:
        links_list.append(link.get('href'))

    contents = []
    # Loop for extracting product details from each link
    for link in links_list:

        new_webpage = requests.get(
            'https://www.amazon.in' + link, headers=HEADERS)
        #new_webpage = requests.get(link1, headers=HEADERS)
        new_soup = BeautifulSoup(new_webpage.content, "lxml")

        titles.append(get_title(new_soup))
        #print("Product Title =", titles)
        prices.append(get_price(new_soup))
        #print("Product Price =", prices)
        ratings.append(get_rating(new_soup))
        #print("Product Rating =", ratings)
        reviews.append(get_review_count(new_soup))
        #print("Number of Product Reviews =", reviews)

        contents = zip(links_list, titles, prices, ratings, reviews)
        print(contents)


# print()

    # file_name = 'amazon.csv'  # title of excel file
        with open('amazon.csv', 'w', encoding="utf-8", newline='') as f:

            # intializing the writer object to insert data in the csv file
            writer = csv.writer(f)
        # the headers of the CSV file
            header = ['link', 'title', 'price', 'rating', 'review']
            writer.writerow(header)
            writer.writerows(contents)
