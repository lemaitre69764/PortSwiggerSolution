def replace_space(text):
    return text.replace("_"," ")

text = "SQL_injection_vulnerability_allowing_login_bypass_dir"
new_text = replace_space(text)
print(new_text)