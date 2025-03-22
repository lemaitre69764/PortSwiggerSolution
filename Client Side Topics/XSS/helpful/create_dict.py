def create_alphabet_file(filename):
    import string

    content = string.ascii_lowercase + string.ascii_uppercase + string.digits

    with open(filename, 'w') as file:
        for char in content:
            file.write(char + '\n')

output_file = "alphabet.txt"
create_alphabet_file(output_file)
print(f"Файл '{output_file}' создан!")
