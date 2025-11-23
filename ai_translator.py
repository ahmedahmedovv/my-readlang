"""
AI Translator Service using Mistral AI API.
Handles example sentence generation for words/phrases.
"""
import os
import json
import logging
import requests
from typing import Dict, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AITranslator:
    """Service for generating example sentences using Mistral AI API."""
    
    def __init__(self):
        """Initialize the AI translator with API key from environment."""
        self.api_key = os.getenv("MISTRAL_API_KEY")
        if not self.api_key:
            raise ValueError(
                "MISTRAL_API_KEY environment variable is required. "
                "Please set it before running the application. "
                "You can get an API key from https://console.mistral.ai/"
            )
        
        self.api_url = "https://api.mistral.ai/v1/chat/completions"
        self.model = "mistral-medium-latest"  # or "mistral-large-latest" for better quality
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def get_examples(self, word: str) -> Dict[str, any]:
        """
        Get example sentences for a word or phrase.
        
        Args:
            word: The word or phrase to get examples for
            
        Returns:
            Dictionary with 'examples' list or 'error' string
        """
        if not word or len(word.strip()) == 0:
            return {'error': 'Empty word provided'}
        
        # Limit word length to prevent abuse
        if len(word) > 100:
            return {'error': 'Word too long (max 100 characters)'}
        
        try:
            prompt = (
                f"For the word/phrase: '{word}', provide:\n"
                "1. A brief definition (1-2 sentences explaining what it means)\n"
                "2. Three example sentences demonstrating its usage\n\n"
                "Format your response as JSON with this structure:\n"
                '{"definition": "Brief definition here", "examples": ["Example 1", "Example 2", "Example 3"]}'
            )
            
            # Prepare request payload
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 200,
                "temperature": 0.7
            }
            
            # Call Mistral AI API
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            # Check for HTTP errors
            if response.status_code != 200:
                error_msg = f"API returned status {response.status_code}"
                try:
                    error_data = response.json()
                    error_msg = error_data.get("error", {}).get("message", error_msg)
                except:
                    error_msg = response.text[:200] if response.text else error_msg
                logger.error(f"Mistral AI API error: {error_msg}")
                return {'error': f'API error: {error_msg}'}
            
            # Parse JSON response
            response_data = response.json()
            
            # Extract content from response
            if "choices" not in response_data or not response_data["choices"]:
                logger.error("No choices in API response")
                return {'error': 'Invalid API response format'}
            
            text = response_data["choices"][0]["message"]["content"].strip()
            
            # Remove markdown code blocks if present
            if text.startswith("```json"):
                text = text[7:]
            elif text.startswith("```"):
                text = text[3:]
            if text.endswith("```"):
                text = text[:-3]
            text = text.strip()
            
            # Try to parse JSON
            try:
                result_data = json.loads(text)
                
                # Check if we have the expected structure
                if isinstance(result_data, dict):
                    definition = result_data.get('definition', '')
                    examples = result_data.get('examples', [])
                    
                    # Validate examples
                    if isinstance(examples, list):
                        examples = [e for e in examples if isinstance(e, str) and len(e) >= 5]
                        examples = examples[:3]  # Limit to 3 examples
                    
                    # If we have either definition or examples, return them
                    if definition or examples:
                        return {
                            'definition': definition.strip() if definition else '',
                            'examples': examples
                        }
                
                # Fallback: if it's an array (old format), treat as examples only
                if isinstance(result_data, list):
                    examples = [e for e in result_data if isinstance(e, str) and len(e) >= 5]
                    if examples:
                        return {
                            'definition': '',
                            'examples': examples[:3]
                        }
                        
            except json.JSONDecodeError:
                # If not JSON, try to extract definition and sentences from plain text
                lines = [s.strip() for s in text.split('\n') if s.strip()]
                
                # Try to find definition (usually first line or lines starting with specific markers)
                definition = ''
                examples = []
                
                for i, line in enumerate(lines):
                    line_lower = line.lower()
                    # Check if this looks like a definition
                    if any(marker in line_lower for marker in ['is', 'means', 'refers to', 'definition']):
                        definition = line
                        # Examples usually come after definition
                        remaining_lines = lines[i+1:]
                        examples = [s.strip().lstrip('- ').lstrip('* ').lstrip('1. ').lstrip('2. ').lstrip('3. ')
                                   for s in remaining_lines if s.strip() and len(s.strip()) >= 5]
                        break
                
                # If no definition found, treat first part as definition, rest as examples
                if not definition and lines:
                    if len(lines) >= 4:
                        definition = lines[0]
                        examples = [s.strip().lstrip('- ').lstrip('* ').lstrip('1. ').lstrip('2. ').lstrip('3. ')
                                   for s in lines[1:] if s.strip() and len(s.strip()) >= 5]
                    else:
                        # All are examples
                        examples = [s.strip().lstrip('- ').lstrip('* ').lstrip('1. ').lstrip('2. ').lstrip('3. ')
                                   for s in lines if s.strip() and len(s.strip()) >= 5]
                
                # Fallback: try splitting by sentences
                if not examples:
                    sentences = [s.strip() for s in text.split('.') if s.strip() and len(s.strip()) >= 5]
                    if len(sentences) >= 3:
                        definition = sentences[0] if sentences else ''
                        examples = sentences[1:4] if len(sentences) > 1 else sentences[:3]
                    elif sentences:
                        examples = sentences[:3]
                
                if definition or examples:
                    return {
                        'definition': definition.strip(),
                        'examples': examples[:3] if examples else []
                    }
            
            return {'error': 'Failed to generate valid response'}
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error for word '{word}': {e}")
            return {'error': 'Failed to parse API response'}
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error for word '{word}': {type(e).__name__}: {e}")
            return {'error': f'Network error: {str(e)}'}
        except Exception as e:
            logger.error(f"API error for word '{word}': {type(e).__name__}: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return {'error': f'API error: {str(e)}'}

