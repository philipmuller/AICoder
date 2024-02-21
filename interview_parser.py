from paragraph import Paragraph

def parse_transcript(file_path) -> [Paragraph]:
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
