from openai import OpenAI
from dotenv import load_dotenv
from create_assistant import (
    get_product_info,
    check_stock,
    get_all_products,
    get_product_price,
    filter_products_by_price_range,
    get_products_in_stock,
    count_available_products,
    find_closest_product,
    get_recommendations
)
import json
import os

# Load environment variables from a .env file
load_dotenv()
client = OpenAI()

# Check if a thread ID already exists
thread_id_file = "thread_id.txt"

if os.path.exists(thread_id_file):
    with open(thread_id_file, "r") as file:
        thread_id = file.read().strip()
    # Retrieve the existing thread
    thread = client.beta.threads.retrieve(thread_id=thread_id)
else:
    # Create a new thread and save its ID
    thread = client.beta.threads.create()
    with open(thread_id_file, "w") as file:
        file.write(thread.id)

# Get user input for the query
user_query = input("Enter your query: ")

# Create a new message with the user's input
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content=user_query
)

# Initiate a run with the assistant
run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id="asst_WPF5tvpYLSgjBXqf1kcPfgHO"
)

# Continuously check the status of the run
while run.status != "completed":  
    keep_retrieving_run = client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
    )
    print(f"Run status: {keep_retrieving_run.status}")

    # List all messages in the thread
    all_messages = client.beta.threads.messages.list(
        thread_id=thread.id
    )

    # Handle required actions if the run status is "requires_action"
    if keep_retrieving_run.status == "requires_action":
        print("Function Calling")
        required_actions = keep_retrieving_run.required_action.submit_tool_outputs.model_dump()
        print(required_actions)
        tool_outputs = []
        
        # Execute the required functions based on the action
        for action in required_actions["tool_calls"]:
            func_name = action['function']['name']
            arguments = json.loads(action['function']['arguments'])
            
            if func_name == "get_product_info":
                output = get_product_info(arguments["productName"])
            elif func_name == "check_stock":
                output = check_stock(arguments["productName"])
            elif func_name == "get_all_products":
                output = get_all_products()
            elif func_name == "get_product_price":
                output = get_product_price(arguments["productName"])
            elif func_name == "filter_products_by_price_range":
                output = filter_products_by_price_range(arguments["min_price"], arguments["max_price"])
            elif func_name == "get_products_in_stock":
                output = get_products_in_stock()
            elif func_name == "count_available_products":
                output = count_available_products()
            elif func_name == "find_closest_product":
                output = find_closest_product(arguments["query"])
            elif func_name == "get_recommendations":
                output = get_recommendations(arguments["productName"])
            else:
                raise ValueError(f"Unknown function: {func_name}")
            
            tool_outputs.append({
                "tool_call_id": action['id'],
                "output": str(output)
            })
        
        # Submit the tool outputs back to the assistant
        print("Submitting outputs back to the Assistant...")
        print(tool_outputs,'frrf')
        client.beta.threads.runs.submit_tool_outputs(
            thread_id=thread.id,
            run_id=run.id,
            tool_outputs=tool_outputs
        )
        
    # If the run is completed, print the assistant's response
    if keep_retrieving_run.status == "completed":
        print("\n")
        assistant_response = all_messages.data[0].content[0]
        print(assistant_response.text.value)
        break

    # Print the messages from the user and the assistant
    print("###################################################### \n")
    print(f"USER: {user_query}")

