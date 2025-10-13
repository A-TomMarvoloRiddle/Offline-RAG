# Multimodal RAG System - SIH 2025 Prototype

A comprehensive offline Retrieval-Augmented Generation (RAG) system prototype designed to demonstrate multimodal search capabilities across text, images, and audio content.

## 🚀 Features

- **Unified Search Interface**: Single query box for searching across all media types
- **Multimodal Results**: Display text snippets, images, and audio clips with confidence scores
- **Live Citations**: Interactive citation system with detailed source information
- **Cross-modal Linking**: Connect related content across different media types
- **Realistic Demo Data**: Convincing placeholder content for demonstration purposes
- **Modern UI**: Clean, responsive interface built with Streamlit

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8 or higher
- 8GB+ RAM (as specified in requirements)
- Windows or Linux laptop

### Quick Start

1. **Clone or download the project files**
   ```bash
   # Ensure you have all files in a single directory:
   # - app.py
   # - demo_data.py
   # - requirements.txt
   # - README.md
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Open your browser**
   - The app will automatically open at `http://localhost:8501`
   - If it doesn't open automatically, navigate to the URL manually

## 🎯 Demo Workflow

### 1. Landing Page
- Clean branding with system overview
- Quick action buttons for common demo scenarios
- System status indicators

### 2. Search Interface
- **Text Query**: Enter natural language queries
- **File Upload**: Upload PDF, DOC, images, or audio files
- **Search Button**: Triggers processing simulation

### 3. Processing Simulation
- Realistic loading animation with progress steps
- Simulated AI processing stages:
  - Document analysis
  - Image processing with CLIP
  - Audio transcription with Whisper
  - Embedding generation
  - Semantic search
  - Result ranking

### 4. Results Display
- **Text Results**: Highlighted relevant snippets with confidence scores
- **Image Results**: Thumbnail previews with descriptions
- **Audio Results**: Audio clip indicators with timestamps
- **Citations**: Clickable citation numbers linking to source details

### 5. Citation System
- Modal-style citation details
- Source metadata and related content
- Cross-modal linking between related items

## 🎬 Demo Scenarios

### Scenario 1: Financial Report Analysis
1. Click "📊 Demo: Financial Report" in sidebar
2. Observe processing simulation
3. Review text, chart, and audio results
4. Click citations to see detailed sources

### Scenario 2: Product Specifications
1. Click "🔧 Demo: Product Specs" in sidebar
2. See technical specifications and architecture diagrams
3. Explore benchmark results and performance metrics

### Scenario 3: Market Analysis
1. Click "📈 Demo: Market Analysis" in sidebar
2. Review market trends and growth charts
3. Listen to expert interviews and analysis

### Scenario 4: Custom Query
1. Enter your own search query
2. Upload sample files (optional)
3. Experience the full search workflow

## 🔧 Technical Details

### Architecture
- **Frontend**: Streamlit with custom CSS styling
- **Backend**: Python with simulated AI processing
- **Data**: Hardcoded demo data for realistic results
- **Storage**: Session state for user interactions

### Key Components
- `app.py`: Main application with UI and logic
- `demo_data.py`: Extended demo data and helper functions
- `requirements.txt`: Python dependencies

### Customization
- Modify `DEMO_RESULTS` in `demo_data.py` for different scenarios
- Update `CITATION_DATA` for custom source information
- Adjust styling in the CSS section of `app.py`

## 📱 UI/UX Features

- **Responsive Design**: Works on different screen sizes
- **Loading Animations**: Realistic processing simulation
- **Interactive Elements**: Clickable citations and expandable sections
- **Visual Hierarchy**: Clear information organization
- **Professional Styling**: Modern gradient backgrounds and cards

## 🎥 Video Demo Tips

### For Presenters
1. **Start with Quick Actions**: Use sidebar buttons for instant demos
2. **Show Processing**: Let loading animations complete for realism
3. **Click Citations**: Demonstrate the citation system interactivity
4. **Upload Files**: Show file upload capability (even with dummy files)
5. **Cross-modal Results**: Highlight how different media types are connected

### Recording Setup
- Use full-screen browser window
- Ensure good lighting and clear audio
- Record at 1080p for best quality
- Keep cursor movements smooth and deliberate

## 🔍 System Capabilities (Simulated)

- **Document Processing**: PDF, DOC, DOCX support
- **Image Analysis**: PNG, JPG, JPEG with CLIP-like processing
- **Audio Transcription**: MP3, WAV with Whisper-like capabilities
- **Semantic Search**: Vector-based similarity search
- **Multimodal Fusion**: Cross-media content linking
- **Confidence Scoring**: Relevance ranking for results

## 📊 Performance Metrics (Demo)

- Documents Indexed: 1,247
- Images Processed: 3,456
- Audio Files Transcribed: 89
- Average Response Time: 1.2s
- System Uptime: 99.9%

## 🚀 Future Enhancements

This prototype demonstrates the core workflow. The real system would include:
- Actual AI model integration
- Real vector database
- Live document processing
- Advanced multimodal fusion
- User authentication and preferences
- API endpoints for integration

## 📞 Support

For questions or issues with the demo:
1. Check that all dependencies are installed correctly
2. Ensure Python 3.8+ is being used
3. Verify all files are in the same directory
4. Try refreshing the browser if the app doesn't load

## 🏆 SIH 2025

This prototype showcases the vision for an advanced multimodal RAG system that can revolutionize how users interact with diverse content types. The interface demonstrates seamless integration of text, image, and audio search capabilities with transparent citation and source tracking.

---

**Built with ❤️ for SIH 2025**
*Demonstrating the future of multimodal information retrieval*
