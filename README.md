# AI-Based Handwriting & Signature Authentication System

> Status: 🚧 Under active development. This README is updated at each milestone
> with real results - no numbers here are placeholders once filled in.

## 1. Project Overview
A CNN-based system that:
1. Identifies which registered user wrote a handwriting sample.
2. Identifies which registered user a signature belongs to.
3. Verifies whether an identified user's signature is genuine or forged.

## screen shots
<img width="899" height="483" alt="Screenshot 2026-09-05 131825" src="https://github.com/user-attachments/assets/ab1a10b1-edb1-4028-be52-7344eafaf4a1" />
<img width="956" height="499" alt="Screenshot 2026-09-05 132624" src="https://github.com/user-attachments/assets/5c431236-a11d-452f-b2b4-53ef46d550a7" />
<img width="752" height="499" alt="Screenshot 2026-09-05 132858" src="https://github.com/user-attachments/assets/e0b5c2cb-11f5-432e-9fbf-f297b7a43f42" />
<img width="956" height="499" alt="Screenshot 2026-09-05 132624" src="https://github.com/user-attachments/assets/06883dd9-a210-4c7a-a310-0dea55deee91" />




## 2. Problem Statement
Manual handwriting/signature verification is slow and error-prone at scale.
This project automates it using computer vision and deep learning.

## 3. Features
- Handwriting Identification (who wrote this?)
- Signature Identification (whose signature is this?)
- Signature Verification (genuine vs forged, with a validated similarity threshold)
- REST API (FastAPI)
- Responsive HTML/CSS/JS frontend
signature-authentication/
│
├── api/
│   ├── __init__.py
│   └── main.py
│
├── data/
│   └── raw/
│       └── signatures/
│           └── data/
│               └── data/
│                   ├── real/
│                   └── forged/
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── models/
│   └── signature_authentication_model.keras
│
├── notebooks/
│
├── src/
│   ├── preprocessing/
│   │   └── dataset.py
│   │
│   └── training/
│       └── train.py
│
├── tests/
│
├── screenshots/
│   ├── home.png
│   ├── prediction.png
│   └── api-docs.png
│
├── .gitignore
├── config.yaml
├── requirements.txt
└── README.md

## 5. Dataset Sources
- Handwriting: [IAM Handwritten Forms Dataset](https://www.kaggle.com/datasets/naderabdelghany/iam-handwritten-forms-dataset)
- Signatures: [Handwritten Signature Verification](https://www.kaggle.com/datasets/tienen/handwritten-signature-verification)

Datasets are downloaded locally via `src/data_acquisition/download_kaggle.py`
and are **not** committed to this repository (see `.gitignore`).

## 6. Dataset Preparation
_To be filled in once the raw dataset structure has been inspected (Step 6)._

## 7. Image Preprocessing
Pipeline: Resize -> Grayscale -> Noise Removal -> Thresholding -> Normalization.
Implemented in `src/preprocessing/`, shared between training and inference.

## 8. CNN Architecture
```
Input -> Conv2D(32) -> ReLU -> MaxPool
      -> Conv2D(64) -> ReLU -> MaxPool
      -> Conv2D(128) -> ReLU -> MaxPool
      -> Flatten -> Dense(128) -> Dropout -> Dense(num_users) -> Softmax
```

## 9. Signature Verification Methodology
_To be filled in with the actual embedding approach and the validated
similarity threshold once Step 13 is complete._

## 10. Training
_To be filled in with real training logs/results (Steps 8-11)._

## 11. Evaluation Metrics
_To be filled in with real Accuracy / Precision / Recall / F1 / Confusion
Matrix (handwriting) and Accuracy / Precision / Recall / F1 / FAR / FRR
(signature verification), computed on unseen test data._

## 12. API Endpoints

### `POST /predict-handwriting`
```json
{
  "user": "User_02",
  "confidence": 0.92
}
```

### `POST /verify-signature`
```json
{
  "user": "User_02",
  "status": "genuine",
  "confidence": 0.91,
  "similarity": 0.91
}
```

## 13. Frontend
Plain HTML/CSS/JavaScript (no framework), served as static files, communicating
with FastAPI via `fetch()`.

## 14. Project Structure
```
AI-Handwriting-Signature-Authentication/
├── data/
│   ├── raw/            (gitignored)
│   └── processed/      (gitignored)
├── notebooks/
├── src/
│   ├── data_acquisition/
│   ├── preprocessing/
│   ├── training/
│   ├── prediction/
│   ├── evaluation/
│   └── utils/
├── models/              (large artifacts gitignored, see below)
├── api/
├── frontend/
├── tests/
├── config.yaml
├── requirements.txt
└── README.md
```

## 15. Installation
```
conda create -p ai_cnn_proj python=3.11 -y
conda activate ./ai_cnn_proj
pip install -r requirements.txt
```

## 16. Running the Project
_To be filled in once the API and frontend are complete (Steps 15-19)._

## 17. Example API Responses
_See section 12 above; will be updated with real captured responses._

## 18. Screenshots
_To be added once the frontend is built._

## 19. Future Improvements
- Mobile-camera-based verification
- OCR integration
- Cheque/document authentication use cases

## 20. Limitations
_To be filled in honestly based on real evaluation results (e.g. dataset size,
class imbalance, generalization to unseen writers)._

## 21. License / Dataset Attribution
Datasets used under their respective Kaggle licenses/terms - see the dataset
pages linked above for details.
