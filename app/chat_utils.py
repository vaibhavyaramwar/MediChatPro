import openai
from typing import List, Dict, Any
import re
from app.config import OPENAI_API_BASE, OPENAI_API_KEY, LLM_MODEL

# Configure OpenAI for self-hosted model
openai.api_base = OPENAI_API_BASE
openai.api_key = OPENAI_API_KEY

TEMPERATURE = 0.7

def get_chat_model(api_key: str = None):
    """Get chat model configuration for self-hosted LLM"""
    return {
        'model': LLM_MODEL,
        'temperature': TEMPERATURE,
        'api_base': OPENAI_API_BASE,
        'api_key': OPENAI_API_KEY
    }

def ask_chat_model(chat_model, prompt: str):
    """Ask the self-hosted LLM model"""
    try:
        response = openai.ChatCompletion.create(
            model=LLM_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=TEMPERATURE,
            stream=False
        )
        # Handle different response formats
        if hasattr(response, 'choices') and len(response.choices) > 0:
            choice = response.choices[0]
            if hasattr(choice, 'message') and hasattr(choice.message, 'content'):
                return choice.message.content
            elif hasattr(choice, 'text'):
                return choice.text
            else:
                return str(choice)
        else:
            return str(response)
    except Exception as e:
        print(f"Error calling self-hosted LLM: {e}")
        return f"Error: Unable to get response from the AI model. Please try again."

def generate_medical_insights(text: str) -> Dict[str, Any]:
    """Generate medical insights from text analysis"""
    insights = {
        'medical_terms': [],
        'potential_conditions': [],
        'medications': [],
        'vital_signs': [],
        'symptoms': [],
        'recommendations': []
    }
    
    # Medical terms detection
    medical_patterns = {
        'medications': r'\b(?:medication|drug|prescription|tablet|capsule|injection|dose|mg|ml)\b',
        'symptoms': r'\b(?:pain|ache|fever|nausea|dizziness|fatigue|weakness|shortness|breath)\b',
        'conditions': r'\b(?:diabetes|hypertension|asthma|pneumonia|infection|inflammation|chronic|acute)\b',
        'vital_signs': r'\b(?:blood pressure|heart rate|temperature|pulse|respiratory rate|oxygen saturation)\b'
    }
    
    text_lower = text.lower()
    
    for category, pattern in medical_patterns.items():
        matches = re.findall(pattern, text_lower, re.IGNORECASE)
        insights[category] = list(set(matches))
    
    return insights

def enhance_medical_response(response: str, insights: Dict[str, Any]) -> str:
    """Enhance medical response with additional context"""
    enhanced_response = response
    
    # Add medical disclaimer
    disclaimer = "\n\n⚠️ **Medical Disclaimer**: This information is for educational purposes only and should not be considered as medical advice. Please consult with a qualified healthcare professional for proper diagnosis and treatment."
    
    # Add relevant insights if available
    if insights.get('medications'):
        enhanced_response += f"\n\n💊 **Medications mentioned**: {', '.join(insights['medications'][:3])}"
    
    if insights.get('symptoms'):
        enhanced_response += f"\n\n🩺 **Symptoms identified**: {', '.join(insights['symptoms'][:3])}"
    
    if insights.get('conditions'):
        enhanced_response += f"\n\n🏥 **Conditions discussed**: {', '.join(insights['conditions'][:3])}"
    
    enhanced_response += disclaimer
    
    return enhanced_response 

