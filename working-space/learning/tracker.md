# Learning Tracker

Last updated: 2026-05-24

Mapping to Google Calendar events:
- **AI VIETNAM** → Tuesday/Thursday evening study "AI VIETNAM"
- **DSP Coursera** → Monday/Wednesday/Friday evening study "DSP Coursera"
- **Speech Processing** → Tuesday/Thursday evening study "Speech Processing"

---

## AI VIETNAM (AIO-2024)

Repo: `/home/heigatvu/MyFile/my-project/my-assistance/working-space/learning/AIO-2024/implment-algorithm`

| Status | Topic | Details |
|--------|-------|---------|
| ✅ Done | Logistic regression | basic + advanced (mini-batch, batch) |
| ✅ Done | Softmax regression | 1D, multi-class, simple-version |
| ✅ Done | PyTorch framework + regression metrics | Basic PyTorch warm-up complete |
| ✅ Done | PyTorch: linear regression, logistic regression, softmax | Run regression/softmax models with PyTorch |
| 🔄 Current | TA-exercise + multilayer perceptron | Course exercises + MLP implementation with PyTorch |

Key files:
- `deep-learning/2_softmax-regression/basic/1_softmaxRegression-1D-2class.ipynb` ✅
- `deep-learning/2_softmax-regression/simple-version.ipynb` ✅

---

## DSP Coursera (Digital Signal Processing)

Repo: `/home/heigatvu/MyFile/my-project/my-assistance/working-space/learning/DSP-coursera`

| Status | Topic | Details |
|--------|-------|---------|
| 🔄 Current | Course 1, Week 1 | ks-algorithm, signal-transmission basics |
| ⏳ Next | Course 1, Week 1 | Complete signal-transmission, start week-2 |

Key files:
- `course-1/week-1/ks-algorithm.ipynb`
- `course-1/week-1/signal-transmission.ipynb`

---

## Practice Speech Processing

Repo: `/home/heigatvu/MyFile/my-project/my-assistance/working-space/learning/practice-speech-processing`

| Status | Topic | Details |
|--------|-------|---------|
| ✅ Done | MFCCs | Cepstrum and MFCC implementation complete |
| 🔄 Current | Speech representations | Linear prediction coding (LPC) |
| ⏳ Next | Fundamental Frequency (F0) | Finish LPC, then move to F0 estimation |

Key files:
- `speech-representations/cepstrum-MFCCs.ipynb`
- `speech-representations/linear_prediction.ipynb`
- `speech-representations/helper_functions.ipynb`

---

## How to update

Tell Hermes:

```
Update learning tracker: [course] — completed [topic], next [topic]
```

Example:
```
Update learning tracker: AI VIETNAM — completed softmax regression, next MLP
```

Or edit this file directly.

## How Hermes uses this

- On `/daily-brief`: reads this file to tell you what specific topic to study tonight
- On study session: reads this file + git log to tell you where to pick up
- After study: you update what you completed and what's next
