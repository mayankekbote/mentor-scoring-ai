"""Quick test script to verify Ollama availability"""
import requests

try:
    response = requests.get("http://localhost:11434/api/tags", timeout=5)
    if response.status_code == 200:
        data = response.json()
        models = [m['name'] for m in data.get('models', [])]
        print("✓ Ollama is running")
        print(f"Available models: {models}")
        if 'mistral' in str(models).lower():
            print("✓ Mistral model is available")
        else:
            print("⚠ Mistral model not found. Run: ollama pull mistral")
    else:
        print("⚠ Ollama responded but with error")
except requests.exceptions.ConnectionError:
    print("✗ Ollama is not running")
    print("Please start Ollama:")
    print("  1. Open a new terminal")
    print("  2. Run: ollama serve")
    print("  3. In another terminal run: ollama pull mistral")
except Exception as e:
    print(f"Error checking Ollama: {e}")
