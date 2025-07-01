import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import time
import json
from infer import info_response, chat_response, get_multiple_sensor_samples

# Page configuration
st.set_page_config(
    page_title="Soil Quality Analysis",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize language in session state
if 'language' not in st.session_state:
    st.session_state.language = "English"  # Default language

# Translation dictionaries
content_en = {
    "title": "🌱 Soil Quality Analysis System",
    "sensor_data": "📊 Sensor Data",
    "load_new_samples": "🔄 Load New Samples",
    "getting_data": "Getting live sensor data...",
    "live_sensor": "Live sensor data",
    "analyze": "Analyze",
    "analyzing": "Analyzing soil data...",
    "chat_title": "💬 Soil Expert Chat",
    "analysis_results": "📈 Analysis Results:",
    "detected_for": "soil detected for",
    "quick_questions": "Quick Questions:",
    "nutrient_improvement": "🌱 Nutrient Improvement",
    "fertilizer_guide": "🧪 Fertilizer Guide",
    "ask_anything": "Ask me anything about your soil analysis!",
    "analyze_first": "Please analyze a soil sample first to start the conversation",
    "chat_placeholder": "Ask about nutrient levels, pH balance, organic content, fertilizers...",
    "thinking": "Thinking...",
    "less_fertile": "Less fertile",
    "fertile": "Fertile",
    "highly_fertile": "Highly fertile",
    "sample": "Sample",
    "language_label": "Select Language / 言語を選択",
    "analysis_complete": "Analysis complete for",
    "soil_classified": "The soil is classified as",
    "how_help": "How can I help you improve your soil quality?",
    "nutrient_question": "What specific nutrients does my soil need based on the analysis? How can I improve them?",
    "fertilizer_question": "What type and amount of fertilizers should I use for this soil condition?"
}

content_ja = {
    #"title": "🌱 土壌品質分析システム",
    "sensor_data": "📊 センサーデータ",
    "load_new_samples": "🔄 新しいサンプルを読み込む",
    "getting_data": "ライブセンサーデータを取得中...",
    "live_sensor": "ライブセンサーデータ",
    "analyze": "分析",
    "analyzing": "土壌データを分析中...",
    "chat_title": "💬 土壌専門家チャット",
    "analysis_results": "📈 分析結果：",
    "detected_for": "の土壌が検出されました",
    "quick_questions": "クイック質問：",
    "nutrient_improvement": "🌱 栄養改善",
    "fertilizer_guide": "🧪 肥料ガイド",
    "ask_anything": "土壌分析について何でも聞いてください！",
    "analyze_first": "会話を開始するには、まず土壌サンプルを分析してください",
    "chat_placeholder": "栄養レベル、pH バランス、有機物含有量、肥料について質問...",
    "thinking": "考え中...",
    "less_fertile": "低肥沃度",
    "fertile": "肥沃",
    "highly_fertile": "高肥沃度",
    "sample": "サンプル",
    "language_label": "Select Language / 言語を選択",
    "analysis_complete": "分析が完了しました：",
    "soil_classified": "土壌は次のように分類されます：",
    "how_help": "土壌品質の改善についてどのようにお手伝いできますか？",
    "nutrient_question": "分析に基づいて、私の土壌にはどのような特定の栄養素が必要ですか？どのように改善できますか？",
    "fertilizer_question": "この土壌状態にはどのような種類と量の肥料を使用すべきですか？"
}

# Function to get text based on language
def get_text(key):
    if st.session_state.language == "Japanese":
        return content_ja.get(key, content_en.get(key))
    return content_en.get(key)

# Custom CSS (updated with better language selector positioning)
st.markdown("""
    <style>
    /* Main container styling */
    .main {
        padding: 1rem;
        background-color: #1a1a1a;
    }
    
    /* White container for all content */
    .stApp > main > div > div > div {
        background-color: white;
        border-radius: 10px;
        padding: 2rem;
        margin: 1rem 0;
    }
    
    /* Title styling */
    h1 {
        color: #333;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    h3 {
        color: #333;
        margin-bottom: 1rem;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: #0066cc;
        color: white;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        border: none;
        font-weight: 500;
        width: 100%;
    }
    
    .stButton > button:hover {
        background-color: #0052a3;
    }
    
    /* Column styling */
    [data-testid="column"] {
        background-color: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Dark background for main app */
    [data-testid="stAppViewContainer"] {
        background-color: #1a1a1a;
    }
    
    [data-testid="stHeader"] {
        background-color: #1a1a1a;
    }
    
    /* Sensor data container styling */
    .sensor-container {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 1rem;
        height: 500px;
        overflow-y: auto;
    }
    
    /* Individual sensor box styling */
    .sensor-box {
        background-color: white;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 0.75rem 1rem;
        margin-bottom: 0.5rem;
    }
    
    .sensor-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #0066cc;
        margin: 0;
    }
    
    /* Chat container styling */
    .chat-container {
        background-color: #f5f5f5;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 1rem;
        height: 500px;
        overflow-y: auto;
    }
    
    /* Analysis result styling */
    .analysis-result-box {
        border-radius: 8px;
        padding: 0.75rem 1rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    .analysis-result-text {
        font-size: 1rem;
        font-weight: 500;
        margin: 0;
        color: #333;
    }
    
    /* Scrollbar styling */
    .sensor-container::-webkit-scrollbar {
        width: 8px;
    }
    
    .sensor-container::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 4px;
    }
    
    .sensor-container::-webkit-scrollbar-thumb {
        background: #888;
        border-radius: 4px;
    }
    
    .sensor-container::-webkit-scrollbar-thumb:hover {
        background: #555;
    }
    
    /* Live data indicator */
    .live-indicator {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        color: #0066cc;
        font-size: 0.9rem;
        margin-bottom: 0.5rem;
    }
    
    .pulse-dot {
        width: 8px;
        height: 8px;
        background-color: #0066cc;
        border-radius: 50%;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% {
            opacity: 1;
            transform: scale(1);
        }
        50% {
            opacity: 0.5;
            transform: scale(1.2);
        }
        100% {
            opacity: 1;
            transform: scale(1);
        }
    }
    </style>
""", unsafe_allow_html=True)

# Initialize other session states
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'sensor_samples' not in st.session_state:
    st.session_state.sensor_samples = get_multiple_sensor_samples(3)
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = {}
if 'current_analysis' not in st.session_state:
    st.session_state.current_analysis = None
if 'loading_data' not in st.session_state:
    st.session_state.loading_data = False

# Create a container for title and language selector
title_container = st.container()
with title_container:
    # Create columns for title and language selector
    col1, col2, col3 = st.columns([2, 8, 2])
    
    with col1:
        st.empty()  # Empty space on the left
    
    with col2:
        # Title in the center
        st.markdown(f"<h1>{get_text('title')}</h1>", unsafe_allow_html=True)
    
    with col3:
        # Language selector aligned with title
        st.markdown("<div style='margin-top: 20px;'>", unsafe_allow_html=True)
        language = st.selectbox(
            get_text("language_label"),
            ["English", "Japanese"],
            index=0 if st.session_state.language == "English" else 1,
            key="language_selector"
        )
        st.session_state.language = language
        st.markdown("</div>", unsafe_allow_html=True)

# Create main container
with st.container():
    # Create two columns with spacing
    col1, spacer, col2 = st.columns([5, 0.5, 5])
    
    # Left column - Sensor Data
    with col1:
        st.markdown(f"### {get_text('sensor_data')}")
        
        # Load New Samples button at the top
        if st.button(get_text('load_new_samples'), key="refresh_samples", use_container_width=True):
            st.session_state.loading_data = True
            st.rerun()
        
        # Show loading indicator when getting new data
        if st.session_state.loading_data:
            with st.spinner(get_text('getting_data')):
                time.sleep(1.5)  # Simulate data fetching
                st.session_state.sensor_samples = get_multiple_sensor_samples(3)
                st.session_state.analysis_results = {}
                st.session_state.current_analysis = None
                st.session_state.chat_history = []
                st.session_state.loading_data = False
                st.rerun()
        
        # Live data indicator
        st.markdown(f"""
            <div class="live-indicator">
                <div class="pulse-dot"></div>
                <span>{get_text('live_sensor')}</span>
            </div>
        """, unsafe_allow_html=True)
        
        # Scrollable container for sensor data
        sensor_container = st.container(height=500)
        
        with sensor_container:
            # Display sensor samples
            for i, sample in enumerate(st.session_state.sensor_samples):
                with st.container():
                    # Compact sensor box header
                    st.markdown(f"""
                        <div class='sensor-box'>
                            <p class='sensor-title'>{get_text('sample')} {i+1}</p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Display sensor values in a more compact format
                    col_a, col_b = st.columns(2)
                    
                    sensor_items = list(sample['data_dict'].items())
                    half = len(sensor_items) // 2
                    
                    with col_a:
                        for key, value in sensor_items[:half]:
                            param_key = key.split(' - ')[0]
                            st.markdown(f"**{param_key}:** {value}")
                    
                    with col_b:
                        for key, value in sensor_items[half:]:
                            param_key = key.split(' - ')[0]
                            st.markdown(f"**{param_key}:** {value}")
                    
                    # Analyze button
                    if st.button(f"{get_text('analyze')} {get_text('sample')} {i+1}", key=f"analyze_{sample['sample_id']}", use_container_width=True):
                        with st.spinner(get_text('analyzing')):
                            # Get analysis from backend with language
                            explanation, data_json = info_response(sample['input_sensor'], st.session_state.language)
                            
                            # Store results
                            st.session_state.analysis_results[sample['sample_id']] = {
                                'explanation': explanation,
                                'data_json': data_json,
                                'sample': sample
                            }
                            st.session_state.current_analysis = sample['sample_id']
                            
                            # Translate status
                            status = data_json['status']
                            translated_status = get_text(status.lower().replace(' ', '_'))
                            
                            # Add initial message to chat
                            initial_msg = f"{get_text('analysis_complete')} {get_text('sample')} {i+1}. {get_text('soil_classified')} **{translated_status}**. {get_text('how_help')}"
                            
                            st.session_state.chat_history = [{
                                "role": "assistant",
                                "content": initial_msg
                            }]
                            
                            time.sleep(0.5)
                            st.rerun()
                    
                    st.markdown("---")
    
    # Right column - Chat Bot
    with col2:
        st.markdown(f"### {get_text('chat_title')}")
        
        # Display analysis result at the top of chat if available
        if st.session_state.current_analysis and st.session_state.current_analysis in st.session_state.analysis_results:
            result = st.session_state.analysis_results[st.session_state.current_analysis]
            status = result['data_json']['status']
            
            # Translate status
            translated_status = get_text(status.lower().replace(' ', '_'))
            
            # Determine styling based on status
            if status == "Less fertile":
                status_color = "#f44336"
                bg_color = "#ffebee"
                border_color = "#ffcdd2"
            elif status == "Fertile":
                status_color = "#ff9800"
                bg_color = "#fff3e0"
                border_color = "#ffe0b2"
            else:
                status_color = "#4caf50"
                bg_color = "#e8f5e9"
                border_color = "#c8e6c9"
            
            sample_num = st.session_state.current_analysis.split()[-1]
            
            st.markdown(f"""
                <div class='analysis-result-box' style='background-color: {bg_color}; border: 2px solid {border_color};'>
                    <div>
                        <span style='font-size: 1.1rem; color: {status_color}; font-weight: 600;'>{get_text('analysis_results')} {translated_status}</span>
                        <p class='analysis-result-text'>{translated_status} {get_text('detected_for')} {get_text('sample')} {sample_num}</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        # Quick action buttons
        if st.session_state.current_analysis:
            st.markdown(f"**{get_text('quick_questions')}**")
            
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if st.button(get_text('nutrient_improvement'), use_container_width=True):
                    question = get_text('nutrient_question')
                    
                    st.session_state.chat_history.append({
                        "role": "user",
                        "content": question
                    })
                    
                    response = chat_response(st.session_state.chat_history[:-1], question, st.session_state.language)
                    
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": response
                    })
                    st.rerun()
            
            with col_btn2:
                if st.button(get_text('fertilizer_guide'), use_container_width=True):
                    question = get_text('fertilizer_question')
                    
                    st.session_state.chat_history.append({
                        "role": "user",
                        "content": question
                    })
                    
                    response = chat_response(st.session_state.chat_history[:-1], question, st.session_state.language)
                    
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": response
                    })
                    st.rerun()
        
        # Chat messages container
        st.markdown("---")
        chat_container = st.container(height=350)
        
        with chat_container:
            if st.session_state.chat_history:
                for message in st.session_state.chat_history:
                    with st.chat_message(message["role"]):
                        st.markdown(message["content"])
            else:
                if st.session_state.current_analysis:
                    st.info(get_text('ask_anything'))
                else:
                    st.info(get_text('analyze_first'))
        
        # Chat input
        if st.session_state.current_analysis:
            placeholder = get_text('chat_placeholder')
            user_question = st.chat_input(placeholder, key="chat_input")
            
            if user_question:
                # Add user message
                st.session_state.chat_history.append({
                    "role": "user",
                    "content": user_question
                })
                
                # Get AI response with language
                with st.spinner(get_text('thinking')):
                    response = chat_response(st.session_state.chat_history[:-1], user_question, st.session_state.language)
                    
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": response
                    })
                
                st.rerun()

# Add footer
st.markdown("<br><br>", unsafe_allow_html=True)
