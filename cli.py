from llm_client import get_response
import config
from git_stage import get_staged_changes
from logger import file_logger

def main():
    staged_changes = get_staged_changes(config.LOCAL_GIT_PATH)
    response = get_response(staged_changes)
    file_logger.info(f"response {response}")
    print(f"response {response}")
    
if __name__ == "__main__":
    main()
