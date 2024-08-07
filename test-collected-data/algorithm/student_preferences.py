from objects import Student
from objects import df_student, df_student_discarded, project_correspondence_dict

def process_list(lst, level):
    processed_list = []
    
    for item in lst:
        if isinstance(item, str):
            if item.isdigit():  # Check if the string is a number
                processed_list.append(f"Project-{int(item)}")
            else: 
                # Split the string by comma and take the last word, then add "Project-"
                last_word = item.split(',')[-1].strip()
                # Manual selections
                if last_word != 'Patakfalvi' and last_word != 'Aru':
                    processed_list.append(f"Project-{last_word}-{level}")
                if last_word != 'Eisenbrand' and last_word != 'Michel' and last_word != 'Perraudin' and last_word != 'Monod':
                    processed_list.append(f"Project-{last_word}-undefined")      
    
    return processed_list


def remove_duplicates(input_dict):
    # Create a new dictionary to store the result
    output_dict = {}
    
    # Iterate through each key-value pair in the input dictionary
    for key, value_list in input_dict.items():
        # Remove duplicates while preserving order
        seen = set()
        unique_list = []
        for item in value_list:
            if item not in seen:
                unique_list.append(item)
                seen.add(item)
        
        # Store the unique list in the output dictionary
        output_dict[key] = unique_list
    
    return output_dict

# Convert DataFrame to list of Student instances and create student_preferences dictionary
students = []
student_preferences = {}

# # Function to handle the conversion with nan check
# def convert_id(id, choice):
#     if isinstance(id, float) and math.isnan(id):
#         # Check if choice is a string and handle accordingly
#         if isinstance(choice, str):
#             parts = choice.split(',')
#             if len(parts) > 2:
#                 return 'Project-' + parts[2].strip()
#             else:
#                 return choice.strip()  # In case there are less than 2 commas, return the whole choice
#         else:
#             return None  # In case choice is not a string
#     else:
#         return f'Project-{int(id)}'

# Loop through each row in the dataframe
for _, row in df_student.iterrows():
    student = Student(
        ID=row['user_id'],
        # email=row['Email'],
        # first_name=row['First Name'],
        # last_name=row['Last Name'],

        first_choice=row['first_choice'],
        second_choice=row['second_choice'],
        third_choice=row['third_choice'],
        fourth_choice=row['fourth_choice'],
        fifth_choice=row['fifth_choice'], 

        master=row['master']
    )
    students.append(student)
    
    # Create the student_preferences entry with nan handling
    preferences = [
        student.first_choice, 
        student.second_choice, 
        student.third_choice,
        student.fourth_choice,
        student.fifth_choice
    ]
    level = 'master' if student.master == 1 else 'bachelor'
    preferences = process_list(preferences, level)

    # Filter out None values
    preferences = [p for p in preferences if p is not None]
    
    # Check if all values in preferences are not None
    if all(p is not None for p in preferences):
        # Add to dictionary
        student_preferences[f'Student-{student.ID}'] = [p for p in preferences if p is not None]

# print(f"{len(student_preferences)}")
# Display the student_preferences dictionary with each entry on a separate line
# for ID, preferences in student_preferences.items():
#     print(f"{ID}: {preferences}")

def remove_empty_lists(input_dict):
    # Use a dictionary comprehension to filter out empty lists
    return {k: v for k, v in input_dict.items() if v}

student_preferences = remove_empty_lists(student_preferences)
student_preferences = remove_duplicates(student_preferences)

# Function to convert student IDs to names
def convert_ids_to_names(stud_prefs, df):
    id_to_name = df.set_index('ID').apply(lambda row: f"{row['First Name']} {row['Last Name']}", axis=1).to_dict()
    converted_dict = {}
    for student, projects in stud_prefs.items():
        converted_dict[id_to_name[int(student.split('-')[1])]] = projects
    return id_to_name, converted_dict

id_to_name, student_preferences = convert_ids_to_names(student_preferences, df_student_discarded)
# print(id_to_name)
# print(student_preferences)

student_preferences['asdf Perraudin'] += ['Project-28', "Project-77", "Project-33"]