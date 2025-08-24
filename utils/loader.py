# utils/loader.py
import os
import pandas as pd

def load_all_csvs(data_folder="data"):
    """
    Loads all CSV files in the data folder.
    Returns:
        data (dict): {category_name: DataFrame}
    """
    data = {}
    if not os.path.exists(data_folder):
        raise FileNotFoundError(f"Data folder '{data_folder}' not found.")

    for file in os.listdir(data_folder):
        if file.endswith(".csv"):
            category = file.replace(".csv", "").lower()
            df = pd.read_csv(os.path.join(data_folder, file), encoding='latin1')
            data[category] = df.fillna("Unknown")  # handle missing values
    return data


def prepare_docs_from_data(data, include_columns=None):
    """
    Converts DataFrames into text docs for embeddings.
    Args:
        data (dict): {category: DataFrame}
        include_columns (list): Columns to include in doc (optional)
    Returns:
        docs (list of Document): Document objects ready for embeddings
    """
    from langchain.schema import Document
    docs = []
    for category, df in data.items():
        for _, row in df.iterrows():
            # If no columns specified, use default
            if include_columns is None:
                include_columns = ["Product Name", "Company", "Range", "SkinType"]

            details = []
            for col in include_columns:
                if col in row:
                    details.append(f"{col}: {row[col]}")

            text = f"Category: {category}, " + ", ".join(details)
            docs.append(Document(page_content=text, metadata={"category": category}))
    return docs
