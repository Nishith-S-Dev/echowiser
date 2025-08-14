
# import streamlit as st
# import os
# from pathlib import Path
# from utils.pdf_processor import PDFProcessor
# from models.tts_engine import TTSEngine
# from models.tone_processor import ToneProcessor
# import tempfile

# # Page configuration
# st.set_page_config(
#     page_title="AI Audiobook Generator",
#     page_icon="🎧",
#     layout="wide"
# )

# def main():
#     st.title("🎧 AI Audiobook Generator")
#     st.subheader("Transform your texts and PDFs into engaging audiobooks with multiple tones!")
    
#     # Sidebar for configuration
#     with st.sidebar:
#         st.header("Configuration")
        
#         # Model selection
#         model_choice = st.selectbox(
#             "Choose TTS Model:",
#             ["Edge TTS", "Google TTS", "IBM Granite"]  # Remove Bark temporarily
#         )
        
#         # Tone selection
#         tone = st.selectbox(
#             "Select Tone:",
#             ["Neutral", "Inspiring", "Suspenseful", "Dramatic", "Calm", "Energetic"]
#         )
        
#         # Voice settings
#         voice_speed = st.slider("Voice Speed", 0.5, 2.0, 1.0, 0.1)
#         voice_pitch = st.slider("Voice Pitch", -20, 20, 0, 1)
    
#     # Main content area
#     col1, col2 = st.columns([2, 1])
    
#     with col1:
#         st.header("Input Content")
        
#         # Input method selection
#         input_method = st.radio(
#             "Choose input method:",
#             ["Upload PDF", "Enter Text"]
#         )
        
#         text_content = ""
        
#         if input_method == "Upload PDF":
#             uploaded_file = st.file_uploader(
#                 "Upload PDF file",
#                 type=['pdf'],
#                 help="Upload a PDF file to convert to audiobook"
#             )
            
#             if uploaded_file:
#                 try:
#                     processor = PDFProcessor()
#                     text_content = processor.extract_text(uploaded_file)
#                     st.text_area("Extracted Text (Preview):", 
#                                text_content[:500] + "..." if len(text_content) > 500 else text_content,
#                                height=200, disabled=True)
#                 except Exception as e:
#                     st.error(f"Error processing PDF: {str(e)}")
        
#         else:
#             text_content = st.text_area(
#                 "Enter your text:",
#                 placeholder="Paste or type the text you want to convert to audiobook...",
#                 height=100
#             )
    
#     with col2:
#         st.header("Audio Generation")
        
#         if st.button("🎵 Generate Audiobook", type="primary"):
#             if text_content.strip():
#                 with st.spinner("Generating audiobook... Please wait"):
#                     try:
#                         # Initialize TTS engine
#                         tts_engine = TTSEngine(model_choice)
#                         tone_processor = ToneProcessor()
                        
#                         # Process text with selected tone
#                         processed_text = tone_processor.apply_tone(text_content, tone)
                        
#                         # Generate audio
#                         audio_file = tts_engine.generate_audio(
#                             processed_text,
#                             tone=tone,
#                             speed=voice_speed,
#                             pitch=voice_pitch
#                         )
                        
#                         if audio_file:
#                             st.success("✅ Audiobook generated successfully!")
                            
#                             # Audio player
#                             st.audio(audio_file, format='audio/wav')
                            
#                             # Download button
#                             with open(audio_file, "rb") as f:
#                                 st.download_button(
#                                     label="📥 Download Audiobook",
#                                     data=f.read(),
#                                     file_name=f"audiobook_{tone.lower()}.wav",
#                                     mime="audio/wav"
#                                 )
                                
#                     except Exception as e:
#                         st.error(f"Error generating audiobook: {str(e)}")
#             else:
#                 st.warning("Please provide text content to generate audiobook.")

# if __name__ == "__main__":
#     main()








# # import streamlit as st
# # import os
# # from pathlib import Path
# # from utils.pdf_processor import PDFProcessor
# # from models.hf_tts_engine import HuggingFaceTTS
# # from models.hf_text_enhancer import HuggingFaceTextEnhancer
# # from dotenv import load_dotenv

# # # Load environment variables
# # load_dotenv()

# # # Page configuration
# # st.set_page_config(
# #     page_title="🎧 AI Audiobook Generator - Hugging Face Edition",
# #     page_icon="🎧",
# #     layout="wide"
# # )

# # def main():
# #     st.title("🎧 AI Audiobook Generator")
# #     st.header("🤗 Powered by Hugging Face Models - Transform texts into engaging audiobooks!")
    
# #     # Check for API token
# #     if not os.getenv('HUGGINGFACE_API_TOKEN'):
# #         st.error("⚠️ **Missing Hugging Face API Token!**")
# #         st.info("1. Go to https://huggingface.co/settings/tokens")
# #         st.info("2. Create a new token")
# #         st.info("3. Add it to your .env file: `HUGGINGFACE_API_TOKEN=hf_your_token_here`")
# #         st.stop()
    
# #     # Sidebar configuration
# #     with st.sidebar:
# #         st.header("🛠️ Model Configuration")
        
# #         # Text Enhancement
# #         st.subheader("📝 Text Enhancement")
# #         enhancement_model = st.selectbox(
# #             "Enhancement Model:",
# #             [
# #                 "None (Skip Enhancement)",
# #                 "ibm-granite/granite-3.1-8b-instruct",
# #                 "ibm-granite/granite-3.0-8b-instruct", 
# #                 "microsoft/DialoGPT-medium"
# #             ],
# #             help="Enhance your text with AI before converting to speech"
# #         )
        
# #         # TTS Model
# #         st.subheader("🎤 Text-to-Speech")
# #         tts_model = st.selectbox(
# #             "TTS Model:",
# #             [
# #                 "parler-tts/parler-tts-large-v1",
# #                 "microsoft/speecht5_tts", 
# #                 "facebook/mms-tts-eng",
# #                 "espnet/kan-bayashi_ljspeech_vits"
# #             ],
# #             help="Choose the voice generation model"
# #         )
        
# #         # Tone/Style
# #         st.subheader("🎭 Voice Style")
# #         tone = st.selectbox(
# #             "Select Tone:",
# #             ["neutral", "inspiring", "suspenseful", "dramatic", "calm", "energetic"],
# #             help="Choose the emotional tone for your audiobook"
# #         )
        
# #         # Advanced settings
# #         with st.expander("🔧 Advanced Settings"):
# #             enhance_text = st.checkbox("Enhance text before TTS", value=True)
            
# #             if "parler" in tts_model:
# #                 voice_description = st.text_area(
# #                     "Custom Voice Description:",
# #                     value="A clear female voice with natural pacing and good articulation",
# #                     help="Describe the voice characteristics you want"
# #                 )
# #             else:
# #                 voice_description = None
                
# #             # Text length limit
# #             max_text_length = st.slider(
# #                 "Max text length for TTS:",
# #                 500, 2000, 1000,
# #                 help="Longer texts take more time to process"
# #             )
    
# #     # Main content
# #     col1, col2 = st.columns([3, 2])
    
# #     with col1:
# #         st.header("📄 Input Content")
        
# #         # Input method
# #         input_method = st.radio(
# #             "Choose input method:",
# #             ["📝 Enter Text", "📄 Upload PDF"],
# #             horizontal=True
# #         )
        
# #         text_content = ""
        
# #         if input_method == "📄 Upload PDF":
# #             uploaded_file = st.file_uploader(
# #                 "Upload your PDF file",
# #                 type=['pdf'],
# #                 help="Upload a PDF document to convert to audiobook"
# #             )
            
# #             if uploaded_file:
# #                 try:
# #                     with st.spinner("🔍 Extracting text from PDF..."):
# #                         processor = PDFProcessor()
# #                         text_content = processor.extract_text(uploaded_file)
                    
# #                     if text_content.strip():
# #                         st.success(f"✅ Extracted {len(text_content)} characters from PDF")
                        
# #                         # Truncate if too long
# #                         if len(text_content) > max_text_length:
# #                             text_content = text_content[:max_text_length]
# #                             st.warning(f"⚠️ Text truncated to {max_text_length} characters for processing")
                        
# #                         with st.expander("📖 Preview extracted text"):
# #                             st.text_area("", text_content[:500] + "..." if len(text_content) > 500 else text_content, height=200, disabled=True)
# #                     else:
# #                         st.error("❌ Could not extract text from PDF. Please try a different file.")
# #                 except Exception as e:
# #                     st.error(f"❌ Error processing PDF: {str(e)}")
# #                     st.info("💡 **Troubleshooting:**")
# #                     st.info("- Try a different PDF file")
# #                     st.info("- Ensure the PDF contains readable text (not scanned images)")
# #                     st.info("- Check if the PDF is password protected")
        
# #         else:
# #             text_content = st.text_area(
# #                 "Enter your text:",
# #                 placeholder="Paste or type the text you want to convert to audiobook...\n\nExample: 'Once upon a time, in a land far away, there lived a brave knight who embarked on an extraordinary adventure...'",
# #                 height=400,
# #                 help="Enter the text you want to convert to speech"
# #             )
            
# #             # Truncate if too long
# #             if text_content and len(text_content) > max_text_length:
# #                 text_content = text_content[:max_text_length]
# #                 st.warning(f"⚠️ Text truncated to {max_text_length} characters for processing")
    
# #     with col2:
# #         st.header("🎵 Generate Audio")
        
# #         # Show current settings
# #         with st.container():
# #             st.info(f"""
# #             **Current Settings:**
# #             - 🤖 Enhancement: {enhancement_model.split('/')[-1] if '/' in enhancement_model else enhancement_model}
# #             - 🎤 TTS Model: {tts_model.split('/')[-1]}
# #             - 🎭 Tone: {tone.title()}
# #             - 📏 Max Length: {max_text_length} chars
# #             """)
        
# #         # Generate button
# #         if st.button("🚀 Generate Audiobook", type="primary", use_container_width=True):
# #             if not text_content.strip():
# #                 st.warning("⚠️ Please provide text content to generate audiobook.")
# #                 st.stop()
            
# #             # Show progress
# #             try:
# #                 # Initialize engines
# #                 text_enhancer = HuggingFaceTextEnhancer()
# #                 tts_engine = HuggingFaceTTS()
                
# #                 processed_text = text_content
                
# #                 # Text Enhancement Step
# #                 if enhance_text and enhancement_model != "None (Skip Enhancement)":
# #                     with st.spinner("🔄 Enhancing text with AI..."):
# #                         processed_text = text_enhancer.enhance_text(
# #                             text_content, 
# #                             tone, 
# #                             enhancement_model
# #                         )
                    
# #                     st.success("✅ Text enhanced successfully!")
                    
# #                     with st.expander("📖 Enhanced Text Preview"):
# #                         st.text_area("Enhanced version:", processed_text[:500] + "..." if len(processed_text) > 500 else processed_text, height=150, disabled=True)
                
# #                 # TTS Generation Step
# #                 with st.spinner("🎤 Converting text to speech... This may take 30-60 seconds..."):
# #                     audio_file = tts_engine.generate_audio(
# #                         processed_text,
# #                         model=tts_model,
# #                         tone=tone,
# #                         voice_description=voice_description
# #                     )
                
# #                 if audio_file and os.path.exists(audio_file):
# #                     st.success("🎉 **Audiobook generated successfully!**")
                    
# #                     # Audio player
# #                     st.audio(audio_file, format='audio/wav')
                    
# #                     # File info
# #                     file_size = os.path.getsize(audio_file) / 1024  # KB
# #                     st.info(f"📊 Audio file: {file_size:.1f} KB")
                    
# #                     # Download button
# #                     with open(audio_file, "rb") as f:
# #                         st.download_button(
# #                             label="📥 Download Audiobook",
# #                             data=f.read(),
# #                             file_name=f"audiobook_{tone}.wav",
# #                             mime="audio/wav",
# #                             use_container_width=True
# #                         )
# #                 else:
# #                     st.error("❌ Failed to generate audio. Please try again with a different model.")
                    
# #             except Exception as e:
# #                 st.error(f"❌ **Generation Error:** {str(e)}")
# #                 st.info("💡 **Troubleshooting tips:**")
# #                 st.info("- Try a shorter text (under 500 characters)")
# #                 st.info("- Wait a few minutes if models are loading")
# #                 st.info("- Try a different TTS model")
# #                 st.info("- Check your Hugging Face API token")

# # if __name__ == "__main__":
# #     main()






import streamlit as st
import os
from pathlib import Path
from utils.pdf_processor import PDFProcessor
from models.tts_engine import TTSEngine
from models.tone_processor import ToneProcessor
import tempfile

# Page configuration
st.set_page_config(
    page_title="EchoV - AI Audiobook Generator",
    page_icon="🎧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Dark theme CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Dark theme base */
    .stApp {
        background: #0a0a0a;
        color: #e5e5e5;
    }
    
    .main {
        font-family: 'Inter', sans-serif;
        background: #0a0a0a;
        padding: 0 2rem;
    }
    
    /* Header */
    .main-header {
        text-align: center;
        margin: 3rem 0 4rem 0;
    }
    
    .logo {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        letter-spacing: -2px;
    }
    
    .tagline {
        font-size: 1.1rem;
        color: #9ca3af;
        font-weight: 400;
        margin: 0;
    }
    
    /* Content containers */
    .content-section {
        background: #111111;
        border: 1px solid #1f1f1f;
        border-radius: 12px;
        padding: 2rem;
        margin-bottom: 2rem;
    }
    
    .section-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #f3f4f6;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Controls row */
    .controls-row {
        background: #111111;
        border: 1px solid #1f1f1f;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 2rem;
        display: flex;
        gap: 2rem;
        align-items: center;
        flex-wrap: wrap;
    }
    
    .control-group {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }
    
    .control-label {
        font-size: 0.9rem;
        color: #9ca3af;
        font-weight: 500;
    }
    
    /* Input styling */
    .stTextArea textarea {
        background: #0a0a0a !important;
        border: 1px solid #2a2a2a !important;
        border-radius: 8px !important;
        color: #e5e5e5 !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 1px #6366f1 !important;
    }
    
    .stSelectbox > div > div {
        background: #0a0a0a;
        border: 1px solid #2a2a2a;
        color: #e5e5e5;
    }
    
    .stSlider > div > div > div > div {
        background: #6366f1;
    }
    
    /* File uploader */
    .stFileUploader > div {
        background: #0a0a0a;
        border: 2px dashed #2a2a2a;
        border-radius: 8px;
        padding: 2rem;
        text-align: center;
    }
    
    .stFileUploader > div:hover {
        border-color: #6366f1;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 20px rgba(99, 102, 241, 0.3);
    }
    
    .generate-btn {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 1rem 2rem;
        font-weight: 600;
        font-size: 1.1rem;
        cursor: pointer;
        width: 100%;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .generate-btn:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 25px rgba(99, 102, 241, 0.4);
    }
    
    /* Status messages */
    .success-msg {
        background: linear-gradient(135deg, #059669 0%, #047857 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        font-weight: 500;
    }
    
    .warning-msg {
        background: linear-gradient(135deg, #d97706 0%, #b45309 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        font-weight: 500;
    }
    
    .error-msg {
        background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        font-weight: 500;
    }
    
    /* Audio player */
    .stAudio {
        margin: 1.5rem 0;
    }
    
    /* Progress */
    .stProgress > div > div > div > div {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
    }
    
    /* Stats */
    .stats-row {
        display: flex;
        gap: 1rem;
        margin: 1rem 0;
    }
    
    .stat-item {
        background: #1a1a1a;
        border: 1px solid #2a2a2a;
        border-radius: 8px;
        padding: 1rem;
        flex: 1;
        text-align: center;
    }
    
    .stat-value {
        font-size: 1.5rem;
        font-weight: 600;
        color: #6366f1;
        margin-bottom: 0.25rem;
    }
    
    .stat-label {
        font-size: 0.9rem;
        color: #9ca3af;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Radio buttons */
    .stRadio > div {
        flex-direction: row;
        gap: 2rem;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: #1a1a1a;
        border: 1px solid #2a2a2a;
        color: #e5e5e5;
    }
    
    .streamlit-expanderContent {
        background: #0a0a0a;
        border: 1px solid #2a2a2a;
        border-top: none;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'errors' not in st.session_state:
    st.session_state.errors = []

def add_error(error_msg):
    st.session_state.errors.append(error_msg)

def clear_errors():
    st.session_state.errors = []

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1 class="logo">EchoV</h1>
        <p class="tagline">Transform text into engaging audiobooks with AI</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Controls Row
    st.markdown('<div class="controls-row">', unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns([2, 1.5, 1, 1, 1])
    
    with col1:
        st.markdown('<div class="control-group">', unsafe_allow_html=True)
        st.markdown('<span class="control-label">TTS Model</span>', unsafe_allow_html=True)
        model_choice = st.selectbox("", ["Edge TTS", "Google TTS", "IBM Granite"], label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="control-group">', unsafe_allow_html=True)
        st.markdown('<span class="control-label">Voice Tone</span>', unsafe_allow_html=True)
        tone = st.selectbox("", ["Neutral", "Inspiring", "Suspenseful", "Dramatic", "Calm", "Energetic"], label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="control-group">', unsafe_allow_html=True)
        st.markdown('<span class="control-label">Speed</span>', unsafe_allow_html=True)
        voice_speed = st.slider("", 0.5, 2.0, 1.0, 0.1, label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="control-group">', unsafe_allow_html=True)
        st.markdown('<span class="control-label">Pitch</span>', unsafe_allow_html=True)
        voice_pitch = st.slider("", -20, 20, 0, 1, label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col5:
        st.markdown('<div class="control-group">', unsafe_allow_html=True)
        st.markdown('<span class="control-label">&nbsp;</span>', unsafe_allow_html=True)
        if st.button("🔄 Reset", use_container_width=True):
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Main content
    col_main, col_output = st.columns([1.2, 1], gap="large")
    
    with col_main:
        # Input Section
        st.markdown("""
        <div class="content-section">
            <div class="section-title">📝 Content Input</div>
        """, unsafe_allow_html=True)
        
        # Input method
        input_method = st.radio("", ["Upload PDF", "Enter Text"], horizontal=True, label_visibility="collapsed")
        
        text_content = ""
        
        if input_method == "Upload PDF":
            uploaded_file = st.file_uploader("", type=['pdf'], label_visibility="collapsed")
            
            if uploaded_file:
                try:
                    with st.spinner("Extracting text..."):
                        processor = PDFProcessor()
                        text_content = processor.extract_text(uploaded_file)
                    
                    if text_content.strip():
                        st.markdown(f"""
                        <div class="success-msg">
                            ✅ Extracted {len(text_content):,} characters
                        </div>
                        """, unsafe_allow_html=True)
                        
                        with st.expander("Preview content"):
                            preview = text_content[:500] + "..." if len(text_content) > 500 else text_content
                            st.text_area("", preview, height=150, disabled=True, label_visibility="collapsed")
                    else:
                        add_error("Could not extract text from PDF")
                        
                except Exception as e:
                    add_error(f"PDF processing failed: {str(e)}")
        
        else:
            text_content = st.text_area(
                "",
                placeholder="Enter your text content here...",
                height=200,
                label_visibility="collapsed"
            )
            
            if text_content:
                char_count = len(text_content)
                word_count = len(text_content.split())
                est_time = max(1, word_count // 150)
                
                st.markdown(f"""
                <div class="stats-row">
                    <div class="stat-item">
                        <div class="stat-value">{char_count:,}</div>
                        <div class="stat-label">Characters</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">{word_count:,}</div>
                        <div class="stat-label">Words</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">~{est_time}</div>
                        <div class="stat-label">Min Audio</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_output:
        # Generation Section
        st.markdown("""
        <div class="content-section">
            <div class="section-title">🎵 Generate Audio</div>
        """, unsafe_allow_html=True)
        
        # Generate button
        if st.button("🚀 Generate Audiobook", type="primary", use_container_width=True):
            if not text_content.strip():
                st.markdown("""
                <div class="warning-msg">
                    ⚠️ Please provide text content first
                </div>
                """, unsafe_allow_html=True)
            else:
                clear_errors()
                
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                try:
                    # Initialize
                    status_text.text("🔧 Initializing...")
                    progress_bar.progress(25)
                    
                    tts_engine = TTSEngine(model_choice)
                    tone_processor = ToneProcessor()
                    
                    # Process
                    status_text.text("🎭 Processing tone...")
                    progress_bar.progress(50)
                    
                    processed_text = tone_processor.apply_tone(text_content, tone)
                    
                    # Generate
                    status_text.text("🎤 Generating audio...")
                    progress_bar.progress(75)
                    
                    audio_file = tts_engine.generate_audio(
                        processed_text,
                        tone=tone,
                        speed=voice_speed,
                        pitch=voice_pitch
                    )
                    
                    progress_bar.progress(100)
                    status_text.text("✅ Complete!")
                    
                    if audio_file:
                        st.markdown("""
                        <div class="success-msg">
                            🎉 Audiobook generated successfully!
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Audio player
                        st.audio(audio_file, format='audio/wav')
                        
                        # Download
                        with open(audio_file, "rb") as f:
                            st.download_button(
                                "📥 Download",
                                f.read(),
                                f"echov_audiobook_{tone.lower()}.wav",
                                "audio/wav",
                                use_container_width=True
                            )
                    else:
                        add_error("Audio generation failed")
                        
                except Exception as e:
                    add_error(f"Error: {str(e)}")
                
                finally:
                    progress_bar.empty()
                    status_text.empty()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Error display
    if st.session_state.errors:
        for error in st.session_state.errors:
            st.markdown(f"""
            <div class="error-msg">
                🚨 {error}
            </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()