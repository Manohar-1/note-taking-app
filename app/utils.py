import language_tool_python

def check_grammar(text: str):
    errors = []
    tool = language_tool_python.LanguageTool('en-US')
    
    matches = tool.check(text)
    print(matches)
    for match in matches:

        errors.append({
            "message": match.message,
            "replacements": match.replacements,
            "rule_id": match.rule_id,
            "matched_text": match.matched_text,
            "offset":match.offset
        })
    return errors