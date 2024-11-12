# AI E-Commerce Assistant

An AI-powered assistant built to help users interact with an e-commerce platform by answering queries about products, stock availability, and pricing. This assistant utilizes OpenAI's API with function calling to retrieve and display product data.

## Project Overview

This application is designed to create a conversational experience for an e-commerce platform using OpenAI's GPT model with function calling. Users can ask for product details, check stock availability, view all available products, and even filter by price range, and the assistant responds with accurate and relevant information.

## Features

- **Product Information**: Get detailed descriptions of products.
- **Stock Check**: Check if a product is available in stock.
- **Price Filtering**: Find products within a specific price range.
- **All Products List**: Retrieve a list of all products.
- **Product Price Check**: Check the price of a specific product.
- **Dynamic Thread Management**: Continuation of conversation with thread ID persistence.
- **Closest Product Match**: Find the closest matching product name using fuzzy matching.
- **Product Recommendations**: Get recommendations for products similar to a specified product.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/CPTCIC5/my-assignment
   ```

2. **Install Dependencies**: Ensure you have Python and pip installed. Install the required packages using:
   ```bash
   pip install openai python-dotenv fuzzywuzzy
   ```

3. **Setup Environment Variables**:
   - Create a `.env` file in the root directory.
   - Add your OpenAI API key in the `.env` file:
     ```
     OPENAI_API_KEY=your_openai_api_key
     ```

## Usage

### Running the Application

- **Start the Assistant**: Run the `run.py` file to interact with the assistant in the terminal.
  ```bash
  python run.py
  ```

- **Enter Queries**: When prompted, enter a query to interact with the assistant.

  **Example queries**:
  - "Tell me about the 'Wireless Bluetooth Headphones'."
  - "Is the 'Smart Fitness Watch' in stock?"
  - "What products are available under $50?"
  - "Find the closest match for 'Bluetooth Earbuds'."
  - "Recommend products similar to 'Smart Fitness Watch'."

## How It Works

- **Session Continuity**: The assistant uses a file named `thread_id.txt` to manage conversation continuity. If this file exists and contains a thread ID, the assistant will resume the conversation from the existing thread. If the file is deleted or does not exist, a new thread will be created, and its ID will be saved in `thread_id.txt` for future use. **Important**: Deleting `thread_id.txt` will start a fresh conversation thread, so ensure to keep it if you wish to continue your previous chat.
- **Function Calling**: The assistant dynamically triggers function calls based on the user's query, such as retrieving product details, checking stock, and filtering by price range.
- **Assistant Response**: The assistant processes the query, calls relevant functions as needed, and returns the results in a conversational manner.

## Available Functions

- `get_product_info(productName)`: Retrieves detailed information for a specified product.
- `check_stock(productName)`: Checks if a specific product is in stock.
- `get_all_products()`: Lists all available products.
- `get_product_price(productName)`: Returns the price of a specified product.
- `filter_products_by_price_range(min_price, max_price)`: Returns products within a specified price range.
- `get_products_in_stock()`: Lists all products currently in stock.
- `count_available_products()`: Returns the count of products in stock.
- `find_closest_product(query)`: Finds the closest matching product name to the query using fuzzy matching.
- `get_recommendations(productName)`: Returns a list of recommended products similar to the specified product.

## Example Queries and Outputs

- **Query**: "Tell me about 'Smart Fitness Watch'."
  - **Response**: Product details including description, price, and stock status.
- **Query**: "What products are available under $50?"
  - **Response**: List of products within the specified price range.
- **Query**: "Is the 'LED Desk Lamp with Wireless Charger' available?"
  - **Response**: Stock availability of the product.
- **Query**: "Find the closest match for 'Bluetooth Earbuds'."
  - **Response**: Closest matching product details.
- **Query**: "Recommend products similar to 'Smart Fitness Watch'."
  - **Response**: List of recommended products.

## Code Structure

- **data**: Mock product catalog containing product details.
- **run.py**: Main script to initialize the assistant, handle user queries, check run statuses, and manage tool outputs.
- **create_assistant.py**: Defines and registers functions available to the assistant, enabling interaction with the product catalog.
- **thread_id.txt**: Stores the thread ID for continuity across user sessions.

## Known Issues / Limitations

- **Static Product Data**: The product catalog is hardcoded. For production use, connect to a dynamic database.
- **Error Handling**: Basic error handling is in place; improvements can be added for robustness in edge cases.

## Contributing

If you'd like to contribute, please fork the repository and create a pull request with your enhancements or fixes.

## License

This project is licensed under the MIT License.

