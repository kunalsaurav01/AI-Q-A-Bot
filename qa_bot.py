import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class AIQuestionAnswerBot:
    def __init__(self):
        """Initialize the AI Q&A Bot with Gemini API"""
        # Get API key from environment variable
        api_key = os.getenv('GEMINI_API_KEY')
        
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found! Please set it in .env file")
        
        # Configure Gemini API
        genai.configure(api_key=api_key)
        
        # Initialize the model
        self.model = genai.GenerativeModel('gemini-pro')
        
        print("🤖 AI Q&A Bot initialized successfully!")
        print("=" * 50)
    
    def ask_question(self, question):
        """Send a question to Gemini and get an answer"""
        try:
            # Generate response
            response = self.model.generate_content(question)
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"
    
    def run(self):
        """Main loop for the command-line interface"""
        print("\n💬 Welcome to the AI Q&A Bot!")
        print("Ask me anything, or type 'quit' to exit.\n")
        
        while True:
            # Get user input
            question = input("You: ").strip()
            
            # Check if user wants to quit
            if question.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Thank you for using AI Q&A Bot! Goodbye!")
                break
            
            # Skip empty questions
            if not question:
                print("Please enter a question.\n")
                continue
            
            # Get answer from AI
            print("\n🤔 Thinking...\n")
            answer = self.ask_question(question)
            print(f"Bot: {answer}\n")
            print("-" * 50 + "\n")

def main():
    """Main entry point"""
    try:
        bot = AIQuestionAnswerBot()
        bot.run()
    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
        print("\nPlease follow these steps:")
        print("1. Create a .env file in the project directory")
        print("2. Add this line: GEMINI_API_KEY=your_actual_api_key")
        print("3. Replace 'your_actual_api_key' with your real Gemini API key")
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")

if __name__ == "__main__":
    main()