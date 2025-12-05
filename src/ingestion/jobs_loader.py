# src/ingestion/jobs_loader.py
import pandas as pd

def load_jobs(path="data/jobs.csv"):
    return pd.read_csv(path)
