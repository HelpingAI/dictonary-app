from flask import Flask, render_template, request, jsonify, redirect, url_for
import requests
from bs4 import BeautifulSoup
import pyttsx3

app = Flask(__name__)

def get_word_definition(word):
    base_url = f"https://www.merriam-webster.com/dictionary/{word}"

    # Send an HTTP GET request
    response = requests.get(base_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the definition element on the page
        definition = soup.find("span", class_="dtText")

        # Check if a definition was found
        if definition:
            # Get the full definition text
            full_definition = definition.get_text()

            # Split the full definition into sentences
            sentences = full_definition.split('. ')

            # Combine the first few sentences to limit the definition to 20-25 words
            limited_definition = '. '.join(sentences[:3])  # Adjust the number of sentences as needed

            return limited_definition
        else:
            return "Definition not found."

    else:
        return "Word not found or unable to retrieve data."

def speak_word(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/lookup', methods=['POST'])
def lookup():
    word = request.form['word']
    definition = get_word_definition(word)
    formatted_definition = f"<span style='color: blue;'>{definition}</span>"
    speak_word(definition)
    return render_template('result.html', word=word, definition=formatted_definition)

if __name__ == '__main__':
    app.run(debug=True)
