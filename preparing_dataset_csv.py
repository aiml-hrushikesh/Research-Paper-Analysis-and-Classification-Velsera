import os
import pandas as pd
import re

# Define base directory
base_dir = r"C:\Users\2020714\OneDrive - Revvity\Documents\Practice_self_projects\Velsera Research Paper Analysis\Research-Paper-Analysis-and-Classification-Velsera\Dataset"

# Initialize list to store data
data = []

# Loop through both categories
for folder in ["Cancer", "Non-Cancer"]:
    folder_path = os.path.join(base_dir, folder)

    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)

        try:
            # Skip system files or non-text files
            if not file_name.endswith(".txt"):
                continue  

            # Read the content of the text file with encoding handling
            with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
                content = file.read().strip()
            
            # Skip empty files
            if not content:
                print(f"Skipping empty file: {file_name}")
                continue  

            # Extract ID using regex
            doc_id_match = re.search(r"<ID:(\d+)>", content)
            doc_id = doc_id_match.group(1) if doc_id_match else "Unknown"

            # Extract Title
            title_match = re.search(r"Title:\s*(.*?)\s*Abstract:", content, re.DOTALL)
            title = f"Title: {title_match.group(1).strip()}" if title_match else "Title: Not Found"

            # Extract Abstract
            abstract_match = re.search(r"Abstract:\s*(.*)", content, re.DOTALL)
            abstract = f"Abstract: {abstract_match.group(1).strip()}" if abstract_match else "Abstract: Not Found"

            # Combine Title and Abstract properly
            full_text = f"{title} {abstract}".strip()

            # Append to dataset only if there's actual text
            if full_text and full_text != "Title: Not Found Abstract: Not Found":
                data.append([doc_id, full_text, folder])
            else:
                print(f"Skipping file with no useful data: {file_name}")

        except Exception as e:
            print(f"Error reading file {file_name}: {e}")

# Convert to DataFrame
df = pd.DataFrame(data, columns=["ID", "text", "label"])

# Save as CSV
df.to_csv("fine_tuning_data.csv", index=False, encoding="utf-8")

print("CSV file created successfully!")
