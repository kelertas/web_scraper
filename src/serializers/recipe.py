from pydantic import BaseModel


class RecipeSetter(BaseModel):
    title : str
    image_url : str
    about : str
    making_time : str
    ingredients : str
    making_steps : str
    
    
class RecipeGetter(BaseModel):
    id : int
    title : str
    image_url : str
    about : str
    making_time : str
    ingredients : str
    making_steps : str