# Harmony Helper - Development Guide

This document provides a comprehensive guide for developers who want to understand, extend, or maintain the Harmony Helper project.

## 📋 Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Backend Deep Dive](#backend-deep-dive)
3. [Frontend Deep Dive](#frontend-deep-dive)
4. [Harmony Algorithms Explained](#harmony-algorithms-explained)
5. [Future Development Roadmap](#future-development-roadmap)
6. [Performance Optimization](#performance-optimization)
7. [Troubleshooting](#troubleshooting)

---

## Architecture Overview

Harmony Helper follows a **client-server architecture** with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────┐
│                    User's Browser                        │
│  ┌───────────────────────────────────────────────────┐  │
│  │  React Frontend (Port 3000)                       │  │
│  │  - Piano Keyboard UI                              │  │
│  │  - Tone.js Audio Engine                           │  │
│  │  - State Management                               │  │
│  └───────────────┬───────────────────────────────────┘  │
└──────────────────┼──────────────────────────────────────┘
                   │ HTTP/JSON
                   │ (CORS enabled)
┌──────────────────▼──────────────────────────────────────┐
│  FastAPI Backend (Port 8000)                            │
│  ┌───────────────────────────────────────────────────┐  │
│  │  REST API Endpoints                               │  │
│  │  - /harmony-types                                 │  │
│  │  - /generate-harmony                              │  │
│  └───────────────┬───────────────────────────────────┘  │
│                  │                                       │
│  ┌───────────────▼───────────────────────────────────┐  │
│  │  Harmony Generation Engine (music21)             │  │
│  │  - Parallel Intervals                             │  │
│  │  - Contrary Motion                                │  │
│  │  - Oblique Motion                                 │  │
│  │  - Pedal Tones                                    │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### Key Design Decisions

1. **Why FastAPI?**
   - Automatic API documentation (Swagger UI)
   - Type validation with Pydantic
   - High performance (async support)
   - Easy to extend

2. **Why music21?**
   - Industry-standard music theory library
   - Rich set of music analysis tools
   - Handles pitch, intervals, chords natively
   - Extensible for advanced algorithms

3. **Why Tone.js?**
   - Best-in-class Web Audio API wrapper
   - Precise timing and scheduling
   - Built-in synthesizers
   - Active community

---

## Backend Deep Dive

### File Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app & routes
│   └── harmony_engine/
│       ├── __init__.py
│       └── core.py             # Harmony algorithms
└── requirements.txt
```

### Core Components

#### 1. `app/main.py` - API Layer

**Responsibilities:**
- Define REST API endpoints
- Request/response validation (Pydantic models)
- CORS configuration
- Error handling

**Key Endpoints:**

```python
GET  /                    # API info
GET  /health             # Health check
GET  /harmony-types      # List all harmony types
POST /generate-harmony   # Generate harmony for melody
POST /quick-harmony      # Quick single-note test
```

#### 2. `app/harmony_engine/core.py` - Business Logic

**Classes:**

```python
class HarmonyType(Enum):
    """Enumeration of all supported harmony types"""
    THIRD = "third"
    FIFTH = "fifth"
    # ... etc

class HarmonyGenerator:
    """Main harmony generation engine"""
    
    def generate_harmony(melody_notes, harmony_type):
        """Entry point for harmony generation"""
        
    def _generate_parallel_interval(melody_notes, semitones):
        """Algorithm for parallel motion"""
        
    def _generate_contrary_motion(melody_notes):
        """Algorithm for contrary motion"""
        
    # ... other algorithms
```

**Data Flow:**

```
User Request → FastAPI Route → HarmonyGenerator.generate_harmony()
                                      ↓
                            Select algorithm based on type
                                      ↓
                            Apply music21 transformations
                                      ↓
                            Return harmony notes → JSON Response
```

### Adding New Harmony Algorithms

To add a new harmony type (e.g., "jazz_voicing"):

1. **Add to enum:**
   ```python
   class HarmonyType(Enum):
       # ... existing types ...
       JAZZ_VOICING = "jazz_voicing"
   ```

2. **Implement algorithm:**
   ```python
   def _generate_jazz_voicing(self, melody_notes):
       """
       Generate jazz-style voicings (e.g., 7th chords, extensions)
       """
       harmony_notes = []
       for note in melody_notes:
           # Your algorithm here
           # Example: add 3rd, 7th, and 9th
           pass
       return harmony_notes
   ```

3. **Wire it up:**
   ```python
   def generate_harmony(self, melody_notes, harmony_type):
       # ... existing code ...
       elif harmony_type == HarmonyType.JAZZ_VOICING:
           return self._generate_jazz_voicing(melody_notes)
   ```

4. **Update API metadata:**
   ```python
   @app.get("/harmony-types")
   async def get_harmony_types():
       return {
           "harmony_types": [
               # ... existing types ...
               {
                   "value": "jazz_voicing",
                   "name": "爵士和弦配置",
                   "description": "使用7和弦和扩展音的爵士风格和声"
               }
           ]
       }
   ```

---

## Frontend Deep Dive

### File Structure

```
client/
├── src/
│   ├── App.tsx                 # Root component & routing
│   ├── pages/
│   │   └── Home.tsx            # Main application page
│   ├── components/
│   │   ├── Piano.tsx           # Virtual piano keyboard
│   │   └── ui/                 # shadcn/ui components
│   └── lib/
│       ├── audioEngine.ts      # Tone.js wrapper
│       ├── api.ts              # Backend API client
│       └── utils.ts            # Utilities
└── public/
```

### Core Components

#### 1. `lib/audioEngine.ts` - Audio Management

**Responsibilities:**
- Initialize Tone.js
- Play individual notes
- Play sequences with timing
- Manage volume

**Key Methods:**

```typescript
class AudioEngine {
    async initialize()              // Must be called after user interaction
    playNote(pitch, duration)       // Play single note
    playSequence(notes, volume)     // Play melody
    playWithHarmony(melody, harmony, volumes) // Play both
    stopAll()                       // Stop playback
}
```

**Important:** Web Audio API requires user interaction before playing sound (browser security). The app handles this by initializing on first piano key click.

#### 2. `lib/api.ts` - Backend Communication

**Functions:**

```typescript
getHarmonyTypes()                    // Fetch available harmony types
generateHarmony(melody, harmonyType) // Request harmony generation
```

**Error Handling:**
- Network errors → fallback to default harmony types
- API errors → display toast notification

#### 3. `components/Piano.tsx` - Virtual Keyboard

**Features:**
- 2 octaves (C4-B5)
- White and black keys
- Visual feedback on click
- Responsive layout

**Implementation Details:**

```typescript
// Key positioning calculation for black keys
const leftOffset = (whiteKeyIndex + 1) * 48.5 + (whiteKeyIndex + 1) * 2 - 16;
```

Black keys are absolutely positioned between white keys using calculated offsets.

#### 4. `pages/Home.tsx` - Main Application

**State Management:**

```typescript
const [melody, setMelody] = useState<Note[]>([])
const [harmony, setHarmony] = useState<Note[]>([])
const [selectedHarmonyType, setSelectedHarmonyType] = useState("third")
const [isPlaying, setIsPlaying] = useState(false)
const [melodyVolume, setMelodyVolume] = useState(1.0)
const [harmonyVolume, setHarmonyVolume] = useState(0.7)
```

**User Flow:**

```
1. User clicks piano key
   → handleNoteClick()
   → Add note to melody
   → Play note sound

2. User selects harmony type
   → setSelectedHarmonyType()

3. User clicks "Generate Harmony"
   → handleGenerateHarmony()
   → Call API
   → Update harmony state

4. User clicks "Play"
   → handlePlay()
   → audioEngine.playWithHarmony()
```

---

## Harmony Algorithms Explained

### 1. Parallel Intervals (Third, Fifth, Fourth, Sixth)

**Concept:** Move each harmony note by a fixed interval from the melody.

**Implementation:**
```python
def _generate_parallel_interval(self, melody_notes, semitones):
    for melody_note in melody_notes:
        m21_note = note.Note(melody_note['pitch'])
        harmony_pitch = m21_note.pitch.transpose(-semitones)
        # Add to harmony
```

**Examples:**
- Third (3 semitones down): C4 → A3
- Fifth (7 semitones down): C4 → F3
- Fourth (5 semitones up): C4 → F4

### 2. Contrary Motion

**Concept:** When melody goes up, harmony goes down (and vice versa).

**Algorithm:**
1. Start harmony at a fifth below first melody note
2. For each subsequent note:
   - Calculate melody interval (current - previous)
   - Move harmony in opposite direction by same interval

**Example:**
```
Melody:   C4 → E4 → G4
          (0)  (+4) (+3)
Harmony:  F3 → C#3 → B♭2
          (0)  (-4) (-3)
```

**Implementation:**
```python
melody_interval = curr_melody.pitch.ps - prev_melody.pitch.ps
new_harmony_pitch = prev_harmony.pitch.transpose(-melody_interval)
```

### 3. Oblique Motion

**Concept:** Harmony stays on one pitch while melody moves.

**Implementation:**
```python
pedal_pitch = first_melody.pitch.transpose(-7)  # Fifth below
for melody_note in melody_notes:
    harmony_notes.append(pedal_pitch)  # Same pitch for all
```

### 4. Pedal Tone

**Concept:** A single sustained bass note throughout the melody.

**Implementation:**
```python
min_pitch = min([note.pitch.ps for note in melody_notes])
pedal_pitch = min_pitch - 12  # Octave below lowest note
total_duration = sum(note.duration for note in melody_notes)
return [{'pitch': pedal_pitch, 'duration': total_duration, 'offset': 0}]
```

---

## Future Development Roadmap

### Phase 1: Audio Export (High Priority)

**Goal:** Allow users to download their harmonized melodies.

**Implementation Steps:**

1. **Backend: Generate audio files**
   ```python
   from music21 import midi
   
   def export_to_midi(melody, harmony):
       stream = music21.stream.Stream()
       # Add melody and harmony parts
       stream.write('midi', fp='output.mid')
   ```

2. **Frontend: Trigger download**
   ```typescript
   async function downloadAudio(format: 'mp3' | 'midi') {
       const response = await fetch('/export', {
           method: 'POST',
           body: JSON.stringify({ melody, harmony, format })
       })
       const blob = await response.blob()
       // Trigger download
   }
   ```

3. **Required Libraries:**
   - Backend: `pydub` (for MP3), `music21` (for MIDI)
   - Frontend: Browser's `Blob` API

### Phase 2: Recording Input

**Goal:** Let users record melodies via microphone.

**Technologies:**
- `Web Audio API` (MediaRecorder)
- `music21` pitch detection
- Or use external API like Google Cloud Speech-to-Text

**Challenges:**
- Pitch detection accuracy
- Rhythm quantization
- Noise filtering

### Phase 3: Advanced Harmony Styles

**Ideas:**
- **Jazz voicings:** 7th chords, extensions (9th, 11th, 13th)
- **Gospel:** Call-and-response patterns
- **Barbershop:** Close harmony with overtones
- **Classical:** Species counterpoint rules

**Implementation:**
Each style would be a new method in `HarmonyGenerator` with specific music theory rules.

### Phase 4: Machine Learning

**Goal:** Learn harmony styles from real music.

**Approach:**
1. Train a model on MIDI datasets (e.g., Lakh MIDI Dataset)
2. Use sequence-to-sequence architecture (e.g., Transformer)
3. Input: melody → Output: harmony

**Libraries:**
- TensorFlow / PyTorch
- Magenta (Google's music ML library)

---

## Performance Optimization

### Backend

**Current Performance:**
- Harmony generation: ~10ms for 10-note melody
- API response time: ~50ms

**Optimization Opportunities:**

1. **Caching:**
   ```python
   from functools import lru_cache
   
   @lru_cache(maxsize=1000)
   def generate_harmony_cached(melody_tuple, harmony_type):
       # Convert tuple back to list
       melody = list(melody_tuple)
       return generate_harmony(melody, harmony_type)
   ```

2. **Async Processing:**
   For long melodies, use background tasks:
   ```python
   from fastapi import BackgroundTasks
   
   @app.post("/generate-harmony-async")
   async def generate_async(request, background_tasks):
       task_id = uuid4()
       background_tasks.add_task(process_harmony, task_id, request)
       return {"task_id": task_id}
   ```

### Frontend

**Current Performance:**
- Initial load: ~2s
- Piano key response: <50ms
- Audio playback latency: ~100ms

**Optimization Opportunities:**

1. **Code Splitting:**
   ```typescript
   const Piano = lazy(() => import('./components/Piano'))
   ```

2. **Memoization:**
   ```typescript
   const MemoizedPiano = React.memo(Piano)
   ```

3. **Audio Buffer Preloading:**
   Preload common notes on app start.

---

## Troubleshooting

### Common Issues

#### 1. "No sound when clicking piano keys"

**Cause:** Web Audio API not initialized (requires user interaction).

**Solution:** The app initializes audio on first key click. Check browser console for errors.

**Debug:**
```typescript
console.log('Audio context state:', Tone.context.state)
// Should be "running" after first click
```

#### 2. "CORS error when calling API"

**Cause:** Backend CORS not configured for frontend origin.

**Solution:** Update `main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Add your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

#### 3. "Harmony generation fails with 'Invalid pitch'"

**Cause:** music21 doesn't recognize the pitch format.

**Solution:** Ensure pitches are in format: `C4`, `D#5`, `Bb3` (note name + octave).

**Debug:**
```python
from music21 import note
try:
    n = note.Note('C4')
    print(n.pitch.nameWithOctave)
except:
    print("Invalid pitch format")
```

#### 4. "Frontend can't connect to backend"

**Checklist:**
- [ ] Backend server is running (`python -m app.main`)
- [ ] Backend is on port 8000
- [ ] Frontend API URL is correct (`http://localhost:8000`)
- [ ] No firewall blocking the connection

**Test:**
```bash
curl http://localhost:8000/health
# Should return: {"status":"healthy"}
```

---

## Testing Strategy

### Backend Tests

**Unit Tests (pytest):**

```python
# tests/test_harmony_engine.py
def test_third_harmony():
    generator = HarmonyGenerator()
    melody = [{'pitch': 'C4', 'duration': 1.0, 'offset': 0.0}]
    harmony = generator.generate_harmony(melody, HarmonyType.THIRD)
    assert harmony[0]['pitch'] == 'A3'

def test_contrary_motion():
    generator = HarmonyGenerator()
    melody = [
        {'pitch': 'C4', 'duration': 1.0, 'offset': 0.0},
        {'pitch': 'E4', 'duration': 1.0, 'offset': 1.0}
    ]
    harmony = generator.generate_harmony(melody, HarmonyType.CONTRARY)
    # First note should be fifth below
    assert harmony[0]['pitch'] == 'F3'
    # Second note should move opposite direction
    # (melody up 4 semitones → harmony down 4 semitones)
```

**API Tests:**

```python
from fastapi.testclient import TestClient

def test_generate_harmony_endpoint():
    client = TestClient(app)
    response = client.post("/generate-harmony", json={
        "melody": [{"pitch": "C4", "duration": 1.0, "offset": 0.0}],
        "harmony_type": "third"
    })
    assert response.status_code == 200
    assert "harmony" in response.json()
```

### Frontend Tests

**Component Tests (Vitest + React Testing Library):**

```typescript
import { render, fireEvent } from '@testing-library/react'
import Piano from './Piano'

test('piano key click triggers callback', () => {
  const handleClick = vi.fn()
  const { getByText } = render(<Piano onNoteClick={handleClick} />)
  
  fireEvent.click(getByText('C4'))
  expect(handleClick).toHaveBeenCalledWith('C4')
})
```

---

## Deployment Guide

### Backend Deployment (Example: Railway / Render)

1. **Add `Procfile`:**
   ```
   web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```

2. **Environment Variables:**
   - `PORT` (auto-set by platform)

3. **Deploy:**
   ```bash
   git push railway master
   ```

### Frontend Deployment (Example: Vercel / Netlify)

1. **Update API URL:**
   ```typescript
   const API_BASE_URL = import.meta.env.VITE_API_URL || 'https://your-backend.railway.app'
   ```

2. **Build:**
   ```bash
   pnpm build
   ```

3. **Deploy:**
   ```bash
   vercel deploy
   ```

---

## Additional Resources

### Music Theory
- [Music21 Documentation](https://web.mit.edu/music21/doc/)
- [Harmony in Music (Wikipedia)](https://en.wikipedia.org/wiki/Harmony)

### Web Audio
- [Tone.js Documentation](https://tonejs.github.io/)
- [Web Audio API (MDN)](https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API)

### FastAPI
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

---

**Happy Developing! 🎵**
