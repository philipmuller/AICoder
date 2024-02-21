import os
from util import parse_transcript, createUserPrompt, handleResponse, save_to_txt
from paragraph import Paragraph
from prompts import system
from ai import OpenAIEngine, AIEngine

interviewTopic = "Describe topic"
ai: AIEngine = OpenAIEngine(None, system)
# Load interview file
paragraphs = parse_transcript("data/transcript.txt")


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
                        message = createUserPrompt(sentence, paragraph.provideContext(sentence), currentQuestion, interviewTopic, codes)
                        response = ai.send(message)
                        new_codes = handleResponse(response)
                        codes.extend(new_codes)
                        save_to_txt(codes, "data/codes.txt")
                        start_from_target = False
                else:
                    message = createUserPrompt(sentence, paragraph.provideContext(sentence), currentQuestion, interviewTopic, codes)
                    response = ai.send(message)
                    new_codes = handleResponse(response)
                    codes.extend(new_codes)
                    save_to_txt(codes, "data/codes.txt")
        else:
            if start_from_target:
                if paragraph.text == target_sentence:
                    message = createUserPrompt(paragraph.text, "", currentQuestion, interviewTopic, codes)
                    response = ai.send(message)
                    new_codes = handleResponse(response)
                    codes.extend(new_codes)
                    save_to_txt(codes, "data/codes.txt")
                    start_from_target = False
                else:
                    message = createUserPrompt(paragraph.text, "", currentQuestion, interviewTopic, codes)
                    response = ai.send(message)
                    new_codes = handleResponse(response)
                    codes.extend(new_codes)
                    save_to_txt(codes, "data/codes.txt")


save_to_txt(codes, "codes.txt")
