def get_prediction():
    """Function to get prediction input from another source."""
    return input("Enter your prediction: ")

def save_prediction_to_file(filename="Prediction_Data.txt", input_func=get_prediction):
    """Appends user input to the file and structures it after 5 entries."""
    
    # Read existing data
    try:
        with open(filename, "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        lines = []
    
    # Get new input from provided function
    new_input = input_func()
    lines.append(new_input + "\n")
    
    # Check if 5 entries exist
    if len(lines) >= 5:
        questions = [
            "QES1=\"What is your goal?\"\n",
            "QES2=\"What challenges do you anticipate?\"\n",
            "QES3=\"What resources do you have?\"\n",
            "QES4=\"What timeline are you aiming for?\"\n",
            "QES5=\"What are the potential outcomes?\"\n"
        ]
        
        answers = [f"ANS{i+1}={lines[i]}" for i in range(5)]
        lines = questions + ["\n"] + answers + ["\n"]
    
    # Write back to file
    with open(filename, "w") as file:
        file.writelines(lines)
    
    print("Data successfully saved to", filename)
def load_prediction_data(filename="Prediction_Data.txt"):
    """Loads the content of the prediction file into a variable."""
    try:
        with open(filename, "r") as file:
            data = file.read()
        return data
    except FileNotFoundError:
        print("File not found.")
        return ""

if __name__ == "__main__":
    save_prediction_to_file()
    print(load_prediction_data())