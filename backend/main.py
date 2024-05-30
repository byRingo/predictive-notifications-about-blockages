from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
from typing import Dict, Any
import pandas as pd
import numpy as np
import json
from statistics import median
from datetime import datetime, timedelta
import os
import httpx

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTION"],
    allow_headers=["*"],
)

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

    flag = True
    for day in median_values:
        if day < percentage_values["50%"]:
            flag = False
            break
    
    if flag:
        resp = await create_new_ticket('ust-739111-c7b6945a90129919f7811aa2941542ed', 1)

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
        "percentage_last_day": percentage,
        "ticket_response": resp
    }  
    
@app.get("/test_info")
async def test_info():
    # Fetch the JSON data from the provided URL
    try:
        response = requests.get(DATA_URL)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data: {str(e)}")
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Error decoding JSON data")

    # Process the JSON data into a DataFrame
    records = []
    for day, events in data.items():
        for event_id, event_details in events.items():
            timestart = event_details['alert']['timestart']
            timestop = event_details['alert']['timestop']
            duration = timestop - timestart
            records.append([int(day), timestart, timestop, duration])

    df = pd.DataFrame(records, columns=['day', 'timestart', 'timestop', 'duration'])

    # Get unique days and ensure there are enough data points
    unique_days = sorted(df['day'].unique())
    if len(unique_days) < 80:
        raise HTTPException(status_code=400, detail="Not enough data for the last 80 days")

    # Get the last 20, 40, 60, and 80 days
    days_to_check = unique_days[-80:][::20]
    days_data = df[df['day'].isin(days_to_check)]

    # Calculate the median duration for the selected days
    median_duration_days = days_data.groupby('day')['duration'].apply(median).to_dict()

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

    # Calculate percentages for each selected day
    percentages = {}
    for day in days_to_check:
        day_duration = median_duration_days.get(day, None)
        if day_duration is not None:
            if max_duration != min_duration:  # Avoid division by zero
                percentage = ((day_duration - min_duration) / (max_duration - min_duration)) * 100
            else:
                percentage = 100  # If all values are the same, consider it 100%
            # Bound the percentage between 0% and 100%
            percentage = max(0, min(100, percentage))
            percentages[int(day)] = percentage  # Convert day to int for JSON serialization

    return {
        "percentages": percentages
    }


async def create_new_ticket(token: str, number: int = 1):
    api_url = f'https://lk-hackaton.ujin.tech/api/v1/tck/bms/tickets/create/?{token}'
    async with httpx.AsyncClient() as client:
        response = await client.post(api_url, data={
            "title": "Заявка для проведения сантехнического обслуживания",
            "description": "Засор общей системы канализации подъезда №1",
            "priority": "high",
            "class": "default",
            "status": "new",
            "initiator.id": None,
            "types": [
                {
                "types": 1
                }
            ],
            "assignees": [
                {
                "assignees": 1
                }
            ],
            "contracting_companies": [
                {
                "id": None
                }
            ],
            "objects": [
                {
                "type": "complex"
                },
                {
                "id": number
                }
            ],
            "planned_start_at": None,
            "planned_end_at": None,
            "hide_planned_at_from_resident": None,
            "extra": None
        })
        return response
