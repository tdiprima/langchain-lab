"""
Diabetes Medication Advisor with Web Search and Safety Checks
No LangChain libraries; linear, non-agentic script.
Note: Requires SERPAPI_API_KEY and OPENAI_API_KEY
Author: tdiprima
"""
import os
import requests

# Load API keys from environment variables
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not SERPAPI_API_KEY or not OPENAI_API_KEY:
    raise ValueError("Missing SERPAPI_API_KEY or OPENAI_API_KEY in environment variables.")


# Function to fetch medical guidelines via SerpAPI
def retrieve_medical_guidelines(query):
    """Searches medical guidelines using SerpAPI."""
    url = "https://serpapi.com/search"
    params = {
        "q": query,
        "api_key": SERPAPI_API_KEY,
        "engine": "google",
        "num": 5  # Limit to 5 results for brevity
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        results = response.json().get("organic_results", [])
        # Extract snippets from top results
        guidelines = [result.get("snippet", "No snippet available") for result in results]
        return "\n".join(guidelines) if guidelines else "No guidelines found."
    except requests.RequestException as e:
        print(f"SerpAPI error: {e}")
        return "Failed to retrieve guidelines."


# Function to fetch drug contraindications via FDA API
def check_drug_contraindications(medication, condition):
    """Fetch drug contraindications based on a condition."""
    url = f"https://api.fda.gov/drug/label.json?search={medication}+AND+{condition}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        warnings = data.get("results", [{}])[0].get("warnings", ["No warnings found."])[0]
        return warnings
    except requests.RequestException as e:
        print(f"FDA API error: {e}")
        return "No data available."


# Function to call OpenAI API directly
def generate_response(prompt):
    """Generate a response using OpenAI API."""
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gpt-4",
        "messages": [
            {"role": "system", "content": "You are a medical assistant providing medication recommendations."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0,
        "max_tokens": 500
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except requests.RequestException as e:
        print(f"OpenAI API error: {e}")
        return "Failed to generate response."


# Main logic
def process_query(query):
    """Process a medical query and return a recommendation."""
    # Step 1: Retrieve guidelines
    guideline_query = "diabetes treatment guidelines kidney disease"
    guidelines = retrieve_medical_guidelines(guideline_query)
    print("Retrieved Guidelines:")
    print(guidelines)
    print("\n")

    # Step 2: Check contraindications for common diabetes meds
    medications = ["metformin", "insulin", "sitagliptin"]  # Example meds
    condition = "kidney disease"
    contraindications = {}
    for med in medications:
        result = check_drug_contraindications(med, condition)
        contraindications[med] = result
        print(f"Contraindications for {med}:")
        print(result)
        print("\n")

    # Step 3: Generate recommendation with OpenAI
    prompt = f"""
    Based on the following information:
    - Query: {query}
    - Retrieved Guidelines: {guidelines}
    - Contraindications:
      - Metformin: {contraindications['metformin']}
      - Insulin: {contraindications['insulin']}
      - Sitagliptin: {contraindications['sitagliptin']}
    Recommend the best medication for a diabetic patient with kidney disease and explain why.
    """
    response = generate_response(prompt)
    return response


# Execute
if __name__ == "__main__":
    query = "What is the best medication for a diabetic patient with kidney disease?"
    response = process_query(query)
    print("Final Recommendation:")
    print(response)
