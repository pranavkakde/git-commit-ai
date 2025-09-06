import yaml
from logger import file_logger


def merge_dict_list(dict_list):
    return {k: v for d in dict_list for k, v in d.items()}

    
try:
    with open('config.yml', 'r') as file:
        config = yaml.safe_load(file)
    model_config = merge_dict_list(config.get("model_config", {}))
    
    git_config = merge_dict_list(config.get("git_config", {}))
    
    grpc_config = merge_dict_list(config.get("grpc_config", {}))
    
    MODEL_PROVIDER = model_config["model_provider"]
    MODEL_NAME = model_config["model_name"]
    LOCAL_GIT_PATH = git_config["local_git_path"]
    GRPC_SERVER_PORT = grpc_config["grpc_server_port"]
    
except FileNotFoundError:
    file_logger.info("Error: config.yaml not found.")
except yaml.YAMLError as e:
    file_logger.info(f"Error parsing YAML: {e}")
except ValueError as ve:
    file_logger.info(str(ve))