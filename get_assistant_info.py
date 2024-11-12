from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()
client = OpenAI()

assis= client.beta.assistants.retrieve(
    assistant_id='asst_WPF5tvpYLSgjBXqf1kcPfgHO'
)

print(assis.tools)