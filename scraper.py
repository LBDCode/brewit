import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl
import psycopg2

#establishing the connection
conn = psycopg2.connect(
   database="", user='postgres', password='', host='127.0.0.1', port= '5432'
)
#Creating a cursor object using the cursor() method
cursor = conn.cursor()


recipeURLs = []
url = "https://www.homebrewersassociation.org/homebrew-recipes/page/"

def scrapeSite(link):
    for x in range(2, 84):
        newURL = f'{url}{x}/'
        scrapePageRecipes(newURL)

def scrapePageRecipes(page):
    html = urllib.request.urlopen(page).read()
    soup = BeautifulSoup(html, 'html.parser')
    recipeBlock = soup.find('div', {"class": "recipe-container"})
    tags = recipeBlock.find_all('a')
    for tag in tags:
        htag = tag.get('href', None)
        if htag not in recipeURLs and 'homebrew-recipe' in htag:
            recipeURLs.append(htag)
    for item in recipeURLs:
        parseRecipePage(item)
    print (len(recipeURLs))

scrapeSite(url)


def parseRecipePage(url):

    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')

    recipe = soup.find("article", class_="recipes")
    recipeContents = recipe.contents


    titleBlock = recipe.find("h1").contents[0]

    ingredientsAndSpecsBlock = recipe.find("div", class_="ingredients")
    ingredientsBlock = ingredientsAndSpecsBlock.children

    ingredientsBlock = ingredientsAndSpecsBlock.find_all("li")
    ingredients = []

    for i in ingredientsBlock:
        if not i.strong:
            ingredients.append(i.contents[0])


    specsBlock = ingredientsAndSpecsBlock.find_all("p")
    specValues = {
        "Yield": "",
        "Original Gravity": "",
        "Final Gravity": "",
        "ABV": "",
        "IBU": "",
        "SRM": ""
    }

    for spec in specsBlock:
        s = spec.contents[0].string.split(':')[0]
        v = spec.contents[1]
        specValues[s] = v


    directionsBlock = recipe.find("div", {"itemprop":"recipeInstructions"})
    directions = directionsBlock.p.contents[0]

    batchYield = specValues["Yield"]
    og = specValues["Original Gravity"]
    fg = specValues["Final Gravity"]
    abv = specValues["ABV"]
    ibu = specValues["IBU"]
    srm = specValues["SRM"]

    sql = """INSERT INTO recipes(title, original_gravity, final_gravity, abv, ibu, srm, ingredients, yield, directions)
             VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s) ;"""

    cursor.execute(sql, (titleBlock, og, fg, abv, ibu, srm, ingredients,))
