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
        pass
    def get_calories(self):
        pass
    def get_is_vegan_info(self):
        pass
    def get_is_gluten_free(self):
        pass
    def get_is_halal_or_kosher(self):
        pass
    def get_nutrition_score(self):
        pass

    
        