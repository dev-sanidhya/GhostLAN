# GhostLAN - Advanced eSports Anti-Cheat Testing Platform

<div align="center">

**A comprehensive digital twin simulation platform for offline eSports anti-cheat testing**

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![Next.js](https://img.shields.io/badge/Next.js-15.2.4-black.svg)](https://nextjs.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-blue.svg)](https://typescriptlang.org)

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Architecture](#-architecture) • [API](#-api) • [Contributing](#-contributing)

</div>

## 🎯 Overview

GhostLAN is a cutting-edge digital twin simulation platform designed for comprehensive eSports anti-cheat testing. Powered by advanced AI agents and real-time analytics, it creates realistic LAN environments where both normal and cheat-prone behaviors can be simulated and detected.

### 🚀 Key Highlights

- **🤖 AI-Powered Simulation**: Realistic gaming environments with intelligent agents
- **🛡️ Multi-Layer Anti-Cheat**: Rule-based and ML-based cheat detection
- **📊 Real-time Analytics**: Comprehensive player and match analytics
- **🎬 Match Recording & Replay**: Full match capture and playback system
- **🏆 Tournament Management**: Advanced tournament systems
- **🎨 Modern Web Interface**: Beautiful, responsive dashboard built with Next.js

## ✨ Features

### Core Systems
- **Duality AI Integration**: Advanced AI agents with realistic gaming behaviors
- **Multi-Layer Anti-Cheat**: Rule-based and ML-based cheat detection
- **Real-time Analytics**: Comprehensive player and match analytics
- **Match Recording & Replay**: Full match capture and playback system
- **Tournament Management**: Advanced tournament systems with multiple formats

### Advanced Features
- **Deep Learning Models**: CNN, RNN, and GAN for advanced cheat detection
- **Real-time Streaming**: WebRTC, RTMP, and HLS live broadcasting
- **Mobile App Support**: iOS/Android integration with REST APIs
- **Cloud Integration**: AWS, Azure, and GCP with auto-scaling
- **Behavioral Analysis**: Advanced pattern recognition and anomaly detection

## 🏗️ Architecture

```
GhostLAN/
├── backend/                 # Python FastAPI backend
│   ├── duality_scene/      # AI simulation environment
│   ├── ghostlan_core/      # Anti-cheat engine
│   ├── analytics/          # Analytics and visualization
│   ├── api/               # FastAPI endpoints
│   └── main.py            # Backend entry point
├── frontend/               # Next.js React frontend
│   ├── app/               # Next.js app directory
│   ├── components/        # React components
│   ├── lib/              # Utilities and API client
│   └── public/           # Static assets
└── README.md             # This file
```

## 🛠️ Installation

### Prerequisites

- **Python 3.9+**
- **Node.js 18+**
- **FFmpeg** (for streaming features)
- **Git**

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Set environment variables
export JWT_SECRET_KEY="your-secret-key"
export DATABASE_URL="sqlite:///./ghostlan.db"
export DUALITY_API_KEY="your-duality-api-key-here"

# Run the backend server
python main.py
```

The backend will be available at `http://localhost:8000`

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install Node.js dependencies
npm install
# or
yarn install
# or
pnpm install

# Create environment file
cp .env.example .env.local

# Start the development server
npm run dev
# or
yarn dev
# or
pnpm dev
```

The frontend will be available at `http://localhost:3000` (or next available port)

## 🎮 Usage

### Quick Start

1. **Start Backend**: Run `python main.py` in the backend directory
2. **Start Frontend**: Run `npm run dev` in the frontend directory
3. **Access Dashboard**: Open `http://localhost:3000` in your browser
4. **View API Docs**: Visit `http://localhost:8000/docs` for API documentation

### Core Features

#### 1. Anti-Cheat Monitoring
- Real-time detection of suspicious activities
- Multi-level severity classification
- Detailed evidence and confidence scores
- Historical alert tracking

#### 2. Duality AI Integration
- **API Key Setup**: Configure your Duality AI API key in `backend/.env`
- **AI Agents**: Realistic gaming behaviors with configurable cheat injection
- **Simulation Environment**: Digital twin LAN environment for testing
- **Real-time Events**: Live streaming of agent actions and behaviors

#### 3. Analytics Dashboard
- Player performance metrics
- Match statistics and trends
- Real-time leaderboards
- Interactive charts and visualizations

#### 4. Match Recording & Replay
- Full match capture with events
- Interactive replay system
- Export capabilities (CSV, JSON)
- Timeline-based navigation

#### 5. Tournament Management
- Multiple tournament formats
- Automated bracket generation
- Real-time standings
- Prize distribution

### API Endpoints

#### Core Endpoints
- `GET /health` - System health check
- `GET /api/v1/status` - System status and services
- `GET /api/v1/export/anticheat` - Anti-cheat alerts
- `GET /api/v1/export/matches` - Match history
- `GET /api/v1/export/analytics` - Analytics data

#### WebSocket
- `ws://localhost:8000/ws` - Real-time updates

## 🎨 Frontend Features

### Modern UI Components
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Dark Theme**: Cyberpunk-inspired dark theme
- **Real-time Updates**: Live data streaming via WebSocket
- **Interactive Charts**: Beautiful data visualizations
- **Accessibility**: WCAG compliant with proper contrast ratios

### Key Pages
- **Dashboard**: Overview of system status and key metrics
- **Anti-Cheat**: Real-time monitoring and alert management
- **Analytics**: Detailed performance analysis and charts
- **Players**: Player profiles and statistics
- **Voice Chat**: Voice communication monitoring
- **Settings**: System configuration and preferences

## 🔧 Configuration

### Environment Variables

#### Backend (.env)
```bash
JWT_SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///./ghostlan.db
CORS_ORIGINS=http://localhost:3000
LOG_LEVEL=INFO
DUALITY_API_KEY=your-duality-api-key-here
```

#### Frontend (.env.local)
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
```

### Database Setup
The application uses SQLite by default. For production, consider using PostgreSQL or MySQL.

## 🚀 Deployment

### Backend Deployment
```bash
# Using Docker
docker build -t ghostlan-backend ./backend
docker run -p 8000:8000 ghostlan-backend

# Using systemd (Linux)
sudo systemctl enable ghostlan-backend
sudo systemctl start ghostlan-backend
```

### Frontend Deployment
```bash
# Build for production
npm run build

# Deploy to Vercel
vercel --prod

# Deploy to Netlify
netlify deploy --prod
```

## 🧪 Testing

### Backend Tests
```bash
cd backend
python -m pytest tests/
```

### Frontend Tests
```bash
cd frontend
npm run test
npm run test:e2e
```

## 📊 Performance

- **Backend**: Handles 1000+ concurrent connections
- **Frontend**: Optimized for 60fps animations
- **Database**: Supports 1M+ records with efficient indexing
- **WebSocket**: Real-time updates with <100ms latency

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Add tests for new functionality
5. Commit your changes: `git commit -m 'Add amazing feature'`
6. Push to the branch: `git push origin feature/amazing-feature`
7. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Duality AI** for advanced simulation capabilities
- **FastAPI** for the excellent web framework
- **Next.js** for the powerful React framework
- **Tailwind CSS** for the beautiful styling system
- **Lucide React** for the amazing icons

---

<div align="center">

**Made with ❤️ by Cache Money**

</div>
