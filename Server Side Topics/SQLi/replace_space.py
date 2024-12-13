def replace_space(text):
    return text.replace(" ","_")

text = "SQL injection vulnerability allowing login bypass"
new_text = replace_space(text)
print(new_text)