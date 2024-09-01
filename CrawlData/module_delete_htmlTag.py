import re

def remove_html_tags(text):
    # Define a regular expression pattern to match HTML tags
    clean = re.compile('<.*?>')
    # Substitute the matched tags with an empty string
    return re.sub(clean, '', text)