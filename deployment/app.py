from fastai.vision.all import *

import gradio as gr

from PIL import Image, UnidentifiedImageError
import os

cuisines = {
    'American burger': 'American burger',
    'American fried_chicken': 'American Fried chicken',
    'American hot_dog': 'American Hot dog',
    'Indian Fuchka': 'Indian Fuchka',
    'Indian biriyani': 'Indian biriyani',
    'Indian khichudi': 'Indian khichudi',
    'Indian khichuri': 'Indian khichuri',
    'Indian samosa': 'Indian Samosa',
    'Italian lasagna': 'Italian lasagna',
    'Italian pizza': 'Italian pizza',
    'Italian speggeti': 'Italian speggeti',
    'Japanese okonomiyaki': 'Japanese okonomiyaki',
    'Japanese ramen': 'Japanese ramen',
    'Japanese sushi': 'Japanese sushi',
    'Mexican Chilaquiles': 'Mexican Chilaquiles',
    'Mexican nachos': 'Mexican nachos',
    'Mexican tacos': 'Mexican tacos',
    'Turkish baklava': 'Turkish baklava',
    'Turkish kebab': 'Turkish kebab',
    'Turkish meze_food': 'Turkish Meze food',
    'Turkish swarma': 'Turkish swarma'
}


cuisine_description = """

Please Drop a picture of a Cuisine from the following list  

### American
- burger, Fried chicken, Hot dog

### Indian
- Fuchka, biriyani, khichuri, Samosa

### Italian
- lasagna, pizza, spaghetti

### Japanese
- okonomiyaki, ramen, sushi

### Mexican
- Chilaquiles, nachos, tacos

### Turkish
- baklava, kebab, Meze food, shawarma

"""


def get_labels(file_path):
    cuisine = file_path.parent.parent.name  
    dish = file_path.parent.name            
    return f"{cuisine} {dish}"             

# Custom function to load and convert images to RGBA
def load_image_safe(fn):
    try:
        img = Image.open(fn)
        # If the image has a palette and transparency, convert it to RGBA
        if img.mode == "P":
            img = img.convert("RGBA")
        return PILImage.create(img)
    except UnidentifiedImageError:
        print(f"Skipping corrupt image: {fn}")
        return None  

# Custom function to check if an image is valid and of a valid file type
def valid_image_filter(fn):
    # Check file extension
    if not fn.suffix.lower() in valid_extensions:
        print(f"Skipping invalid file type: {fn}")
        return False 

    # Check if the image can be loaded safely
    img = load_image_safe(fn)
    if img is None:
        return False  
    return True  

def get_valid_image(fn):
    return fn if valid_image_filter(fn) else None


dls = torch.load("cousine_dataloader_v1.pkl")


def rec_img(image):
    image = image.convert('RGB')
    #img_tensor = PILImage.create(image) # not working for pytorch version 2.7 
    img_tensor = tensor(image)
    try:
        pred, idx, probs = model.predict(img_tensor)  
    except Exception as e:
        print(f"Error during prediction: {e}")
        return {"error": "Prediction failed"}

    # Prepare the probabilities dictionary
    food_probabilities = dict(zip(cuisines.keys(), map(float, probs)))

    cuisine_probs = {}
    for food, prob in food_probabilities.items():
        cuisine = cuisines[food]
        if cuisine in cuisine_probs:
            cuisine_probs[cuisine] += prob
        else:
            cuisine_probs[cuisine] = prob

    return cuisine_probs
    
model_path = "models"  
model = load_learner(f'models/models.pkl')
# Gradio interface setup
image = gr.Image(type='pil',shape=(192, 192))
label = gr.Label(num_top_classes=3)
examples = [    
    'example_data/1.png',
    'example_data/2.png',
    'example_data/3.png',
    'example_data/4.png',
]

gr.Interface(
    fn=rec_img,
    inputs=image,
    outputs=label,
    live=True,
    examples=examples,
    description=cuisine_description, 
).launch( inline=False, debug=True)
