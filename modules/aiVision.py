import os
from openai import OpenAI
import cv2
import speech_recognition as sr
import pyttsx3
from dotenv import load_dotenv

load_dotenv()
# OpenAI API key setup
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# Function for speech-to-text (voice recognition)
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for a command...")
        audio = recognizer.listen(source)
        try:
            # Convert speech to text
            command = recognizer.recognize_google(audio)
            print(f"Command received: {command}")
            return command
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio")
            return None
        except sr.RequestError:
            print("Could not request results from Google Speech Recognition service")
            return None

# Function to interact with OpenAI GPT and process the command
# def process_command(command):
#     # Send the command to OpenAI for interpretation and response
#     if command:
#         response = openai.Completion.create(
#             model="gpt-4",  # or use gpt-3.5-turbo
#             prompt=f"Interpret the following command: '{command}'. What should I do next?",
#             max_tokens=100
#         )
#         return response.choices[0].text.strip()
#     return None

def process_command(command):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": f"Interpret the following command: '{command}'. What should I do next?",}],
            max_tokens=500,
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error processing command: {e}"
    

# # Function to display the camera feed and analyze surroundings
# def analyze_surroundings():
#     # Capture video from the webcam (device 0 is default)
#     cap = cv2.VideoCapture(0)
#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break

#         # Display the resulting frame in a window
#         cv2.imshow("Camera Feed - Press 'q' to exit", frame)

#         # Check if 'q' is pressed to exit the loop
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     cap.release()
#     cv2.destroyAllWindows()

# Function to analyze surroundings using OpenCV
def analyze_surroundings(camera_index=0):
    # Load the pre-trained Haar Cascade for face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Capture video from the selected camera
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print(f"Error: Could not open camera {camera_index}. Please check your camera connection.")
        return

    print(f"Using Camera {camera_index}...")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break

        # Convert the frame to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        # Draw rectangles around detected faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Display the resulting frame in a window
        cv2.imshow(f"Camera {camera_index} Feed - Press 'q' to exit", frame)

        # If faces are detected, we send this info to OpenAI
        if len(faces) > 0:
            description = f"Detected {len(faces)} face(s) in the frame."
            # openai_response = process_command(description)
            print(f"OpenAI response: {description}")
            # speak_response(openai_response)

        # Check if 'q' is pressed to exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Function to speak back the response (using text-to-speech)
def speak_response(response):
    engine = pyttsx3.init()
    engine.say(response)
    engine.runAndWait()

def main():
    # Recognize voice command
    command = recognize_speech()

    # Process command using OpenAI
    if command:
        # openai_response = process_command(command)
        # print(f"OpenAI response: {openai_response}")

        # # Speak the response
        # speak_response(openai_response)

        # Analyze the surroundings (activate camera if needed)
        if "analyze surroundings" in command.lower():
            print("Analyzing surroundings...")
            
            # Allow the user to choose which camera to use (0 = first camera, 1 = second camera, etc.)
            try:
                camera_index = int(input("Enter camera index (0 for first camera, 1 for second, etc.): "))
                analyze_surroundings(camera_index)
            except ValueError:
                print("Invalid camera index. Using default camera (0).")
                analyze_surroundings(0)  # Default to the first camera

if __name__ == "__main__":
    main()
