# Harmony Helper: AI-Powered Vocal Harmony Generator

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![React](https://img.shields.io/badge/react-19-61dafb.svg)](https://reactjs.org/)

An open-source web application designed for vocalists and musicians to automatically generate diverse and creative harmonies for their melodies.

## 🌟 Project Vision

Many vocalists can create beautiful melodies but struggle with writing compelling harmony parts, especially beyond basic thirds and fifths. **Harmony Helper** aims to bridge this gap by providing an intuitive, AI-powered tool that takes a simple melody and generates a wide range of harmonic arrangements, from classic contrary motion to modern parallel harmonies.

## ✨ Features

### Current Features (MVP - v0.1.0)

✅ **Melody Input**
- Interactive on-screen piano keyboard (2 octaves: C4-B5)
- Click-to-add notes with visual feedback
- Real-time melody display

✅ **Harmony Generation** (7 Types)
- **Basic Harmony:** Classic 3rd and 5th harmonies
- **Parallel Motion:** 4ths and 6ths
- **Contrary Motion:** Inverse movement (melody up → harmony down)
- **Oblique Motion:** One voice moves, one holds
- **Pedal/Drone:** Sustained note under moving melody

✅ **Audio Playback**
- Play melody alone or with harmony
- Independent volume controls for melody and harmony
- Built with Tone.js for high-quality browser-based audio

✅ **User Interface**
- Modern, responsive design with Tailwind CSS
- Real-time visual feedback
- Intuitive controls

### Roadmap (Future Versions)

- [ ] **Audio Export:** Download as MP3, WAV, or MIDI
- [ ] **Recording:** Record melodies via microphone
- [ ] **More Harmony Styles:** Call-and-response, arpeggiated chords
- [ ] **Rhythmic Variation:** Different rhythms for harmony
- [ ] **Style-Specific Models:** Jazz, Gospel, Pop harmonies
- [ ] **User Accounts:** Save and share your creations

## 🛠️ Tech Stack

### Backend
- **Language:** Python 3.11
- **API Framework:** FastAPI
- **Music Theory Engine:** music21 (for harmony logic and generation)

### Frontend
- **Framework:** React 19
- **Audio Engine:** Tone.js (Web Audio API wrapper)
- **UI Components:** shadcn/ui + Tailwind CSS
- **Build Tool:** Vite

## 📂 Project Structure

```
harmony-helper/
├── backend/              # Python FastAPI server
│   ├── app/
│   │   ├── harmony_engine/
│   │   │   ├── __init__.py
│   │   │   └── core.py          # Core harmony generation algorithms
│   │   └── main.py              # FastAPI routes
│   └── requirements.txt
│
└── frontend/             # React application (managed separately)
    └── harmony-helper-frontend/
```

## 🚀 Getting Started

### Prerequisites

- **Python 3.11+**
- **Node.js 18+** and **pnpm**
- **Git**

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/harmony-helper.git
   cd harmony-helper/backend
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the backend server**
   ```bash
   python -m app.main
   ```
   
   The API will be available at `http://localhost:8000`
   
   📖 **API Documentation:** `http://localhost:8000/docs`

### Frontend Setup

The frontend is managed as a separate web development project. To run it locally:

1. **Navigate to the frontend directory**
   ```bash
   cd harmony-helper-frontend
   ```

2. **Install dependencies**
   ```bash
   pnpm install
   ```

3. **Start the development server**
   ```bash
   pnpm dev
   ```
   
   The app will be available at `http://localhost:3000`

### Running the Full Stack

You need to run both the backend and frontend simultaneously:

**Terminal 1 (Backend):**
```bash
cd harmony-helper/backend
python -m app.main
```

**Terminal 2 (Frontend):**
```bash
cd harmony-helper-frontend
pnpm dev
```

Then open `http://localhost:3000` in your browser.

## 📖 API Documentation

### Endpoints

#### `GET /harmony-types`
Get all available harmony types with descriptions.

**Response:**
```json
{
  "harmony_types": [
    {
      "value": "third",
      "name": "三度和声",
      "description": "经典的三度平行和声"
    },
    ...
  ]
}
```

#### `POST /generate-harmony`
Generate harmony for a given melody.

**Request:**
```json
{
  "melody": [
    {"pitch": "C4", "duration": 1.0, "offset": 0.0},
    {"pitch": "E4", "duration": 1.0, "offset": 1.0}
  ],
  "harmony_type": "third"
}
```

**Response:**
```json
{
  "melody": [...],
  "harmony": [
    {"pitch": "A3", "duration": 1.0, "offset": 0.0},
    {"pitch": "C#4", "duration": 1.0, "offset": 1.0}
  ],
  "harmony_type": "third",
  "message": "Successfully generated third harmony"
}
```

## 🎵 How It Works

### Harmony Generation Algorithm

The core harmony generation engine uses the **music21** library to analyze melodic intervals and apply music theory rules:

1. **Parallel Intervals:** Transpose each note by a fixed interval (e.g., -3 semitones for thirds)
2. **Contrary Motion:** When melody moves up by N semitones, harmony moves down by N semitones
3. **Oblique Motion:** Harmony stays on a fixed pitch while melody moves
4. **Pedal Tone:** A sustained bass note throughout the entire melody

### Example: Contrary Motion

```
Melody:   C4 → E4 → G4  (up 4 semitones, up 3 semitones)
Harmony:  F3 → C#3 → B2 (down 4 semitones, down 3 semitones)
```

## 🤝 Contributing

We welcome contributions from everyone! Whether you're a developer, musician, or designer:

1. **Fork** the repository
2. Create a **feature branch** (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. Open a **Pull Request**

### Development Guidelines

- Follow PEP 8 for Python code
- Use ESLint/Prettier for JavaScript/TypeScript
- Write descriptive commit messages
- Add tests for new features
- Update documentation as needed

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **music21** - Comprehensive music analysis toolkit
- **Tone.js** - Web Audio framework for interactive music
- **FastAPI** - Modern Python web framework
- **shadcn/ui** - Beautiful UI components

## 📧 Contact

For questions, suggestions, or feedback:
- Open an issue on GitHub
- Email: [your-email@example.com]

---

**Made with ❤️ for vocalists who want to explore harmony**
