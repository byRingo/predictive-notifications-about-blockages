from fastapi import FastAPI, Request
from typing import Dict, Any
import pandas as pd
import numpy as np
import json
from statistics import median
from datetime import datetime, timedelta
import os
import httpx

app = FastAPI()

PERCENTAGES_FILE = 'percentages.json'

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


# @app.post("/create_new_ticket")
# async def new_ticket(request: Request):
#     params = request.query_params
#     api_url = f'https://lk-hackaton.ujin.tech/api/v1/tck/bms/tickets/create/?{params}'
#     if True:
#         create_new_ticket(api_url, number=1)


async def create_new_ticket(token: str, number: int = 1):
    api_url = f'https://lk-hackaton.ujin.tech/api/v1/tck/bms/tickets/create/?{token}'
    async with httpx.AsyncClient() as client:
        response = await client.post(api_url, data={
            {
                "title": "Заявка для проведения сантехнического обслуживания",
                "description": f"Засор общей системы канализации подъезда №{number}",
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
            }
        })
        return response
