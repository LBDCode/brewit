import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl

recipeURLs = []
url = "https://www.homebrewersassociation.org/homebrew-recipes/page/"

def scrapeSite(link):
    for x in range(2, 84):
        newURL = f'{url}{x}/'
        scrapePageRecipes(newURL)

def scrapePageRecipes(page):
    html = urllib.request.urlopen(page).read()
    soup = BeautifulSoup(html, 'html.parser')
    recipeBlock = soup.find('div', {"id": "recipe-list"})
    tags = recipeBlock.find_all('a')
    for tag in tags:
        htag = tag.get('href', None)
        if htag not in recipeURLs and 'page' not in htag:
            recipeURLs.append(htag)
    for item in recipeURLs:
        print(item)
    print (len(recipeURLs))

scrapeSite(url)
