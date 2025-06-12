"""
Sentiment Analysis Agent

This agent handles sentiment analysis of text using the Grok API.
It can analyze sentiment of various text inputs and return sentiment scores.
"""

import requests
from typing import Dict, Any, Optional
from src.utils.database import log_audit
from src.utils.config_manager import get_config


def analyze_sentiment(text: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    """
    Analyze the sentiment of the given text using the Grok API.

    Args:
        text: The text to analyze
        api_key: Optional API key for Grok. If not provided, will try to get from config.

    Returns:
        Dict containing sentiment analysis results including:
        - sentiment: Overall sentiment (positive, negative, neutral)
        - score: Sentiment score between -1 and 1
        - confidence: Confidence score between 0 and 1
    """
    if not api_key:
        api_key = get_config('grok', 'api_key')
    
    if not api_key:
        raise ValueError("Grok API key not found in configuration")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "text": text,
        "language": "en"  # Default to English, can be made configurable
    }
    
    try:
        response = requests.post(
            "https://api.groq.com/v1/sentiment",
            headers=headers,
            json=payload,
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {
            "error": f"Failed to analyze sentiment: {str(e)}",
            "status": "error"
        }


def handle_sentiment_request(data: Dict[str, Any], user_id: str) -> Dict[str, Any]:
    """
    Handle sentiment analysis requests.
    
    Args:
        data: Request data containing:
            - text: The text to analyze
            - api_key: (Optional) Grok API key
        user_id: ID of the user making the request
        
    Returns:
        Dict containing sentiment analysis results or error information
    """
    text = data.get('text')
    if not text:
        log_audit(user_id, 'sentiment_analysis', {'error': 'No text provided'})
        return {'error': 'Text is required for sentiment analysis'}
    
    log_audit(user_id, 'sentiment_analysis', {'text_length': len(text)})
    
    try:
        result = analyze_sentiment(
            text=text,
            api_key=data.get('api_key')
        )
        
        if 'error' in result:
            log_audit(user_id, 'sentiment_analysis_error', {'error': result['error']})
            return {'status': 'error', 'message': result['error']}
            
        log_audit(user_id, 'sentiment_analysis_success', {
            'sentiment': result.get('sentiment'),
            'score': result.get('score')
        })
        
        return {
            'status': 'success',
            'result': {
                'sentiment': result.get('sentiment'),
                'score': result.get('score'),
                'confidence': result.get('confidence')
            }
        }
        
    except Exception as e:
        error_msg = f"Failed to process sentiment analysis: {str(e)}"
        log_audit(user_id, 'sentiment_analysis_error', {'error': error_msg})
        return {'status': 'error', 'message': error_msg}


if __name__ == "__main__":
    # Example usage
    test_text = "I really love this product! It's amazing and works perfectly."
    print(f"Analyzing sentiment for: {test_text}")
    result = analyze_sentiment(test_text)
    print(f"Sentiment result: {result}")
