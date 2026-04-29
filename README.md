The Shakespearean — A Historical Figure Chatbot
A command-line chatbot that impersonates William Shakespeare as he would have been in 1605. Type in plain modern English and Shakespeare responds in Elizabethan style.

Requirements:

Python 3.7 or higher
A HuggingFace account and API token

Setup:
1. Install the required library:
pip install huggingface_hub

2. Get a HuggingFace API token:

Go to huggingface.co
Click your profile → Settings → Access Tokens
Create a new token with read permissions

3. Set your token as an environment variable:

Mac/Linux:
export HF_TOKEN=your_token_here

Windows:
set HF_TOKEN=your_token_here

4. Make sure both files are in the same folder:

your-folder/
├── TheShakespearean.py
└── system_prompt.txt

Running the Chatbot
python3 TheShakespearean.py


Note:

If you see a HF_TOKEN error, make sure you set your environment variable before running the app