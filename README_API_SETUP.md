# Google AI API Setup Guide

## Getting a Valid API Key

1. **Go to Google AI Studio**: Visit https://makersuite.google.com/app/apikey
2. **Sign in** with your Google account
3. **Create a new API key** by clicking "Create API Key"
4. **Copy the API key** - it should look like: `AIzaSyC...` (much longer than the current one)

## Setting Up the API Key

### Option 1: Update .env file
Edit the `.env` file and replace the current API key:
```
GEMINI_API_KEY=your_new_api_key_here
```

### Option 2: Set environment variable
```bash
export GEMINI_API_KEY=your_new_api_key_here
```

## Testing the API Key

Run the test script to verify your API key works:
```bash
python test_api_key.py
```

## Current Issue

The current API key `AIzaSyAh-xagm9EVv2zJ6rHB_FavTVRXG7oSh6A` is invalid or doesn't have Gemini API access. You need a fresh API key from Google AI Studio. 