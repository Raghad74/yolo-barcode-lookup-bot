import requests

class Product():
    def __init__(self,barcode):
        self.barcode=barcode

        url=f'https://world.openfoodfacts.net/api/v2/product/{self.barcode}.json'
        response=requests.get(url)
        self.openfoodfacts_data_json=response.json()
    
    def get_name_and_brand(self):
        product = self.openfoodfacts_data_json["product"]
        name = product.get("product_name", "Unknown")
        brand = product.get("brands", "Unknown")
        response_str=f'the provided product name is : {name} ,for the brand : {brand}'
        return response_str
    
    def get_allergens(self):
        product = self.openfoodfacts_data_json["product"]
        allergens = product.get("allergens", "").split(',')
        allergensList=[element[3:] for element in allergens]
        response_str="allergens are:"
        for allergen in allergensList:
            response_str+=f'\n{allergen}'
        return response_str

    def get_calories(self):
        product = self.openfoodfacts_data_json["product"]
        nutriments = product.get("nutriments", {})
        calories_per_serving = nutriments.get("energy-kcal_serving","")
        calories_in_100gram=nutriments.get("energy-kcal_100g","")
        response_str=f"calories for 100g is {calories_in_100gram} , and per serving is {calories_per_serving}"
        return response_str


    def get_is_vegan_info(self):
        product = self.openfoodfacts_data_json["product"]
        tags=product.get("ingredients_analysis_tags", [])
        is_vegan = "en:vegan" in tags
        is_vegetarian = "en:vegetarian" in tags
        response_str="according to info in open food facts:\n"
        response_str+=f"is it vegan? {is_vegan} \n"
        response_str+=f"is it vegetarian? {is_vegetarian}"
        return response_str

    def get_is_gluten_free(self):
        product = self.openfoodfacts_data_json["product"]
        labels_tags = product.get("labels_tags", [])
        is_gluten_free = any(label in ["en:gluten-free", "en:no-gluten"] for label in labels_tags)
        response_str="Serching for gluten free labels ..."
        if is_gluten_free:
            response_str+="\n gluten free label found"
        else:
            response_str+="\n gluten free label has not been found but you can check the ingredient list"
        return response_str

        
    def get_is_halal_or_kosher(self):
        product = self.openfoodfacts_data_json["product"]
        labels = product.get("labels_tags", [])
        is_halal = any("halal" in label for label in labels)
        is_kosher = any("kosher" in label for label in labels)
        response_str="Serching for Halal labels ..."
        if is_halal:
            response_str+="\n halal label found"
        else:
            response_str+="\n halal label has not been found but you can check the ingredient list"

        response_str+="\nSerching for Kosher labels ..."
        if is_kosher:
            response_str+="\n kosher label found"
        else:
            response_str+="\n kosher label has not been found but you can check the ingredient list"
        
        return response_str


    def get_nutrition_score(self):
        product = self.openfoodfacts_data_json["product"]
        nutri_grade = product.get("nutriscore_grade")
        response_str="Nutrition grades go from A to E "
        response_str+=f"\n this products nutrition Grade is : {nutri_grade}"
        return response_str
    
    



    
        