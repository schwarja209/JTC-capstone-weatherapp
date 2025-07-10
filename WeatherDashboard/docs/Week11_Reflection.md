# Week 11 Reflection

## Section 0: Fellow Details

| Field                   | Your Entry                 |
|-------------------------|----------------------------|
| Name                    | Jacob Schwartz             |
| GitHub Username         | schwarja209                |
| Preferred Feature Track | Data/Visual/Smart          |
| Team Interest           | No                         |


## Section 1: Week 11 Reflection

**Key Takeaways:**
- This capstone prioritizes architectural planning over strict assignment-style coding.
- GitHub structure and documentation matter as much as functional code.
- Features will be used to practice key areas from the class material, not just UI polish.
- Scoping will be crucial, to handle complexity.
- Everything will be built around a core loop (along the lines of user input → weather fetch → response).
- Partners are required for a later collaborative feature.

**Concept Connections:**
- Strongest: Tkinter GUI design, class-based structure within a given file.
- Need more practice: Algorithms, error handling and calling/referencing multiple different files/packages as I go.
- Also could improve testing.  I have no experience with that yet.

**Early Challenges:**
- Initial confusion around the fact that openweather does not have free historical data.
- How to construct precipitation values (if any), due to number imperfect of options on openweather.
- Managing folder structure for modular code while avoiding circular imports and repeated code.
- Pushing to GitHub had a fast-forward error that required a pull and merge.
- Avoiding feature creep.

**Support Strategies:**
- Consult online example projects for file structure best practices.
- consult with classmates and TAs on decisions around precipitation values, historical data, and other road blocks
- Refer to previous weeks' assignments (HW8 and HW10 in particular) for my core template.

---

## Section 2: Feature Selection Rationale

| # | Feature Name          | Difficulty (1–3) | Why You Chose It / Learning Goal |
|---|-----------------------|------------------|----------------------------------|
| 1 | Theme Switcher        | 2 | I think it offers the most flexibility in terms of interpretation, and provides a clear structure for other features. |
| 2 | Tomorrow’s Guess      | 3 | Good practice for machine learning, and easily fits into my theme framework. |
| 3 | Weather History Tracker | 1 | Necessary for effective machine learning, and in lieu of such data being available through openweather. |
| Enh | Badge or Achievement System | – | An idea I have to gamify both themes differently and reward user exploration or perserverance (will tie in with a throwback to my impossible button). |

---

## Section 3: High-Level Architecture Sketch

### Core Structure
- `/main.py`: App entry point
- `/config.py`: App constants and default settings
- `/data/`: Stored outputs (e.g., weather history)
- `/services/`: API and simulation logic (e.g., `weather_api.py`, `sample_generator.py`)
- `/features/`: Modular feature scripts (e.g., `theme_switcher.py`, `tomorrows_guess.py`)
- `/gui/`: Main GUI composition and control logic
- `/widgets/`: Reusable UI components
- `/utils/`: Shared helper functions and formatters
- `/tests/`: Unit tests and integration checks

### Flow
1. `main.py` initializes app and GUI
2. GUI loads default theme → pulls from `features/theme_switcher.py`
3. User interacts (e.g., updates weather, toggles theme)
4. Data flow: API/Simulated fetch → UI update → optional logging/prediction

---

## Section 4: Data Model Plan

| File/Table Name        | Format | Example Row                                   |
|------------------------|--------|----------------------------------------------|
| `data.txt`             | txt    | Time: 2025-06-29 21:00:00 ... (full summary) |
| `weather_history.csv`  | csv    | 2025-06-09,New Brunswick,78,Sunny            |
| `badges_unlocked.json` | json   | {"grit_mode": true, "first_guess": "correct"} |

---

## Section 5: Personal Project Timeline

| Week | Monday         | Tuesday        | Wednesday      | Thursday       | Key Milestone              |
|------|----------------|----------------|----------------|----------------|----------------------------|
| 12   | Refactor Main  | Refactor Main  | Theme handler  | Layout switch  | Refactored core app supports both UIs |
| 13   | History creation | History creation | History fetch | Integration with sim | Transition from simulated to historical data |
| 14   | Prediction logic | Prediction logic | Integration with history | Integration with history | Prediciton feature complete    |
| 15   | Theme development | Theme development | Badge logic | Badge Logic | All features implemented   |
| 16   | Tests          | README/docs    | .env cleanup   | Packaging      | App is production-ready    |
| 17   | Rehearse       | Demo prep      | Showcase       | —              | Demo Day                   |

---

## Section 6: Risk Assessment

| Risk                 | Likelihood | Impact | Mitigation Plan                                     |
|----------------------|------------|--------|-----------------------------------------------------|
| API Rate Limit       | Medium     | Medium | Add delays, fallback to simulated data              |
| Feature Scope Creep  | High       | Medium | Create basic features early, expand if time permits |
| Tkinter/Theme Bugs   | Medium     | Medium | Isolate widget creation, test events independently  |

---

## Section 7: Support Requests

- How to test tkinter GUIs without full integration testing
- Advice on saving and loading historical data and integrating it with simulated data (initially)
- Cleanest way to log and read past weather from text vs JSON
- How to reuse UI components without cross-file spaghetti

---

## Section 8: Before Monday (Start of Week 12)

- `main.py` and `config.py` pushed to repo root
- core structure laid out
- `/data/` folder created
- `.env` file contains API key (not committed)
- `/features/` folder created with starter files
- README.md (first draft) committed

---

## Final Submission Checklist

✅ `Week11_Reflection.md` completed  
✅ File uploaded to GitHub repo `/docs/`  
✅ Repo link submitted on Canvas
