# Import necessary modules
from openai import OpenAI  # Import OpenAI SDK to interact with OpenAI's API
from dotenv import load_dotenv  # Import dotenv to load environment variables
from fuzzywuzzy import fuzz, process  # Import fuzzy matching tools

# Load environment variables from a .env file 
load_dotenv()

# Initialize OpenAI client
client = OpenAI()

# Mock product catalog data (for testing and function demonstration purposes)
data= [
  {
    "product_id": 101,
    "name": "Wireless Bluetooth Headphones",
    "description": "High-quality wireless headphones with noise-cancellation and 30 hours battery life.",
    "price": 79.99,
    "stock_availability": True
  },
  {
    "product_id": 102,
    "name": "Smart Fitness Watch",
    "description": "Fitness watch with heart rate monitor, GPS tracking, and waterproof design.",
    "price": 129.99,
    "stock_availability": True
  },
  {
    "product_id": 103,
    "name": "Portable Power Bank 20,000mAh",
    "description": "High-capacity portable charger with fast charging and dual USB ports.",
    "price": 29.99,
    "stock_availability": True
  },
  {
    "product_id": 104,
    "name": "USB-C Hub Adapter",
    "description": "7-in-1 USB-C hub with HDMI, USB 3.0, SD card reader, and PD charging.",
    "price": 39.99,
    "stock_availability": True
  },
  {
    "product_id": 105,
    "name": "LED Desk Lamp with Wireless Charger",
    "description": "Dimmable LED lamp with wireless phone charging and touch controls.",
    "price": 49.99,
    "stock_availability": False
  }
]


# Function to retrieve all product names from the catalog
def get_all_products():
    """Returns a list of all products."""
    return [product['name'] for product in data]

# Function to retrieve details of a specific product by name
def get_product_info(productName: str):
    """Returns product details for a given product name."""
    for product in data:
        if product['name'].lower() == productName.lower():
            return product
    return None

# Function to retrieve the price of a specified product by name
def get_product_price(productName: str):
    """Returns the price of the specified product."""
    product = get_product_info(productName)
    if product:
        return product['price']
    return None

# Function to filter products within a specified price range
def filter_products_by_price_range(min_price: float, max_price: float):
    """Returns a list of products within a specified price range."""
    return [
        product for product in data
        if min_price <= product['price'] <= max_price
    ]

# Function to retrieve a list of products that are currently in stock
def get_products_in_stock():
    """Returns a list of product names that are currently in stock."""
    return [product['name'] for product in data if product['stock_availability']]

# Function to count the number of products currently in stock
def count_available_products():
    """Returns the count of products that are currently in stock."""
    return len(get_products_in_stock())

# Function to check the stock availability of a specific product by name
def check_stock(productName: str):
    """Checks if the specified product is in stock."""
    product = get_product_info(productName)
    if product:
        return product['stock_availability']
    return None

def find_closest_product(query: str, threshold: int = 70):
    """
    Finds the product with the closest name match to the query using fuzzy matching.
    Returns the closest match if it meets the threshold; otherwise, returns None.
    """
    product_names = [product['name'] for product in data]
    match, score = process.extractOne(query, product_names, scorer=fuzz.token_sort_ratio)
    if score >= threshold:
        return get_product_info(match)
    return f"No close match found for '{query}'."


def get_recommendations(productName: str):
    """
    Returns a list of recommended products based on the specified product's keywords.
    Products are considered similar if they share keywords in their names.
    """
    product = get_product_info(productName)
    if not product:
        return f"Product '{productName}' not found."

# Setting up the assistant on OpenAI's platform with defined function calls
x1 = client.beta.assistants.create(
    model="gpt-4o",  # Model to use for the assistant
    instructions="You are an AI assistant for an e-commerce platform...",
    name="ShopBot-Test",  # Name of the assistant
    tools=[
        # List of tools (functions) available for the assistant to call
        {
            "type": "function",
            "function": {
                "name": "get_product_info",
                "description": "Returns product details by name",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "productName": {
                            "type": "string",
                            "description": "Name of the product"
                        }
                    },
                    "required": ["productName"],
                    "additionalProperties": False
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "check_stock",
                "description": "Checks if the product is in stock by name",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "productName": {
                            "type": "string",
                            "description": "Name of the product"
                        }
                    },
                    "required": ["productName"],
                    "additionalProperties": False
                }
            }
        },
        # Function to list all products
        {
            "type": "function",
            "function": {
                "name": "get_all_products",
                "description": "Returns a list of all products available",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": [],
                    "additionalProperties": False
                }
            }
        },
        # Function to retrieve the price of a specific product
        {
            "type": "function",
            "function": {
                "name": "get_product_price",
                "description": "Returns the price of the specified product",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "productName": {
                            "type": "string",
                            "description": "Name of the product"
                        }
                    },
                    "required": ["productName"],
                    "additionalProperties": False
                }
            }
        },
        # Function to filter products by price range
        {
            "type": "function",
            "function": {
                "name": "filter_products_by_price_range",
                "description": "Returns a list of products within a specified price range",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "min_price": {
                            "type": "number",
                            "description": "Minimum price"
                        },
                        "max_price": {
                            "type": "number",
                            "description": "Maximum price"
                        }
                    },
                    "required": ["min_price", "max_price"],
                    "additionalProperties": False
                }
            }
        },
        # Function to get products currently in stock
        {
            "type": "function",
            "function": {
                "name": "get_products_in_stock",
                "description": "Returns a list of products currently in stock",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": [],
                    "additionalProperties": False
                }
            }
        },
        # Function to count available products in stock
        {
            "type": "function",
            "function": {
                "name": "count_available_products",
                "description": "Returns the count of products currently in stock",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": [],
                    "additionalProperties": False
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "find_closest_product",
                "description": "Finds the closest matching product name to the query using fuzzy matching.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Approximate name or description of the product"
                        }
                    },
                    "required": ["query"],
                    "additionalProperties": False
                }
            }
        },
        {
            
            "type": "function",
            "function": {
                "name": "get_recommendations",
                "description": "Returns a list of recommended products similar to the specified product.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "productName": {
                            "type": "string",
                            "description": "Name of the product for recommendations"
                        }
                    },
                    "required": ["productName"],
                    "additionalProperties": False
                }
            }
        }
    ]
)

print(x1.id)