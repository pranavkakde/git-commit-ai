def get_prompt(staged_changes: str):
    """
    Function to get the prompt for the LLM model.
    """
    prompt = f"""
    Write brief description of the changes that were done in following files. I need to put these comments in GIT while committing my code. 
    Name of the file is mentioned in the line that contains "--- Diff for ---". Removed text from file is denoted with a minus(-) sign and added text is denoted with a plus (+) sign.
    If a new file is added then following text will contain "File Added with Content:" followed by added text.
    Just print the output message only.
    "
    {staged_changes}
    "

    The comments should be summarized and should be in following format. Based on the changes, please determine if type is chore, fix or feat.
    <type>: <short summary of changes>

    <optional detailed description if needed>
    """
    return prompt