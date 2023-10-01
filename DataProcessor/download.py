import os
import pandas as pd
import requests

# Define the folder where you want to save the videos
output_folder = "videos"

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Load the Excel file into a DataFrame
excel_file = "data/output-excel.csv"  # Replace with the path to your Excel file
df = pd.read_csv(excel_file)

# Loop through each row in the DataFrame
for index, row in df.iterrows():
    # Get the video name from column one
    video_name = str(row[0])
    
    # Get the download link from the Excel sheet
    download_link = row[1]
    
    # Create the full path to save the video
    video_path = os.path.join(output_folder, f"{video_name}.mp4")
    
    # Download the video
    try:
        response = requests.get(download_link)
        if response.status_code == 200:
            with open(video_path, 'wb') as video_file:
                video_file.write(response.content)
            print(f"Downloaded: {video_name}")
        else:
            print(f"Failed to download: {video_name} (Status Code: {response.status_code})")
    except Exception as e:
        print(f"Failed to download: {video_name} (Error: {str(e)})")

print("Download process completed.")
