from paragraph import Paragraph
from typing import List
import json

# Data management
# Parse the transcript file into a list of paragraph objects
def parse_transcript(file_path) -> List[Paragraph]:
    with open(file_path, 'r') as file:
        content = file.read()

    paragraphs = []
    split_tokens = ['R:', 'P:']
    start = 0

    for i in range(len(content)):
        if i > 0 and content[i:i+2] in split_tokens:
            segment = content[start:i].strip()
            if segment.startswith("R:"):
                paragraphs.append(Paragraph("question", segment[2:]))
            elif segment.startswith("P:"):
                paragraphs.append(Paragraph("answer", segment[2:]))
            start = i

    # Handle the last segment
    segment = content[start:].strip()
    if segment.startswith("R:"):
        paragraphs.append(Paragraph("question", segment[2:]))
    elif segment.startswith("P:"):
        paragraphs.append(Paragraph("answer", segment[2:]))

    return paragraphs

# Save the codes to a file
def save_to_txt(strings, filename):
    with open(filename, 'w') as file:
        file.write('\n'.join(strings))

# Extract from JSON object
def extract_json(s):
    start = s.find("{")
    end = s.rfind("}") + 1
    return s[start:end]

# AI related
# Create an AI prompt to send to an AI for coding
def createUserPrompt(sentence: str, sentenceContext: str, interviewerQuestion: str, interviewTopic: str, existingCodes: [str]) -> str:
    start = f"I am coding an interview on {interviewTopic}. I need help coding a sentence from the interview. Please generate codes for the following sentece: \"{sentence}\"\n"
    context = f"To better understand the sentence, here is the participant's response so far: {sentenceContext}\n"
    question = f"Sometimes, the interviewer question may be important to correctly code the sentece. Here is the interviewer question: {interviewerQuestion}\n"
    analysisInstructions = f"Code the sentence by following the below instructions: \n 1. Consider these existing codes: {existingCodes}\n Do any of them apply to the sentence? List any potentially applicable codes and the reasoning as to why they apply.\n2. Carefully consider the sentence and create new codes if applicable. List the potential new codes and the reasoning as to why they apply.\n3. Generate a JSON object that contains all the applied codes, both the ones (if any) selected from existing codes and new codes. The JSON object should contain only an array of strings that represent codes. Do not include the reasoning behind each code. Do not split the codes between existing and newly created. Just add all the codes in one single array in JSON format. The array should be labeled \"codes\""

    final = start+context+question+analysisInstructions
    if sentenceContext == "":
        final = start+question+analysisInstructions

    return final

def handleResponse(response: str) -> List[str]:
    print(response)
    print("Extracting json...")
    new_codes = []
    try:
        json_string = extract_json(response)
        data = json.loads(json_string)
        new_codes = data["codes"]
        print(f"NEW CODES: {new_codes}")

    except ValueError:  # includes simplejson.decoder.JSONDecodeError
        print('Decoding JSON has failed')

    return new_codes
