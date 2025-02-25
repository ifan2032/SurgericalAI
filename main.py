import whisper
import os
from fuzzywuzzy import process #fuzzy matching to get medical lingo
from docx import Document

if __name__ == "__main__":
    model = whisper.load_model("medium")

    # Tests
    i = 2
    #for i in range(test):
    test_name = f"test_{i}"
    recording_file = os.path.join("Benchmark", test_name, f"{test_name}.wav")

    doc = Document(os.path.join("Benchmark", test_name, f"Unique.docx"))
    medical_terms = [para.text.strip() for para in doc.paragraphs if para.text.strip()]  # Remove empty lines



    transcript = model.transcribe(recording_file) # complete string output of callout

    print("model is done")
    transcript_callouts = transcript["text"].split(",")
    transcript_callouts_filtered = [word for word in transcript_callouts if word.strip()] # Remove empty callouts

    transcript_callouts_medical_corrected = [process.extractOne(word, medical_terms)[0] if process.extractOne(word, medical_terms)[1] > 80 else word for word in transcript_callouts_filtered]

    output_file = os.path.join("Output", f"{test_name}.txt")
    with open(output_file, "w") as file:
        output_str = ",".join(transcript_callouts_medical_corrected)
        file.write(output_str)

print("transcript saved")