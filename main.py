import whisper
import os

def transcribe_audio(model, test_name):
    # Given the test_index (Benchmark/test_index), output raw transcript from speech --> text
    recording_file = os.path.join("Benchmark", test_name, f"{test_name}.wav")

    # Transcribe audio [TIME INTENSIVE]
    raw_transcript = model.transcribe(recording_file)
    return raw_transcript

def output_file_from_transcript(output_file, transcript):
    # Save transcript
    with open(output_file, "w") as file:
        file.write(transcript["text"])


def main():
    model = whisper.load_model("medium") # CHANGE to test other speech --> text models

    test_index = 3 # Test case index
    test_name = f"test_{test_index}"
    
    transcript = transcribe_audio(model, test_name)
    output_file = os.path.join("Output", f"{test_name}.txt")

    output_file_from_transcript(output_file, transcript)


if __name__ == "__main__":
    main()
