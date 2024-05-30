from fastapi import FastAPI, HTTPException
import requests
from typing import Dict, Any
import pandas as pd
import numpy as np
import json
from statistics import median
from datetime import datetime, timedelta
import os

app = FastAPI()

PERCENTAGES_FILE = 'percentages.json'
DATA_URL = "http://dev-rkld.ru/hackathon/data-three.json"

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/analyze-duration")
async def analyze_duration():
    file_path = 'data.json'  # Update the file path if necessary

    # Load the JSON data
    with open(file_path, 'r') as file:
        data = json.load(file)

    records = []
    for day, events in data.items():
        for event_id, event_details in events.items():
            timestart = event_details['alert']['timestart']
            timestop = event_details['alert']['timestop']
            duration = timestop - timestart
            records.append([int(day), timestart, timestop, duration])

    # Create a DataFrame from the records
    df = pd.DataFrame(records, columns=['day', 'timestart', 'timestop', 'duration'])

    # Calculate median duration for each day
    median_duration_per_day = df.groupby('day')['duration'].apply(median).to_dict()

    # Calculate the average of median durations
    median_values = list(median_duration_per_day.values())
    average_median_duration = np.mean(median_values)
    
    # Calculate the 0%, 50%, and 100% values
    min_duration = min(median_values)
    max_duration = max(median_values)
    median_duration = np.mean(median_values)

    # Save the 0%, 50%, and 100% values to a JSON file
    percentage_values = {
        "0%": min_duration,
        "50%": median_duration,
        "100%": max_duration
    }

    with open(PERCENTAGES_FILE, 'w') as file:
        json.dump(percentage_values, file)

    # Analyze the sequence to find the condition
    days = list(median_duration_per_day.keys())
    durations = list(median_duration_per_day.values())

    for i in range(2, len(durations)):
        if durations[i] > average_median_duration and durations[i-1] > average_median_duration and durations[i-2] > average_median_duration:
            current_day = days[i]
            min_duration = min(durations)
            max_duration = max(durations)
            if max_duration != min_duration:  # Avoid division by zero
                percentage = ((durations[i] - min_duration) / (max_duration - min_duration)) * 100
            else:
                percentage = 100  # If all values are the same, consider it 100%
            return {
                "day": current_day,
                "percentage": percentage
            }

    return {
        "message": "No such sequence found"
    }
    
@app.get("/get-percentages")
async def get_percentages():
    if os.path.exists(PERCENTAGES_FILE):
        with open(PERCENTAGES_FILE, 'r') as file:
            percentage_values = json.load(file)
        return percentage_values
    else:
        return {"message": "Percentage values not found."}
    
@app.get("/latest_info")
async def latest_info():
    # Fetch the JSON data from the provided URL
    try:
        response = requests.get(DATA_URL)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data: {str(e)}")
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Error decoding JSON data")

    records = []
    for day, events in data.items():
        for event_id, event_details in events.items():
            timestart = event_details['alert']['timestart']
            timestop = event_details['alert']['timestop']
            duration = timestop - timestart
            records.append([int(day), timestart, timestop, duration])

    # Create a DataFrame from the records
    df = pd.DataFrame(records, columns=['day', 'timestart', 'timestop', 'duration'])
    
    # Get the last three days
    unique_days = df['day'].unique()
    if len(unique_days) < 3:
        raise HTTPException(status_code=400, detail="Not enough data for the last three days")
    
    last_three_days = unique_days[-3:]
    last_three_days_data = df[df['day'].isin(last_three_days)]

    # Calculate the median duration for the last three days
    median_duration_last_three_days = last_three_days_data.groupby('day')['duration'].apply(median).to_dict()

    # Calculate the median of the medians
    median_values = list(median_duration_last_three_days.values())

    # Load the saved percentage values
    if os.path.exists(PERCENTAGES_FILE):
        try:
            with open(PERCENTAGES_FILE, 'r') as file:
                percentage_values = json.load(file)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Error decoding JSON data")
    else:
        raise HTTPException(status_code=404, detail="Percentage values not found")

    min_duration = percentage_values["0%"]
    max_duration = percentage_values["100%"]

    # Calculate the percentage for the last day
    last_day_duration = median_duration_last_three_days[last_three_days[-1]]

    if max_duration != min_duration:  # Avoid division by zero
        percentage = ((last_day_duration - min_duration) / (max_duration - min_duration)) * 100
    else:
        percentage = 100  # If all values are the same, consider it 100%

    # Bound the percentage between 0% and 100%
    percentage = max(0, min(100, percentage))
    
    print(min_duration, max_duration, last_day_duration)

    return {
        "percentage_last_day": percentage
    }   