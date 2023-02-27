import pandas as pd # For data manipulation.
pd.set_option('display.max_rows', None) # Show all the rows of the DataFrame.
pd.set_option('display.max_columns', None) # Show all the columns of the DataFrame.
import re # For regular expressions.
import os # For manipulating the operative system.

# Function to make the analysis case sensitive.
def caseSensitivity(text):
    case_sensitivity = input("Do you want to make your analysis case sensitive? Type 'yes' or 'no': ")
    return text.lower() if case_sensitivity == 'no' else text

# Read the text file.
file = input("Select the file to analyze: ")
while not os.path.isfile(file): # Enter the while loop if the file path does not exist.
    file_path = input("The file path is invalid. Please enter a valid path: ")
with open(file, 'r') as f: # Open de file only reading it.
    text = f.read()

# Choose a filter method.
filter_bool = True 
while filter_bool:
    filter_text = input("Choose your filter method: 'alpha', 'numeric', 'alphanumeric': ")
    if filter_text == 'alphanumeric':
        text = re.sub(r'[^\w\sáéíóúÁÉÍÓÚñÑ]+', '', text) # Filter everything that is not a word, number, blank space or speacial characters.
        text = caseSensitivity(text)
        index_name = 'string' # Change the name of the index.
        filter_bool = False
    elif filter_text == 'numeric':
        text = re.findall(r'\d+', text)
        text = ' '.join(text) # Converts a list into a string separeting them with a blank space.
        index_name = 'number' # Change the name of the index.
        filter_bool = False
    elif filter_text == 'alpha':
        text = re.sub(r'[^a-zA-Z\sáéíóúÁÉÍÓÚñÑ]+', ' ', text) # Filter everything that is not a word.
        text = caseSensitivity(text)
        index_name = 'word' # Change the name of the index.
        filter_bool = False
    else:
        print("Unrecognized method, please choose a valid method.")
characters = text.split() # Creates a list splitting a string using a blank space as a separator.

# Choose a text file with the characters you wish to ignore.
common_characters = input("Do you want to filter common strings? Type 'yes' or 'no': ")
if common_characters == 'yes':
    common_file = input("Add the path of the text file: ") # common_file should be a text file with all the characters you wish to ignore.
    while not os.path.isfile(common_file):
        common_file = input("The file path is invalid. Please enter a valid path: ")
    with open(common_file, 'r') as f:
        common_characters = f.read().splitlines() # Creates a list splitting a string using line breaks as a separator.

# Appends the character and the number of times it appears in a dictionary.
characters_counts = {} # We are going to store all the data in this dictionary.
for char in characters: # Iterates for each character in the list.
    if char not in common_characters: # All the characters that we want to count.
        if char not in characters_counts: # This is for the first time we count a character.
            characters_counts[char] = 1
        else: # The character already exist, so we just increase the count in + 1.
            characters_counts[char] += 1

# Replace characters section.
replace_characters = input("Do you wish to replace any string? Type 'yes' or 'no': ")
if replace_characters == 'yes':
    characters_list = list(characters_counts.keys()) # Creates a list using the dictionary keys.
    replacement_bool = True
    while replacement_bool:
        print(characters_list) # We print the list so we can see what strings we can replace.
        word_search = input("Type the string that you want to replace: ")
        if word_search not in characters_list: # If the string does not exist in the text after filtering.
            print("The character could not be found in the text.")
        else:
            replacement = input("Type the string that will replace it: ") # The new string.
            characters_counts[replacement] = characters_counts.pop(word_search) # Adds the replacement string to the dictionary.
            characters_list.remove(word_search) # Remove the string from the list.
            characters_list.append(replacement) # Adds the new string to the list.
        replace_question = input("Do you want to replace another string? Type 'yes' or 'no': ")
        if replace_question == 'no':
            replacement_bool = False

# Sort section.
sort_bool = True
while sort_bool:
    sort_order = input("Choose the type of sorting: 'freq', 'alpha': ")
    if sort_order == 'freq': # Sort by frequency.
        characters_counts = dict(sorted(characters_counts.items(), key = lambda x: x[1], reverse = True))
        sort_bool = False
    elif sort_order == 'alpha': # Sort by ascendent order (alphabetic or numeric)
        characters_counts = dict(sorted(characters_counts.items(), key = lambda x: x[0]))
        sort_bool = False
    else:
        print("Unrecognized method, please choose a valid method.")

total_characters = sum(characters_counts.values())

# Create the DataFrame.
df = pd.DataFrame.from_dict(characters_counts, orient = 'index', columns = ['count'])
df.index.name = index_name # Change the column names for the index names.
df['frequency %'] = (df['count'] / total_characters) * 100 # Add relative frequency column.
df.loc['TOTAL', 'count'] = total_characters # Add TOTAL row at the end of the DataFrame for the count value.
df.loc['TOTAL', 'frequency %'] = 100 # Add TOTAL row at the end of the DataFrame for the frequency value.

print(df) # Print the DataFrame.
print("The total number of unique strings is:", df.shape[0] - 1)

# Save the DataFrame.
save_bool = True
extension_bool = True
while save_bool:
    save = input("Do you wish to save the table? Type 'yes' or 'no': ")
    if save == 'yes':
        filename = input("Type the file name (without the extension): ") # Choose a file name.
        while extension_bool:
            extension = input("Choose your extension (without the .) Type 'csv', 'json', xlsx: ") # Choose a extension.
            if extension == 'csv':
                df.to_csv(filename + '.csv')
                extension_bool = False
            elif extension == 'json':
                df.to_json(filename + '.json')
                extension_bool = False
            elif extension == 'xlsx':
                df.to_excel(filename + '.xlsx')
                extension_bool = False
            else:
                print("Unrecognized extension, please choose a valid extension.")
        save_bool = False
    elif save == 'no':
        save_bool = False
    else:
        print("Please type 'yes' or 'no'.")