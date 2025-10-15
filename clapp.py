import streamlit as st
import time
import base64
from datetime import datetime

# Page config
st.set_page_config(
    page_title="IntelliSearch - SIH 2025",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for research-oriented styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #1e3a8a 0%, #3730a3 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
        font-family: 'Times New Roman', serif;
    }
    .research-paper {
        background: #1f2937;
        padding: 2rem;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        margin-bottom: 2rem;
        border-left: 4px solid #1e3a8a;
        font-family: 'Times New Roman', serif;
        line-height: 1.8;
        color: #f9fafb;
    }
    .llm-response {
        background: #1f2937;
        padding: 2rem;
        border-radius: 8px;
        border: 1px solid #374151;
        margin-bottom: 2rem;
        font-family: 'Georgia', serif;
        line-height: 1.7;
        color: #f9fafb;
    }
    .response-header {
        display: flex;
        align-items: center;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #374151;
    }
    .ai-avatar {
        width: 32px;
        height: 32px;
        background: linear-gradient(135deg, #1e3a8a 0%, #3730a3 100%);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
        margin-right: 0.75rem;
    }
    .footnote-section {
        background: #374151;
        padding: 1.5rem;
        border-radius: 8px;
        margin-top: 2rem;
        border-left: 4px solid #64748b;
    }
    .footnote-item {
        margin-bottom: 1rem;
        padding: 0.75rem;
        background: #1f2937;
        border-radius: 4px;
        border-left: 3px solid #1e3a8a;
        color: #f9fafb;
    }
    .citation-badge {
        display: inline-block;
        background: #1e3a8a;
        color: white;
        padding: 0.2rem 0.5rem;
        border-radius: 3px;
        font-size: 0.8rem;
        margin: 0 0.1rem;
        cursor: pointer;
        font-weight: 600;
        text-decoration: none;
        vertical-align: super;
    }
    .citation-badge:hover {
        background: #3730a3;
        text-decoration: none;
        color: white;
    }
    .highlight {
        background: #fef3c7;
        padding: 0.1rem 0.3rem;
        border-radius: 3px;
        font-weight: 500;
        color: #92400e;
    }
    .sidebar-query {
        padding: 0.75rem;
        margin: 0.5rem 0;
        background: #374151;
        border-radius: 6px;
        border-left: 3px solid #1e3a8a;
        cursor: pointer;
        transition: all 0.2s ease;
        color: white;
    }
    .sidebar-query:hover {
        background: #4b5563;
        transform: translateX(2px);
    }
    .query-timestamp {
        font-size: 0.75rem;
        color: #9ca3af;
        margin-top: 0.25rem;
    }
    .result-card {
        background: #1f2937;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
        margin-bottom: 1rem;
        border-left: 4px solid #1e3a8a;
        color: white;
    }
    .media-thumbnail {
        border-radius: 8px;
        border: 2px solid #374151;
        padding: 1rem;
        margin: 0.5rem 0;
        background: linear-gradient(135deg, #374151 0%, #1f2937 100%);
        min-height: 150px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
    }
    .content-box {
        background: #374151;
        padding: 1rem;
        border-radius: 6px;
        margin: 0.5rem 0;
        line-height: 1.6;
        color: #f9fafb;
        border-left: 3px solid #1e3a8a;
    }
    .match-badge {
        background: #059669;
        color: white;
        padding: 0.3rem 0.7rem;
        border-radius: 15px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    .page-info {
        color: #9ca3af;
        font-size: 0.9rem;
        margin: 0.5rem 0;
        font-style: italic;
    }
    .audio-transcript {
        background: #374151;
        padding: 1rem;
        border-radius: 6px;
        border-left: 3px solid #1e3a8a;
        font-style: italic;
        margin: 0.5rem 0;
        color: #f9fafb;
    }
    .research-title {
        font-size: 1.5rem;
        font-weight: bold;
        color: #1e3a8a;
        margin-bottom: 0.5rem;
        font-family: 'Times New Roman', serif;
    }
    .research-subtitle {
        font-size: 1rem;
        color: #64748b;
        margin-bottom: 1rem;
        font-style: italic;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'search_done' not in st.session_state:
    st.session_state.search_done = False
if 'query' not in st.session_state:
    st.session_state.query = ""
if 'show_citation' not in st.session_state:
    st.session_state.show_citation = None
if 'selected_sidebar_query' not in st.session_state:
    st.session_state.selected_sidebar_query = None
if 'recent_queries' not in st.session_state:
    st.session_state.recent_queries = [
        {"query": "Revenue analysis Q4", "timestamp": "2 hours ago", "results": 5},
        {"query": "Product roadmap 2025", "timestamp": "1 day ago", "results": 8},
        {"query": "Customer feedback summary", "timestamp": "3 days ago", "results": 12},
        {"query": "Market research findings", "timestamp": "1 week ago", "results": 15}
    ]

# Mock data for demo
MOCK_RESULTS = {
    "text": [
        {
            "id": 1,
            "content": "The quarterly financial report indicates a 23% increase in revenue compared to Q3 2024. Operating expenses remained stable at 15.2 million, while net profit margins improved to 18.5%. The growth was primarily driven by expanded market presence in Southeast Asian regions.",
            "source": "Q4_Financial_Report_2024.pdf",
            "page": 12,
            "relevance": 0.94
        },
        {
            "id": 2,
            "content": "Market analysis shows strong consumer demand for sustainable products, with 67% of surveyed customers indicating willingness to pay premium prices for eco-friendly alternatives. This trend aligns with our strategic pivot towards green technology solutions.",
            "source": "Market_Research_Summary.docx",
            "page": 5,
            "relevance": 0.89
        }
    ],
    "images": [
        {
            "id": 3,
            "description": "Revenue growth chart showing Q1-Q4 2024 performance metrics with projections for 2025",
            "source": "Financial_Presentation.png",
            "page": 1,
            "relevance": 0.92
        },
        {
            "id": 4,
            "description": "Product roadmap diagram illustrating development timeline and key milestones",
            "source": "Strategy_Document.jpg",
            "page": 1,
            "relevance": 0.85
        }
    ],
    "audio": [
        {
            "id": 5,
            "transcript": "In today's board meeting, we discussed the expansion strategy for Q1 2025. The CEO emphasized focusing on customer retention while exploring new market segments. We're allocating 2.5 million for R&D initiatives and expect to launch three new products by March.",
            "source": "Board_Meeting_Jan2025.mp3",
            "duration": "2:45",
            "relevance": 0.87
        }
    ]
}

CITATION_DETAILS = {
    1: {
        "type": "PDF Document",
        "title": "Q4 Financial Report 2024",
        "author": "Finance Department",
        "date": "December 31, 2024",
        "context": "This report provides comprehensive analysis of company financial performance including revenue streams, expense management, and profit margins across all business units."
    },
    2: {
        "type": "Word Document",
        "title": "Market Research Summary",
        "author": "Marketing Analytics Team",
        "date": "January 15, 2025",
        "context": "Consumer behavior study conducted across 5,000 participants examining purchasing patterns and sustainability preferences in technology sector."
    },
    3: {
        "type": "PNG Image",
        "title": "Revenue Growth Chart",
        "author": "CFO Office",
        "date": "December 31, 2024",
        "context": "Visual representation of quarterly revenue trends with comparative analysis against industry benchmarks and forecast models."
    },
    4: {
        "type": "PNG Image",
        "title": "Product Roadmap",
        "author": "Product Management",
        "date": "January 10, 2025",
        "context": "Strategic planning document outlining product development phases, resource allocation, and go-to-market timelines for upcoming releases."
    },
    5: {
        "type": "Audio Recording",
        "title": "Board Meeting Recording",
        "author": "Executive Team",
        "date": "January 8, 2025",
        "context": "Full recording of monthly board meeting discussing strategic initiatives, financial performance review, and key decision points for Q1 2025."
    }
}

# Mock LLM responses for different queries
LLM_RESPONSES = {
    "Revenue analysis Q4": {
        "response": """Based on the comprehensive analysis of Q4 2024 financial data, the company has demonstrated remarkable growth across multiple key performance indicators. The quarterly financial report reveals a substantial 23% increase in revenue compared to Q3 2024, which significantly exceeds industry benchmarks and internal projections.<sup><a href="#footnote-1" class="citation-badge">1</a></sup>

This growth trajectory is particularly noteworthy when considering the broader market context. The revenue expansion was primarily driven by strategic market penetration in Southeast Asian regions, where the company has successfully capitalized on emerging opportunities.<sup><a href="#footnote-1" class="citation-badge">1</a></sup> The operating expenses remained remarkably stable at 15.2 million, indicating efficient cost management practices that have been maintained despite the significant revenue growth.

The net profit margins improved to 18.5%, representing a substantial enhancement in operational efficiency. This improvement suggests that the company's strategic initiatives, including the focus on sustainable products and green technology solutions, are yielding positive financial returns.<sup><a href="#footnote-2" class="citation-badge">2</a></sup>

From a strategic perspective, the board meeting discussions indicate that the company is well-positioned for continued growth in Q1 2025, with 2.5 million allocated for R&D initiatives and plans to launch three new products by March.<sup><a href="#footnote-5" class="citation-badge">5</a></sup>""",
        "footnotes": [1, 2, 5]
    },
    "Product roadmap 2025": {
        "response": """The 2025 product roadmap presents a comprehensive strategic vision that aligns with both market demands and the company's commitment to sustainable innovation. The roadmap illustrates a carefully planned development timeline with key milestones that position the company for continued market leadership.<sup><a href="#footnote-4" class="citation-badge">4</a></sup>

The strategic planning document reveals a multi-phase approach to product development, with particular emphasis on green technology solutions. This focus is well-aligned with market research findings that show 67% of surveyed customers are willing to pay premium prices for eco-friendly alternatives.<sup><a href="#footnote-2" class="citation-badge">2</a></sup>

The resource allocation strategy demonstrates prudent financial management, with significant investment in R&D initiatives that support the product development pipeline. The board meeting discussions confirm the allocation of 2.5 million for R&D, with expectations of launching three new products by March 2025.<sup><a href="#footnote-5" class="citation-badge">5</a></sup>

The go-to-market timelines outlined in the roadmap suggest a systematic approach to product launches, ensuring that each release is supported by adequate market research and customer feedback integration. This methodology has proven successful in previous quarters and is expected to drive continued revenue growth.<sup><a href="#footnote-1" class="citation-badge">1</a></sup>""",
        "footnotes": [4, 2, 5, 1]
    },
    "Customer feedback summary": {
        "response": """The customer feedback analysis reveals significant insights into consumer behavior and preferences that directly inform strategic decision-making. The comprehensive study of customer sentiment demonstrates a clear trend toward sustainability-focused purchasing decisions, with 67% of participants indicating willingness to pay premium prices for eco-friendly alternatives.<sup><a href="#footnote-2" class="citation-badge">2</a></sup>

This consumer behavior pattern aligns perfectly with the company's strategic pivot toward green technology solutions, suggesting that the market is receptive to sustainable product offerings. The feedback data provides strong validation for the product roadmap initiatives planned for 2025.<sup><a href="#footnote-4" class="citation-badge">4</a></sup>

The analysis also reveals important insights about customer retention strategies, which were emphasized in the recent board meeting discussions. The CEO's focus on customer retention while exploring new market segments appears to be well-supported by the feedback data.<sup><a href="#footnote-5" class="citation-badge">5</a></sup>

These findings have significant implications for revenue growth strategies, particularly given the 23% increase in Q4 2024 revenue. The customer feedback suggests that the company's current approach to market expansion and product development is resonating well with target demographics.<sup><a href="#footnote-1" class="citation-badge">1</a></sup>""",
        "footnotes": [2, 4, 5, 1]
    },
    "Market research findings": {
        "response": """The market research findings provide compelling evidence of shifting consumer preferences and emerging opportunities in the technology sector. The study, conducted across 5,000 participants, reveals a strong consumer demand for sustainable products that aligns with broader environmental consciousness trends.<sup><a href="#footnote-2" class="citation-badge">2</a></sup>

The research demonstrates that 67% of surveyed customers are willing to pay premium prices for eco-friendly alternatives, indicating a significant market opportunity for companies that can effectively position themselves in the sustainability space. This finding directly supports the company's strategic initiatives in green technology solutions.<sup><a href="#footnote-2" class="citation-badge">2</a></sup>

The market analysis also provides valuable insights into the Southeast Asian market expansion that has contributed to the 23% revenue increase in Q4 2024. The research suggests that these regions present continued growth opportunities, particularly for sustainable technology products.<sup><a href="#footnote-1" class="citation-badge">1</a></sup>

These findings have informed the strategic planning outlined in the 2025 product roadmap, ensuring that market research insights are directly integrated into product development and go-to-market strategies.<sup><a href="#footnote-4" class="citation-badge">4</a></sup> The board meeting discussions reflect this integration, with strategic initiatives focused on capitalizing on identified market opportunities.<sup><a href="#footnote-5" class="citation-badge">5</a></sup>""",
        "footnotes": [2, 1, 4, 5]
    }
}

def show_landing_page():
    st.markdown("""
    <div class="main-header">
        <h1>IntelliSearch</h1>
        <p style="font-size: 1.2rem; margin: 0;">Advanced Research Intelligence Platform</p>
        <p style="font-size: 0.9rem; margin-top: 0.5rem; opacity: 0.9;">Multimodal Retrieval-Augmented Generation</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    
    # Main query section
    st.markdown("###  Search Across All Your Content")
    query = st.text_input(
        "Enter your query",
        placeholder="e.g., Show me the sales analysis of 2024...",
        label_visibility="collapsed"
    )
    
    # Upload section
    st.markdown("####  Upload New Content (Optional)")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        pdf_file = st.file_uploader(" PDF/DOC", type=['pdf', 'doc', 'docx'], key="pdf")
    with col2:
        img_file = st.file_uploader(" Images", type=['png', 'jpg', 'jpeg'], key="img")
    with col3:
        audio_file = st.file_uploader(" Audio", type=['mp3', 'wav', 'ogg'], key="audio")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    
    # Search button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Search", use_container_width=True, type="primary"):
            if query or pdf_file or img_file or audio_file:
                st.session_state.query = query if query else "Uploaded content analysis"
                st.session_state.selected_sidebar_query = None  # Clear sidebar selection for new queries
                st.session_state.search_done = True
                st.rerun()
            else:
                st.warning("Please enter a query or upload files to search!")

    # Add Recent Queries Section on Landing Page
    st.markdown("###  Recent Queries")
    cols = st.columns(2)
    for i, recent_query in enumerate(st.session_state.recent_queries):
        with cols[i % 2]:
            if st.button(
                f" {recent_query['query']}\n{recent_query['timestamp']}  {recent_query['results']} results", 
                key=f"landing_query_{i}", 
                use_container_width=True
            ):
                st.session_state.query = recent_query['query']
                st.session_state.selected_sidebar_query = recent_query['query']
                st.session_state.search_done = True
                st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)

def show_loading_animation():
    with st.spinner(''):
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        stages = [
            "Analyzing query semantics...",
            "Generating embeddings...",
            "Searching vector database...",
            "Processing multimodal content...",
            "Ranking results by relevance...",
            "Preparing citations..."
        ]
        
        for i, stage in enumerate(stages):
            status_text.text(stage)
            progress_bar.progress((i + 1) / len(stages))
            time.sleep(3)
        
        progress_bar.empty()
        status_text.empty()

def show_llm_response(query):
    """Display LLM-style response with citations"""
    if query in LLM_RESPONSES:
        response_data = LLM_RESPONSES[query]
        
        st.markdown("""
        <div class="llm-response">
            <div class="response-header">
                <div class="ai-avatar">AI</div>
                <div>
                    <h3 style="margin: 0; color: #f9fafb;">Research Analysis</h3>
                    <p style="margin: 0; color: #9ca3af; font-size: 0.9rem;">Generated by IntelliSearch</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="llm-response">
            {response_data['response']}
        </div>
        """, unsafe_allow_html=True)
        
        # Display footnotes
        if response_data['footnotes']:
            st.markdown("""
            <div class="footnote-section">
                <h4 style="color: #f9fafb; margin-bottom: 1rem;">References</h4>
            </div>
            """, unsafe_allow_html=True)
            
            for footnote_id in response_data['footnotes']:
                if footnote_id in CITATION_DETAILS:
                    details = CITATION_DETAILS[footnote_id]
                    st.markdown(f"""
                    <div class="footnote-item">
                        <p style="margin: 0;"><strong>[{footnote_id}]</strong> {details['title']}</p>
                        <p style="margin: 0.25rem 0; color: #64748b; font-size: 0.9rem;">
                            {details['type']}  {details['author']}  {details['date']}
                        </p>
                        <p style="margin: 0; color: #64748b; font-size: 0.85rem; font-style: italic;">
                            {details['context']}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)

def show_citation_modal(citation_id):
    if citation_id in CITATION_DETAILS:
        details = CITATION_DETAILS[citation_id]
        
        st.markdown(f"""
        <div style="background: #1f2937; padding: 1.5rem; border-radius: 10px; border-left: 4px solid #1e3a8a; margin-top: 1rem;">
            <h4 style="color: #60a5fa;"> Citation [{citation_id}] Details</h4>
            <p style="color: #f9fafb;"><strong>Type:</strong> {details['type']}</p>
            <p style="color: #f9fafb;"><strong>Title:</strong> {details['title']}</p>
            <p style="color: #f9fafb;"><strong>Author:</strong> {details['author']}</p>
            <p style="color: #f9fafb;"><strong>Date:</strong> {details['date']}</p>
            <p style="color: #f9fafb;"><strong>Context:</strong> {details['context']}</p>
        </div>
        """, unsafe_allow_html=True)

def show_results():
    # Check if a sidebar query was selected
    if st.session_state.selected_sidebar_query:
        query_to_show = st.session_state.selected_sidebar_query
    else:
        query_to_show = st.session_state.query

    # If the query is not in our predefined responses, use a default one
    if query_to_show not in LLM_RESPONSES:
        # Use the first available response as default
        query_to_show = list(LLM_RESPONSES.keys())[0]
    
    st.markdown(f"""
    <div class="main-header">
        <h1>Research Analysis</h1>
        <p style="font-size: 1.5rem; margin: 0.5rem 0 0 0;">Query: "{query_to_show}"</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Show loading animation
    show_loading_animation()
    
    # Display LLM response first
    show_llm_response(query_to_show)
    
    st.success(f" Found {len(MOCK_RESULTS['text']) + len(MOCK_RESULTS['images']) + len(MOCK_RESULTS['audio'])} supporting documents across all modalities")
    
    # Sidebar for filters and recent queries
    with st.sidebar:
        st.markdown("###  Filters")
        show_text = st.checkbox(" Text Documents", value=True)
        show_images = st.checkbox(" Images", value=True)
        show_audio = st.checkbox(" Audio", value=True)
        
        st.markdown("###  Relevance Threshold")
        relevance = st.slider("Minimum Score", 0.0, 1.0, 0.8)
        
        st.markdown("###  Recent Queries")
        for i, recent_query in enumerate(st.session_state.recent_queries):
            if st.button(f" {recent_query['query']}\n{recent_query['timestamp']}  {recent_query['results']} results", 
                        key=f"sidebar_query_{i}", use_container_width=True):
                st.session_state.selected_sidebar_query = recent_query['query']
                st.rerun()
    
    # Text results
    if show_text:
        st.markdown("##  Supporting Documents")
        for result in MOCK_RESULTS['text']:
            if result['relevance'] >= relevance:
                # Highlight keywords in content
                highlighted_content = result['content'].replace(
                    "quarterly financial report",
                    '<span class="highlight">quarterly financial report</span>'
                ).replace(
                    "23% increase in revenue",
                    '<span class="highlight">23% increase in revenue</span>'
                ).replace(
                    "Market analysis",
                    '<span class="highlight">Market analysis</span>'
                ).replace(
                    "sustainable products",
                    '<span class="highlight">sustainable products</span>'
                )
                
                with st.container():
                    # Create a custom container with proper styling
                    st.markdown(f"""
                    <div class="result-card">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                            <h4 style="margin: 0; color: #60a5fa;">{result['source']}</h4>
                            <span class="match-badge">{result["relevance"]*100:.0f}% match</span>
                        </div>
                        <p class="page-info">Page {result["page"]}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Content box using Streamlit components
                    st.markdown(f"""
                    <div class="content-box">{highlighted_content}</div>
                    """, unsafe_allow_html=True)
                    
                    # Citation and button row
                    col1, col2 = st.columns([1, 5])
                    with col1:
                        st.markdown(f'<span class="citation-badge">[{result["id"]}]</span>', unsafe_allow_html=True)
                    with col2:
                        if st.button(f"View Citation Details", key=f"cite_{result['id']}"):
                            show_citation_modal(result['id'])
    
    # Image results
    if show_images:
        st.markdown("##  Visual Data")
        cols = st.columns(2)
        for idx, result in enumerate(MOCK_RESULTS['images']):
            if result['relevance'] >= relevance:
                with cols[idx % 2]:
                    # Header with title and match badge
                    st.markdown(f"""
                    <div class="result-card">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                            <h4 style="margin: 0; color: #60a5fa;">{result['source']}</h4>
                            <span class="match-badge">{result["relevance"]*100:.0f}% match</span>
                        </div>
                        <p class="page-info">Page {result["page"]}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Media thumbnail
                    # Replace the media thumbnail section with actual image display
                    #if result.get('image_path'):
                        # If you have actual image files
                        #st.image(result['image_path'], use_container_width=True)
                    # Replace the media thumbnail section with actual image display
                    if result['id'] == 3:
                        st.image("Q4 Revenue Table.jpg", use_container_width=True)
                    elif result['id'] == 4:
                        st.image("Q4_Rev Analysis.jpg", use_container_width=True)
                    else:
                        # For demo purposes with placeholder
                        st.markdown(f"""
                        <div class="media-thumbnail">
                            <div style="text-align: center;">
                                <p style="color: #60a5fa; font-weight: bold; font-size: 1.1rem; margin-bottom: 0.5rem;">📊 Chart Visualization</p>
                                <p style="color: #9ca3af; font-size: 0.9rem;">{result["description"]}</p>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Description content
                    st.markdown(f"""
                    <div class="content-box">{result["description"]}</div>
                    """, unsafe_allow_html=True)
                    
                    # Citation and button
                    col1, col2 = st.columns([1, 5])
                    with col1:
                        st.markdown(f'<span class="citation-badge">[{result["id"]}]</span>', unsafe_allow_html=True)
                    with col2:
                        if st.button(f"View Details", key=f"img_{result['id']}"):
                            show_citation_modal(result['id'])
    
    # Audio results
    if show_audio:
        st.markdown("##  Audio Recordings")
        for result in MOCK_RESULTS['audio']:
            if result['relevance'] >= relevance:
                # Header with title and match badge
                st.markdown(f"""
                <div class="result-card">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                        <h4 style="margin: 0; color: #60a5fa;">{result['source']}</h4>
                        <span class="match-badge">{result["relevance"]*100:.0f}% match</span>
                    </div>
                    <p class="page-info">Duration: {result["duration"]}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Audio transcript
                st.markdown(f"""
                <div class="audio-transcript">
                    <strong> Transcript:</strong><br>
                    {result["transcript"]}
                </div>
                """, unsafe_allow_html=True)
                
                # Action buttons
                col1, col2, col3 = st.columns([1, 1, 4])
                with col1:
                    st.button(" Play Audio", key=f"play_{result['id']}")
                with col2:
                    st.markdown(f'<span class="citation-badge">[{result["id"]}]</span>', unsafe_allow_html=True)
                with col3:
                    if st.button(f"View Full Transcript", key=f"audio_{result['id']}"):
                        show_citation_modal(result['id'])
    
    # New search button
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button(" New Research Query", use_container_width=True, type="primary"):
            st.session_state.search_done = False
            st.session_state.query = ""
            st.session_state.selected_sidebar_query = None
            st.rerun()

# Main app logic
if not st.session_state.search_done:
    show_landing_page()
else:
    show_results()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; padding: 1rem; font-family: 'Times New Roman', serif;">
    <p style="font-size: 0.9rem; margin: 0.5rem 0;">IntelliSearch Research Platform | SIH 2025 Project</p>
    <p style="font-size: 0.8rem; margin: 0;">Research - Grade Analysis 100% Offline & Secure</p>
</div>
""", unsafe_allow_html=True)