# Demo Assets and Data for Multimodal RAG System

import json
import base64
from PIL import Image, ImageDraw, ImageFont
import io

# Extended demo results with more variety
EXTENDED_DEMO_RESULTS = {
    "financial report": [
        {
            "type": "text",
            "content": "The quarterly revenue increased by 23% compared to the previous quarter, reaching $2.4M in total sales. This growth was primarily driven by increased demand in the enterprise segment.",
            "source": "Q3_Financial_Report.pdf",
            "page": 12,
            "confidence": 0.94,
            "citations": [1, 2],
            "highlighted_text": "quarterly revenue increased by 23%"
        },
        {
            "type": "image",
            "content": "Revenue Growth Chart",
            "source": "Q3_Financial_Report.pdf",
            "page": 13,
            "confidence": 0.89,
            "citations": [3],
            "description": "Bar chart showing quarterly revenue growth with Q3 showing highest growth"
        },
        {
            "type": "audio",
            "content": "CEO discussing quarterly performance",
            "source": "Q3_Earnings_Call.mp3",
            "timestamp": "12:34",
            "confidence": 0.91,
            "citations": [4],
            "transcript": "We're pleased to report strong growth this quarter..."
        }
    ],
    "product specifications": [
        {
            "type": "text",
            "content": "The new AI processor features 128 cores with 512GB unified memory, supporting up to 8TB/s memory bandwidth. Power consumption is optimized to 250W under full load.",
            "source": "Product_Specs_v2.1.pdf",
            "page": 5,
            "confidence": 0.96,
            "citations": [5],
            "highlighted_text": "128 cores with 512GB unified memory"
        },
        {
            "type": "image",
            "content": "Processor Architecture Diagram",
            "source": "Product_Specs_v2.1.pdf",
            "page": 6,
            "confidence": 0.92,
            "citations": [6],
            "description": "Detailed architecture diagram showing core layout and memory hierarchy"
        },
        {
            "type": "text",
            "content": "Benchmark results show 40% improvement over previous generation in machine learning workloads, with particular strength in transformer model inference.",
            "source": "Benchmark_Results.pdf",
            "page": 8,
            "confidence": 0.88,
            "citations": [7],
            "highlighted_text": "40% improvement over previous generation"
        }
    ],
    "market analysis": [
        {
            "type": "text",
            "content": "Market research indicates a 35% year-over-year growth in AI infrastructure spending, with cloud providers leading adoption. Edge computing shows promising 45% growth trajectory.",
            "source": "Market_Analysis_2024.pdf",
            "page": 3,
            "confidence": 0.93,
            "citations": [8],
            "highlighted_text": "35% year-over-year growth in AI infrastructure"
        },
        {
            "type": "image",
            "content": "Market Growth Trends Chart",
            "source": "Market_Analysis_2024.pdf",
            "page": 4,
            "confidence": 0.90,
            "citations": [9],
            "description": "Line chart showing market growth trends across different sectors"
        },
        {
            "type": "audio",
            "content": "Industry expert interview on market trends",
            "source": "Expert_Interview.mp3",
            "timestamp": "8:45",
            "confidence": 0.87,
            "citations": [10],
            "transcript": "The AI market is experiencing unprecedented growth..."
        }
    ],
    "research paper": [
        {
            "type": "text",
            "content": "Our novel approach achieves state-of-the-art performance on multimodal understanding tasks, with 15% improvement over existing methods. The architecture combines vision transformers with language models.",
            "source": "Research_Paper_2024.pdf",
            "page": 7,
            "confidence": 0.95,
            "citations": [11],
            "highlighted_text": "15% improvement over existing methods"
        },
        {
            "type": "image",
            "content": "Model Architecture Diagram",
            "source": "Research_Paper_2024.pdf",
            "page": 8,
            "confidence": 0.91,
            "citations": [12],
            "description": "Architecture diagram showing vision transformer and language model integration"
        },
        {
            "type": "text",
            "content": "Experimental results demonstrate superior performance across multiple benchmarks including VQA, image captioning, and multimodal retrieval tasks.",
            "source": "Research_Paper_2024.pdf",
            "page": 12,
            "confidence": 0.89,
            "citations": [13],
            "highlighted_text": "superior performance across multiple benchmarks"
        }
    ]
}

# Extended citation data
EXTENDED_CITATION_DATA = {
    1: {
        "type": "document", 
        "title": "Q3 Financial Report", 
        "content": "Complete quarterly financial analysis including revenue breakdown, cost analysis, and growth projections.",
        "metadata": {"pages": 45, "date": "2024-10-15", "author": "Finance Team"}
    },
    2: {
        "type": "document", 
        "title": "Revenue Analysis", 
        "content": "Detailed revenue analysis showing enterprise segment growth of 28% and consumer segment growth of 18%.",
        "metadata": {"pages": 12, "date": "2024-10-20", "author": "Analytics Team"}
    },
    3: {
        "type": "image", 
        "title": "Revenue Growth Chart", 
        "content": "Interactive chart showing quarterly revenue trends with breakdown by product category and geographic region.",
        "metadata": {"resolution": "1920x1080", "format": "PNG", "created": "2024-10-15"}
    },
    4: {
        "type": "audio", 
        "title": "Q3 Earnings Call", 
        "content": "Full earnings call transcript with CEO discussing quarterly performance, market outlook, and strategic initiatives.",
        "metadata": {"duration": "45:30", "format": "MP3", "date": "2024-10-15"}
    },
    5: {
        "type": "document", 
        "title": "Product Specifications", 
        "content": "Complete technical specifications including architecture details, performance metrics, and compatibility information.",
        "metadata": {"pages": 67, "version": "v2.1", "date": "2024-09-30"}
    },
    6: {
        "type": "image", 
        "title": "Architecture Diagram", 
        "content": "Detailed processor architecture diagram showing core layout, memory hierarchy, and interconnect topology.",
        "metadata": {"resolution": "2560x1440", "format": "SVG", "created": "2024-09-30"}
    },
    7: {
        "type": "document", 
        "title": "Benchmark Results", 
        "content": "Comprehensive benchmark testing results across various workloads including ML, HPC, and general computing tasks.",
        "metadata": {"pages": 23, "date": "2024-10-01", "author": "Performance Team"}
    },
    8: {
        "type": "document", 
        "title": "Market Analysis", 
        "content": "Industry market analysis covering trends, growth projections, and competitive landscape assessment.",
        "metadata": {"pages": 89, "date": "2024-10-10", "author": "Market Research Team"}
    },
    9: {
        "type": "image", 
        "title": "Growth Trends", 
        "content": "Visual representation of market growth trends with regional breakdown and sector analysis.",
        "metadata": {"resolution": "1920x1080", "format": "PNG", "created": "2024-10-10"}
    },
    10: {
        "type": "audio", 
        "title": "Expert Interview", 
        "content": "Interview transcript with industry expert discussing market dynamics, challenges, and future opportunities.",
        "metadata": {"duration": "32:15", "format": "MP3", "date": "2024-10-12"}
    },
    11: {
        "type": "document", 
        "title": "Research Paper", 
        "content": "Novel multimodal architecture combining vision transformers with language models for improved understanding tasks.",
        "metadata": {"pages": 15, "conference": "NeurIPS 2024", "authors": "Smith et al."}
    },
    12: {
        "type": "image", 
        "title": "Model Architecture", 
        "content": "Detailed diagram showing the integration of vision transformers with language models in the proposed architecture.",
        "metadata": {"resolution": "2048x1536", "format": "PNG", "created": "2024-11-01"}
    },
    13: {
        "type": "document", 
        "title": "Experimental Results", 
        "content": "Comprehensive experimental evaluation across multiple benchmarks demonstrating superior performance.",
        "metadata": {"pages": 8, "section": "Results", "date": "2024-11-01"}
    }
}

def create_demo_chart_image(width=400, height=300, chart_type="bar"):
    """Create a demo chart image"""
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    
    # Draw a simple bar chart
    if chart_type == "bar":
        bars = [60, 80, 95, 120, 110]
        bar_width = width // len(bars) - 10
        bar_height_unit = height // max(bars)
        
        for i, bar_height in enumerate(bars):
            x1 = i * (bar_width + 10) + 20
            y1 = height - (bar_height * bar_height_unit) - 20
            x2 = x1 + bar_width
            y2 = height - 20
            
            # Color bars with gradient
            color = (100 + i * 30, 150 + i * 20, 200 + i * 10)
            draw.rectangle([x1, y1, x2, y2], fill=color)
            
            # Add value labels
            draw.text((x1 + bar_width//2 - 10, y1 - 20), str(bar_height), fill='black')
    
    # Add title
    draw.text((width//2 - 50, 10), "Demo Chart", fill='black')
    
    return img

def create_demo_diagram_image(width=400, height=300):
    """Create a demo architecture diagram"""
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    
    # Draw boxes and connections
    boxes = [
        {"x": 50, "y": 50, "w": 80, "h": 40, "text": "Input"},
        {"x": 150, "y": 50, "w": 80, "h": 40, "text": "Process"},
        {"x": 250, "y": 50, "w": 80, "h": 40, "text": "Output"},
        {"x": 100, "y": 150, "w": 80, "h": 40, "text": "Memory"},
        {"x": 200, "y": 150, "w": 80, "h": 40, "text": "Cache"}
    ]
    
    for box in boxes:
        draw.rectangle([box["x"], box["y"], box["x"] + box["w"], box["y"] + box["h"]], 
                      outline='blue', width=2)
        draw.text((box["x"] + 10, box["y"] + 15), box["text"], fill='black')
    
    # Draw connections
    connections = [
        (90, 70, 150, 70),  # Input to Process
        (230, 70, 250, 70), # Process to Output
        (190, 90, 140, 150), # Process to Memory
        (190, 90, 200, 150)  # Process to Cache
    ]
    
    for x1, y1, x2, y2 in connections:
        draw.line([x1, y1, x2, y2], fill='red', width=2)
    
    return img

# Sample queries for demo
SAMPLE_QUERIES = [
    "Show me the financial performance for Q3",
    "What are the technical specifications of the new processor?",
    "Analyze the market trends for AI infrastructure",
    "Find research papers on multimodal learning",
    "Compare revenue growth across different segments",
    "Show me the architecture diagram for the AI model",
    "What did the CEO say about quarterly performance?",
    "Find benchmark results for machine learning workloads"
]

# System metrics for demo
SYSTEM_METRICS = {
    "documents_indexed": 1247,
    "images_processed": 3456,
    "audio_files_transcribed": 89,
    "total_queries": 15678,
    "average_response_time": "1.2s",
    "system_uptime": "99.9%"
}
