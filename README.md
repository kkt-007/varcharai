# AI Assistant 

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
[![Cross-Platform](https://img.shields.io/badge/Cross%20Platform-MacOS%20%7C%20Windows-blue)](https://www.python.org/downloads/)

## 📖 Overview  
AI Assistant is a **cross-platform supported code** that launches a real-time typing assistant. The assistant listens for a trigger word and generates AI-powered suggestions.

## ✨ Features  
✅ AI-Powered ** Assistance**

    ✅ aitext: # for general usage, e.g aitext: Write a short parahgraph on AI topic.  
    ✅ aicode: # for writng code, e.g aicode: Write a python code to identify odd even.  
    ✅ aiimage: # for generating images, e.g aiimage: Generate an ai image of varcharai.  
✅ Uses **QProcess** to run background AI listener  
✅ **Cross-Platform** (Windows, macOS)  

## ✨ Features- coming soon
✅ AI-Powered Audio and Vision  
✅ Support to other LLM Models

## 🚀 Installation  

### 1️⃣ Clone the Repository  
```sh
git clone https://github.com/kkt-007/varcharai.git
cd varcharai
```
### 2️⃣ Create a Virtual Environment
```sh
python3 -m venv .venv
source .venv/bin/activate   # macOS/Linux
# OR
.venv\Scripts\activate      # Windows
```
### 3️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```
### 4️⃣ Setup keys in .env
```sh
OPENAI_API_KEY = ''
```
### 5️⃣ Run the Application
```sh
python main.py
```
Once the Application is running it listens to the trigger words and once trigger word is detected whatever user types is taken as input after pressing the enter button.
```sh
aitext: # for general usage, looses the response format
aicode: # for wiritng code , keeps the response format
aiimage: # for generating images
```
### ⚙️ Project Structure
```sh
📂 varcharai
│── 📂 modules
│   ├── typingAssist.py  # AI typing assistant module
│   ├── aiResponder.py   # AI response processing
│   ├── activeWindow.py  # Detect active window (Mac & Windows)
│── .env  
│── main.py              # Main entry point 
│── requirements.txt     # Dependencies
│── README.md            # Documentation
```

### 🛠️ Troubleshooting

Virtual Environment Not Detected?

If python main.py does not work, ensure you’re inside the virtual environment:
```sh
source .venv/bin/activate   # macOS/Linux
# OR
.venv\Scripts\activate      # Windows
```

### macOS Permission Issues?

If you get security warnings on macOS, allow the app in:

	System Preferences → Security & Privacy → Allow Python & Terminal

### 📝 License

This project is open-source under the MIT License. Feel free to contribute! 🚀
