# 🎮 Pokemon Chat App

A beautiful web-based Pokemon chat application that imports Pokemon from .pk8 files and enables personality-driven conversations. Features stunning sprites from PokeAPI, detailed Pokemon information, and an intuitive chat interface.

![Pokemon Chat App](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)
![Docker](https://img.shields.io/badge/Docker-Supported-blue.svg)
![PokeAPI](https://img.shields.io/badge/PokeAPI-Integrated-yellow.svg)

## ✨ Features

### 📁 **Import System**
- Upload and parse Generation 8 (.pk8) files
- Accurate byte-level parsing with error handling
- Automatic PokeAPI integration for enhanced data
- Duplicate prevention with smart IV comparison
- Support for 300-400 byte pk8 files

### 🎨 **Enhanced Visuals**
- **High-quality sprites** from official Pokemon artwork
- **Legendary/Mythical badges** with beautiful gradients
- **Pokédex descriptions** with flavor text
- **Base stats visualization** with animated progress bars
- **Physical dimensions** and habitat information

### 📚 **Pokedex Management**
- Browse your Pokemon collection with stunning visuals
- Filter and search capabilities
- Detailed Pokemon information display
- Team management (up to 6 Pokemon)
- Release Pokemon functionality

### 💬 **AI-Powered Personality Chat**
- **Dynamic AI responses** using ChatGPT or Claude APIs
- **Personality-driven conversations** based on species, nature, friendship, and level
- **Friendship evolution** affects response warmth and openness
- **Nature-based communication** styles (e.g., Timid Pokemon are shy, Jolly Pokemon are upbeat)
- **Species-specific traits** influence conversation topics and behavior
- **Context-aware responses** that remember conversation history
- **Graceful fallbacks** to template responses when AI is unavailable
- Mobile-responsive chat interface

### 🌟 **PokeAPI Integration**
- Automatic sprite fetching (artwork, shiny variants, showdown sprites)
- Species information (genus, descriptions, abilities)
- Base stats and type information  
- Legendary/Mythical status detection
- Habitat and physical data

## 🚀 Quick Start

### Using Docker (Recommended)

1. Clone the repository:
```bash
git clone git@github.com:YourBr0ther/pokemon-chat-app.git
cd pokemon-chat-app
```

2. Build and run with Docker:
```bash
docker compose up --build
```

3. Open your browser to `http://localhost:5005`

## 🤖 AI Chat Configuration

To enable AI-powered Pokemon conversations, you'll need API keys from OpenAI or Anthropic:

### Option 1: OpenAI (ChatGPT)
1. Visit [OpenAI Platform](https://platform.openai.com/api-keys)
2. Create an API key
3. Add to your `.env` file:
```bash
AI_PROVIDER=openai
OPENAI_API_KEY=your-openai-api-key-here
```

### Option 2: Claude (Anthropic)
1. Visit [Anthropic Console](https://console.anthropic.com/)
2. Create an API key
3. Add to your `.env` file:
```bash
AI_PROVIDER=claude
CLAUDE_API_KEY=your-claude-api-key-here
```

### Configuration Steps
1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` and add your API keys

3. Restart the application to enable AI features

**Note**: Without API keys, the app will use template-based responses as a fallback.

### Manual Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
cd app
python main.py
```

3. Open your browser to `http://localhost:5000`

## Usage

### 1. Import Pokemon
- Go to the Import screen
- Upload a .pk8 file (drag & drop or click to browse)
- Review the Pokemon data and personality traits
- Confirm to add to your Pokedex

### 2. Build Your Team
- Visit the Pokedex screen
- Click on Pokemon to view details
- Add up to 6 Pokemon to your active team
- Remove or release Pokemon as needed

### 3. Chat with Pokemon
- Go to the Chat screen
- Select a Pokemon from your team in the sidebar
- Start chatting! Each Pokemon has unique personality traits based on:
  - Species characteristics
  - Type influences
  - Nature traits
  - Friendship level
  - Experience level

## Pokemon Personality System

The chat responses are influenced by multiple factors:

- **Species**: Each species has unique personality traits (e.g., Celebi is gentle)
- **Types**: Type combinations affect communication style (e.g., Psychic types are thoughtful)
- **Nature**: Affects personality traits (e.g., Modest Pokemon are humble)
- **Friendship**: Determines closeness and response warmth
- **Level**: Higher levels show more maturity and wisdom

## File Structure

```
pokemon-chat-app/
├── app/
│   ├── __init__.py           # Flask app factory
│   ├── main.py              # Application entry point
│   ├── main_routes.py       # Main page routes
│   ├── models/
│   │   └── pokemon.py       # Database models
│   ├── parsers/
│   │   └── pk8_parser.py    # PK8 file parser
│   ├── personality/
│   │   └── chat_engine.py   # Personality-based chat engine
│   ├── api/
│   │   ├── import_routes.py # Import API endpoints
│   │   ├── chat_routes.py   # Chat API endpoints
│   │   └── pokedex_routes.py# Pokedex API endpoints
│   ├── static/
│   │   ├── css/style.css    # Styling
│   │   └── js/              # JavaScript files
│   └── templates/           # HTML templates
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## API Endpoints

### Import
- `POST /api/upload` - Upload and parse PK8 file
- `POST /api/save` - Save Pokemon to database

### Pokedex
- `GET /api/pokemon` - Get all Pokemon
- `GET /api/pokemon/<id>` - Get specific Pokemon
- `DELETE /api/pokemon/<id>` - Delete Pokemon

### Team
- `GET /api/team` - Get current team
- `POST /api/team/add` - Add Pokemon to team
- `POST /api/team/remove` - Remove Pokemon from team

### Chat
- `GET /api/pokemon/<id>/messages` - Get chat history
- `POST /api/pokemon/<id>/send` - Send message and get response
- `POST /api/pokemon/<id>/clear-history` - Clear chat history

## 🛠️ Development

### Prerequisites
- Python 3.9+
- Docker and Docker Compose (recommended)
- Git

### Local Development Setup
```bash
# Clone the repository
git clone git@github.com:YourBr0ther/pokemon-chat-app.git
cd pokemon-chat-app

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run database migration (if needed)
python migrate_database.py

# Start the application
cd app
python main.py
```

### Database Migration
If you're upgrading from an older version, run the migration script:
```bash
python migrate_database.py
```

## 🧪 Testing

### Test Suite
```bash
# Test AI integration and personality system
python test_ai_integration.py

# Test PokeAPI integration and database schema
python test_pokeapi_integration.py

# Test double import prevention
python test_double_import_fix.py

# Test pk8 parser accuracy
python test_parser.py
```

### PK8 Parser Features
- **Accurate byte offsets** reverse-engineered from actual pk8 files
- **Flexible file size** support (300-400 bytes)
- **Smart duplicate detection** using IV comparison
- **Error handling** with graceful fallbacks
- **Generation 8 Pokemon** recognition (810+ species)

### AI Personality System
The AI creates unique personalities for each Pokemon based on:

**Friendship Level:**
- **Distant** (0-69): Cautious, formal, keeps responses brief
- **Warming Up** (70-149): Friendly but careful, gradually opens up  
- **Loyal** (150-255): Warm, affectionate, completely trusting

**Nature Influence:**
- **Timid**: Shy and nervous, speaks softly
- **Jolly**: Cheerful and upbeat responses
- **Adamant**: Determined and speaks with conviction
- **Modest**: Humble and understated
- **And 21 other unique nature personalities**

**Species Traits:**
- **Celebi**: Gentle and wise, references time travel
- **Pikachu**: Energetic and electric-themed responses
- **Grookey**: Musical and rhythm-focused conversations
- **Each species has unique characteristics**

**Dynamic Conversations:**
- Responses evolve as friendship grows
- Pokemon remember previous conversations
- Personality traits combine for unique interactions
- Species lore and abilities influence topics

## 🌐 API Endpoints

### Import
- `POST /api/upload` - Upload and parse PK8 file
- `POST /api/save` - Save Pokemon to database

### Pokedex
- `GET /api/pokemon` - Get all Pokemon
- `GET /api/pokemon/<id>` - Get specific Pokemon
- `DELETE /api/pokemon/<id>` - Delete Pokemon

### Team Management
- `GET /api/team` - Get current team
- `POST /api/team/add` - Add Pokemon to team
- `POST /api/team/remove` - Remove Pokemon from team

### Chat
- `GET /api/pokemon/<id>/messages` - Get chat history
- `POST /api/pokemon/<id>/send` - Send message and get response
- `POST /api/pokemon/<id>/clear-history` - Clear chat history

## ⚙️ Configuration

Environment variables:
- `SECRET_KEY` - Flask secret key for sessions
- `DATABASE_URL` - Database connection URL (default: SQLite)
- `FLASK_ENV` - Environment mode (development/production)

## 🎯 Features Roadmap

### ✅ Completed
- [x] AI-powered chat with ChatGPT/Claude integration
- [x] Personality-based responses using friendship, nature, and species
- [x] PokeAPI integration with sprites and detailed information
- [x] Smart duplicate detection and pk8 parsing

### 🚧 Planned Features
- [ ] **Enhanced AI Features**
  - [ ] Conversation memory across sessions
  - [ ] Emotional state tracking
  - [ ] Learning from user interactions
- [ ] **Visual Enhancements**
  - [ ] Shiny Pokemon detection and display
  - [ ] Animated sprites and reactions
  - [ ] Custom Pokemon portraits
- [ ] **Game Mechanics**
  - [ ] Move information and battle mechanics
  - [ ] Pokemon evolution chains
  - [ ] Experience and level progression
- [ ] **Social Features**
  - [ ] Trading system between users
  - [ ] Multi-user chat rooms
  - [ ] Pokemon sharing and showcasing
- [ ] **Advanced Features**
  - [ ] Voice chat integration
  - [ ] Mobile app version
  - [ ] Pokemon breeding system

## 🌍 Browser Support

- Chrome 70+
- Firefox 65+
- Safari 12+
- Edge 79+

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is for educational purposes only. Pokemon and related characters are trademarks of Nintendo, Game Freak, and The Pokemon Company.