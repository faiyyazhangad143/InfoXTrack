import streamlit as st
import requests
import json
import base64
from io import BytesIO
from PIL import Image


OPENROUTER_API_KEY = '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'

# Function to encode the image into base64 format
def encode_image(img):
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    encoded_string = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return encoded_string

#Streamlit App
st.set_page_config(page_title="InfoxTrack", page_icon="📊", layout="wide")

#Display the title and subtitle at the center of the home page with larger fonts
st.markdown("""
    <div style="text-align: center;">
        <h1 style="font-size: 100px;">📊 InfoXtract</h1>
        <h3 style="font-size: 50px;">Where Documents Meet Automation</h3>
    </div>
""", unsafe_allow_html=True)



#Sidebar for selecting file and feature with added space
# st.sidebar.title("📊 InfoxTrack")
# st.sidebar.markdown("<br>", unsafe_allow_html=True)
st.sidebar.markdown(
    "<h1 style='font-size: 80px;'>📊 InfoxTract</h1>",
    unsafe_allow_html=True
)

st.sidebar.markdown("<br><br>", unsafe_allow_html=True)

st.markdown("""
    <style>
    .css-1s5h7v1 {
        font-size: 20px !important;
    }
    .css-1aumxhk {
        font-size: 20px !important;
    }
    .css-1lcbm12 {
        font-size: 20px !important;
    }
    </style>
    """, unsafe_allow_html=True)



st.sidebar.markdown("<h3 style='font-size: 50px;'>Choose a file</h3>", unsafe_allow_html=True)
file_option = st.sidebar.selectbox("", ["Select", "Custom Upload", "Claim", "Invoice", "Receipt"])
st.sidebar.markdown("<br><br><br>", unsafe_allow_html=True)



# Dropdown for selecting feature with increased text size
st.sidebar.markdown("<h3 style='font-size: 50px;'>Select Feature</h3>", unsafe_allow_html=True)
feature_option = st.sidebar.selectbox("", [
    "Select", 
    "Attribute Value Extraction", 
    "Automated Workflow Code Generator", 
    "Chat", 
    "Document Auto-Categorization", 
    "Document Content Validation",  
    "Document Sentiment Analysis", 
    "Dynamic SQL Query Generation", 
    "Multi-Modal Document Translation", 
    "Multi-Modal KPI Tracker", 
    "Named Entity Recognition", 
    "Smart Contract Risk Assessment", 
    "Summarization", 
    "Table Detection and Extraction"
])

# # Dropdown for selecting feature
# feature_option = st.sidebar.selectbox("Select Feature", [
#     "Select", 
#     "Attribute Value Extraction", 
#     "Automated Workflow Code Generator", 
#     "Chat", 
#     "Document Auto-Categorization", 
#     "Document Content Validation", 
#     "Document Sentiment Analysis", 
#     "Document Sentiment Analysis", 
#     "Dynamic SQL Query Generation", 
#     "Multi-Modal Document Translation", 
#     "Multi-Modal KPI Tracker", 
#     "Named Entity Recognition", 
#     "Smart Contract Risk Assessment", 
#     "Summarization", 
#     "Table Detection and Extraction"
# ])



uploaded_file = None
if file_option == "Custom Upload":
    # Create a centered layout for the file uploader
    col1, col2, col3 = st.columns([1, 2, 1])  # Define the columns for centering
    with col2:  # Use the middle column to place the uploader
        uploaded_file = st.file_uploader("Upload an image (JPG, PNG, JPEG)", type=["jpg", "jpeg", "png"])



# Display image based on file selection
if uploaded_file is not None or file_option in ["Claim", "Invoice", "Receipt"]:
    if file_option == "Claim":
        image_path = "E:\\DOCXAI\\Claims.jpg"  # Replace with actual image path or URL
        img = Image.open(image_path)
    elif file_option == "Invoice":
        image_path = "E:\\DOCXAI\\Invoice.jpeg"  # Replace with actual image path or URL
        img = Image.open(image_path)
    elif file_option == "Receipt":
        image_path = "E:\\DOCXAI\\Receipt.png"  # Replace with actual image path or URL
        img = Image.open(image_path)
    elif uploaded_file is not None:
        img = Image.open(uploaded_file)

    # Display the image on the main page
    st.image(img, caption="Uploaded Image", use_column_width=True)
    base64_img = encode_image(img)

    # Chat feature
    if feature_option == "Chat":
        st.subheader("Ask a question about the document:")
        user_question = st.text_input("Your Question", "")

        if user_question:
            with st.spinner("Processing..."):
                response = requests.post(
                    url="https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {OPENROUTER_API_KEY}"
                    },
                    data=json.dumps({
                        "model": "qwen/qwen-2-vl-72b-instruct",
                        "messages": [
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": "You are a document assistant. Answer the user's question based on the document."
                                    },
                                    {
                                        "type": "text",
                                        "text": user_question
                                    },
                                    {
                                        "type": "image_url",
                                        "image_url": {
                                            "url": f"data:image/png;base64,{base64_img}"
                                        }
                                    }
                                ]
                            }
                        ],
                        "max_tokens": 500,
                        "temperature": 0.5
                    })
                )

                # Handle response
                if response.status_code == 200:
                    chat_response = response.json()
                    if "choices" in chat_response and len(chat_response["choices"]) > 0:
                        answer = chat_response["choices"][0]["message"]["content"]
                        st.subheader("Answer:")
                        st.write(answer)
                    else:
                        st.error("No response from the model.")
                else:
                    st.error(f"Failed to get a valid response. Status Code: {response.status_code}")
                    
    ################################################################
    # Attribute Value Extraction feature
    elif feature_option == "Attribute Value Extraction":
        if st.button("Submit"):
            with st.spinner("Extracting data..."):
                request_payload = {
                "model": "qwen/qwen-2-vl-72b-instruct",
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "You are Document Attribute Extractor. Extract all the key-value pairs in the document as JSON."
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{base64_img}"
                                }
                            }
                        ]
                    }
                ],
                "max_tokens": 4837,
                "temperature": 0.2,
                "top_p": 0.04
            }
                
        
            try:
                # Send the POST request
                response = requests.post(
                    url="https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                        "Content-Type": "application/json"
                    },
                    data=json.dumps(request_payload)
                )

                # Check if the response is successful
                if response.status_code == 200:
                    raw_output = response.text
                    
                    try:
                        # Parse the JSON response
                        json_output = response.json()

                        # Check if the response contains the expected structure
                        if "choices" in json_output and len(json_output["choices"]) > 0:
                            extracted_content = json_output["choices"][0]["message"]["content"]

                            if extracted_content:  # Ensure content exists
                                cleaned_content = extracted_content.strip("```json").strip("```").strip()
                                
                                try:
                                    # Attempt to parse the extracted JSON
                                    parsed_json = json.loads(cleaned_content)
                                    st.subheader("Extracted JSON:")
                                    st.json(parsed_json)
                                except json.JSONDecodeError as e:
                                    # Handle malformed JSON content
                                    st.error(f"Malformed JSON in response: {str(e)}")
                                    st.code(cleaned_content, language="text")
                            else:
                                st.warning("No content found in the response. Please check the document or API response.")
                        else:
                            st.warning("Unexpected response structure. 'Choices' field missing or empty.")
                    except json.JSONDecodeError as e:
                        st.error(f"Failed to parse the raw JSON response: {str(e)}")
                        st.code(raw_output, language="json")
                else:
                    st.error(f"API request failed with status code: {response.status_code}")
                    st.code(response.text, language="json")

            except requests.exceptions.RequestException as req_e:
                st.error(f"Network error occurred: {str(req_e)}")
            except Exception as e:
                st.error(f"An unexpected error occurred: {str(e)}")

                    
    
    
                
   

    
    # Summarization feature
    elif feature_option == "Summarization":
        
        if st.button("Summarize"):
            with st.spinner("Generating summary..."):
                summarization_response = requests.post(
                    url="https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {OPENROUTER_API_KEY}"
                    },
                    data=json.dumps({
                        "model": "qwen/qwen-2-vl-72b-instruct",
                        "messages": [
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": "You are a document summarizer. Summarize the key points of this document."
                                    },
                                    {
                                        "type": "image_url",
                                        "image_url": {
                                            "url": f"data:image/png;base64,{base64_img}"
                                        }
                                    }
                                ]
                            }
                        ],
                        "max_tokens": 1024,
                        "temperature": 0.2
                    })
                )

                if summarization_response.status_code == 200:
                    summary_output = summarization_response.json()
                    if "choices" in summary_output and len(summary_output["choices"]) > 0:
                        summary_text = summary_output["choices"][0]["message"]["content"]
                        st.markdown(f"<div style='text-align: center; font-size: 20px;'><b>Summary:</b><br>{summary_text}</div>", unsafe_allow_html=True)
                    else:
                        st.error("No summary found in the response.")
                else:
                    st.error(f"Failed to generate summary. Status Code: {summarization_response.status_code}")

# Table Detection and Extraction feature
    elif feature_option == "Table Detection and Extraction":
        if st.button("Extract Tables"):
            with st.spinner("Detecting and extracting tables..."):
                table_response = requests.post(
                    url="https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {OPENROUTER_API_KEY}"
                    },
                    data=json.dumps({
                        "model": "qwen/qwen-2-vl-72b-instruct",
                        "messages": [
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": "You are a table detection and extraction system. Detect and extract any tables from this document."
                                    },
                                    {
                                        "type": "image_url",
                                        "image_url": {
                                            "url": f"data:image/png;base64,{base64_img}"
                                        }
                                    }
                                ]
                            }
                        ],
                        "max_tokens": 1024,
                        "temperature": 0.2
                    })
                )

                if table_response.status_code == 200:
                    table_output = table_response.json()
                    if "choices" in table_output and len(table_output["choices"]) > 0:
                        table_data = table_output["choices"][0]["message"]["content"]
                        st.subheader("Extracted Tables:")
                        st.markdown(table_data)
                    else:
                        st.error("No tables found in the response.")
                else:
                    st.error(f"Failed to detect tables. Status Code: {table_response.status_code}")
    
    
    



    
    # Named Entity Recognition feature
    elif feature_option == "Named Entity Recognition":
        if st.button("Extract Entities"):
            with st.spinner("Extracting named entities..."):
                # NER API request logic
                ner_response = requests.post(
                    url="https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {OPENROUTER_API_KEY}"
                    },
                    data=json.dumps({
                        "model": "qwen/qwen-2-vl-72b-instruct",
                        "messages": [
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": "You are a Named Entity Recognition model. Extract all named entities from the document."
                                    },
                                    {
                                        "type": "image_url",
                                        "image_url": {
                                            "url": f"data:image/png;base64,{base64_img}"
                                        }
                                    }
                                ]
                            }
                        ],
                        "max_tokens": 1024,
                        "temperature": 0.2
                    })
                )

                if ner_response.status_code == 200:
                    ner_output = ner_response.json()
                    if "choices" in ner_output and len(ner_output["choices"]) > 0:
                        ner_entities = ner_output["choices"][0]["message"]["content"]
                        st.subheader("Extracted Named Entities:")
                        st.write(ner_entities)
                    else:
                        st.error("No entities found in the response.")
                else:
                    st.error(f"Failed to extract named entities. Status Code: {ner_response.status_code}")
                    
    
    
    
    # Feature Option for Document Content Validation
    elif feature_option == "Document Content Validation":
        if st.button("Validate Document Content"):
            with st.spinner("Validating document content..."):
                validation_response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}"
                },
                data=json.dumps({
                    "model": "qwen/qwen-2-vl-72b-instruct",
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": "You are a Document Content Validation model. Validate the completeness and compliance of the document."
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/png;base64,{base64_img}"
                                    }
                                }
                            ]
                        }
                    ],
                    "max_tokens": 1024,
                    "temperature": 0.5
                })
            )
            if validation_response.status_code == 200:
                validation_output = validation_response.json()
                if "choices" in validation_output and len(validation_output["choices"]) > 0:
                    validation_result = validation_output["choices"][0]["message"]["content"]
                    st.subheader("Document Content Validation Result:")
                    st.write(validation_result)
                else:
                    st.error("No validation result found in the response.")
            else:
                st.error(f"Failed to validate document content. Status Code: {validation_response.status_code}")
    
    
    
    
    
    
     
     
    elif feature_option == "Multi-Modal Document Translation":
        
        target_language = st.text_input("Enter target language for translation (e.g., 'en' for English, 'fr' for French):")
        if st.button("Translate Document"):
            if target_language:
                with st.spinner("Translating document..."):
                    translation_response = requests.post(
                    url="https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {OPENROUTER_API_KEY}"
                    },
        
    
    
          
            
                
                    data=json.dumps({
                        "model": "qwen/qwen-2-vl-72b-instruct",
                        "messages": [
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": f"You are a Multi-Modal Document Translation model. Translate the text in this multilingual document, including both text and image-based content, into {target_language} while maintaining its original formatting."
                                    },
                                    {
                                        "type": "image_url",
                                        "image_url": {
                                            "url": f"data:image/png;base64,{base64_img}"
                                        }
                                    }
                                ]
                            }
                        ],
                        "max_tokens": 1024,
                        "temperature": 0.5
                    })
                )

            if translation_response.status_code == 200:
                translation_output = translation_response.json()
                if "choices" in translation_output and len(translation_output["choices"]) > 0:
                    translation_result = translation_output["choices"][0]["message"]["content"]
                    st.subheader("Document Translation Result:")
                    st.write(translation_result)
                else:
                    st.error("No translation found in the response.")
            else:
                st.error(f"Failed to translate document. Status Code: {translation_response.status_code}")
        else:
            st.error("Please enter a target language.")
            
    #############################################################################################################################################
    # Document Auto-Categorization feature
    elif feature_option == "Document Auto-Categorization":
        if st.button("Submit"):
            with st.spinner("Categorizing document..."):
                response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",  # Ensure the correct API URL
                headers={
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}"
                },
        
    
        
            
                data=json.dumps({
                    "model": "qwen/qwen-2-vl-72b-instruct",  # Check the model and consider alternatives
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": "You are a Document Classifier. Classify the document and provide all relevant categories (e.g., legal, medical, financial, etc.) and explain briefly what the document is about."
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/png;base64,{base64_img}"
                                    }
                                }
                            ]
                        }
                    ],
                    "max_tokens": 150,
                    "temperature": 0.2,
                    "top_p": 0.04
                })
            )

            if response.status_code == 200:
                raw_output = response.text
                st.subheader("Raw API Response:")
                st.code(raw_output, language="json")  # Display the raw response

                try:
                    # Parse JSON response
                    json_output = response.json()
                    if "choices" in json_output and len(json_output["choices"]) > 0:
                        # Extract the document classification result
                        categorized_content = json_output["choices"][0]["message"]["content"]
                        cleaned_category = categorized_content.strip("\n").strip()

                        # Display the detailed document classification
                        st.subheader("Document Category:")
                        st.write(cleaned_category)  # Display full category explanation here
                    else:
                        st.error("No category data found in the response.")
                except json.JSONDecodeError as e:
                    st.error(f"JSON Parse Error: {str(e)}")
            else:
                st.error(f"Failed to get a valid response. Status Code: {response.status_code}")
    

    # Dynamic SQL Query Generation
    elif feature_option == "Dynamic SQL Query Generation":
        table_name = st.text_input("Enter the table name where the data should be stored:", key="table_name")
   
        sql_requirement = st.text_input("Enter your SQL requirement (e.g., 'Store all dates', 'Save names and addresses'):", key="sql_requirement")
        if st.button("Submit"):
            if not table_name:
                st.error("Please specify the table name.")
            elif not sql_requirement:
                st.error("Please specify your SQL requirement.")
            else:
                with st.spinner("Processing image and generating SQL query..."):
                    response = requests.post(
                    url="https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {OPENROUTER_API_KEY}"
                    },
            
        
                    data=json.dumps({
                        "model": "qwen/qwen-2-vl-72b-instruct",
                        "messages": [
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": (
                                            f"You are an expert SQL Query Generator. "
                                            f"Extract the required data from the document as per the user's input: '{sql_requirement}'. "
                                            f"Generate a 'CREATE TABLE' query for the '{table_name}' table and an 'INSERT INTO' query for storing the data. "
                                            f"Ensure that the SQL queries you generate are 100% syntactically correct, "
                                            f"follow standard SQL practices, and accurately fulfill the given requirements. "
                                            f"The generated queries must run without any errors when copied into a SQL compiler. "
                                            f"Avoid any errors or incomplete output, even for complex or large queries."
                                        )
                                    },
                                    {
                                        "type": "image_url",
                                        "image_url": {
                                            "url": f"data:image/png;base64,{base64_img}"
                                        }
                                    }
                                ]
                            }
                        ],
                        "max_tokens": 4837,
                        "temperature": 0.2,
                        "top_p": 0.04
                    })
                )

            if response.status_code == 200:
                raw_output = response.text
                st.subheader("Raw API Response:")
                st.code(raw_output, language="json")  # Display the raw response in the Streamlit app

                try:
                    # Parse JSON response
                    json_output = response.json()
                    if "choices" in json_output and len(json_output["choices"]) > 0:
                        extracted_content = json_output["choices"][0]["message"]["content"]
                        cleaned_content = extracted_content.strip("\n").strip()

                        # Display the generated CREATE TABLE and INSERT INTO queries
                        st.subheader("Generated SQL Queries:")
                        st.code(cleaned_content, language="sql")
                    else:
                        st.error("No SQL query found in the response.")
                except json.JSONDecodeError as e:
                    st.error(f"JSON Parse Error: {str(e)}")
            else:
                st.error(f"Failed to get a valid response. Status Code: {response.status_code}")

   
    #############################################################################################################################################
    # Image-to-Code Conversion for Workflow Automation feature
    elif feature_option == "Automated Workflow Code Generator":
        if st.button("Submit"):
            with st.spinner("Converting diagram to code..."):
                response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}"
                },
                
                data=json.dumps({
                    "model": "qwen/qwen-2-vl-72b-instruct",  # Use Qwen-2VL for visual language processing
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": "You are a Process Diagram to Code Converter. Convert the process diagram into executable code for automation tools like RPA or Python scripts. The output code must be error-free and syntactically correct, ready to be copied and run."
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/png;base64,{base64_img}"  # Pass the uploaded image (base64 encoded)
                                    }
                                }
                            ]
                        }
                    ],
                    "max_tokens": 5000,  # Increase max tokens if necessary
                    "temperature": 0.2,  # Lower temperature for more deterministic output
                    "top_p": 0.04  # Control diversity in the response
                })
            )

            if response.status_code == 200:
                raw_output = response.text
                st.subheader("Raw API Response:")
                st.code(raw_output, language="json")  # Display the raw response

                try:
                    # Parse JSON response
                    json_output = response.json()
                    if "choices" in json_output and len(json_output["choices"]) > 0:
                        # Extract the content from the response
                        extracted_content = json_output["choices"][0]["message"]["content"]
                        cleaned_content = extracted_content.strip("\n").strip()

                        # Since the content is plain text Python code, directly display it
                        st.subheader("Generated Code:")
                        st.code(cleaned_content, language="python")
                    else:
                        st.error("No code generated in the response.")
                except json.JSONDecodeError as e:
                    st.error(f"Error in parsing JSON: {str(e)}")
            else:
                st.error(f"Failed to get a valid response. Status Code: {response.status_code}")
                
    
    ##########################################################################################################################################
   

    #############################################################################################################################################
    # Smart Contract Risk Assessment feature
    elif feature_option == "Smart Contract Risk Assessment":
        if st.button("Analyze Risks"):
            with st.spinner("Analyzing risks in the contract..."):
                response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}"
                },
        
    
            
                data=json.dumps({
                    "model": "qwen/qwen-2-vl-72b-instruct",
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": "You are a Contract Risk Assessor. Highlight problematic clauses such as penalties, termination conditions, or confidentiality clauses in the document. Provide explanations for each identified risk."
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/png;base64,{base64_img}"
                                    }
                                }
                            ]
                        }
                    ],
                    "max_tokens": 5000,
                    "temperature": 0.3,
                    "top_p": 0.4
                })
            )

            if response.status_code == 200:
                raw_output = response.text
                st.subheader("Raw API Response:")
                st.code(raw_output, language="json")  # Display the raw response

                try:
                    # Parse JSON response
                    json_output = response.json()
                    if "choices" in json_output and len(json_output["choices"]) > 0:
                        risk_analysis = json_output["choices"][0]["message"]["content"]
                        cleaned_analysis = risk_analysis.strip("\n").strip()

                        # Parse the cleaned JSON or display the analysis directly
                        st.subheader("Risk Assessment:")
                        st.write(cleaned_analysis)
                    else:
                        st.error("No risk analysis data found in the response.")
                except json.JSONDecodeError as e:
                    st.error(f"JSON Parse Error: {str(e)}")
            else:
                st.error(f"Failed to analyze the document. Status Code: {response.status_code}")
    
    
    
    
    
    ##############################################################################################################################################
    # Multi-Modal KPI Tracker feature
    elif feature_option == "Multi-Modal KPI Tracker":
        if st.button("Track KPIs"):
            with st.spinner("Tracking KPIs across multi-modal documents..."):
                response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}"
                },
              
                data=json.dumps({
                    "model": "qwen/qwen-2-vl-72b-instruct",
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": "You are a KPI Tracker. Extract and analyze the performance metrics from the uploaded multi-modal documents (PDFs, images, spreadsheets, etc.). Provide insights and summary of KPIs across these documents."
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/png;base64,{base64_img}"
                                    }
                                }
                            ]
                        }
                    ],
                    "max_tokens": 5000,
                    "temperature": 0.3,
                    "top_p": 0.4
                })
            )

            if response.status_code == 200:
                raw_output = response.text
                st.subheader("Raw API Response:")
                st.code(raw_output, language="json")  # Display the raw response

                try:
                    # Parse JSON response
                    json_output = response.json()
                    if "choices" in json_output and len(json_output["choices"]) > 0:
                        kpi_analysis = json_output["choices"][0]["message"]["content"]
                        cleaned_analysis = kpi_analysis.strip("\n").strip()

                        # Parse the cleaned JSON or display the analysis directly
                        st.subheader("KPI Tracking Insights:")
                        st.write(cleaned_analysis)
                    else:
                        st.error("No KPI data found in the response.")
                except json.JSONDecodeError as e:
                    st.error(f"JSON Parse Error: {str(e)}")
            else:
                st.error(f"Failed to analyze the document. Status Code: {response.status_code}")
    
    
    
    
    ####################################################################################################################################################
    # Document Sentiment Analysis feature
    elif feature_option == "Document Sentiment Analysis":
        if st.button("Analyze Sentiment"):
            with st.spinner("Analyzing sentiment..."):
                sentiment_response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}"
                },
              
            
                data=json.dumps({
                    "model": "qwen/qwen-2-vl-72b-instruct",
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": "You are a Document Sentiment Analyzer. Analyze the sentiment of the document and return whether the sentiment is positive, negative, or neutral."
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/png;base64,{base64_img}"
                                    }
                                }
                            ]
                        }
                    ],
                    "max_tokens": 1024,
                    "temperature": 0.2
                })
            )

            if sentiment_response.status_code == 200:
                sentiment_output = sentiment_response.json()
                if "choices" in sentiment_output and len(sentiment_output["choices"]) > 0:
                    sentiment_text = sentiment_output["choices"][0]["message"]["content"]
                    st.markdown(f"<div style='text-align: center; font-size: 20px;'><b>Sentiment Analysis Result:</b><br>{sentiment_text}</div>", unsafe_allow_html=True)
                else:
                    st.error("No sentiment analysis result found in the response.")
            else:
                st.error(f"Failed to analyze sentiment. Status Code: {sentiment_response.status_code}")
                
                
    ##############################################################################################################################################
    