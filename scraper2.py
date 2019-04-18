import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl

url = input('Enter website: ')
html = urllib.request.urlopen(url).read()
soup = BeautifulSoup(html, 'html.parser')

recipe = soup.find("div", class_="info-box")
recipeContents = recipe.contents

# for item in recipeContents:
#     print(item)

#this has title and type
titleBlock = recipe.find("h3")

batch = recipe.find("strong")

ingredientsBlock = recipe.find("div", {"itemprop":"ingredients"})
ingredients = ingredientsBlock.find_all("li")

specsBlock = recipe.find("ul", class_="specs").contents
og = specsBlock[1]
fg = specsBlock[2]
abv = specsBlock[3]
ibu = specsBlock[4]
srm = specsBlock[5]

directionsBlock = recipe.find("div", {"itemprop":"recipeInstructions"})
directions = directionsBlock.find_all("p")


print("Title: ", titleBlock)
print("Yield: ", batch)
print("Ingredients: ", ingredients)
print("Specifications: ", og, fg, abv, ibu, srm)
print("Directions: ", directions)
