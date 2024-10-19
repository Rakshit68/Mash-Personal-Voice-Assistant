import tkinter as tk
import sys
import speech_recognition as sr
import pyttsx3
import os
import datetime
import subprocess
from plyer import notification

# Initialize the text widget
text_widget = None

# Function to set the text widget reference
def set_text_widget(widget):
    global text_widget
    text_widget = widget
    print("Text widget set to:", text_widget)

# Override sys.stdout and sys.stderr to write to the Text widget
class StdoutRedirector(object):
    def __init__(self, widget):
        self.widget = widget

    def write(self, text):
        if self.widget:
            # Temporarily remove the redirection to avoid recursion error
            sys.stdout = sys.__stdout__
            self.widget.insert(tk.END, text)
            self.widget.see(tk.END)
            # Restore the redirection
            sys.stdout = self

    def flush(self):
        pass

class StderrRedirector(object):
    def __init__(self, widget):
        self.widget = widget

    def write(self, text):
        if self.widget:
            # Temporarily remove the redirection to avoid recursion error
            sys.stderr = sys.__stderr__
            self.widget.insert(tk.END, text)
            self.widget.see(tk.END)
            # Restore the redirection
            sys.stderr = self

    def flush(self):
        pass

# Redirect stdout and stderr to the Text widget
sys.stdout = StdoutRedirector(text_widget)
sys.stderr = StderrRedirector(text_widget)

# Initialize speech recognition and text-to-speech engines
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Function to convert text to speech
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to set a reminder
def set_reminder(reminder, time):
    speak(f"Setting reminder: {reminder} at {time}")
    # Here, we'll use the notification library to display a reminder
    notification_title = "Reminder"
    notification_message = f"{reminder} at {time}"
    notification_timeout = 10  # Timeout for the notification in seconds
    notification.notify(title=notification_title, message=notification_message, timeout=notification_timeout)

# Function to add a task to the to-do list
def add_to_do(task):
    speak(f"Adding task to to-do list: {task}")
    # Here, you might implement logic to add the task to a database or file

# Function to switch off the laptop
def switch_off_laptop():
    speak("Shutting down the laptop")
    # Execute system command to shut down the laptop
    subprocess.run(['shutdown', '/s', '/t', '0'])

# Function to execute commands
def execute_command(command):
    if command is None:
        speak("No command detected. Please try again.")
        return
    
    if "open notepad" in command:
        speak("Opening Notepad")
        os.system("notepad.exe")
    elif "open calculator" in command:
        os.system("calc")
        speak("Opening Calculator")
    elif "set a reminder" in command:
        speak("What do you want to be reminded about?")
        reminder = input_command()
        speak("When do you want to be reminded?")
        time = input_command()  # Assuming user speaks time like "tomorrow at 9 AM"
        set_reminder(reminder, time)
    elif "add to my to-do list" in command:
        speak("What task would you like to add to your to-do list?")
        task = input_command()
        add_to_do(task)
    elif "shutdown" in command:
        switch_off_laptop()
    else:
        speak("Command not recognized")

# Function to capture user input from speech
def input_command():
    try:
        with sr.Microphone() as source:
            sys.stdout.write("Listening...\n")
            audio = recognizer.listen(source, timeout=30, phrase_time_limit=3) # Set a timeout value

        sys.stdout.write("Recognizing...\n")
        command = recognizer.recognize_google(audio).lower()
        sys.stdout.write("Command: " + command + "\n")
        return command
    except sr.WaitTimeoutError:
        sys.stdout.write("Timeout: No speech detected\n")
    except sr.UnknownValueError:
        sys.stdout.write("Could not understand audio.\n")
    except sr.RequestError as e:
        sys.stdout.write("Error: Could not request results; {0}\n".format(e))

# Main function to listen for voice commands
def main():
    speak("Hello! I'm your digital assistant: Mash. I hope you had a good day. How may I help you? ")

    try:
        while True:
            speak("............................")
            command = input_command()
            execute_command(command)
    except KeyboardInterrupt:
        sys.stdout.write("Keyboard interrupt detected. Exiting...\n")

if __name__ == "__main__":
    main()
