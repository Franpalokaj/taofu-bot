# Taofu Ecosystem Chatbot MVP

A minimal chatbot that helps people learn about the Taofu (taofu.xyz) ecosystem. Deployed on both Discord and Twitter to test user engagement.

## 🚀 Quick Start

This project is designed to be deployed in under 2 hours. Follow these steps:

### 1. Get API Keys

#### OpenAI API Key
1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Create an account and add billing information
3. Generate an API key in the API Keys section
4. Copy the key (starts with `sk-`)

#### Discord Bot Token
1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application
3. Go to "Bot" section and create a bot
4. Copy the bot token
5. Enable "Message Content Intent" under Privileged Gateway Intents
6. Use [Discord OAuth2 Generator](https://discord.com/api/oauth2/authorize?client_id=YOUR_CLIENT_ID&permissions=2048&scope=bot) to invite bot to your server

#### Twitter API Keys
1. Go to [Twitter Developer Portal](https://developer.twitter.com/)
2. Apply for a developer account (Basic access is sufficient)
3. Create a new app/project
4. Generate the following keys:
   - API Key and Secret
   - Access Token and Secret
   - Bearer Token

### 2. Set Up Environment Variables

Copy `env.example` to `.env` and fill in your API keys:

```bash
cp env.example .env
```

Edit `.env` with your actual API keys:

```env
OPENAI_API_KEY=sk-your-openai-key-here
DISCORD_TOKEN=your-discord-bot-token-here
TWITTER_API_KEY=your-twitter-api-key-here
TWITTER_API_SECRET=your-twitter-api-secret-here
TWITTER_ACCESS_TOKEN=your-twitter-access-token-here
TWITTER_ACCESS_SECRET=your-twitter-access-secret-here
TWITTER_BEARER_TOKEN=your-twitter-bearer-token-here
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Test Locally

#### Test Discord Bot
```bash
python bot.py
```

In Discord, try:
- `!taofu help`
- `!taofu ask What is Taofu?`

#### Test Twitter Bot
```bash
python twitter_bot.py
```

The bot will monitor mentions and reply to questions.

### 5. Deploy to Railway

1. Install Railway CLI:
```bash
npm install -g @railway/cli
```

2. Login to Railway:
```bash
railway login
```

3. Initialize and deploy:
```bash
railway init
railway up
```

4. Set environment variables in Railway dashboard:
   - Go to your project in Railway
   - Add all variables from your `.env` file

## 📁 Project Structure

```
taofu-bot/
├── bot.py                    # Discord bot with OpenAI integration
├── twitter_bot.py            # Twitter bot with OpenAI integration
├── knowledge.txt             # Taofu documentation and knowledge base
├── system_instructions.txt   # Bot behavior rules and guidelines
├── analytics.json            # Question logging (auto-generated)
├── replied_tweets.json       # Twitter reply tracking (auto-generated)
├── requirements.txt          # Python dependencies
├── railway.json             # Railway deployment config
├── env.example              # Environment variables template
└── README.md                # This file
```

## 🤖 Bot Features

### Discord Bot
- **Commands**: `!taofu ask <question>` and `!taofu help`
- **Features**: 
  - OpenAI GPT-4 integration
  - Question analytics logging
  - Long message splitting
  - Error handling
  - Typing indicators

### Twitter Bot
- **Functionality**: Monitors mentions and replies to questions
- **Features**:
  - Automatic question detection
  - Character limit handling
  - Duplicate reply prevention
  - Analytics logging
  - Rate limit handling

### Analytics
Both bots log questions to `analytics.json` with:
- Timestamp
- User ID/username
- Question asked
- Response preview
- Platform (Discord/Twitter)

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key | Yes |
| `DISCORD_TOKEN` | Discord bot token | Yes |
| `TWITTER_API_KEY` | Twitter API key | Yes |
| `TWITTER_API_SECRET` | Twitter API secret | Yes |
| `TWITTER_ACCESS_TOKEN` | Twitter access token | Yes |
| `TWITTER_ACCESS_SECRET` | Twitter access secret | Yes |
| `TWITTER_BEARER_TOKEN` | Twitter bearer token | Yes |
| `BOT_PREFIX` | Discord command prefix | No (default: `!taofu`) |
| `MAX_RESPONSE_LENGTH` | Max response length | No (default: 2000) |
| `TWITTER_CHECK_INTERVAL` | Twitter check interval (seconds) | No (default: 60) |

### Knowledge Base

Edit `knowledge.txt` to update the bot's knowledge about Taofu. The file contains facts, concepts, and information about the ecosystem. This gets injected into the AI system prompt.

### System Instructions

Edit `system_instructions.txt` to modify the bot's behavior rules, response guidelines, safety protocols, and limitations. This file controls:
- What the bot should NEVER do
- Authorized numbers the bot can mention
- Response guidelines and tone
- Safety rules and fallback responses
- Platform-specific behavior

## 📊 Analytics

The bots automatically log all interactions to `analytics.json`. You can analyze this data to understand:

- Most common questions
- User engagement patterns
- Response effectiveness
- Platform usage

## 🚨 Troubleshooting

### Common Issues

1. **Discord Bot Not Responding**
   - Check if bot has proper permissions
   - Verify `Message Content Intent` is enabled
   - Ensure bot is invited to the server

2. **Twitter Bot Not Replying**
   - Verify all Twitter API keys are correct
   - Check if the bot account has proper permissions
   - Ensure the bot is mentioned in tweets

3. **OpenAI API Errors**
   - Verify your API key is correct
   - Check your OpenAI billing/credits
   - Ensure you're using a valid model

4. **Railway Deployment Issues**
   - Check environment variables are set correctly
   - Verify the start command in `railway.json`
   - Check Railway logs for specific errors

### Logs

Both bots print detailed logs to help with debugging:
- Discord bot: Shows connection status and command processing
- Twitter bot: Shows mention monitoring and reply attempts

## 🔄 Updates

### Updating Knowledge Base
1. Edit `knowledge.txt` for new Taofu information
2. Edit `system_instructions.txt` for behavior changes
3. Redeploy to Railway: `railway up`

### Adding New Commands
1. Modify `bot.py` to add new Discord commands
2. Test locally first
3. Deploy changes

### Monitoring Performance
- Check Railway dashboard for resource usage
- Monitor OpenAI API usage and costs
- Review analytics.json for user patterns

## 📈 Success Metrics

Track these metrics to measure success:
- **50+ unique users** asking questions in first week
- **80%+ accurate responses** (community validated)
- **Clear data** on what people want to know
- **User engagement** patterns and trends

## 🛡️ Safety Features

- Rate limiting per user (configurable)
- Content filtering for inappropriate questions
- Error handling that doesn't expose system details
- Backup responses when APIs are down

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review Railway logs
3. Check analytics.json for patterns
4. Visit taofu.xyz for official information

## 🎯 Next Steps

After successful MVP launch:
1. **Week 1**: Monitor questions and update knowledge base
2. **Week 2**: Add frequently asked questions
3. **Future**: Consider web interface, more commands, advanced analytics

---

**Built for the Taofu ecosystem** - Visit [taofu.xyz](https://taofu.xyz) for more information! 