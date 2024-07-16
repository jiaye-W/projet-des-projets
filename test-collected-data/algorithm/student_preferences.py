from objects import Student
from objects import df_student

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
                if last_word != 'Eisenbrand' and last_word != 'Michel' and last_word != 'Perraudin':
                    processed_list.append(f"Project-{last_word}-undefined")      
    
    return processed_list


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