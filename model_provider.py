import openai
from google import genai
import anthropic
from abc import ABC, abstractmethod
from logger import file_logger

class IModel(ABC):
    """
    Interface for the model provider.
    """
    @abstractmethod
    def get_client(self):
        pass

    @abstractmethod
    def get_response(self, prompt: str) -> str:
        pass


class GeminiModel(IModel):
    """
    Gemini model provider.
    """
    def __init__(self, model_name, model_key):
        self.model_name = model_name
        self.model_key = model_key

    def get_client(self):
        return genai.Client(api_key=self.model_key)

    def get_response(self, prompt: str) -> str:
        client = self.get_client()
        response = client.models.generate_content(
            model=self.model_name,
            contents=prompt
        )
        return response.text


class OpenAIModel(IModel):
    """
    OpenAI model provider.
    """
    def __init__(self, model_name, model_key):
        self.model_name = model_name
        self.model_key = model_key

    def get_client(self):
        return openai.OpenAI(api_key=self.model_key)

    def get_response(self, prompt: str) -> str:
        client = self.get_client()
        response = client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content


class AnthropicModel(IModel):
    """
    Anthropic model provider.
    """
    def __init__(self, model_name, model_key):
        self.model_name = model_name
        self.model_key = model_key

    def get_client(self):
        return anthropic.Anthropic(api_key=self.model_key)

    def get_response(self, prompt: str) -> str:
        client = self.get_client()
        response = client.messages.create(
            model=self.model_name,
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text


class ModelFactory:
    """
    Factory for the LLM model provider.
    """
    @staticmethod
    def create_model(provider: str, model_name: str, model_key: str) -> IModel:
        """
        Factory method to create the model provider.

        Returns:
        Instance of the model through IModel interface.
        """
        try:
            provider = provider.lower()
            if provider == "gemini":
                return GeminiModel(model_name, model_key)
            elif provider == "openai":
                return OpenAIModel(model_name, model_key)
            elif provider == "anthropic":
                return AnthropicModel(model_name, model_key)
            else:
                raise ValueError(f"Unsupported model provider: {provider}")
        except Exception as e:
            file_logger.error(f"Error creating model: {e}")
            raise e


def get_model_instance(provider, name, key):
    return ModelFactory.create_model(provider, name, key)
