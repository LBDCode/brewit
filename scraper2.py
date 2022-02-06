import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl

url = 'https://www.homebrewersassociation.org/homebrew-recipe/double-black-imperial-black-ipa/'
html = urllib.request.urlopen(url).read()
soup = BeautifulSoup(html, 'html.parser')

recipe = soup.find("article", class_="recipes")
recipeContents = recipe.contents

# for item in recipeContents:
#     print(item)

#this has title and type
titleBlock = recipe.find("h1").contents[0]

# batch = recipe.find("strong")

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


print("This is the title: ", titleBlock)
print("Directions: ", directions)
# for i in ingredients:
#     print(i)
