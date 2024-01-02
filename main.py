import pyttsx4
import speech_recognition as sr
#import openai
import random

# set openai api key

#
# openai.api_key =  " "

model_id = 'gpt-3.5-turbo'

#initialize speech engine

engine = pyttsx4.init()

#change speech rate

engine.setProperty('rate', 180)

#get the available voice

voices = engine.getProperty('voice')

#choose a voice based on voice id
#engine.setProperty('voice',  voices[1].id)

#counter for interaction purposes
interaction_counter = 0

def transcribe_audio_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
        try:
            return recognizer.recognize_google(audio)
        except:
            print("")

def ChatGpt_Convo(conversation):
    response = openai.ChatCompletion.create(
        model = model_id,
        messages=conversation
    ) 
    
    api_usage = response['usage']
    print ('total token consumed: {0}'.format(api_usage['total_tokens']))
    conversation.append({'role': response.choices[0].message.role, 'content': response.choice[0].messge.content})
    return conversation

def speak_text(text):
    engine.say(text)
    engine.runAndWait()
    
# starting a conversation
conversation = []
conversation.append({'role': 'user', 'content': 'Please act like Friday AI from Iron Man, make a 1 sentence phrase introducing yourself without saying something that sounds like this chat is already'})
conversation = ChatGpt_Convo(conversation)
print('{0}: {1}\n'.format(conversation[-1]['role'].strip(), conversation[-1]['content'].strip()))
speak_text(conversation[-1]['content'].strip())


def activate_assistant():
    starting_chat_phrases = ["Hello Cienne, what can I do for you?", 
                            "Hey Cienne, what's up?",
                            "Hi Lhue, having trouble?",
                            "Yo! Missing me already?",
                            "Cienne! Good to hear from you again. What can assist you with?",
                            "Eliah here!! Need a companion? I'm here for you",
                            "Eliah to the rescue!! What's on your mind honey? You can tell me anything"]
    
    continued_chat_phrases = ["yes", "of course", "okay", "I'm listening", "and"]
    random_chat = "" 
    if(interaction_counter == 1):
        random_chat = random.choice(starting_chat_phrases)
    else:
        random_chat = random.choice(continued_chat_phrases)
        
        return random_chat
    
def append_to_log(text):
    with open("chat_log.txt", "a") as f:
        f.write(text + "\n")
        
while True:
    print("Say 'Eliah' to start...")
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        audio = recognizer.listen(source)
        try:
            transcription = recognizer.recognize_google(audio)
            if "Eliah" in transcription.lower():
                interaction_counter += 1
                
                # record audio
                filename = "input.wav"
                
                readyToWork = activate_assistant()
                speak_text(readyToWork)
                print(readyToWork)
                recognizer = sr.Recognizer()
                with sr.Microphone() as source:
                    source.pause_threshold = 1
                    audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)
                    with open(filename, "wb") as f:
                        f.write(audio.get_wav_data())
                        
                text = transcribe_audio_to_text(filename)
                
                if text:
                    print(f"You said: {text}")
                    append_to_log(f"You: {text}\n")
                    
                    #generate response using ChatGPT
                    print(f"Eliah says: {conversation}")
                    
                    prompt = text
                    
                    conversation.append({'role': 'user', 'content': prompt})
                    conversation = ChatGpt_Convo(conversation)
                    
                    print('{0}: {1}\n'.format(conversation[1]['role'].strip(),conversation[-1]['content'].strip()))
                    
                    append_to_log(f"Eliah: {conversation[-1]['content'].strip()}")
                    
                    #read response using text to speech
                    speak_text(conversation[-1]['content'].strip())
                    
        except Exception as e:
            continue 
        #print("an error occured: {}".format(e))
                    
                                
    
       
 
