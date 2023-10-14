# Define a dictionary to store the converted data
converted_data = {}

# Read the input file line by line
with open(f'./inputs/ibm-2023.txt', 'r') as file:
    for line in file:
        # Split the line into three values
        values = line.split()
        
        # Convert the values to the desired format
        t_value = 'T' + values[0]
        i_values = ['I' + values[2]]
        
        # Check if the t_value already exists in the dictionary
        if t_value in converted_data:
            converted_data[t_value].extend(i_values)
        else:
            converted_data[t_value] = i_values

# Write the converted data to the output file
with open('ttt.txt', 'w') as file:
    for key, value in converted_data.items():
        file.write(f"'{key}': {value},\n")
