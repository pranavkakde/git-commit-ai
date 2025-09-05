from llm_client import get_response
import config
from git_stage import get_staged_changes

def main():
    staged_changes = get_staged_changes(config.LOCAL_GIT_PATH)
    print(f"staged changes {staged_changes}")
    response = get_response(staged_changes)
    print(response)
    
if __name__ == "__main__":
    main()
