from typing import List, Optional

from bs4 import BeautifulSoup

from src.models.recipe import Recipe, RecipeLink
from src.scrapers.base import BaseScraper

class Min15(BaseScraper):
    __items_per_page__: int = 20
    __domain__: str = "https://www.15min.lt/maistas/receptai/"
    
    def _retrieve_items_list(self, pages_count: int, keyword: str) -> List[RecipeLink]:
        results: List[RecipeLink] = []
        
        for page_num in range(2, pages_count + 2):
                content = self._get_page_content(f"paieska?f%5Bphrase%5D={keyword}&f%5Bingredients%5D%5B%5D=&f%5Bingredients%5D%5B%5D=&f%5Bingredients%5D%5B%5D=&f%5Bingredients%5D%5B%5D=&f%5Bingredients%5D%5B%5D=&f%5Bingredients%5D%5B%5D=&f%5Bingredients%5D%5B%5D=&f%5Bingredients%5D%5B%5D=&f%5Bingredients%5D%5B%5D=&f%5Bduration%5D=&s={page_num}")
                if content:
                    recipe_items = content.find("div", class_="recipe-list col-18").find("div", class_="list").find_all("div", class_="list-row")
                    for recipe_item in recipe_items:
                        recipe_link = recipe_item.find("a", class_="list-row-img fl")["href"]
                        results.append(RecipeLink(url=recipe_link))
                else:
                    continue
        return results
    
    def _extract_ingredients(self, content: BeautifulSoup) -> str:
        ingredients_list = content.find("div", class_="text").find("ul", class_="ingredients").find_all("li")
        ingredients: List[str] = []
        for ingredient in ingredients_list:
            title = ingredient.find("span", class_= "ing_title").find("a").text
            quantity = ingredient.find("span", class_= "ing_quantity").find_all("strong")[0].text 
            units = ingredient.find("span", class_= "ing_quantity").find_all("strong")[1].find("abbr").text
            ingredients.append(title + " " + quantity + " " + units)
        return ", ".join(ingredients)
    
    
    def _extract_making_steps(self, content: BeautifulSoup) -> str:
        making_steps: List[str] = []
        making_steps_lis = content.find("div", class_="text").find("div", class_="description_text").find("ol").find_all("li")
        for making_steps_li in making_steps_lis:
            making_steps.append(making_steps_li.text)
        return ", ". join(making_steps)
    
    def _retrieve_recipe_info(self, link: RecipeLink) -> Optional[Recipe]:
        content = self._get_page_content(link.url)
        if content:
            try:
                recipe_title = content.find("div", class_= "recipe-head").find("h1").text
            except AttributeError:
                return None
            
            making_time = content.find("div", class_="top-actions").find("span", class_="recipe-duration fl").find("span", class_="duration").find("time").text
            main_recipe_image = content.find("div", class_="image col-18").find("div", class_="badge-layers-holder").find("span").find("img")["src"]
            
            return Recipe(
                title=recipe_title,
                image_url=main_recipe_image,
                about="",
                making_time=making_time,
                ingredients=self._extract_ingredients(content),
                making_steps=self._extract_making_steps(content)
            )               
        else:
            return None 