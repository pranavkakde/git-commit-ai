import difflib
from types import NoneType
from git import Repo

def get_staged_changes(repo_path: str):
    """This function gets the staged changes from a git repo.

    Args:
        repo_path (str): full path of the git repo on local.

    Returns:
        str: returns a string with changes from git repo.
    """
    repo = Repo(repo_path)

    diff_index = repo.index.diff("HEAD")
    all_changes = ""

    for diff in diff_index:
        if diff.change_type in ['M', 'A', 'D']: # Modified, Added, Deleted
            header = f"\n--- Diff for {diff.a_path if diff.change_type != 'A' else diff.b_path} ---"
            all_changes = all_changes + header
            try:
                # For modified files, get the diff content
                if diff.a_blob and diff.b_blob:
                    before = diff.b_blob.data_stream.read().decode('utf-8')
                    after = diff.a_blob.data_stream.read().decode('utf-8')
                    diff_text = print_string_diff(before, after)
                    if type(diff_text) is not NoneType:
                        all_changes = all_changes + '\n' + diff_text
                # For added files, show the new content
                elif diff.a_blob and not diff.b_blob:
                    modified = diff.a_blob.data_stream.read().decode('utf-8')
                    all_changes = f"{all_changes}\nFile Added with Content: \n{modified}"
                # For deleted files, show the old content
                elif diff.b_blob and not diff.a_blob:
                    deleted = diff.b_blob.data_stream.read().decode('utf-8')
                    all_changes = f"{all_changes}\n File Deleted {diff.b_path}" 
            except Exception as e:
                print(f"Could not retrieve diff content: {e}")
    return all_changes


def print_string_diff(s1, s2, fromdesc='String 1', todesc='String 2'):
    """
    Prints the unified difference between two UTF-8 encoded strings.

    Args:
        s1 (str): The first string.
        s2 (str): The second string.
        fromdesc (str): A description for the first string (for display).
        todesc (str): A description for the second string (for display).
    """
    diff = difflib.unified_diff(
        s1.splitlines(keepends=True),
        s2.splitlines(keepends=True),
        fromfile=fromdesc,
        tofile=todesc,
        lineterm=''  # Suppress default newline handling
    )
    returnvalue = [line for line in diff]
    return ''.join(returnvalue) 