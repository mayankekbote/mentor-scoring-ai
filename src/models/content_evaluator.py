"""
Content Evaluator Module
Uses Groq API for fast LLM-based content evaluation.
"""

from groq import Groq
import json
import os
from typing import Dict, Optional
from src import config


class ContentEvaluator:
    """
    Evaluates teaching content using Groq API.
    Much faster than local Ollama (10-20x speedup).
    Supports bilingual evaluation (Hindi + English).
    """
    
    def __init__(self):
        """Initialize content evaluator."""
        self.client = None
        self.model = "llama-3.1-8b-instant"  # Fast Groq model
    
    def get_groq_client(self) -> Groq:
        """
        Get or initialize Groq client.
        
        Returns:
            Groq client instance
            
        Raises:
            ValueError: If GROQ_API_KEY is not set
        """
        if self.client is None:
            api_key = os.getenv("GROQ_API_KEY")
            if not api_key:
                raise ValueError(
                    "GROQ_API_KEY environment variable not set. "
                    "Get your free key at: https://console.groq.com/keys"
                )
            self.client = Groq(api_key=api_key)
        return self.client
    
    def check_groq_available(self) -> bool:
        """
        Check if Groq API key is set.
        
        Returns:
            True if API key is available, False otherwise
        """
        return os.getenv("GROQ_API_KEY") is not None
    
    def evaluate_content(self, transcript: str) -> Dict[str, any]:
        """
        Evaluate teaching content from transcript using Groq.
        
        Args:
            transcript: Text transcript of teaching session
            
        Returns:
            Dictionary with:
            - clarity: 0-100
            - structure: 0-100
            - technical: 0-100
            - engagement: 0-100
            - summary: Brief summary text
            - success: bool (whether evaluation succeeded)
            - error: Optional error message
        """
        if not transcript or len(transcript.strip()) < 10:
            return {
                'clarity': 50,
                'structure': 50,
                'technical': 50,
                'engagement': 50,
                'summary': 'Insufficient content for evaluation',
                'success': False,
                'error': 'Transcript too short'
            }
        
        # Build prompt
        prompt = config.CONTENT_EVALUATION_PROMPT.format(transcript=transcript)
        
        try:
            # Get Groq client
            client = self.get_groq_client()
            
            # Call Groq API (much faster than Ollama)
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert educational content evaluator. Respond only with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=500
            )
            
            # Parse response
            llm_output = response.choices[0].message.content
            
            # Extract JSON from response
            evaluation = self._parse_json_response(llm_output)
            
            if evaluation:
                evaluation['success'] = True
                return evaluation
            else:
                return self._error_response("Failed to parse LLM response")
                
        except Exception as e:
            return self._error_response(f"Groq API error: {str(e)}")
    
    def _parse_json_response(self, llm_output: str) -> Optional[Dict]:
        """
        Parse JSON from LLM output.
        
        Args:
            llm_output: Raw LLM response
            
        Returns:
            Parsed evaluation dict or None
        """
        try:
            # Try direct JSON parse first
            data = json.loads(llm_output)
            return self._validate_evaluation(data)
        except json.JSONDecodeError:
            # Try to extract JSON from text
            start = llm_output.find('{')
            end = llm_output.rfind('}')
            
            if start != -1 and end != -1:
                json_str = llm_output[start:end+1]
                try:
                    data = json.loads(json_str)
                    return self._validate_evaluation(data)
                except json.JSONDecodeError:
                    pass
        
        return None
    
    def _validate_evaluation(self, data: Dict) -> Optional[Dict]:
        """
        Validate and normalize evaluation data.
        
        Args:
            data: Parsed JSON data
            
        Returns:
            Validated dict or None
        """
        required_keys = ['clarity', 'structure', 'technical', 'engagement', 'summary']
        
        if not all(key in data for key in required_keys):
            return None
        
        # Normalize scores to 0-100 range
        for key in ['clarity', 'structure', 'technical', 'engagement']:
            try:
                score = float(data[key])
                data[key] = max(0, min(100, score))
            except (ValueError, TypeError):
                return None
        
        if not isinstance(data['summary'], str):
            data['summary'] = str(data['summary'])
        
        return data
    
    def _error_response(self, error_msg: str) -> Dict:
        """Generate error response with neutral scores."""
        return {
            'clarity': 50,
            'structure': 50,
            'technical': 50,
            'engagement': 50,
            'summary': 'Evaluation unavailable',
            'success': False,
            'error': error_msg
        }
    
    def evaluate_chunks(self, transcripts: list) -> Dict[str, any]:
        """
        Evaluate multiple transcript chunks and aggregate.
        
        Args:
            transcripts: List of transcript strings
            
        Returns:
            Aggregated evaluation scores
        """
        if not transcripts:
            return self._error_response("No transcripts provided")
        
        evaluations = []
        
        for transcript in transcripts:
            eval_result = self.evaluate_content(transcript)
            if eval_result.get('success', False):
                evaluations.append(eval_result)
        
        if not evaluations:
            return self._error_response("All chunk evaluations failed")
        
        # Aggregate scores (average)
        aggregated = {
            'clarity': sum(e['clarity'] for e in evaluations) / len(evaluations),
            'structure': sum(e['structure'] for e in evaluations) / len(evaluations),
            'technical': sum(e['technical'] for e in evaluations) / len(evaluations),
            'engagement': sum(e['engagement'] for e in evaluations) / len(evaluations),
            'summary': ' '.join(e['summary'] for e in evaluations),
            'success': True
        }
        
        return aggregated


    def generate_comprehensive_summary(self, full_transcript: str) -> Dict[str, str]:
        """
        Generate a comprehensive summary of the entire teaching session.
        
        Args:
            full_transcript: Complete transcript of all chunks
            
        Returns:
            Dictionary with:
            - topic: What the teacher was trying to explain
            - what_went_well: Positive aspects of the teaching
            - improvements: Specific suggestions for improvement
            - success: bool (whether generation succeeded)
            - error: Optional error message
        """
        if not full_transcript or len(full_transcript.strip()) < 10:
            return {
                'topic': 'Insufficient content',
                'what_went_well': 'N/A',
                'improvements': 'N/A',
                'success': False,
                'error': 'Transcript too short'
            }
        
        # Build prompt
        prompt = config.COMPREHENSIVE_SUMMARY_PROMPT.format(transcript=full_transcript)
        
        try:
            # Get Groq client
            client = self.get_groq_client()
            
            # Call Groq API
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert educational content evaluator. Respond only with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=800  # More tokens for comprehensive summary
            )
            
            # Parse response
            llm_output = response.choices[0].message.content
            
            # Extract JSON from response
            summary = self._parse_summary_response(llm_output)
            
            if summary:
                summary['success'] = True
                return summary
            else:
                return self._error_summary_response("Failed to parse LLM response")
                
        except Exception as e:
            return self._error_summary_response(f"Groq API error: {str(e)}")
    
    def _parse_summary_response(self, llm_output: str) -> Optional[Dict]:
        """
        Parse JSON from LLM output for comprehensive summary.
        
        Args:
            llm_output: Raw LLM response
            
        Returns:
            Parsed summary dict or None
        """
        try:
            # Try direct JSON parse first
            data = json.loads(llm_output)
            return self._validate_summary(data)
        except json.JSONDecodeError:
            # Try to extract JSON from text
            start = llm_output.find('{')
            end = llm_output.rfind('}')
            
            if start != -1 and end != -1:
                json_str = llm_output[start:end+1]
                try:
                    data = json.loads(json_str)
                    return self._validate_summary(data)
                except json.JSONDecodeError:
                    pass
        
        return None
    
    def _validate_summary(self, data: Dict) -> Optional[Dict]:
        """
        Validate comprehensive summary data.
        
        Args:
            data: Parsed JSON data
            
        Returns:
            Validated dict or None
        """
        required_keys = ['topic', 'what_went_well', 'improvements']
        
        if not all(key in data for key in required_keys):
            return None
        
        # Ensure all values are strings
        for key in required_keys:
            if not isinstance(data[key], str):
                data[key] = str(data[key])
        
        return data
    
    def _error_summary_response(self, error_msg: str) -> Dict:
        """Generate error response for comprehensive summary."""
        return {
            'topic': 'Summary unavailable',
            'what_went_well': 'Unable to generate summary',
            'improvements': 'Unable to generate summary',
            'success': False,
            'error': error_msg
        }



def evaluate_transcript(transcript: str) -> Dict[str, any]:
    """
    Convenience function to evaluate a transcript.
    
    Args:
        transcript: Text transcript
        
    Returns:
        Evaluation scores and summary
    """
    evaluator = ContentEvaluator()
    return evaluator.evaluate_content(transcript)

    """
    Evaluates teaching content using Ollama LLM.
    Supports bilingual evaluation (Hindi + English).
    """
    
    def __init__(self):
        """Initialize content evaluator."""
        self.base_url = config.OLLAMA_BASE_URL
        self.model = config.OLLAMA_MODEL
        self.timeout = config.OLLAMA_TIMEOUT
    
    def check_ollama_available(self) -> bool:
        """
        Check if Ollama is running and accessible.
        
        Returns:
            True if Ollama is available, False otherwise
        """
        try:
            response = requests.get(
                f"{self.base_url}/api/tags",
                timeout=5
            )
            return response.status_code == 200
        except Exception:
            return False
    
    def evaluate_content(self, transcript: str) -> Dict[str, any]:
        """
        Evaluate teaching content from transcript.
        
        Args:
            transcript: Text transcript of teaching session
            
        Returns:
            Dictionary with:
            - clarity: 0-100
            - structure: 0-100
            - technical: 0-100
            - engagement: 0-100
            - summary: Brief summary text
            - success: bool (whether evaluation succeeded)
            - error: Optional error message
        """
        if not transcript or len(transcript.strip()) < 10:
            # Too short to evaluate meaningfully
            return {
                'clarity': 50,
                'structure': 50,
                'technical': 50,
                'engagement': 50,
                'summary': 'Insufficient content for evaluation',
                'success': False,
                'error': 'Transcript too short'
            }
        
        # Build prompt
        prompt = config.CONTENT_EVALUATION_PROMPT.format(transcript=transcript)
        
        try:
            # Call Ollama API
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    'model': self.model,
                    'prompt': prompt,
                    'stream': False,
                    'options': {
                        'temperature': 0.3,  # Lower temperature for more consistent JSON
                        'num_predict': 500   # Limit response length
                    }
                },
                timeout=self.timeout
            )
            
            if response.status_code != 200:
                return self._error_response(f"Ollama API error: {response.status_code}")
            
            # Parse response
            result = response.json()
            llm_output = result.get('response', '')
            
            # Extract JSON from response
            evaluation = self._parse_json_response(llm_output)
            
            if evaluation:
                evaluation['success'] = True
                return evaluation
            else:
                return self._error_response("Failed to parse LLM response")
                
        except requests.exceptions.Timeout:
            return self._error_response("Ollama request timed out")
        except requests.exceptions.ConnectionError:
            return self._error_response("Cannot connect to Ollama. Is it running?")
        except Exception as e:
            return self._error_response(f"Evaluation error: {str(e)}")
    
    def _parse_json_response(self, llm_output: str) -> Optional[Dict]:
        """
        Parse JSON from LLM output.
        
        LLM might return JSON with extra text, so we try to extract it.
        
        Args:
            llm_output: Raw LLM response
            
        Returns:
            Parsed evaluation dict or None
        """
        try:
            # Try direct JSON parse first
            data = json.loads(llm_output)
            return self._validate_evaluation(data)
        except json.JSONDecodeError:
            # Try to extract JSON from text
            # Look for content between { and }
            start = llm_output.find('{')
            end = llm_output.rfind('}')
            
            if start != -1 and end != -1:
                json_str = llm_output[start:end+1]
                try:
                    data = json.loads(json_str)
                    return self._validate_evaluation(data)
                except json.JSONDecodeError:
                    pass
        
        return None
    
    def _validate_evaluation(self, data: Dict) -> Optional[Dict]:
        """
        Validate and normalize evaluation data.
        
        Args:
            data: Parsed JSON data
            
        Returns:
            Validated dict or None
        """
        required_keys = ['clarity', 'structure', 'technical', 'engagement', 'summary']
        
        # Check all keys present
        if not all(key in data for key in required_keys):
            return None
        
        # Normalize scores to 0-100 range
        for key in ['clarity', 'structure', 'technical', 'engagement']:
            try:
                score = float(data[key])
                data[key] = max(0, min(100, score))
            except (ValueError, TypeError):
                return None
        
        # Ensure summary is string
        if not isinstance(data['summary'], str):
            data['summary'] = str(data['summary'])
        
        return data
    
    def _error_response(self, error_msg: str) -> Dict:
        """
        Generate error response with neutral scores.
        
        Args:
            error_msg: Error message
            
        Returns:
            Error response dict
        """
        return {
            'clarity': 50,
            'structure': 50,
            'technical': 50,
            'engagement': 50,
            'summary': 'Evaluation unavailable',
            'success': False,
            'error': error_msg
        }
    
    def evaluate_chunks(self, transcripts: list) -> Dict[str, any]:
        """
        Evaluate multiple transcript chunks and aggregate.
        
        Args:
            transcripts: List of transcript strings
            
        Returns:
            Aggregated evaluation scores
        """
        if not transcripts:
            return self._error_response("No transcripts provided")
        
        evaluations = []
        
        for transcript in transcripts:
            eval_result = self.evaluate_content(transcript)
            if eval_result.get('success', False):
                evaluations.append(eval_result)
        
        if not evaluations:
            return self._error_response("All chunk evaluations failed")
        
        # Aggregate scores (average)
        aggregated = {
            'clarity': sum(e['clarity'] for e in evaluations) / len(evaluations),
            'structure': sum(e['structure'] for e in evaluations) / len(evaluations),
            'technical': sum(e['technical'] for e in evaluations) / len(evaluations),
            'engagement': sum(e['engagement'] for e in evaluations) / len(evaluations),
            'summary': ' '.join(e['summary'] for e in evaluations),
            'success': True
        }
        
        return aggregated


def evaluate_transcript(transcript: str) -> Dict[str, any]:
    """
    Convenience function to evaluate a transcript.
    
    Args:
        transcript: Text transcript
        
    Returns:
        Evaluation scores and summary
    """
    evaluator = ContentEvaluator()
    return evaluator.evaluate_content(transcript)
