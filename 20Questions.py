import openai
import os

from openai import OpenAI 

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


def openTextFile(input: str) -> None:
    f = open("20_Questions_Glossary.txt", "a")
    f.write(f"{input}\n")
    f.close()
    return 

def readTextFile() -> str:
    f = open("20_Questions_Glossary.txt")
    fileGlossary = ""
    for _ in f: 
        fileGlossary += f.read()
    return fileGlossary

def thinkWord() -> str:
    fileGlossary = readTextFile()
    model = "gpt-4o"
    prompt = f"hi chatgpt. I want to play a game of 20 questions. To avoid confusion. I'm not going to be playing the game with you. Just name me a random thing? The only catch is you can't use any of these words: {fileGlossary}"
    completions = client.chat.completions.create(model=model, messages = [{"role": "system", "content": "You are a helpful assistant that only answers in 1 word answers"},
                                                                        {"role": "user", "content" : prompt}])

    answer = completions.choices[0].message.content
    return answer


def runGame() -> None:
    numGuesses = 20
    answer = thinkWord()
    if answer[-1] == '.':
        answer = answer[0,-1]
        
    # If you would like to know the generated word
    # print("word is: ", answer)
    openTextFile(answer)
    while numGuesses != 0: 
        question = input(f"Input Question {numGuesses}: ")

        model = "gpt-4o"
        completion = client.chat.completions.create(model=model, messages = [{"role": "system", "content": f"You are an assistant helping me play 20 questions. You have already been given the answer word which is: {answer}. If you believe the user has guessed the word I want you to say Victory! \nOtherwise, I need you to answer in only yes or no responses."},
                                                                             {"role": "user", "content": question}])
        hint = completion.choices[0].message.content
        print("\nchatgpt outputs", hint,"\n")
        if hint == "Victory!":
            againInput = input("You Won 20 Questions!\n\nWould you like to play again?\n\nInput: y/n   ")
            if againInput == 'y':
                runGame()
            else: 
                return 
        numGuesses -= 1
    
    print(f"You LOST! The word was: {answer}!\n\nWould you like to play again?\n\nInput: y/n   ")
    
    return

runGame()

