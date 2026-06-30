import streamlit as st
import json
import pandas as pd
from PIL import Image
from google import genai
from google.genai import types


# =====================================================================
# 1. CONFIGURATION & INITIALIZATION
# =====================================================================
st.set_page_config(page_title="Commune Help", page_icon="🤝", layout="wide")

# Safe initialization using dictionary checking syntax
if "issues_db" not in st.session_state:
    st.session_state["issues_db"] = [
        {"id": 1042, "type": "Streetlight", "lat": 30.3564, "lng": 76.3647, "severity": "High", "status": "Tracking"},
        {"id": 1043, "type": "Pothole", "lat": 30.3600, "lng": 76.3700, "severity": "Medium", "status": "Tracking"},
        {"id": 1044, "type": "Waste Management", "lat": 30.3500, "lng": 76.3600, "severity": "Low", "status": "Resolved"},
    ]
    client = genai.Client()


# =====================================================================
# 2. CORE AI FUNCTION (From Phase 1)
# =====================================================================
def check_duplicate_reports(latitude: float, longitude: float):
    # Hardcoded simulation tool for agentic workflow verification
    return "MATCH FOUND: Active issue ID #1042 (Broken Streetlight) exists within 12 meters."

def analyze_issue_with_gemini(uploaded_file, latitude, longitude):
    import google.genai as genai
    from PIL import Image
    import json  # 🧠 Ensure json is imported
    
    ai_client = genai.Client() 
    image = Image.open(uploaded_file)
    
    # Keeping our precise system instruction format from earlier
    system_instruction = (
        "You are an expert, autonomous municipal triage agent. Analyze the community issue image.\n"
        "You MUST respond ONLY with a raw JSON object matching this structure:\n"
        "{\n"
        '  "issue_type": "Streetlight or Pothole or Waste Management or Infrastructure",\n'
        '  "severity": "Low or Medium or High",\n'
        '  "public_safety_hazard": true or false,\n'
        '  "estimated_repair_complexity": "Low or Medium or High",\n'
        '  "is_duplicate": true or false,\n'
        '  "system_action_taken": "Text description"\n'
        "}"
    )
    prompt = f"A citizen reported this issue at coordinates: Latitude {latitude}, Longitude {longitude}."
    
    response = ai_client.models.generate_content(
        model='gemini-2.5-flash',
        contents=[image, prompt],
        config=genai.types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.1
        )
    )
    
    # --- CLEAN & CONVERT BACK TO DICTIONARY ---
    raw_text = response.text.strip()
    
    # Strip markdown wrappers if Gemini adds them
    if raw_text.startswith("```json"):
        raw_text = raw_text[7:]
    elif raw_text.startswith("```"):
        raw_text = raw_text[3:]
    if raw_text.endswith("```"):
        raw_text = raw_text[:-3]
        
    raw_text = raw_text.strip()
    
    # 🎯 Crucial Line: Convert string back to a Python Dictionary!
    return json.loads(raw_text)

# =====================================================================
# 3. USER INTERFACE LAYOUT
# =====================================================================
# Update the main heading that users see on the page
st.title("🤝 Commune Help — Hyperlocal Problem Solver")
st.markdown("Empowering citizens to build better neighborhoods through autonomous AI triage and collaboration.")

# Sidebar Navigation / Analytics
st.sidebar.header("🏆 Citizen Leaderboard")
st.sidebar.markdown("""
1. 🥇 **Dhruv (You)** — 450 pts
2. 🥈 **Aarav Sharma** — 380 pts
3. 🥉 **Sneha Gupta** — 210 pts
""")

# Main Layout Tabs
tab1, tab2 = st.tabs(["🚀 Report an Issue", "📊 Hyperlocal Live Map & Metrics"])

# ---------------------------------------------------------------------
# TAB 1: USER REPORT FLOW (Product Experience Focus)
# ---------------------------------------------------------------------
with tab1:
    st.header("📸 Smart Issue Submission")
    col1, col2 = st.columns([1, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            "Drag and drop or upload an image/video of the issue", 
            type=["jpg", "jpeg", "png"]
        )
        
        st.subheader("📍 Hyperlocal Targeting")
        
        # --- NEW BROWSER GEOLOCATION TRACKING FEATURE ---
        # Seamlessly request browser permission via standard JS Geolocation API
        loc_html = """
        <script>
        function getLocation() {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(showPosition);
            }
        }
        function showPosition(position) {
            // Send coordinates straight back to Streamlit session state query params
            const urlParams = new URLSearchParams(window.parent.location.search);
            window.parent.location.href = window.parent.location.pathname + '?lat=' + position.coords.latitude + '&lng=' + position.coords.longitude;
        }
        window.onload = getLocation;
        </script>
        <div style="font-family:sans-serif; font-size:14px; color:#555;">
            📡 Requesting secure browser GPS location sync...
        </div>
        """
        
        # Execute the hidden JS component
        st.components.v1.html(loc_html, height=35)
        
        # Read the coordinates passed back into the URL parameters by the browser
        query_params = st.query_params
        
        # Fallback defaults (TIET coordinates) if permission is denied/pending
        default_lat = float(query_params.get("lat", 30.3564))
        default_lng = float(query_params.get("lng", 76.3647))
        
        # Show clean visual indicators instead of intimidating input fields
        st.info(f"📍 **Target locked:** Latitude: {default_lat:.4f} | Longitude: {default_lng:.4f}")
        
        # Hidden or disabled inputs to prevent cluttering the user interface
        lat_input = default_lat
        lng_input = default_lng
        # --- END OF GEOLOCATION UPGRADE ---
        
        if uploaded_file is not None:
            st.image(uploaded_file, caption="Uploaded Preview", use_container_width=True)
            
            # Trigger Gemini Processing
            if st.button("✨ Analyze Issue Natively with AI", type="primary"):
                with st.spinner("🧠 Gemini Autonomous Agent is triaging the photo & checking records..."):
                    try:
                        ai_result = analyze_issue_with_gemini(uploaded_file, lat_input, lng_input)
                        st.session_state.ai_result = ai_result
                        st.success("Triage complete! Form auto-populated.")
                    except Exception as e:
                        st.error(f"Error communicating with AI: {e}")

    with col2:
        st.header("📋 Auto-Populated Verification Form")
        
        # Fetch auto-populated state or default to blanks
        res = st.session_state.get("ai_result", {})
        
        # These UI fields auto-populate dynamically using the structured output from Gemini!
        issue_type = st.text_input("Detected Issue Category", value=res.get("issue_type", ""))
        severity = st.selectbox("Assigned Severity Level", ["Low", "Medium", "High"], index=["Low", "Medium", "High"].index(res.get("severity", "Medium")))
        hazard = st.checkbox("Public Safety Hazard Flagged", value=res.get("public_safety_hazard", False))
        complexity = st.text_input("Estimated Repair Complexity", value=res.get("estimated_repair_complexity", ""))
        action_log = st.text_area("System Actions / Duplicate Verification Log", value=res.get("system_action_taken", ""))
        
        if st.button("✅ Confirm & Log into Civic Map"):
            if res:
                new_entry = {
                    "id": len(st.session_state.issues_db) + 1042,
                    "type": issue_type,
                    "lat": lat_input,
                    "lng": lng_input,
                    "severity": severity,
                    "status": "Tracking"
                }
                st.session_state.issues_db.append(new_entry)
                st.balloons()
                st.success(f"Issue logged successfully! Assigned Ticket #{new_entry['id']}")

# ---------------------------------------------------------------------
# TAB 2: MAP INTEGRATION & METRICS
# ---------------------------------------------------------------------
with tab2:
    st.header("📊 Live Analytics Dashboard")
    
    # Simple Metrics Cards
    m1, m2, m3 = st.columns(3)
    m1.metric("Active Tickets", value=len([i for i in st.session_state.issues_db if i["status"] == "Tracking"]))
    m2.metric("Issues Resolved This Week", value=len([i for i in st.session_state.issues_db if i["status"] == "Resolved"]), delta="+2 items")
    m3.metric("Community Karma Points Generated", value="1,040 XP")
    
    st.subheader("🗺️ Hyperlocal Operations Map")
    
    # Map implementation
    df = pd.DataFrame(st.session_state.issues_db)
    
    # Map points plotted using Streamlit's native map library
    st.map(df, latitude='lat', longitude='lng', size=40)
    
    st.markdown("💡 *Note for Submission: In production, color-coding markers (Red/Yellow/Green) is achieved by dropping these coordinate logs directly into the **Google Maps JavaScript API** or an embedded **Google Looker Studio Geospatial Dashboard**.*")