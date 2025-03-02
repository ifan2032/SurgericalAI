import whisper
import os

def transcribe_audio(model, test_index):
    # Given the test_index (Benchmark/test_index), output raw transcript from speech --> text
    test_name = f"test_{test_index}"
    recording_file = os.path.join("Benchmark", test_name, f"{test_name}.wav")
    output_file = os.path.join("Output", f"{test_name}.txt")

    # Transcribe audio [TIME INTENSIVE]
    raw_transcript = model.transcribe(recording_file)
    return raw_transcript

def output_file_from_transcript(transcript):
    # Save transcript
    with open(output_file, "w") as file:
        file.write(raw_transcript["text"])


def main():
    model = whisper.load_model("medium") # CHANGE to test other speech --> text models
    test_index = 1 # Test case index
    transcript = transcribe_audio(model, test_index)
    output_file_from_transcript(transcript)


if __name__ == "__main__":
    main()
