# Run Mentor Scoring AI with OpenAI + Groq
# PowerShell script

# Set OpenAI API key
$env:OPENAI_API_KEY = "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"

# Set Groq API key
$env:GROQ_API_KEY = "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"

# Start Streamlit app
streamlit run app.py
