import yaml
from logger import file_logger


def merge_dict_list(dict_list):
    return {k: v for d in dict_list for k, v in d.items()}


def check_missing_keys(config):
    REQUIRED_KEYS = [
    "local_git_path",
    "model_provider",
    "model_name",
    "grpc_server_port"
    ]
    missing_keys = [key for key in REQUIRED_KEYS if not config.get(key)]
    if missing_keys:
        raise ValueError(f"Missing keys in config.yml: {', '.join(missing_keys)}")
    
try:
    with open('config.yml', 'r') as file:
        config = yaml.safe_load(file)
    model_config = merge_dict_list(config.get("model_config", {}))
    #check_missing_keys(model_config)
    
    git_config = merge_dict_list(config.get("git_config", {}))
    #check_missing_keys(git_config)
    
    grpc_config = merge_dict_list(config.get("grpc_config", {}))
    #check_missing_keys(grpc_config)
    
    MODEL_PROVIDER = model_config["model_provider"]
    print(f"model provider {MODEL_PROVIDER}")
    MODEL_NAME = model_config["model_name"]
    print(f"model provider {MODEL_NAME}")
    LOCAL_GIT_PATH = git_config["local_git_path"]
    print(f"model provider {LOCAL_GIT_PATH}")
    GRPC_SERVER_PORT = grpc_config["grpc_server_port"]
    print(f"model provider {GRPC_SERVER_PORT}")
    
except FileNotFoundError:
    file_logger.info("Error: config.yaml not found.")
except yaml.YAMLError as e:
    file_logger.info(f"Error parsing YAML: {e}")
except ValueError as ve:
    file_logger.info(str(ve))