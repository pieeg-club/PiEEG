#input_data = "[192, 0, 8, 0, 226, 222, 0, 132, 196, 254, 141, 17, 1, 11, 17, 255, 253, 34, 255, 251, 228, 255, 252, 81, 255, 252, 113][192, 0, 8, 0, 226, 185, 0, 132, 157, 254, 140, 228, 1, 10, 227, 255, 253, 36, 255, 251, 233, 255, 252, 83, 255, 252, 119][192, 0, 8, 0, 226, 23, 0, 130, 249, 254, 140, 23, 1, 11, 138, 255, 253, 36, 255, 251, 233, 255, 252, 83, 255, 252, 120][192, 0, 8, 0, 225, 61, 0, 131, 152, 254, 139, 80, 1, 12, 8, 255, 253, 34, 255, 251, 229, 255, 252, 82, 255, 252, 120]"


with open('data.txt', 'r') as file:
    # Read the contents of the file
    input_data = file.read()
    
    # Print the contents
    print(input_data)

# Split the input string into separate lists
lists = input_data.split(']')

# Remove empty strings and strip whitespace
lists = [lst.strip() for lst in lists if lst.strip()]

# Write the formatted lists to a text file
with open('output.txt', 'w') as f:
    for lst in lists:
        f.write(f"{lst}]\n")
