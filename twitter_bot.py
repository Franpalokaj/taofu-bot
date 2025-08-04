import tweepy
import openai
import json
import os
import time
from datetime import datetime
from dotenv import load_dotenv
import re

# Load environment variables
load_dotenv()

# Twitter API configuration
auth = tweepy.OAuthHandler(
    os.getenv('TWITTER_API_KEY'),
    os.getenv('TWITTER_API_SECRET')
)
auth.set_access_token(
    os.getenv('TWITTER_ACCESS_TOKEN'),
    os.getenv('TWITTER_ACCESS_SECRET')
)

# Create API object
api = tweepy.API(auth, wait_on_rate_limit=True)

# Create client for Twitter API v2
client = tweepy.Client(
    bearer_token=os.getenv('TWITTER_BEARER_TOKEN'),
    consumer_key=os.getenv('TWITTER_API_KEY'),
    consumer_secret=os.getenv('TWITTER_API_SECRET'),
    access_token=os.getenv('TWITTER_ACCESS_TOKEN'),
    access_token_secret=os.getenv('TWITTER_ACCESS_SECRET'),
    wait_on_rate_limit=True
)

# OpenAI configuration
openai.api_key = os.getenv('OPENAI_API_KEY')

# Load knowledge base
def load_knowledge_base():
    try:
        with open('knowledge.txt', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "Taofu is a decentralized ecosystem. Visit taofu.xyz for more information."

# Load system instructions
def load_system_instructions():
    try:
        with open('system_instructions.txt', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return """You are the official Taofu ecosystem assistant on Twitter. You help people learn about the Taofu ecosystem and provide accurate information based on the official documentation.

IMPORTANT RULES:
1. Only answer questions based on the provided Taofu knowledge base
2. Never make up numbers, technical details, or tokenomics information
3. If you're unsure about something, admit it and direct users to taofu.xyz
4. Keep responses concise (under 250 characters for Twitter)
5. Always mention you're the official Taofu assistant
6. Encourage users to visit taofu.xyz for more information
7. Be friendly and helpful"""

KNOWLEDGE_BASE = load_knowledge_base()
SYSTEM_INSTRUCTIONS = load_system_instructions()

# Load replied tweets
def load_replied_tweets():
    try:
        with open('replied_tweets.json', 'r') as f:
            return set(json.load(f))
    except (FileNotFoundError, json.JSONDecodeError):
        return set()

def save_replied_tweets(replied_tweets):
    with open('replied_tweets.json', 'w') as f:
        json.dump(list(replied_tweets), f)

# Analytics logging
def log_question(user_id, username, question, response_preview, platform="Twitter"):
    try:
        with open('analytics.json', 'r') as f:
            analytics = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        analytics = []
    
    analytics.append({
        'timestamp': datetime.now().isoformat(),
        'user_id': str(user_id),
        'username': username,
        'question': question,
        'response_preview': response_preview[:100] + "..." if len(response_preview) > 100 else response_preview,
        'platform': platform
    })
    
    with open('analytics.json', 'w') as f:
        json.dump(analytics, f, indent=2)

# System prompt for OpenAI
SYSTEM_PROMPT = f"""{SYSTEM_INSTRUCTIONS}

TAOFU KNOWLEDGE BASE:
{KNOWLEDGE_BASE}

Remember: If asked about specific technical details, tokenomics, or information not covered in the knowledge base, direct users to taofu.xyz for the most current and accurate information."""

def get_ai_response(question):
    """Get response from OpenAI API"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": question}
            ],
            max_tokens=200,  # Shorter for Twitter
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return "I'm having trouble connecting right now. Please visit taofu.xyz for information."

def clean_question(text, bot_username):
    """Extract the actual question from a tweet"""
    # Remove the bot mention
    text = re.sub(f'@{bot_username}', '', text, flags=re.IGNORECASE)
    # Remove common prefixes
    text = re.sub(r'^(hey|hi|hello|yo)\s+', '', text, flags=re.IGNORECASE)
    # Clean up extra whitespace
    text = ' '.join(text.split())
    return text.strip()

def is_valid_question(text):
    """Check if the text contains a valid question"""
    # Remove common words that don't indicate a question
    question_words = ['what', 'how', 'when', 'where', 'why', 'who', 'which', 'can', 'could', 'would', 'should', 'is', 'are', 'do', 'does', 'tell', 'explain', 'help']
    
    text_lower = text.lower()
    return any(word in text_lower for word in question_words) or '?' in text

def truncate_response(response, max_length=250):
    """Truncate response to fit Twitter character limit"""
    if len(response) <= max_length:
        return response
    
    # Try to end at a sentence
    truncated = response[:max_length-3]
    last_period = truncated.rfind('.')
    last_exclamation = truncated.rfind('!')
    last_question = truncated.rfind('?')
    
    end_point = max(last_period, last_exclamation, last_question)
    
    if end_point > max_length * 0.7:  # If we can end at a sentence
        return response[:end_point+1]
    else:
        return truncated + "..."

def monitor_mentions():
    """Monitor mentions and respond to questions"""
    replied_tweets = load_replied_tweets()
    bot_username = api.verify_credentials().screen_name
    
    print(f"Monitoring mentions for @{bot_username}")
    
    while True:
        try:
            # Get mentions
            mentions = api.mentions_timeline(count=20)
            
            for mention in mentions:
                tweet_id = mention.id
                
                # Skip if we've already replied
                if tweet_id in replied_tweets:
                    continue
                
                # Extract the question
                question = clean_question(mention.text, bot_username)
                
                # Check if it's a valid question
                if not is_valid_question(question):
                    print(f"Skipping tweet {tweet_id}: Not a valid question")
                    replied_tweets.add(tweet_id)
                    save_replied_tweets(replied_tweets)
                    continue
                
                print(f"Processing question: {question}")
                
                # Get AI response
                response = get_ai_response(question)
                
                # Truncate for Twitter
                response = truncate_response(response)
                
                # Add signature if space allows
                if len(response) < 200:
                    response += " Learn more at taofu.xyz"
                
                # Log the question
                log_question(
                    user_id=mention.user.id,
                    username=mention.user.screen_name,
                    question=question,
                    response_preview=response,
                    platform="Twitter"
                )
                
                # Reply to the tweet
                try:
                    api.update_status(
                        status=response,
                        in_reply_to_status_id=tweet_id,
                        auto_populate_reply_metadata=True
                    )
                    print(f"Replied to tweet {tweet_id}: {response}")
                    
                    # Mark as replied
                    replied_tweets.add(tweet_id)
                    save_replied_tweets(replied_tweets)
                    
                except Exception as e:
                    print(f"Error replying to tweet {tweet_id}: {e}")
            
            # Wait before next check
            time.sleep(int(os.getenv('TWITTER_CHECK_INTERVAL', 60)))
            
        except Exception as e:
            print(f"Error in mention monitoring: {e}")
            time.sleep(60)  # Wait a minute before retrying

def main():
    """Main function to run the Twitter bot"""
    try:
        # Verify credentials
        user = api.verify_credentials()
        print(f"Twitter bot authenticated as @{user.screen_name}")
        
        # Start monitoring mentions
        monitor_mentions()
        
    except Exception as e:
        print(f"Error starting Twitter bot: {e}")

if __name__ == "__main__":
    main() 