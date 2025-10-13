import streamlit as st
import time
import random
from datetime import datetime
import base64
from io import BytesIO
from PIL import Image, ImageDraw
import json
from demo_data import (
    EXTENDED_DEMO_RESULTS, 
    EXTENDED_CITATION_DATA, 
    SAMPLE_QUERIES, 
    SYSTEM_METRICS,
    create_demo_chart_image,
    create_demo_diagram_image
)

# Page configuration
st.set_page_config(
    page_title="Multimodal RAG System - SIH 2025",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .upload-section {
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        border: 2px dashed #dee2e6;
        margin: 1rem 0;
    }
    
    .result-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }
    
    .citation {
        background: #e3f2fd;
        color: #1976d2;
        padding: 0.2rem 0.5rem;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: bold;
        cursor: pointer;
        display: inline-block;
        margin: 0 0.2rem;
    }
    
    .loading-spinner {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 2rem;
    }
    
    .feature-highlight {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .sidebar-section {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'search_results' not in st.session_state:
    st.session_state.search_results = []
if 'recent_queries' not in st.session_state:
    st.session_state.recent_queries = []
if 'uploaded_files' not in st.session_state:
    st.session_state.uploaded_files = []

# Demo data
DEMO_RESULTS = EXTENDED_DEMO_RESULTS
CITATION_DATA = EXTENDED_CITATION_DATA

def create_placeholder_image(width=300, height=200, text="Sample Image", image_type="generic"):
    """Create a placeholder image"""
    if image_type == "chart":
        return create_demo_chart_image(width, height)
    elif image_type == "diagram":
        return create_demo_diagram_image(width, height)
    else:
        img = Image.new('RGB', (width, height), color='#f0f0f0')
        draw = ImageDraw.Draw(img)
        # Add some visual elements
        draw.rectangle([10, 10, width-10, height-10], outline='#ccc', width=2)
        draw.text((width//2 - 50, height//2 - 10), text, fill='#666')
        return img

def simulate_processing():
    """Simulate AI processing with loading animation"""
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    steps = [
        "Analyzing uploaded documents...",
        "Extracting text and metadata...",
        "Processing images with CLIP...",
        "Transcribing audio with Whisper...",
        "Generating embeddings...",
        "Performing semantic search...",
        "Ranking results by relevance..."
    ]
    
    for i, step in enumerate(steps):
        status_text.text(step)
        progress_bar.progress((i + 1) / len(steps))
        time.sleep(0.5)
    
    status_text.text("Search complete!")
    time.sleep(0.5)
    progress_bar.empty()
    status_text.empty()

def display_search_results(results):
    """Display multimodal search results"""
    st.markdown("### 🔍 Search Results")
    
    for i, result in enumerate(results):
        with st.container():
            st.markdown(f'<div class="result-card">', unsafe_allow_html=True)
            
            # Result type indicator
            type_emoji = {"text": "📄", "image": "🖼️", "audio": "🎵"}
            st.markdown(f"**{type_emoji[result['type']]} {result['type'].title()} Result**")
            
            if result['type'] == 'text':
                # Highlight the relevant text if available
                if 'highlighted_text' in result:
                    content = result['content'].replace(
                        result['highlighted_text'], 
                        f"<mark style='background-color: yellow'>{result['highlighted_text']}</mark>"
                    )
                    st.markdown(content, unsafe_allow_html=True)
                else:
                    st.write(result['content'])
            elif result['type'] == 'image':
                st.write(f"**{result['content']}**")
                # Determine image type for better placeholder
                image_type = "generic"
                if "chart" in result['content'].lower():
                    image_type = "chart"
                elif "diagram" in result['content'].lower() or "architecture" in result['content'].lower():
                    image_type = "diagram"
                
                placeholder_img = create_placeholder_image(text=result['content'], image_type=image_type)
                st.image(placeholder_img, caption=f"From {result['source']}, Page {result['page']}")
                
                # Show description if available
                if 'description' in result:
                    st.caption(f"📝 {result['description']}")
            elif result['type'] == 'audio':
                st.write(f"**{result['content']}**")
                st.markdown(f"🎵 Audio clip at {result['timestamp']} from {result['source']}")
                
                # Show transcript if available
                if 'transcript' in result:
                    with st.expander("📝 View Transcript"):
                        st.write(result['transcript'])
            
            # Citations
            citation_text = "Citations: "
            for citation_num in result['citations']:
                citation_text += f'<span class="citation" onclick="showCitation({citation_num})">[{citation_num}]</span>'
            
            st.markdown(citation_text, unsafe_allow_html=True)
            
            # Confidence score
            confidence_color = "green" if result['confidence'] > 0.9 else "orange" if result['confidence'] > 0.8 else "red"
            st.markdown(f"**Confidence:** <span style='color: {confidence_color}'>{result['confidence']:.2f}</span>", unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)

def show_citation_modal(citation_num):
    """Show citation details in a modal-like format"""
    if citation_num in CITATION_DATA:
        citation = CITATION_DATA[citation_num]
        st.markdown("---")
        st.markdown(f"### 📚 Citation [{citation_num}] Details")
        
        with st.expander(f"{citation['title']}", expanded=True):
            st.write(citation['content'])
            
            # Show metadata if available
            if 'metadata' in citation:
                st.markdown("**Metadata:**")
                for key, value in citation['metadata'].items():
                    st.write(f"• **{key.title()}:** {value}")
            
            # Show related content if available
            if citation['type'] == 'document':
                st.markdown("**Related Content:**")
                st.write("• Full document available for download")
                st.write("• Highlighted relevant sections")
                st.write("• Cross-references to related documents")
            elif citation['type'] == 'image':
                st.markdown("**Image Details:**")
                st.write("• High-resolution version available")
                st.write("• Interactive zoom and annotation tools")
                st.write("• Related images and diagrams")
            elif citation['type'] == 'audio':
                st.markdown("**Audio Details:**")
                st.write("• Full transcript available")
                st.write("• Playback controls and timestamp navigation")
                st.write("• Speaker identification and analysis")

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🔍 Multimodal RAG System</h1>
        <p>Advanced Offline Retrieval-Augmented Generation for SIH 2025</p>
        <p><em>Powered by CLIP • Whisper • LLM • Vector Search</em></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🎯 Quick Actions")
        
        if st.button("📊 Demo: Financial Report", use_container_width=True):
            st.session_state.demo_query = "financial report"
        
        if st.button("🔧 Demo: Product Specs", use_container_width=True):
            st.session_state.demo_query = "product specifications"
        
        if st.button("📈 Demo: Market Analysis", use_container_width=True):
            st.session_state.demo_query = "market analysis"
        
        if st.button("📚 Demo: Research Paper", use_container_width=True):
            st.session_state.demo_query = "research paper"
        
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown("### 📁 Recent Queries")
        for query in st.session_state.recent_queries[-5:]:
            if st.button(f"🔍 {query}", key=f"recent_{query}"):
                st.session_state.demo_query = query
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown("### ⚙️ System Status")
        st.success("🟢 All Systems Online")
        st.info(f"📊 {SYSTEM_METRICS['documents_indexed']:,} documents indexed")
        st.info(f"🖼️ {SYSTEM_METRICS['images_processed']:,} images processed")
        st.info(f"🎵 {SYSTEM_METRICS['audio_files_transcribed']} audio files transcribed")
        st.info(f"⚡ Avg Response: {SYSTEM_METRICS['average_response_time']}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown("### 💡 Sample Queries")
        for query in SAMPLE_QUERIES[:3]:
            if st.button(f"💭 {query[:30]}...", key=f"sample_{query[:10]}"):
                st.session_state.demo_query = query
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 🔍 Search Query")
        query = st.text_input(
            "Enter your search query:",
            placeholder="e.g., 'Show me the report about quarterly revenue growth'",
            key="main_query"
        )
        
        # Check for demo query from sidebar
        if hasattr(st.session_state, 'demo_query'):
            query = st.session_state.demo_query
            st.session_state.main_query = query
            delattr(st.session_state, 'demo_query')
    
    with col2:
        st.markdown("### 📎 Upload Files")
        uploaded_files = st.file_uploader(
            "Upload documents, images, or audio:",
            accept_multiple_files=True,
            type=['pdf', 'doc', 'docx', 'png', 'jpg', 'jpeg', 'mp3', 'wav']
        )
        
        if uploaded_files:
            st.session_state.uploaded_files = uploaded_files
            st.success(f"✅ {len(uploaded_files)} file(s) uploaded")
    
    # Search button
    if st.button("🔍 Search", type="primary", use_container_width=True):
        if query:
            # Add to recent queries
            if query not in st.session_state.recent_queries:
                st.session_state.recent_queries.append(query)
            
            # Simulate processing
            simulate_processing()
            
            # Get demo results
            results = []
            query_lower = query.lower()
            
            # Check for specific keywords to match demo scenarios
            if any(word in query_lower for word in ["financial", "revenue", "quarterly", "earnings"]):
                results = DEMO_RESULTS["financial report"]
            elif any(word in query_lower for word in ["product", "specification", "processor", "architecture", "benchmark"]):
                results = DEMO_RESULTS["product specifications"]
            elif any(word in query_lower for word in ["market", "analysis", "trend", "growth", "industry"]):
                results = DEMO_RESULTS["market analysis"]
            elif any(word in query_lower for word in ["research", "paper", "model", "multimodal", "learning"]):
                results = DEMO_RESULTS["research paper"]
            else:
                # Default to financial report for any other query
                results = DEMO_RESULTS["financial report"]
            
            st.session_state.search_results = results
    
    # Display results
    if st.session_state.search_results:
        display_search_results(st.session_state.search_results)
        
        # Show citation modals for clicked citations
        for result in st.session_state.search_results:
            for citation_num in result['citations']:
                if st.button(f"View Citation [{citation_num}]", key=f"cite_{citation_num}"):
                    show_citation_modal(citation_num)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem;">
        <p><strong>Multimodal RAG System</strong> - SIH 2025 Prototype</p>
        <p>Built with Streamlit • Powered by Offline AI Models</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
