import os
import json
from PIL import Image
from google import genai
from google.genai import types

# Initialize the client (Make sure your key is directly pasted here if environment variables are acting up)
client = genai.Client()

# =====================================================================
# AGENTIC DEPTH: Define the mock tool function
# =====================================================================
def check_duplicate_reports(latitude: float, longitude: float, radius_meters: float = 50.0) -> str:
    """
    Checks the local database for existing reported issues within a specific radius.
    """
    print(f"\n[AGENT ACTION] Checking database near coordinates: {latitude}, {longitude}...")
    
    # Simulating a duplicate check match
    duplicate_found = True 
    
    if duplicate_found:
        return "MATCH FOUND: Active issue ID #1042 (Broken Streetlight) exists within 12 meters."
    return "NO DUPLICATES: This coordinates region is completely clear."

# =====================================================================
# EXECUTION: Updated Agent logic
# =====================================================================
def run_prototype(image_path: str, lat: float, lng: float):
    print("Loading community issue report image...")
    try:
        img = Image.open(image_path)
    except FileNotFoundError:
        print(f"Please put an image file at {image_path} to run this prototype!")
        return

    # Injected the expected JSON schema explicitly into the instructions instead of using config constraints
    system_instruction = (
        "You are an expert, autonomous municipal triage agent. Your job is to analyze "
        "incoming community issues via images.\n\n"
        "CRITICAL STEP: You MUST first call the 'check_duplicate_reports' tool using the provided coordinates "
        "to check for surrounding matches.\n\n"
        "After evaluating the tool response and the image, you MUST respond ONLY with a raw JSON object matching this structure:\n"
        "{\n"
        '  "issue_type": "string (e.g. Streetlight, Pothole, Waste Management)",\n'
        '  "severity": "string (Low, Medium, High)",\n'
        '  "public_safety_hazard": true/false,\n'
        '  "estimated_repair_complexity": "string (Low, Medium, High)",\n'
        '  "is_duplicate": true/false,\n'
        '  "system_action_taken": "string describing what you did (e.g., Merged with issue #1042)"\n'
        "}\n"
        "Do not include markdown blocks like ```json or trailing text. Return raw stringified JSON text."
    )

    prompt = f"A citizen reported this issue at coordinates: Latitude {lat}, Longitude {lng}. Process it completely."

    print("Sending agentic request to Gemini...")
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=[img, prompt],
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            tools=[check_duplicate_reports],
            temperature=0.1
        )
    )

    print("\n================== AGENT FINAL RESPONSE (JSON) ==================")
    print(response.text)
    print("=================================================================")

if __name__ == "__main__":
    # Make sure your file name matches here (e.g. "street_light.jpg" or "street_light.png")
    run_prototype("street_light.png", lat=30.3564, lng=76.3647)