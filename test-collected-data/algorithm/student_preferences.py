from objects import Student
from objects import df_student
import math

# Convert DataFrame to list of Student instances and create student_preferences dictionary
students = []
student_preferences = {}

# Function to handle the conversion with nan check
def convert_id(id, choice):
    if isinstance(id, float) and math.isnan(id):
        # Check if choice is a string and handle accordingly
        if isinstance(choice, str):
            parts = choice.split(',')
            if len(parts) > 2:
                return 'Project-' + parts[2].strip()
            else:
                return choice.strip()  # In case there are less than 2 commas, return the whole choice
        else:
            return None  # In case choice is not a string
    else:
        return f'Project-{int(id)}'

# Loop through each row in the dataframe
for _, row in df_student.iterrows():
    student = Student(
        ID=row['ID'],
        
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
        convert_id(student.First_ID, student.First_Choice),
        convert_id(student.Second_ID, student.Second_Choice),
        convert_id(student.Third_ID, student.Third_Choice),
        convert_id(student.Fourth_ID, student.Fourth_Choice),
        convert_id(student.Fifth_ID, student.Fifth_Choice)
    ]

    # student_preferences[f'Student-{student.ID}'] = preferences

    # Filter out None values
    preferences = [p for p in preferences if p is not None]
    
    # Check if all values in preferences are not None
    if all(p is not None for p in preferences):
        # Add to dictionary
        student_preferences[f'Student-{student.ID}'] = [p for p in preferences if p is not None]

# print(f"{len(student_preferences)}")
# Display the student_preferences dictionary with each entry on a separate line
for student_id, preferences in student_preferences.items():
    print(f"{student_id}: {preferences}")