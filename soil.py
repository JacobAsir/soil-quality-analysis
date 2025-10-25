from xgboost import XGBClassifier
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import numpy as np
import os
from dotenv import load_dotenv
load_dotenv()

# Load the model
import joblib
loaded_model = joblib.load("xgb_soil_analysis.bin")


def get_data_JSON(relevant_data, model):
    """Convert sensor data to JSON format with prediction"""
    keys = [
        "N - Ratio of Nitrogen (NH4+) content in soil",
        "P - Ratio of Phosphorous (P) content in soil",
        "K - Ratio of Potassium (K) content in soil",
        "pH - Soil acidity (pH)",
        "ec - Electrical conductivity",
        "oc - Organic carbon",
        "S - Sulfur (S)",
        "zn - Zinc (Zn)",
        "fe - Iron (Fe)",
        "cu - Copper (Cu)",
        "Mn - Manganese (Mn)",
        "B - Boron (B)"
    ]
    
    # Make prediction
    output = model.predict(np.array(relevant_data).reshape(1, -1))
    
    # Determine fertility status
    if output[0] == 0:
        status = "Less fertile"
    elif output[0] == 1:
        status = "Fertile"
    else:
        status = "Highly fertile"
    
    # Create dictionary with all data
    data_dict = dict(zip(keys, relevant_data))
    data_dict["status"] = status
    
    return data_dict

# Prompt templates - Updated to handle language
PROMPT_TEMPLATE1 = """
You are a Soil Quality Expert. Using the given data on soil health and its associated variables, provide feedback to the user. 

{language_instruction}

Health Status: This could be "Less fertile", "Fertile", or "Highly fertile".
Variables associated with soil health:
N - Ratio of Nitrogen (NH4+) content in soil
P - Ratio of Phosphorous (P) content in soil
K - Ratio of Potassium (K) content in soil
pH - Soil acidity (pH)
ec - Electrical conductivity
oc - Organic carbon
S - Sulfur (S)
zn - Zinc (Zn)
fe - Iron (Fe)
cu - Copper (Cu)
Mn - Manganese (Mn)
B - Boron (B)

Based on the health status and the variables provided, please provide feedback as follows:

Highly fertile:
- Congratulate the user with an excitement-filled message. Mention how the soil is perfect for crops and plantations.
- Suggest practices they should use to maintain the fertility of their soil.

Fertile:
- Identify which of the provided indicators make the soil quality good.
- Mention the weaker factors and provide suggestions on how they can be improved.

Less fertile:
- Point out which factors are causing the soil to be less fertile.
- Offer solutions and practices on how the soil quality can be improved.

Following is a JSON containing the health status and variables:
{data_JSON}
"""

PROMPT_TEMPLATE2 = """
You are a Soil Quality Expert. Using the given data on soil health and its associated variables, provide feedback to the user.

{language_instruction}

Health Status: This could be "Less fertile", "Fertile", or "Highly fertile".
Variables associated with soil health:
N - Ratio of Nitrogen (NH4+) content in soil
P - Ratio of Phosphorous (P) content in soil
K - Ratio of Potassium (K) content in soil
pH - Soil acidity (pH)
ec - Electrical conductivity
oc - Organic carbon
S - Sulfur (S)
zn - Zinc (Zn)
fe - Iron (Fe)
cu - Copper (Cu)
Mn - Manganese (Mn)
B - Boron (B)

Based on the health status and the variables provided, please provide expert feedback based on the chat history and user message as follows:

Following is the conversation history between user and expert(You):
{user_history}

Following is the user message:
{user_message}
"""

# Initialize LLM and chains
llm = ChatGroq(model_name="llama-3.1-8b-instant", api_key=os.getenv("GROQ_API_KEY"))

# Create prompts with language handling
def create_prompt1(language="English"):
    lang_instruction = "Please provide your entire response in Japanese language." if language == "Japanese" else "Please provide your response in English."
    return PromptTemplate(
        template=PROMPT_TEMPLATE1,
        input_variables=['data_JSON'],
        partial_variables={'language_instruction': lang_instruction}
    )

def create_prompt2(language="English"):
    lang_instruction = "Please provide your entire response in Japanese language." if language == "Japanese" else "Please provide your response in English."
    return PromptTemplate(
        template=PROMPT_TEMPLATE2,
        input_variables=['user_history', 'user_message'],
        partial_variables={'language_instruction': lang_instruction}
    )

# Modified chains to use LCEL pipe syntax
class LanguageAwareLLMChain:
    def __init__(self, llm, prompt_creator):
        self.llm = llm
        self.prompt_creator = prompt_creator
        self.output_parser = StrOutputParser()

    def predict(self, language="English", **kwargs):
        prompt = self.prompt_creator(language)
        chain = prompt | self.llm | self.output_parser
        return chain.invoke(kwargs)

chain1 = LanguageAwareLLMChain(llm, create_prompt1)
chain2 = LanguageAwareLLMChain(llm, create_prompt2)
