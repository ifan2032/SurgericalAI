import matplotlib.pyplot as plt
import os
from docx import Document
import editdistance
from fuzzywuzzy import process
import numpy as np

def disparity_percentage(list1, list2):
    edit_dist = editdistance.eval(list1, list2)  # Compute edit distance
    max_length = max(len(list1), len(list2))  # Normalize by the longer list

    disparity = (edit_dist / max_length) * 100  # Convert to percentage
    return disparity

def compute_edit_distance_matrix(list1, list2):
    # Initialize a matrix for the edit distances
    matrix = np.zeros((len(list1), len(list2)), dtype=int)
    
    # Calculate the edit distance between each pair of strings
    for i, str1 in enumerate(list1):
        for j, str2 in enumerate(list2):
            matrix[i][j] = editdistance.eval(str1, str2)  # Use the editdistance package
    
    return matrix

def read_docx(file_path):
    doc = Document(file_path)
    text = [para.text.strip() for para in doc.paragraphs if para.text.strip()]
    return text

def get_medical_terms(test_name):
    medical_terms = read_docx(os.path.join("Benchmark", test_name, f"Unique.docx"))
    for i in range(len(medical_terms)):
        medical_terms[i] = medical_terms[i].lower()
        medical_terms[i] = medical_terms[i].strip()
    return medical_terms

def benchmark_postprocess(transcript_array, medical_terms):
    for i in range(len(transcript_array)):
        transcript_array[i] = transcript_array[i].replace(".", "").replace("*", "")
        transcript_array[i] = transcript_array[i].strip()
        transcript_array[i] = transcript_array[i].lower()
    return transcript_array


def model_postprocess(transcript_array, medical_terms):
    for i in range(len(transcript_array)):
        transcript_array[i] = transcript_array[i].replace(".", "").replace("*", "")
        transcript_array[i] = transcript_array[i].strip()
        transcript_array[i] = transcript_array[i].lower()

    transcript = ' '.join(transcript_array)

    processed_transcript_array = transcript.split(" ")

    print("TRANCRIPT", transcript)
    print("PROCESSED_ARRAY", processed_transcript_array)
    final_transcript_array = []
    index = 0
    while (index < len(processed_transcript_array)):
        
        medical_term_notFound = True

        for j in range(3, 0, -1): #check up to 3 words
            if index + j <= len(processed_transcript_array):
                word_to_try = ' '.join(processed_transcript_array[index:index+j])

                words = word_to_try.split()
                if len(words) != len(set(words)): #fix raney clip raney and raney clip applier fuzzy match bug
                    continue

                print("WORD TO TRY", word_to_try)

                if word_to_try in medical_terms: #word is already in medical_terms
                    index = index + j
                    medical_term_notFound = False
                    final_transcript_array.append(word_to_try)
                    #print("FOUND", word_to_try)
                    break

                fuzzy_match = process.extractOne(word_to_try, medical_terms)
                if fuzzy_match[1] > 75 and abs(len(word_to_try) - len(fuzzy_match[0])) <= 2: #word is "close enough" to a medical_term based on fuzzy matching, length is within 2
                    index = index + j
                    medical_term_notFound = False
                    final_transcript_array.append(process.extractOne(word_to_try, medical_terms)[0])
                    #print("FOUND FUZZY", word_to_try, "|", process.extractOne(word_to_try, medical_terms)[0])

                    break

        if medical_term_notFound:
            final_transcript_array.append(processed_transcript_array[index])
            index += 1
    
    print("FINALTRANSFRIPT", final_transcript_array)
    return final_transcript_array


accuracy = []
test_index = 3
test_name = f"test_{test_index}"
model_output_file = os.path.join("Output", f"{test_name}.txt")
benchmark_file = os.path.join("Benchmark", test_name, "CallOutLog.docx")

model = []
benchmark = []

with open(model_output_file, "r", encoding="utf-8") as file:
    model_text = file.read().strip()
    model = model_text.split(",") 

benchmark = read_docx(benchmark_file)
#print("benchmark", benchmark)
#print("model", model)
medical_terms = get_medical_terms(test_name)

print("a")
model_processed = model_postprocess(model, medical_terms)
benchmark_processed = benchmark_postprocess(benchmark, medical_terms)

print("b")

error = disparity_percentage(model_processed, benchmark_processed)
print("MODEL", model_processed)
print("BENCHMARK", benchmark_processed)
print(100-error)

list1 = model_processed
list2 = benchmark_processed
edit_distance_matrix = compute_edit_distance_matrix(list1, list2)

accuracy.append(100 - error)
'''
plt.figure(figsize=(6, 6))
plt.imshow(edit_distance_matrix, cmap='Blues', interpolation='nearest')
plt.colorbar()
plt.title("Edit Distance Matrix")
plt.xlabel("Benchmark")
plt.ylabel("Model")
plt.gca().invert_yaxis()

plt.tight_layout()
plt.show()

'''

print(accuracy)
