from modules.typingAssist import TypingAssistant

if __name__ == "__main__":
    print("Starting AI listener. Type your trigger word to begin.")
    print("Press Ctrl+C to exit.")
    assistant = TypingAssistant()
    assistant.start_listeners()