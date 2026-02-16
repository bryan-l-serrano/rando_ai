import easyocr

    # Create a Reader object with desired languages (e.g., English)
reader = easyocr.Reader(['en'])

    # Perform OCR on an image file
results = reader.readtext('image.png')

wordList = []
    # Extract and print the recognized text
for (bbox, text, prob) in results:
    #print(f"Text: {text}, Confidence: {prob:.2f}")
    wordList.append(text)

print(wordList)