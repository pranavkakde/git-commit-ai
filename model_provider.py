import openai
import google.generativeai as genai
import anthropic
from abc import ABC, abstractmethod

class IModel(ABC):
    @abstractmethod
    def get_model(self):
        pass
    @abstractmethod
    def get_response(self, prompt:str)->str:
        pass

class GeminiModel(IModel):
    def __init__(self, model_name, model_key):
        self.model_name = model_name
        self.model_key = model_key
    def get_model(self):
        genai.configure(api_key=self.model_key)
        model = genai.GenerativeModel(self.model_name)
        return model
    def get_response(self, prompt: str)-> str:
        self.model = self.get_model()
        response = self.model.generate_content(prompt)
        return response.text
        
class OpenAIModel(IModel):
    def __init__(self, model_name, model_key):
        self.model_name = model_name
        self.model_key = model_key
    def get_model(self):
        model = openai.OpenAI(api_key=self.model_key) 
        return model
    def generate_response(self, prompt: str) -> str:
        model = self.get_model()
        response = model.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    
class AnthropicModel(IModel):
    def __init__(self, model_name, model_key):
        self.model_name = model_name
        self.model_key = model_key
    def get_model(self):
        model = anthropic.Anthropic(api_key=self.model_key)
        return model
    def generate_response(self, prompt: str) -> str:
        model = self.get_model()
        response = model.messages.create(
            model=self.model_name,
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
    
class ModelFactory:
    @staticmethod
    def create_model(provider: str, model_name: str, model_key: str) -> IModel:
        provider = provider.lower()
        if provider == "gemini":
            return GeminiModel(model_name, model_key)
        elif provider == "openai":
            return OpenAIModel(model_name, model_key)
        elif provider == "anthropic":
            return AnthropicModel(model_name, model_key)
        else:
            raise ValueError(f"Unsupported model provider: {provider}")


def get_model_instance(provider, name, key):
    model = ModelFactory.create_model(provider, name, key)
    return model

    