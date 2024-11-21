import streamlit as st
import google.generativeai as genai
import re
from typing import Dict, Tuple
from PIL import Image
#img=Image.open(r"C:\Users\saidu\Pictures\Saved Pictures\ai.jpg")
#st.image(img)

# Set your Gemini API key directly
GEMINI_API_KEY = "AIzaSyBiOppVl-ptCaEg2zvCqRLmfvm1EZDBZws"  # Replace with your API key

class CodeReviewer:
    def __init__(self):
        """Initialize the CodeReviewer with Gemini AI."""
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-pro')
        
    def review_code(self, code: str) -> Tuple[Dict, str]:
        """
        Review the provided code using Gemini AI.
        Returns a tuple of (issues_dict, fixed_code).
        """
        try:
            prompt = f"""
            Please review the following Python code and provide:
            1. A list of potential bugs and issues
            2. Code quality improvements
            3. A corrected version of the code
            
            Here's the code to review:
            ```python
            {code}
            ```
            
            Please format your response exactly as shown below:
            ISSUES:
            - [issue description]
            
            IMPROVEMENTS:
            - [improvement suggestion]
            
            FIXED_CODE:
            ```python
            [corrected code]
            ```
            
            Please ensure to maintain this exact format in your response.
            """
            
            response = self.model.generate_content(prompt)
            response_text = response.text
            
            # Initialize dictionary to store issues
            issues = {'bugs': [], 'improvements': []}
            
            # Extract issues
            issues_match = re.findall(r'ISSUES:\n(.*?)(?=IMPROVEMENTS:|FIXED_CODE:|$)', response_text, re.DOTALL)
            if issues_match:
                issues['bugs'] = [bug.strip() for bug in issues_match[0].split('\n') if bug.strip()]

            # Extract improvements
            improvements_match = re.findall(r'IMPROVEMENTS:\n(.*?)(?=FIXED_CODE:|$)', response_text, re.DOTALL)
            if improvements_match:
                issues['improvements'] = [imp.strip() for imp in improvements_match[0].split('\n') if imp.strip()]
            
            # Extract fixed code
            fixed_code_match = re.findall(r'```python\n(.*?)```', response_text, re.DOTALL)
            fixed_code = fixed_code_match[-1].strip() if fixed_code_match else ""
            
            return issues, fixed_code
        
        except Exception as e:
            st.error(f"Error during code review: {str(e)}")
            return {"bugs": [], "improvements": []}, ""


def main():
    st.set_page_config(
        page_title="SmartCode Review Pro",
        page_icon="💡",
        layout="wide"
    )
    
    # Set a blue background
    st.markdown("""
        <style>
            body {
                background-color: #e6f7ff;
            }
            .title {
                font-size: 36px;
                color: #007acc;
                font-weight: bold;
                text-align: center;
                margin-bottom: 20px;
            }
            .subtitle {
                font-size: 18px;
                color: #005f99;
                text-align: center;
                margin-bottom: 30px;
            }
        </style>
    """, unsafe_allow_html=True)

    # Title and description
    st.markdown("<div class='title'>SmartCode Review Pro 💡</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Review your Python code with AI for bugs, improvements, and polished fixes!</div>", unsafe_allow_html=True)
    
    # Sidebar for user input
    st.sidebar.title("📋 Code Submission Panel")
    user_code = st.sidebar.text_area(
        "📝 Paste Your Python Code Below",
        height=250,
        placeholder="# Paste your Python code here..."
    )
    
    if st.sidebar.button("🔍 Analyze Code"):
        if not user_code.strip():
            st.sidebar.warning("⚠️ Please enter some code to review.")
        else:
            with st.spinner("Analyzing your code..."):
                reviewer = CodeReviewer()
                issues, fixed_code = reviewer.review_code(user_code)
                
                st.session_state.issues = issues
                st.session_state.fixed_code = fixed_code

    # Main area for results
    st.header("🔍 AI-Powered Review Results")
    if 'issues' in st.session_state and st.session_state.issues:
        st.subheader("🐞 Identified Issues")
        for bug in st.session_state.issues['bugs']:
            st.markdown(f"- {bug.strip('- ')}")
        
        st.subheader("✨ Suggested Improvements")
        for improvement in st.session_state.issues['improvements']:
            st.markdown(f"- {improvement.strip('- ')}")
        
        st.subheader("✅ Fixed Code")
        if 'fixed_code' in st.session_state:
            st.code(st.session_state.fixed_code, language="python")
    else:
        st.info("Submit your code in the sidebar to get started.")


def initialize_session_state():
    """Initialize session state variables."""
    if 'issues' not in st.session_state:
        st.session_state.issues = {'bugs': [], 'improvements': []}
    if 'fixed_code' not in st.session_state:
        st.session_state.fixed_code = ""


if __name__ == "__main__":
    initialize_session_state()
    main()
