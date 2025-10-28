# Contributing to Harmony Helper

Thank you for your interest in contributing to Harmony Helper! This document provides guidelines and instructions for contributing to the project.

## 🎯 Ways to Contribute

There are many ways to contribute to Harmony Helper:

- **Report bugs** or suggest features by opening issues
- **Improve documentation** (README, code comments, tutorials)
- **Add new harmony algorithms** (e.g., jazz voicings, gospel progressions)
- **Enhance the UI/UX** (design improvements, accessibility)
- **Write tests** to improve code coverage
- **Fix bugs** or implement new features

## 🚀 Getting Started

### 1. Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/harmony-helper.git
   cd harmony-helper
   ```

3. Add the upstream repository:
   ```bash
   git remote add upstream https://github.com/LLuCCKKyyyy/harmony-helper.git
   ```

### 2. Set Up Development Environment

**Backend:**
```bash
cd backend
pip install -r requirements.txt
python -m app.main  # Test that it runs
```

**Frontend:**
```bash
cd harmony-helper-frontend
pnpm install
pnpm dev  # Test that it runs
```

### 3. Create a Branch

Create a descriptive branch name:
```bash
git checkout -b feature/add-jazz-voicings
# or
git checkout -b fix/piano-keyboard-alignment
```

## 📝 Development Guidelines

### Code Style

**Python (Backend):**
- Follow PEP 8
- Use type hints where possible
- Write docstrings for all functions and classes
- Keep functions focused and single-purpose

**TypeScript/React (Frontend):**
- Use functional components with hooks
- Follow the existing component structure
- Use meaningful variable names
- Keep components small and reusable

### Commit Messages

Write clear, descriptive commit messages:

```
✅ Good:
- "Add parallel sixth harmony algorithm"
- "Fix piano keyboard black key positioning"
- "Update README with installation instructions"

❌ Bad:
- "fix bug"
- "update"
- "changes"
```

### Testing

Before submitting a PR:

1. **Test your changes manually**
   - Run both backend and frontend
   - Test all affected features
   - Check for console errors

2. **Test edge cases**
   - Empty melody
   - Single note
   - Very long melodies

3. **Verify backwards compatibility**
   - Ensure existing features still work

## 🎵 Adding New Harmony Types

If you want to add a new harmony algorithm:

1. **Add the algorithm to `backend/app/harmony_engine/core.py`:**
   ```python
   class HarmonyType(Enum):
       # ... existing types ...
       YOUR_NEW_TYPE = "your_new_type"
   
   class HarmonyGenerator:
       def generate_harmony(self, melody_notes, harmony_type):
           # ... existing code ...
           elif harmony_type == HarmonyType.YOUR_NEW_TYPE:
               return self._generate_your_new_harmony(melody_notes)
       
       def _generate_your_new_harmony(self, melody_notes):
           # Your implementation here
           pass
   ```

2. **Add the type to the API response in `backend/app/main.py`:**
   ```python
   @app.get("/harmony-types")
   async def get_harmony_types():
       return {
           "harmony_types": [
               # ... existing types ...
               {
                   "value": HarmonyType.YOUR_NEW_TYPE.value,
                   "name": "Your Harmony Name",
                   "description": "Description of what it does"
               }
           ]
       }
   ```

3. **Test it:**
   ```bash
   curl -X POST "http://localhost:8000/generate-harmony" \
     -H "Content-Type: application/json" \
     -d '{
       "melody": [{"pitch": "C4", "duration": 1.0, "offset": 0.0}],
       "harmony_type": "your_new_type"
     }'
   ```

4. **Update documentation** in README.md

## 🐛 Reporting Bugs

When reporting a bug, please include:

- **Description** of the bug
- **Steps to reproduce** (be specific!)
- **Expected behavior**
- **Actual behavior**
- **Screenshots** (if applicable)
- **Environment** (OS, browser, Python version)

Example:
```markdown
**Bug:** Piano keyboard doesn't play sound on mobile Safari

**Steps to reproduce:**
1. Open the app on iPhone Safari
2. Click any piano key
3. No sound is heard

**Expected:** Should hear the note play
**Actual:** Silence

**Environment:** iOS 17.2, Safari 17.2
```

## 💡 Suggesting Features

When suggesting a feature:

- **Describe the feature** clearly
- **Explain the use case** (why is it needed?)
- **Provide examples** if possible
- **Consider implementation** (is it feasible?)

## 📥 Submitting a Pull Request

1. **Update your fork:**
   ```bash
   git fetch upstream
   git rebase upstream/master
   ```

2. **Push your branch:**
   ```bash
   git push origin feature/your-feature-name
   ```

3. **Open a Pull Request** on GitHub with:
   - Clear title describing the change
   - Description of what was changed and why
   - Screenshots/GIFs for UI changes
   - Reference to related issues (if any)

4. **Respond to feedback** from reviewers

## 🎨 UI/UX Contributions

If you're improving the UI:

- Follow the existing design language (Tailwind CSS)
- Ensure responsive design (mobile, tablet, desktop)
- Test on multiple browsers
- Consider accessibility (keyboard navigation, screen readers)
- Include before/after screenshots in your PR

## 📚 Documentation Contributions

Documentation improvements are always welcome:

- Fix typos or unclear explanations
- Add examples or tutorials
- Improve API documentation
- Translate documentation (future)

## ❓ Questions?

If you have questions about contributing:

- Open a GitHub Discussion
- Comment on an existing issue
- Reach out to the maintainers

## 🙏 Thank You!

Every contribution, no matter how small, helps make Harmony Helper better for everyone. We appreciate your time and effort!

---

**Happy Contributing! 🎵**
