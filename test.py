import matplotlib.pyplot as plt
import os
from docx import Document
import editdistance
accuracy = []

test = 2


def disparity_percentage(list1, list2):
    edit_dist = editdistance.eval(list1, list2)  # Compute edit distance
    max_length = max(len(list1), len(list2))  # Normalize by the longer list
    disparity = (edit_dist / max_length) * 100  # Convert to percentage
    return disparity


def read_docx(file_path):
    doc = Document(file_path)
    text = [para.text.strip() for para in doc.paragraphs if para.text.strip()]
    return text

for i in range(test):
    test_name = f"test_{i+1}"
    model_output_file = os.path.join("Output", f"{test_name}.txt")
    benchmark_file = os.path.join("Benchmark", test_name, "CallOutLog.docx")

    model = []
    benchmark = []

    with open(model_output_file, "r", encoding="utf-8") as file:
        model_text = file.read().strip()
        model = model_text.split(",") 
    
    benchmark = read_docx(benchmark_file)
    
    model_to_lowercase = [word.lower() for word in model]
    benchmark_to_lowercase = [word.lower() for word in benchmark]


    error = disparity_percentage(model_to_lowercase, benchmark_to_lowercase)
    print(model_to_lowercase)
    print(benchmark_to_lowercase)
    accuracy.append(100 - error)

print(accuracy)
