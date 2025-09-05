from dotenv import load_dotenv
from prompt import get_prompt
import config
import os
import model_provider

load_dotenv()

def get_response(staged_changes: str) -> str:
    """
        Function to get response from LLM model based on the staged changes in git repo.
        Returns:
        response from LLM model
    """
    model_key = os.getenv("LLM_API_KEY")
    prompt = get_prompt(staged_changes)
    model = model_provider.get_model_instance(config.MODEL_PROVIDER, config.MODEL_NAME, model_key)
    return model.get_response(prompt=prompt)