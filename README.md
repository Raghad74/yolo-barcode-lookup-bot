# YOLO Barcode Bot

## General Purpose

This is a **Telegram bot that identifies food products by scanning their barcodes** and provides detailed nutritional and dietary information about the scanned products. Users send photos of food items with visible barcodes, and the bot extracts the barcode, looks up the product information from the Open Food Facts API, and provides details like allergens, calories, vegan status, halal certification, and more.

## Key Components

### 1. **Main Application** (`main.py`)
- **Telegram Bot Handler**: Uses the `python-telegram-bot` library to manage user interactions
- **Command Handlers**:
  - `/start` - Welcome message
  - `/help` - Usage instructions
  - `/menu` - Display available product information options
- **Message Handlers**:
  - Processes photo uploads containing barcodes
  - Processes text responses (menu selections) from users
- **Context Management**: Stores user's scanned product data in conversation context

### 2. **Barcode Decoder** (`core/decoder.py`)
- **YOLO11 Model**: Uses a trained YOLOv11 neural network (`trained_yolo_model/weights/best.pt`) to detect barcode regions in images
- **Barcode Extraction**: 
  - Locates barcode position in the food product image
  - Sharpens the barcode image if needed for better reading
- **Barcode Decoding**: Uses `pyzbar` library to extract the actual barcode number from the detected region

### 3. **Product Information Handler** (`core/product.py`)
- **API Integration**: Fetches product data from [Open Food Facts API](https://world.openfoodfacts.net/api/)
- **Product Methods**: Provides 8 different information types:
  - `get_name_and_brand` - Product name and manufacturer
  - `get_allergens` - Allergen information
  - `get_calories` - Caloric content
  - `get_is_vegan_info` - Vegan/vegetarian status
  - `get_is_halal` - Halal certification + ingredient analysis
  - `get_is_kosher` - Kosher status + pork ingredient checks
  - `get_is_gluten_free` - Gluten-free status
  - `get_nutrition_score` - Overall nutrition score

### 4. **Dietary Keywords** (`core/product_dietary_keywords.py`)
- Maintains lists of keywords for dietary restrictions:
  - `PORK_KEYWORDS` - Pork-related ingredients
  - `GELATIN_KEYWORDS` - Gelatin sources
  - `ALCOHOL_KEYWORDS` - Alcohol-containing ingredients
  - `KOSHER_SYMBOLS` - Kosher certification symbols

### 5. **Model Training** (`training/barcode_yolo_training.ipynb`)
- Trains the YOLO11 model on barcode detection dataset
- Uses Roboflow dataset with ~200+ barcode images
- Achieves high accuracy (mAP50: 0.995, mAP50-95: 0.889)

## Data Flow

```
User sends food photo → YOLO detects barcode → Barcode decoded to number 
  → API lookup → Product info retrieved → User selects info type → Response sent
```

## Technologies Used

- **Telegram API** - Bot communication
- **YOLOv11** - Barcode detection
- **pyzbar** - Barcode reading
- **Open Food Facts API** - Product database
- **Python async** - Asynchronous message handling
