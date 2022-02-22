import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl
import psycopg2

#establishing the connection
conn = psycopg2.connect(
   database='', user='postgres', password='', host='127.0.0.1', port= '5432'
)
#Creating a cursor object using the cursor() method
cursor = conn.cursor()


recipeURLs = []
url = "https://www.homebrewersassociation.org/homebrew-recipes/page/"

def scrapeSite(link):
    for x in range(61, 70):
        print("page " + str(x))
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
        try:
            parseRecipePage(item)
        except:
            print("errr:", item)
    print (len(recipeURLs))


def parseRecipePage(url):
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')

    recipe = soup.find("article", class_="recipes")

    titleBlock = recipe.find("h1").contents[0]

    styleDiv = recipe.find("a", itemprop="recipeCuisine")

    style = styleDiv.text

    ingredientsAndSpecsBlock = recipe.find("div", class_="ingredients")
    
    if ingredientsAndSpecsBlock:

        try:

            ingredientsBlock = ingredientsAndSpecsBlock.children

            ingredientsBlock = ingredientsAndSpecsBlock.find_all("li")
            ingredients = []

            for i in ingredientsBlock:
                if not i.strong and i.contents:
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
                specString = str(spec.text)
                specText = specString.split(": ")
                s = specText[0]
                v = specText[1]
                specValues[s] = v


            directionsBlock = recipe.find("div", {"itemprop":"recipeInstructions"})
            directions = directionsBlock.p.contents[0] if directionsBlock.p and directionsBlock.p.contents else ""

            batchYield = specValues["Yield"] if specValues["Yield"] else ""
            og = specValues["Original Gravity"] if specValues["Original Gravity"] else ""
            fg = specValues["Final Gravity"] if specValues["Final Gravity"] else ""
            abv = specValues["ABV"] if specValues["ABV"] else ""
            ibu = specValues["IBU"] if specValues["IBU"] else ""
            srm = specValues["SRM"] if specValues["SRM"] else ""

            sql = """INSERT INTO recipes(title, style, original_gravity, final_gravity, abv, ibu, srm, yield, directions)
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING recipe_id;"""

            cursor.execute(sql, (titleBlock, style, og, fg, abv, ibu, srm, batchYield, directions,))
            id_of_new_recipe = cursor.fetchone()[0]

            ingredientSQL = """INSERT INTO ingredients(recipe_id, ingredient )
                    VALUES(%s, %s); """

            for ingredient in ingredients:
                cursor.execute(ingredientSQL, (id_of_new_recipe, str(ingredient)))

            conn.commit()

        except:
            print("error: ", titleBlock, og, fg, abv, ibu, srm, batchYield, directions)


scrapeSite(url)


