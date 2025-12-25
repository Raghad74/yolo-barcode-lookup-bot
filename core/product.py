import requests
from .product_dietary_keywords import PORK_KEYWORDS,ALCOHOL_ADDITIVES,ALCOHOL_KEYWORDS,GELATIN_KEYWORDS,KOSHER_SYMBOLS

class Product():
    def __init__(self,barcode):
        self.barcode = barcode

        url=f'https://world.openfoodfacts.net/api/v2/product/{self.barcode}.json'
        response=requests.get(url)
        data=response.json()
        if data.get("status") != 1:
            raise ValueError(f"Product with Barcode {self.barcode} not found")
        self.openfoodfacts_data_json=data

    
    def get_name_and_brand(self):
        product = self.openfoodfacts_data_json["product"]
        name = product.get("product_name", "Unknown")
        brand = product.get("brands", "Unknown")
        response_str = f'the provided product name is : {name} ,for the brand : {brand}'
        return response_str
    
    def get_allergens(self):
        product = self.openfoodfacts_data_json["product"]
        allergens = product.get("allergens", "").split(',')
        allergensList = [element[3:] for element in allergens]
        response_str = "allergens are:"
        for allergen in allergensList:
            response_str += f'\n{allergen}'
        return response_str

    def get_calories(self):
        product = self.openfoodfacts_data_json["product"]
        nutriments = product.get("nutriments", {})
        calories_per_serving = nutriments.get("energy-kcal_serving","")
        calories_in_100gram = nutriments.get("energy-kcal_100g","")
        response_str = f"calories for 100g is {calories_in_100gram} , and per serving is {calories_per_serving}"
        return response_str

    def does_contain(self,keywords):
        ingredients_text = self.openfoodfacts_data_json["product"].get("ingredients_text", "")
        if ingredients_text == "":
            raise ValueError("ingredients text not found")
        ingredients_text.lower()
        return any(word in ingredients_text for word in keywords)

    def get_is_vegan_info(self):
        product = self.openfoodfacts_data_json["product"]
        tags=product.get("ingredients_analysis_tags", [])
        is_vegan = "en:vegan" in tags
        is_vegetarian = "en:vegetarian" in tags

        response_str="according to info in open food facts:\n"
        response_str += f"is it vegan? {is_vegan} \n"
        response_str += f"is it vegetarian? {is_vegetarian}"
        return response_str

    def get_is_gluten_free(self):
        product = self.openfoodfacts_data_json["product"]
        labels_tags = product.get("labels_tags", [])
        is_gluten_free = any(label in ["en:gluten-free", "en:no-gluten"] for label in labels_tags)
        response_str = "Serching for gluten free labels ..."
        if is_gluten_free:
            response_str += "\n gluten free label found"
        else:
            response_str += "\n gluten free label has not been found but you can check the ingredient list"
        return response_str

        
    def get_is_halal(self):
        product = self.openfoodfacts_data_json["product"]
        labels = product.get("labels_tags", [])
        is_halal = any("halal" in label for label in labels)
        
        if is_halal:
            response_str = "halal label found"
        else:
            response_str = "halal label has not been found"

        try:
            pork_status = self.does_contain(PORK_KEYWORDS | GELATIN_KEYWORDS)
            alcohol_status = self.does_contain(ALCOHOL_KEYWORDS | ALCOHOL_ADDITIVES)

        except ValueError:
            return response_str
        
        if pork_status or alcohol_status :
            response_str += "\n\n this product cotains pork or alcohol"
        else:
            response_str += "\n\n this product is free of pork and alcohol"

        return response_str
        
    
    def get_is_kosher(self):
        product = self.openfoodfacts_data_json["product"]
        labels = product.get("labels_tags", [])
        is_kosher = any("kosher" in label for label in labels)

        try:
            kosher_symbol_flag = self.does_contain(KOSHER_SYMBOLS)
        except ValueError :
            kosher_symbol_flag = False

        if is_kosher or kosher_symbol_flag:
            response_str = "kosher label found"
        else:
            response_str = "kosher label has not been found"
        

        
        return response_str

    def get_nutrition_score(self):
        product = self.openfoodfacts_data_json["product"]
        nutri_grade = product.get("nutriscore_grade")
        response_str = "Nutrition grades go from A to E "
        response_str += f"\n this products nutrition Grade is : {nutri_grade}"
        return response_str
    
    



    
        