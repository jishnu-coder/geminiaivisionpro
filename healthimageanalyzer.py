import streamlit as st
from pathlib import Path
import google.generativeai as genai

GOOGLE_API_KEY='your api key'
## Streamlit App

genai.configure(api_key=GOOGLE_API_KEY)

# https://aistudio.google.com/app/u/1/prompts/recipe-creator
# Set up the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 0,
  "max_output_tokens": 8192,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

system_prompts = [
    """
    As a domain expert in industrial hardware analysis,
    you are tasked with examining hardware components for a leading manufacturing company. 
    Your expertise is crucial in identifying defects, inefficiencies, or any potential issues within the hardware.
    
   Your key responsibilities:

Detailed Analysis: Scrutinize and thoroughly examine each component, focusing on identifying any abnormalities or issues.
Analysis Report: Document all findings and clearly articulate them in a structured format.
Recommendations: Based on the analysis, suggest remedies, improvements, or further tests as applicable.
Repairs and Maintenance: If applicable, outline detailed repair and maintenance procedures that can enhance performance and longevity.
Important Notes to Remember:

Scope of Response: Only respond if the image pertains to hardware components or related issues.
Clarity of Image: In case the image is unclear, note that certain aspects are 'Unable to be correctly determined based on the provided image.'
Disclaimer: Accompany your analysis with the disclaimer: "Consult with a qualified engineer before making any decisions."
**Your insights are invaluable in guiding operational decisions. Please proceed with the analysis, adhering to the structured approach outlined above.
Please provide the final response with these 4 headings: Detailed Analysis, Analysis Report, Recommendations, and Repairs and Maintenance.
    
"""
]

model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              generation_config=generation_config,
                              safety_settings=safety_settings)


st.set_page_config(page_title="Hardware component Analysis", 
layout="wide")
st.title("Hardware component Analysis")

file_uploaded = st.file_uploader('Upload the image of componenet for analysis', 
type=['png','jpg','jpeg'])

if file_uploaded:
    st.image(file_uploaded, width=200, caption='Uploaded Image')
    
submit=st.button("Generate Analysis")

if submit:

    image_data = file_uploaded.getvalue()
    
    image_parts = [
        {
            "mime_type" : "image/jpg",
            "data" : image_data
        }
    ]
    
#     making our prompt ready
    prompt_parts = [
        image_parts[0],
        system_prompts[0],
    ]
    
#     generate response
    
    response = model.generate_content(prompt_parts)
    if response:
        st.title('Detailed analysis based on the uploaded image')
        st.write(response.text)