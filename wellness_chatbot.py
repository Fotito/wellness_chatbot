import os
from dotenv import load_dotenv
from openai import OpenAI

# ====================== CONFIG ======================
# Load environment variables from .env or chatbot.env
if not load_dotenv("chatbot.env") and not load_dotenv(".env"):
    print("⚠️  Warning: Could not find .env or chatbot.env file!")

# Get API key and check it exists
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError(
        "❌ OPENAI_API_KEY not found!\n"
        "Please create a .env or chatbot.env file with your OpenAI key."
    )

client = OpenAI(api_key=api_key)

# System prompt - This defines the coach's personality
system_prompt = """
You are a supportive wellness and mindset coach inspired by Marisa Peer.
Your core message is "I am enough". 

Help users build confidence, self-belief, overcome limiting beliefs, and support personal transformation.
Be warm, encouraging, empathetic, and practical. 
Keep responses concise but insightful (2-4 paragraphs maximum).
Always end with a gentle follow-up question to continue the conversation.
"""

# Conversation history (memory)
messages = [{"role": "system", "content": system_prompt}]

# ====================== START CHATBOT ======================
print("🌿 Welcome to your Wellness Mindset Coach Chatbot!")
print("Type 'quit', 'exit', or 'bye' to end the conversation.\n")

while True:
    user_input = input("You: ").strip()

    if user_input.lower() in ["quit", "exit", "bye"]:
        print("Coach: Take care — remember, you are enough. 💪")
        break

    # Add user message to history
    messages.append({"role": "user", "content": user_input})

    # Get response from OpenAI
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",   # Fast and affordable model
            messages=messages,
            temperature=0.7,
            max_tokens=600
        )

        assistant_reply = response.choices[0].message.content.strip()

        print(f"Coach: {assistant_reply}\n")

        # Add coach's reply to history so it remembers the conversation
        messages.append({"role": "assistant", "content": assistant_reply})

    except Exception as e:
        print(f"❌ Error: {e}")
        print("   Please check your API key, internet connection, and that you have credits in your OpenAI account.")