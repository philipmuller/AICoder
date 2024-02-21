import openai
import json
import os
from interview_parser import parse_transcript
from paragraph import Paragraph
from prompts import system
from prompts import createUserPrompt
from dotenv import load_dotenv

# Initialize OpenAI API client
load_dotenv()
openai.api_key = os.getenv("OPENAI_KEY")

# Load interview file
paragraphs = parse_transcript("transcript.txt")
interviewTopic = "Describe topic"

codes = []
file_path = "codes.txt" #this is the file in which the codes will be stored

start_from_target = False
target_sentence = "Insert the sentence you want to start with"

if os.path.exists(file_path):
    with open(file_path, 'r') as file:
        sntn = file.readlines()
    sntn = [sentence.strip() for sentence in sntn]
    codes.extend(sntn)
else:
    print("Couldn't find codes file")

def save_to_txt(strings, filename):
    with open(filename, 'w') as file:
        file.write('\n'.join(strings))

def request(sentence: str, context: str, interviewerQuestion: str) -> str:
    requestUserContent = createUserPrompt(sentence, context, interviewerQuestion, interviewTopic, list(set(codes)))
    print(f"\nNEW REQUEST: {requestUserContent}")
    result = openai.ChatCompletion.create(model="gpt-4", messages=[{"role": "system", "content": system}, {"role": "user", "content": requestUserContent}])
    #print(result)
    #print(result["choices"][0]["message"]["content"])
    return result["choices"][0]["message"]["content"]

def extract_json(s):
    start = s.find("{")
    end = s.rfind("}") + 1
    return s[start:end]

def handleResponse(response: str):
    print(response)
    print("Extracting json...")
    try:
        json_string = extract_json(response)
        data = json.loads(json_string)
        new_codes = data["codes"]
        print(f"NEW CODES: {new_codes}")
        codes.extend(new_codes)
        save_to_txt(codes, "codes.txt")
    except ValueError:  # includes simplejson.decoder.JSONDecodeError
        print('Decoding JSON has failed')




# Extract themes from each sentence using OpenAI's API
currentQuestion = ""

for paragraph in paragraphs:
    if paragraph.type == "question":
        currentQuestion = paragraph.text
    else:
        if len(paragraph.sentences) > 1:
            for sentence in paragraph.sentences:
                if start_from_target:
                    if sentence == target_sentence:
                        response = request(sentence, paragraph.provideContext(sentence), currentQuestion)
                        handleResponse(response)
                        start_from_target = False
                else:
                    response = request(sentence, paragraph.provideContext(sentence), currentQuestion)
                    handleResponse(response)
        else:
            if start_from_target:
                if paragraph.text == target_sentence:
                    response = request(paragraph.text, "", currentQuestion)
                    handleResponse(response)
                    start_from_target = False
                else:
                    response = request(paragraph.text, "", currentQuestion)
                    handleResponse(response)


save_to_txt(codes, "codes.txt")
