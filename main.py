from acc_test import ACCTest
from ar_test import ARTest

import pandas as pd
from PIL import Image, ImageTk
import tkinter as tk

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 300

IMG_WIDTH = 500
IMG_HEIGHT = 300
IMG_PAD = 10

TEXT_WIDTH = 150

OUTPUT_FILE = "eval.txt"

tests = []
current_question = 1
current_index = 0


def update_display():
    # Load images (replace 'image1.jpg' and 'image2.jpg' with the actual file paths)
    image1 = Image.open(tests[current_index].get_ref_image(current_question))  # Replace with your image path
    image2 = Image.open(tests[current_index].get_test_img(current_question))  # Replace with your image path

    # Resize images if necessary
    image1 = image1.resize((IMG_WIDTH, IMG_HEIGHT), Image.LANCZOS)
    image2 = image2.resize((IMG_WIDTH, IMG_HEIGHT), Image.LANCZOS)

    # Convert images to PhotoImage
    photo1 = ImageTk.PhotoImage(image1)
    photo2 = ImageTk.PhotoImage(image2)

    # Update image displays
    label_image1.config(image=photo1)
    label_image1.image = photo1
    label_image2.config(image=photo2)
    label_image2.image = photo2

    # Update button labels
    button1.config(text=tests[current_index].get_button_labels(current_question)[0])
    button2.config(text=tests[current_index].get_button_labels(current_question)[1])
    button3.config(text=tests[current_index].get_button_labels(current_question)[2])

    # Update prompt display
    question_label.config(text=tests[current_index].get_question(current_question))

    # Update answer display
    result = tests[current_index].get_result(current_question)

    if result != -1:
        response_label.config(text=tests[current_index].get_choice(current_question))
    else:
        response_label.config(text="")


def submit_answer(answer):
    global current_index, current_question

    # Store the user's choice
    tests[current_index].save_result(answer, current_question)

    # Display the user's choice
    response_label.config(text=tests[current_index].get_choice(current_question))


def prev_image(event=None):
    global current_index, current_question
    if current_index > 0 and current_question == 1:
        current_index = current_index - 1
        current_question = tests[current_index].num_questions
    elif current_question > 1:
        current_question = current_question - 1
    update_display()


def next_image(event=None):
    global current_index, current_question

    if current_index < len(tests) - 1 and current_question == tests[current_index].num_questions:
        current_index = current_index + 1
        current_question = 1
    elif current_question < tests[current_index].num_questions:
        current_question = current_question + 1

    update_display()


# Load in the Accuracy Tests
acc_tests = pd.read_csv("acc_tests.txt")
for i, row in acc_tests.iterrows():
    new_test = ACCTest(row['id'], row['reference'], row['image'], row['prompt'])
    tests.append(new_test)

# Load in the AR Tests
ar_tests = pd.read_csv("ar_tests.txt")
for i, row in ar_tests.iterrows():
    new_test = ARTest(row['id'], row['reference'], row['image1'], row['image2'], row['prompt'])
    tests.append(new_test)

# Create the main window
root = tk.Tk()
root.title("LERF Evaluator")
root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
root.resizable(False, False)

# Images (initially empty)
label_image1 = tk.Label(root)
label_image1.pack(side="left", padx=IMG_PAD, pady=IMG_PAD)
label_image2 = tk.Label(root)
label_image2.pack(side="right", padx=IMG_PAD, pady=IMG_PAD)

# Question (initially empty)
question_label = tk.Label(root, text="", wraplength=TEXT_WIDTH)
question_label.pack()

# Buttons for answers
button1 = tk.Button(root, text="Yes", command=lambda: submit_answer(1))
button1.pack()
button2 = tk.Button(root, text="Somewhat", command=lambda: submit_answer(0.5))
button2.pack()
button3 = tk.Button(root, text="No", command=lambda: submit_answer(0))
button3.pack()

# Response label
response_label = tk.Label(root, text="", wraplength=TEXT_WIDTH)
response_label.pack()

# Prev/Next Buttons
prev_button = tk.Button(root, text="Previous", command=prev_image)
prev_button.pack(side="left")
next_button = tk.Button(root, text="Next", command=next_image)
next_button.pack(side="right")

# Bind keyboard controls
root.bind("<Left>", prev_image)
root.bind("<Right>", next_image)

update_display()

# Run the application
root.mainloop()

# Print final results to console
for test in tests:
    print(test)

# Store final results in output file
with open(OUTPUT_FILE, 'a') as f:
    for test in tests:
        f.write(str(test) + "\n")
