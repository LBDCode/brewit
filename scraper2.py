from imp import is_builtin
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

url = 'https://www.homebrewersassociation.org/homebrew-recipe/double-black-imperial-black-ipa/'
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
abc = specValues["ABV"]
ibu = specValues["IBU"]
srm = specValues["SRM"]


