# Email Spam Classifier

## 📧 Project Overview
Email Spam Classifier is a machine learning application that automatically classifies emails as **spam** or **not spam**. The project uses text preprocessing, TF-IDF vectorization, and a trained classification model to make real-time predictions. It includes both a FastAPI backend and an interactive HTML frontend for easy email classification.

## 📁 Project Structure
```
Email_Spam_Classifier/
├── src/emailClassifier/              # Main package
│   ├── components/
│   │   ├── data_ingestion.py         # Data loading and preprocessing
│   │   ├── data_transformation.py    # Text cleaning, vectorization, and saving
│   │   ├── data_validation.py        # Data validation logic
│   │   └── model_trainer.py          # Model training and evaluation
│   ├── pipeline/
│   │   └── prediction_pipeline.py    # Production prediction pipeline
│   └── utils/                        # Utility functions
├── artifact/                         # Trained models and data
│   ├── build_model/                  # Trained model and vectorizer
│   ├── data_ingestion/               # Ingested data
│   ├── data_transformation/          # Transformed data files
│   ├── data_validation/              # Validation status
│   └── model_evaluation/             # Model metrics
├── templates/
│   └── index.html                    # Web UI for email classification
├── config/
│   └── config.yaml                   # Configuration settings
├── research/                         # Jupyter notebooks for experimentation
│   ├── experiment.ipynb              # Experimental analysis
│   └── trials.ipynb                  # Trial runs
├── main.py                           # Main entry point for all pipelines
├── app.py                            # FastAPI application
├── setup.py                          # Package setup configuration
├── template.py                       # Template configuration and structure
├── schema.yaml                       # Data validation schema
├── params.yaml                       # Algorithm parameters
├── requirements.txt                  # Project dependencies
└── LICENSE                           # Project license
```

## Environment setup for the project
1. Install conda environment
```bash
conda create -p env python==3.12 -y
```

2. Activate the conda environment
```bash
conda activate env/
```

3. install the required library for the project
```bash
pip install -r requirements.txt
```


### To test the Email Classifier
1. Start the server
```bash
uvicorn app:app --reload
```

2. Run the HTML using
```bash
python -m http.server 5500
```