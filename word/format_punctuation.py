import re

def is_chinese(char):
    """Check if a character is a Chinese character."""
    if '\u4e00' <= char <= '\u9fff':
        return True
    return False

def correct_punctuation(text):
    """Correct the punctuation in the text according to the specified rules."""
    # Define patterns for incorrect punctuation
    # Pattern for English period used after a Chinese character
    pattern_en_period_after_chinese = re.compile(r'([\u4e00-\u9fff])\.')
    # Pattern for Chinese period used not at the end of a Chinese sentence
    pattern_ch_period_not_at_end = re.compile(r'。([A-Za-z0-9\u0100-\u024F])')
    
    # Pattern for English comma used after a Chinese character
    pattern_en_comma_after_chinese = re.compile(r'([\u4e00-\u9fff]),')
    # Pattern for Chinese comma used not at the end of a Chinese sentence
    pattern_ch_comma_not_at_end = re.compile(r'，( [A-Za-z0-9\u0100-\u024F])')

    # Function to replace incorrect punctuation with the correct one
    def replace_incorrect_punctuation(match):
        char, punctuation = match.group(1), match.group(0)[-1]
        if punctuation == '.' and is_chinese(char):
            return f'{char}。'
        elif punctuation == '。' and not is_chinese(char):
            return f'.{char}'
        elif punctuation == ',' and is_chinese(char):
            return f'{char}，'
        elif punctuation == '，' and not is_chinese(char):
            return f', {char}'
        return match.group(0)

    # Find all incorrect punctuation and print the context
    for pattern in [pattern_en_period_after_chinese, pattern_ch_period_not_at_end,
                    pattern_en_comma_after_chinese, pattern_ch_comma_not_at_end]:
        for match in pattern.finditer(text):
            print(f"Incorrect punctuation context: {match.group(0)}")

    # Correct the punctuation
    text = pattern_en_period_after_chinese.sub(replace_incorrect_punctuation, text)
    text = pattern_ch_period_not_at_end.sub(replace_incorrect_punctuation, text)
    text = pattern_en_comma_after_chinese.sub(replace_incorrect_punctuation, text)
    text = pattern_ch_comma_not_at_end.sub(replace_incorrect_punctuation, text)

    return text

# Read the LaTeX file
file_path = 'word/out_new.tex'  # Replace with your LaTeX file path

with open(file_path, 'r', encoding='utf-8') as file:
    content = file.read()

# Process the content
corrected_content = correct_punctuation(content)

# For demonstration, print the corrected content
# In a real scenario, you may want to write this back to a file
# print(corrected_content)