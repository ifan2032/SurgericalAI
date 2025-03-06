import requests
import ollama
import os
from docx import Document

test_index = 1
test_name = f"test_{test_index}"

model_output_file = os.path.join("Output", f"{test_name}.txt")

transcript = "" 

with open(model_output_file, "r", encoding="utf-8") as file:
    transcript = file.read().strip()

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

medical_terms = get_medical_terms(test_name)
prompt = f"""The following transcript is from a surgical operating room (OR). The transcript may contain errors because the speech-to-text program was not trained on clinical language, meaning some surgical instrument names could be misspelled or phonetically incorrect.

Given the transcript below and the master list of instrument names, extract the words from the transcript that match the words in the master list. If a word in the transcript is misspelled or phonetically incorrect, correct it by mapping it to the closest word in the master list.

Once the instrument names are corrected, return the list of instruments **in the exact order** they were mentioned in the transcript, separated by commas, without any additional explanation. Each instrument in the output should be a instrument in the master list. 

Transcript:
{transcript}

Master List:
{medical_terms}

"""

print(transcript)


for response in ollama.chat(model='llama3', messages=[{'role': 'user', 'content': prompt}], stream=True):
    print(response['message']['content'], end='', flush=True)


# token: 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