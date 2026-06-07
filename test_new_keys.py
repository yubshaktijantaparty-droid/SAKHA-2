#!/usr/bin/env python3
"""Test the new OpenRouter API keys"""

import os
from dotenv import load_dotenv
import asyncio
import aiohttp

# Load environment variables
load_dotenv()

# Get the new API keys
owl_alpha_key = os.getenv("OPENROUTER_OWL_ALPHA_API_KEY")
premium_key = os.getenv("OPENROUTER_PREMIUM_API_KEY")

print(f"OWL-ALPHA Key loaded: {bool(owl_alpha_key)}")
print(f"PREMIUM Key loaded: {bool(premium_key)}")

if owl_alpha_key:
    print(f"OWL-ALPHA Key starts with: {owl_alpha_key[:20]}...")

if premium_key:
    print(f"PREMIUM Key starts with: {premium_key[:20]}...")

async def test_api_key(api_key: str, key_name: str):
    """Test an API key with OpenRouter"""
    async with aiohttp.ClientSession() as session:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "HTTP-Referer": "http://localhost:5175",
            "X-Title": "SAKHA AI Test",
        }
        
        data = {
            "model": "openai/gpt-3.5-turbo",
            "messages": [{"role": "user", "content": "What is a radar system?"}],
            "temperature": 0.7,
            "max_tokens": 500,
        }
        
        try:
            async with session.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                print(f"\n{key_name} - Status: {response.status}")
                result = await response.json()
                if response.status == 200:
                    print(f"{key_name} - SUCCESS! Got response:")
                    if "choices" in result:
                        print(f"Response: {result['choices'][0]['message']['content'][:100]}...")
                else:
                    print(f"{key_name} - Error: {result.get('error', result)}")
        except Exception as e:
            print(f"{key_name} - Exception: {str(e)}")

async def main():
    """Run all tests"""
    if owl_alpha_key:
        await test_api_key(owl_alpha_key, "OWL-ALPHA")
    
    if premium_key:
        await test_api_key(premium_key, "PREMIUM")

if __name__ == "__main__":
    asyncio.run(main())
