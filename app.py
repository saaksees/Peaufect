import streamlit as st
import utils.loader
from utils.vectorstore import build_vectorstore
from models.llm import build_qa_chain
import time
from datetime import datetime
import base64
import requests
from io import BytesIO

# -------------------------
# Page Config
# -------------------------
st.set_page_config(
    page_title="PEAUFECT: From Questions to Glow -- Peaufect knows!!",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="✨"
)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
if "conversation_count" not in st.session_state:
    st.session_state.conversation_count = 0

# Custom CSS for enhanced styling with animations
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: 700;
        font-family: 'Poppins', sans-serif;
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { text-shadow: 0 0 20px #667eea; }
        to { text-shadow: 0 0 30px #764ba2; }
    }
    
    .subtitle {
        text-align: center;
        color: #555;
        margin-bottom: 2rem;
        font-family: 'Poppins', sans-serif;
        font-size: 1.2rem;
        animation: fadeInUp 1s ease-out;
    }
    
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .hero-section {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        margin: 2rem 0;
        text-align: center;
        color: white;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .feature-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        color: white;
        text-align: center;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        transition: transform 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
    }
    
    .stats-container {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    }
    
    .suggestion-chip {
        display: inline-block;
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        color: #333;
        padding: 0.8rem 1.5rem;
        margin: 0.5rem;
        border-radius: 25px;
        border: none;
        cursor: pointer;
        font-size: 0.9rem;
        font-weight: 500;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .suggestion-chip:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    }
    
    .skin-concern-card {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    
    .skin-concern-card:hover {
        transform: scale(1.05);
    }
    
    .chat-message {
        animation: slideIn 0.5s ease-out;
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    .floating-elements {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: -1;
    }
    
    .floating-element {
        position: absolute;
        font-size: 2rem;
        animation: float 6s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
    }
</style>
""", unsafe_allow_html=True)

# Floating background elements
st.markdown("""
<div class="floating-elements">
    <div class="floating-element" style="top: 10%; left: 10%;">🌸</div>
    <div class="floating-element" style="top: 20%; right: 15%; animation-delay: -2s;">✨</div>
    <div class="floating-element" style="top: 60%; left: 5%; animation-delay: -4s;">🌿</div>
    <div class="floating-element" style="top: 70%; right: 10%; animation-delay: -1s;">💧</div>
    <div class="floating-element" style="top: 40%; right: 20%; animation-delay: -3s;">🌙</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">✨ PEAUFECT: From Questions to Glow</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Peaufect knows!! Your AI-powered skincare companion for personalized beauty solutions</p>', unsafe_allow_html=True)

# Hero Section with Images
st.markdown("""
<div class="hero-section">
    <h2>🌟 Welcome to Your Personal Skincare Journey</h2>
    <p>Discover the perfect skincare routine tailored just for you with AI-powered recommendations</p>
</div>
""", unsafe_allow_html=True)

# Feature highlights with icons
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("""
    <div class="feature-card">
        <h3>🎯</h3>
        <h4>Personalized</h4>
        <p>Tailored advice for your skin type</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <h3>💰</h3>
        <h4>Budget-Friendly</h4>
        <p>Options for every budget range</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <h3>🧪</h3>
        <h4>Science-Based</h4>
        <p>Evidence-backed recommendations</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="feature-card">
        <h3>🌿</h3>
        <h4>Natural & Safe</h4>
        <p>Gentle ingredients for all skin types</p>
    </div>
    """, unsafe_allow_html=True)

# -------------------------
# Sidebar Controls
# -------------------------
with st.sidebar:
    st.header("⚙️ Settings")
    
    # User Profile Section
    st.subheader("👤 Your Profile")
    budget_pref = st.radio("💰 Budget Preference", ["Any", "Low (₹0-₹1,500)", "Mid (₹1,500-₹4,000)", "High (₹4,000+)"])
    skin_type = st.radio("🧴 Skin Type", ["Oily", "Dry", "Combination"])
    
    # Additional preferences
    st.subheader("🎯 Preferences")
    
    # Dynamic brand selection based on budget
    def get_brands_by_budget(budget):
        low_budget_brands = ["Any", "Himalaya", "Biotique", "Garnier", "Lakme", "Simple", "Neutrogena", "Olay", "WOW Skin Science", "Mamaearth", "Plum"]
        mid_budget_brands = ["Any", "Minimalist", "Dot&Key", "Hyphen", "Foxtale", "Nykaa", "Dermaco", "The Ordinary", "CeraVe", "Innisfree", "The Face Shop", "Tony & Tina", "Colorbar"]
        high_budget_brands = ["Any", "Clinique", "Eucerin", "Forest Essentials", "Kama Ayurveda", "Loreal", "SK-II", "Estee Lauder", "Drunk Elephant", "Paula's Choice", "Tatcha", "La Mer"]
        
        if "Low" in budget:
            return low_budget_brands
        elif "Mid" in budget:
            return mid_budget_brands
        elif "High" in budget:
            return high_budget_brands
        else:  # Any budget
            return sorted(list(set(low_budget_brands + mid_budget_brands + high_budget_brands)))
    
    available_brands = get_brands_by_budget(budget_pref)
    selected_brand = st.selectbox("Preferred Brand", available_brands, help=f"Brands filtered by your {budget_pref.lower()} budget preference")
    
    age_range = st.selectbox("Age Range", ["Any", "Teens (13-19)", "20s", "30s", "40s", "50+"])
    
    # Skin Type Tips with Images
    st.divider()
    st.subheader("💡 Quick Tips")
    
    skin_tips = {
        "Oily": {
            "tip": "Use oil-free, non-comedogenic products. Clay masks 2x/week help control excess oil.",
            "emoji": "💧",
            "color": "#b3e5fc",
            "text_color": "#01579b"
        },
        "Dry": {
            "tip": "Look for hyaluronic acid and ceramides. Avoid harsh cleansers and over-exfoliating.",
            "emoji": "🏜️",
            "color": "#ffcc80",
            "text_color": "#e65100"
        },
        "Combination": {
            "tip": "Use different products for T-zone and cheeks. Multi-masking can be very effective.",
            "emoji": "⚖️",
            "color": "#ce93d8",
            "text_color": "#4a148c"
        }
    }
    
    if skin_type in skin_tips:
        tip_info = skin_tips[skin_type]
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, {tip_info['color']} 0%, {tip_info['color']}dd 100%); 
                   padding: 1.5rem; border-radius: 15px; margin: 1rem 0; 
                   border: 2px solid {tip_info['text_color']}33;
                   box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
            <h4 style="color: {tip_info['text_color']}; margin: 0 0 0.5rem 0; font-weight: 600;">
                {tip_info['emoji']} {skin_type} Skin Tip
            </h4>
            <p style="color: {tip_info['text_color']}; margin: 0; font-size: 0.95rem; line-height: 1.4;">
                {tip_info['tip']}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Stats
    st.divider()
    st.subheader("📊 Session Stats")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Questions", st.session_state.conversation_count)
    with col2:
        st.metric("Skin Type", skin_type)
    
    # Enhanced clear chat button
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.session_state.conversation_count = 0
        st.success("Chat cleared! ✨")
        time.sleep(1)
        st.rerun()
    
    # Daily skincare reminder
    st.divider()
    st.subheader("🌟 Daily Reminder")
    reminders = [
        "Don't forget your sunscreen! ☀️",
        "Hydrate inside and out! 💧",
        "Gentle cleansing is key! 🧼",
        "Consistency beats perfection! ⭐",
        "Listen to your skin! 👂"
    ]
    
    import random
    daily_reminder = random.choice(reminders)
    st.info(daily_reminder)

# -------------------------
# Load Data + Build RAG
# -------------------------
@st.cache_resource(show_spinner=True)
def setup_rag():
    """Initialize the RAG system with caching for better performance"""
    try:
        data = utils.loader.load_all_csvs("data")
        docs = utils.loader.prepare_docs_from_data(data)
        vectorstore = build_vectorstore(docs, provider="huggingface")
        qa_chain = build_qa_chain(vectorstore)
        return qa_chain, len(docs)
    except Exception as e:
        st.error(f"Error setting up RAG system: {str(e)}")
        return None, 0

# Initialize RAG system
with st.spinner("🔄 Loading skincare knowledge base..."):
    qa_chain, doc_count = setup_rag()

if qa_chain is None:
    st.error("Failed to initialize the PEAUFECT AI companion. Please check your data files.")
    st.stop()

# Enhanced system info with better styling
st.markdown('<div class="stats-container">', unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("📚 Knowledge Base", f"{doc_count} docs", delta="Updated")
with col2:
    st.metric("🤖 AI Model", "GPT-4", delta="Active")
with col3:
    st.metric("⚡ Status", "Online", delta="Healthy")
with col4:
    st.metric("👥 Users Helped", "1000+", delta="Growing")
st.markdown('</div>', unsafe_allow_html=True)

# -------------------------
# Enhanced Skin Concerns Section with Visual Cards
# -------------------------
st.markdown("## 🎯 What are your skin concerns?")

# Create visual concern cards
concern_options = {
    "Acne": "🔴", "Dark Spots": "🟤", "Wrinkles": "📏", "Fine Lines": "〰️",
    "Dryness": "🏜️", "Oiliness": "💧", "Sensitivity": "🌡️", "Large Pores": "🕳️",
    "Dullness": "😴", "Blackheads": "⚫", "Uneven Skin Tone": "🎨", "Redness": "🔴",
    "Sun Damage": "☀️", "Hyperpigmentation": "🟫"
}

# Display concerns in a grid with visual cards
cols = st.columns(4)
selected_concerns = []

for i, (concern, emoji) in enumerate(concern_options.items()):
    with cols[i % 4]:
        if st.checkbox(f"{emoji} {concern}", key=f"concern_{concern}"):
            selected_concerns.append(concern)

skin_concerns = selected_concerns

# Show selected concerns summary
if skin_concerns:
    st.success(f"Selected concerns: {', '.join(skin_concerns)}")
else:
    st.info("Select your skin concerns above to get personalized recommendations")

# -------------------------
# Enhanced Suggested Questions with Categories
# -------------------------
st.markdown("## 💡 Popular Questions")

# Categorized suggestions with emojis
suggestion_categories = {
    "🌅 Morning Routines": [
        "What's a good morning routine for oily skin?",
        "Best morning skincare for dry skin",
        "Quick 5-minute morning routine"
    ],
    "🌙 Night Care": [
        "Perfect nighttime routine for anti-aging",
        "Best night creams under ₹1000",
        "How to layer skincare products at night"
    ],
    "🎯 Specific Concerns": [
        "How to treat acne scars naturally?",
        "Best ingredients for dark spots",
        "Affordable anti-aging routine under ₹2,000"
    ],
    "🧪 Ingredients": [
        "What's the difference between retinol and retinoid?",
        "Benefits of niacinamide for oily skin",
        "How to use vitamin C serum correctly"
    ]
}

# Create tabs for different categories
tabs = st.tabs(list(suggestion_categories.keys()))

for i, (category, questions) in enumerate(suggestion_categories.items()):
    with tabs[i]:
        for j, question in enumerate(questions):
            if st.button(question, key=f"suggestion_{i}_{j}", use_container_width=True):
                st.session_state.suggested_query = question

# -------------------------
# Chat History Display
# -------------------------
st.subheader("💬 Conversation")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
        if message["role"] == "assistant" and "timestamp" in message:
            st.caption(f"Answered at {message['timestamp']}")

# -------------------------
# Chat Input
# -------------------------
user_query = st.chat_input("Ask me anything about skincare...")

# Handle suggested query
if "suggested_query" in st.session_state:
    user_query = st.session_state.suggested_query
    del st.session_state.suggested_query

if user_query:
    # Function to validate if query is skincare-related
    def is_skincare_related(query):
        """Check if the user query is related to skincare"""
        query_lower = query.lower().strip()
        
        # First, check for obvious non-skincare topics to reject immediately
        non_skincare_topics = [
            'taj mahal', 'weather', 'food', 'cooking', 'recipe', 'movie', 'music', 'sports', 'politics',
            'history', 'geography', 'math', 'science', 'programming', 'code', 'computer', 'technology',
            'travel', 'hotel', 'restaurant', 'car', 'bike', 'phone', 'game', 'book', 'news',
            'stock market', 'investment', 'money', 'job', 'career', 'education', 'school', 'college'
        ]
        
        for topic in non_skincare_topics:
            if topic in query_lower:
                return False
        
        # Skincare-specific keywords (more specific terms)
        skincare_keywords = [
            # Core skincare terms
            'skincare', 'skin care', 'facial', 'complexion', 'pores', 'acne', 'pimple', 'blackhead', 'whitehead',
            # Products
            'cleanser', 'moisturizer', 'moisturiser', 'serum', 'toner', 'sunscreen', 'spf', 'face cream', 
            'face wash', 'face mask', 'eye cream', 'night cream', 'day cream', 'face oil',
            # Ingredients
            'retinol', 'retinoid', 'niacinamide', 'hyaluronic acid', 'salicylic acid', 'glycolic acid', 
            'vitamin c', 'peptide', 'ceramide', 'collagen', 'antioxidant', 'aha', 'bha', 'benzoyl peroxide',
            # Skin concerns
            'wrinkle', 'fine line', 'dark spot', 'age spot', 'pigmentation', 'hyperpigmentation',
            'redness', 'irritation', 'inflammation', 'dullness', 'texture', 'elasticity', 'firmness',
            'sun damage', 'melasma', 'rosacea', 'eczema', 'dermatitis',
            # Routines
            'skincare routine', 'morning routine', 'night routine', 'daily routine', 'cleansing routine',
            # Brands
            'cerave', 'neutrogena', 'olay', 'clinique', 'the ordinary', 'minimalist', 'nykaa', 'lakme',
            'dot&key', 'hyphen', 'foxtale', 'dermaco', 'simple', 'eucerin', 'garnier', 'biotique'
        ]
        
        # Check for direct skincare keywords
        for keyword in skincare_keywords:
            if keyword in query_lower:
                return True
        
        # Check for skin-related terms (must be combined with skincare context)
        skin_terms = ['skin', 'face']
        skincare_context = [
            'routine', 'care', 'product', 'treatment', 'problem', 'issue', 'concern', 'type',
            'oily', 'dry', 'combination', 'sensitive', 'normal', 'aging', 'young', 'healthy',
            'glow', 'radiant', 'clear', 'smooth', 'soft', 'hydrated', 'moisturized'
        ]
        
        has_skin_term = any(term in query_lower for term in skin_terms)
        has_skincare_context = any(context in query_lower for context in skincare_context)
        
        if has_skin_term and has_skincare_context:
            return True
        
        # Check for specific skincare question patterns
        skincare_questions = [
            'skincare routine', 'skin routine', 'face routine', 'beauty routine',
            'best moisturizer', 'best cleanser', 'best serum', 'best sunscreen',
            'how to treat acne', 'how to reduce wrinkles', 'how to get clear skin',
            'what is retinol', 'what is niacinamide', 'benefits of'
        ]
        
        for question in skincare_questions:
            if question in query_lower:
                return True
        
        return False
    
    # Validate if query is skincare-related
    if not is_skincare_related(user_query):
        # Display user message
        with st.chat_message("user"):
            st.write(user_query)
        
        # Show polite rejection message
        with st.chat_message("assistant"):
            st.error("🌸 **Sorry!** I'm PEAUFECT, your dedicated skincare assistant.")
            st.info("""
            **I can only help with skincare-related questions like:**
            • Skincare routines and products
            • Skin concerns (acne, dryness, aging, etc.)
            • Ingredient advice and recommendations
            • Brand suggestions within your budget
            
            **Please ask me something about skincare!** ✨
            """)
        
        # Add messages to chat history
        st.session_state.messages.append({"role": "user", "content": user_query})
        st.session_state.messages.append({
            "role": "assistant", 
            "content": "I'm PEAUFECT, your skincare assistant. I can only help with skincare-related questions. Please ask me about skincare routines, products, or skin concerns!",
            "timestamp": datetime.now().strftime("%H:%M")
        })
        st.session_state.conversation_count += 1
        st.stop()
    
    # Add user message to chat history (only for valid skincare queries)
    st.session_state.messages.append({"role": "user", "content": user_query})
    st.session_state.conversation_count += 1
    
    # Display user message
    with st.chat_message("user"):
        st.write(user_query)
    
    # Build enhanced context
    context_parts = [user_query]
    
    context_parts.append(f"Skin type: {skin_type}")
    if budget_pref != "Any":
        context_parts.append(f"Budget: {budget_pref}")
    if selected_brand != "Any":
        context_parts.append(f"Preferred brand: {selected_brand}")
    if age_range != "Any":
        context_parts.append(f"Age range: {age_range}")
    if skin_concerns:
        context_parts.append(f"Skin concerns: {', '.join(skin_concerns)}")
    
    context_parts.extend([
        "Do NOT include approximate dollar amounts or prices in the response unless specifically asked about pricing.",
        "Format your response in concise bullet points with clear headings.",
        "Use • for main points and ◦ for sub-points.",
        "Keep each point short and actionable (max 1-2 lines).",
        "Structure routine advice as: Morning → Evening → Weekly steps."
    ])
    
    query_context = ". ".join(context_parts)
    
    # Function to format response into bullet points
    def format_to_bullet_points(text):
        """Convert response text to structured bullet points"""
        lines = text.split('\n')
        formatted_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Check if it's a heading (contains keywords like "morning", "evening", "routine", etc.)
            if any(keyword in line.lower() for keyword in ['morning', 'evening', 'night', 'routine', 'step', 'cleansing', 'moisturizing', 'sunscreen']):
                if not line.startswith('**') and ':' in line:
                    formatted_lines.append(f"\n**{line}**")
                else:
                    formatted_lines.append(f"\n{line}")
            # Convert to bullet points if not already formatted
            elif not line.startswith(('•', '◦', '*', '-', '**')):
                # Split long sentences into multiple points
                if '. ' in line and len(line) > 100:
                    sentences = line.split('. ')
                    for sentence in sentences:
                        if sentence.strip():
                            formatted_lines.append(f"• {sentence.strip()}")
                else:
                    formatted_lines.append(f"• {line}")
            else:
                formatted_lines.append(line)
        
        return '\n'.join(formatted_lines)
    
    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("💡 Analyzing your skincare needs..."):
            try:
                response = qa_chain({"query": query_context})
                raw_answer = response["result"]
                
                # Format the answer into bullet points
                answer = format_to_bullet_points(raw_answer)
                
                # Display response with enhanced typing effect and images
                message_placeholder = st.empty()
                full_response = ""
                
                # Add relevant skincare images based on query content
                def get_skincare_image_url(query_lower):
                    """Return relevant skincare image URL based on query content"""
                    if any(word in query_lower for word in ['acne', 'pimple', 'breakout']):
                        return "https://images.unsplash.com/photo-1556228720-195a672e8a03?w=400&h=300&fit=crop"
                    elif any(word in query_lower for word in ['moisturizer', 'dry', 'hydrat']):
                        return "https://images.unsplash.com/photo-1570194065650-d99fb4bedf0a?w=400&h=300&fit=crop"
                    elif any(word in query_lower for word in ['serum', 'vitamin c', 'anti-aging']):
                        return "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=400&h=300&fit=crop"
                    elif any(word in query_lower for word in ['sunscreen', 'spf', 'sun protection']):
                        return "https://images.unsplash.com/photo-1556228578-8c89e6adf883?w=400&h=300&fit=crop"
                    elif any(word in query_lower for word in ['cleanser', 'wash', 'clean']):
                        return "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=400&h=300&fit=crop"
                    else:
                        return "https://images.unsplash.com/photo-1596755389378-c31d21fd1273?w=400&h=300&fit=crop"
                
                # Show relevant image
                query_lower = user_query.lower()
                image_url = get_skincare_image_url(query_lower)
                
                try:
                    st.image(image_url, caption="Related skincare advice", width=300)
                except:
                    pass  # Skip if image fails to load
                
                # Simulate typing effect with better animation
                for chunk in answer.split():
                    full_response += chunk + " "
                    message_placeholder.markdown(f'<div class="chat-message">{full_response}▌</div>', unsafe_allow_html=True)
                    time.sleep(0.03)
                
                message_placeholder.markdown(f'<div class="chat-message">{full_response}</div>', unsafe_allow_html=True)
                
                # Add timestamp
                timestamp = datetime.now().strftime("%H:%M")
                st.caption(f"Answered at {timestamp}")
                
                # Add to chat history
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": full_response.strip(),
                    "timestamp": timestamp
                })
                
                # Show sources if available
                if "source_documents" in response and response["source_documents"]:
                    with st.expander("🔎 Sources & References"):
                        for i, doc in enumerate(response["source_documents"], start=1):
                            st.markdown(f"**Source {i}:**")
                            st.write(doc.page_content[:300] + "..." if len(doc.page_content) > 300 else doc.page_content)
                            if hasattr(doc, 'metadata') and doc.metadata:
                                st.caption(f"Metadata: {doc.metadata}")
                
                # Feedback section
                st.divider()
                col1, col2, col3 = st.columns([1, 1, 4])
                with col1:
                    if st.button("👍", key=f"like_{st.session_state.conversation_count}"):
                        st.success("Thanks for the feedback!")
                with col2:
                    if st.button("👎", key=f"dislike_{st.session_state.conversation_count}"):
                        st.info("We'll work on improving our responses!")
                
            except Exception as e:
                st.error(f"Sorry, I encountered an error: {str(e)}")
                st.info("Please try rephrasing your question or check if the system is properly configured.")

# -------------------------
# Enhanced Footer with Interactive Elements
# -------------------------
st.divider()

# Skincare tips carousel
st.markdown("## 🌟 Did You Know?")
skincare_facts = [
    "💧 Your skin is 64% water - stay hydrated for that natural glow!",
    "🌙 Your skin repairs itself while you sleep - never skip your night routine!",
    "☀️ 80% of skin aging is caused by sun exposure - SPF is your best friend!",
    "🧬 Your skin completely renews itself every 28 days - patience is key!",
    "🥒 What you eat affects your skin - antioxidants are skin superfoods!",
    "💆‍♀️ Facial massage improves circulation and can reduce puffiness!",
    "🧴 Less is more - over-cleansing can damage your skin barrier!"
]

# Random fact display
import random
if st.button("🔄 Get New Skincare Fact", use_container_width=True):
    fact = random.choice(skincare_facts)
    st.success(fact)

# Quick skin assessment
st.markdown("## 🔍 Quick Skin Health Check")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("💧 Hydration Check", use_container_width=True):
        st.info("Pinch test: Pinch skin on back of hand. If it snaps back quickly, you're well hydrated!")

with col2:
    if st.button("🌟 Glow Meter", use_container_width=True):
        st.info("Look in natural light. Healthy skin should have a subtle, even glow without excess shine!")

with col3:
    if st.button("🎯 Routine Check", use_container_width=True):
        st.info("Basic routine: Cleanser → Treatment → Moisturizer → SPF (AM) | Add treatments at night!")

# Newsletter signup mockup
st.markdown("## 📧 Stay Updated")
email_col, button_col = st.columns([3, 1])
with email_col:
    email = st.text_input("Get weekly skincare tips", placeholder="your.email@example.com", label_visibility="collapsed")
with button_col:
    if st.button("Subscribe", use_container_width=True):
        if email:
            st.success("Thanks for subscribing! 💌")

# Enhanced footer
st.markdown("""
<div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
           color: white; padding: 2rem; border-radius: 15px; text-align: center; margin-top: 2rem;'>
    <h3>✨ PEAUFECT v3.0 - From Questions to Glow</h3>
    <p>Made with ❤️ for healthier, happier skin</p>
    <div style='display: flex; justify-content: center; gap: 2rem; margin-top: 1rem;'>
        <span>🌟 Personalized</span>
        <span>🔬 Science-Based</span>
        <span>💰 Budget-Friendly</span>
        <span>🌿 Natural</span>
    </div>
    <hr style='margin: 1rem 0; border: 1px solid rgba(255,255,255,0.3);'>
    <small>⚠️ Always consult with a dermatologist for serious skin concerns | 
    This AI assistant provides general skincare guidance only</small>
</div>
""", unsafe_allow_html=True)

# Floating action button for quick help
st.markdown("""
<style>
.floating-help {
    position: fixed;
    bottom: 20px;
    right: 20px;
    background: linear-gradient(135deg, #ff6b6b, #4ecdc4);
    color: white;
    border-radius: 50%;
    width: 60px;
    height: 60px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    cursor: pointer;
    z-index: 1000;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.1); }
    100% { transform: scale(1); }
}
</style>

<div class="floating-help" title="Need help? Just ask!">
    💬
</div>
""", unsafe_allow_html=True)