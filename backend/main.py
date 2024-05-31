import random
from fastapi import FastAPI, File, HTTPException, UploadFile, Depends
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
MAINTENANCE_FILE = 'maintenances.json'

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/analyze-duration")
async def analyze_duration():
    file_path = 'data.json'

    with open(file_path, 'r') as file:
        data = json.load(file)

    records = []
    for day, events in data.items():
        for event_id, event_details in events.items():
            timestart = event_details['alert']['timestart']
            timestop = event_details['alert']['timestop']
            duration = timestop - timestart
            records.append([int(day), timestart, timestop, duration])

    df = pd.DataFrame(records, columns=['day', 'timestart', 'timestop', 'duration'])

    median_duration_per_day = df.groupby('day')['duration'].apply(median).to_dict()

    median_values = list(median_duration_per_day.values())
    average_median_duration = np.mean(median_values)
    
    min_duration = min(median_values)
    max_duration = max(median_values)
    median_duration = np.mean(median_values)

    percentage_values = {
        "0%": min_duration,
        "50%": median_duration,
        "100%": max_duration
    }

    with open(PERCENTAGES_FILE, 'w') as file:
        json.dump(percentage_values, file)

    days = list(median_duration_per_day.keys())
    durations = list(median_duration_per_day.values())

    for i in range(2, len(durations)):
        if durations[i] > average_median_duration and durations[i-1] > average_median_duration and durations[i-2] > average_median_duration:
            current_day = days[i]
            min_duration = min(durations)
            max_duration = max(durations)
            if max_duration != min_duration: 
                percentage = ((durations[i] - min_duration) / (max_duration - min_duration)) * 100
            else:
                percentage = 100
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

    df = pd.DataFrame(records, columns=['day', 'timestart', 'timestop', 'duration'])
    
    unique_days = df['day'].unique()
    if len(unique_days) < 3:
        raise HTTPException(status_code=400, detail="Not enough data for the last three days")
    
    last_three_days = unique_days[-3:]
    last_three_days_data = df[df['day'].isin(last_three_days)]

    median_duration_last_three_days = last_three_days_data.groupby('day')['duration'].apply(median).to_dict()

    median_values = list(median_duration_last_three_days.values())

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


    last_day_duration = median_duration_last_three_days[last_three_days[-1]]

    if max_duration != min_duration:
        percentage = ((last_day_duration - min_duration) / (max_duration - min_duration)) * 100
    else:
        percentage = 100

    percentage = max(0, min(100, percentage))
    
    print(min_duration, max_duration, last_day_duration)

    flag = True
    for day in median_values:
        if day < percentage_values["50%"]:
            flag = False
            break

    if flag:
        resp = await create_new_ticket('ust-739111-c7b6945a90129919f7811aa2941542ed')
        await send_message()
    else:
        resp = "Не получилось создать тикет..."

    return {
        "percentage_last_day": percentage
    }  

@app.get("/test_info")
async def test_info():
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

    df = pd.DataFrame(records, columns=['day', 'timestart', 'timestop', 'duration'])

    unique_days = sorted(df['day'].unique())
    if len(unique_days) < 80:
        raise HTTPException(status_code=400, detail="Not enough data for the last 80 days")

    days_to_check = random.sample(unique_days, 4)
    days_data = df[df['day'].isin(days_to_check)]

    median_duration_days = days_data.groupby('day')['duration'].apply(median).to_dict()

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

    percentages = {}
    for day in days_to_check:
        day_duration = median_duration_days.get(day, None)
        if day_duration is not None:
            if max_duration != min_duration:
                percentage = ((day_duration - min_duration) / (max_duration - min_duration)) * 100
            else:
                percentage = 100
            percentage = max(0, min(100, percentage))
            percentages[int(day)] = percentage

    return {
        "percentages": percentages
    }


async def create_new_ticket(token: str):
    api_url = f'https://api-uae-test.ujin.tech/api/v1/tck/bms/tickets/create/?token={token}'

    # respns = requests.post(api_url, data={
    #     "title": "Заявка на сантехническое обслуживание",
    #     "description": "Есть вероятность засора канализации, необходимо вызвать сантехническую службу",
    #     "priority": "high",
    #     "class": "inspection",
    #     "status": "new",
    #     "initiator.id": 739111,
    #     "types": [],
    #     "assignees": [],
    #     "contracting_companies": [],
    #     "objects": [
    #         {
    #         "type": "building",
    #         "id": 47
    #         }
    #     ],
    #     "planned_start_at": "",
    #     "planned_end_at": "",
    #     "hide_planned_at_from_resident": "",
    #     "extra": ""
    # })
    async with httpx.AsyncClient() as client:
        respns = await client.post(api_url, json={
            "title": "Заявка на сантехническое обслуживание",
            "description": "Есть вероятность засора канализации, необходимо вызвать сантехническую службу",
            "priority": "high",
            "class": "inspection",
            "status": "new",
            "initiator.id": 739111,
            "types": [],
            "assignees": [],
            "contracting_companies": [],
            "objects": [
                {
                "type": "building",
                "id": 47
                }
            ],
            "planned_start_at": "",
            "planned_end_at": "",
            "hide_planned_at_from_resident": "",
            "extra": ""
        })

    respns = respns.json()

    print(respns)
    return respns


async def send_message():
    api_url = f'https://im-uae-test.ujin.tech/sendMessage'
    async with httpx.AsyncClient() as client:
        respns = await client.post(api_url, json={
            "channel_key": "251",
            "text": "К вам в ближайшее время придет мастер-сантехник, чтобы провести необходимые сантехнические работы. Возможно отключение горячей и холодной воды.",
            "attachment": {},
            "is_hidden": False
            },
            headers={"Authorization": "Token ust-739111-c7b6945a90129919f7811aa2941542ed"}
        )

    respns = respns.json()

    return respns



@app.get("/new_maintenance_date")
async def new_maintenance_date(pipe_id: int, date: str):
    # Load existing maintenance data
    if os.path.exists(MAINTENANCE_FILE):
        with open(MAINTENANCE_FILE, 'r') as file:
            try:
                maintenance_data = json.load(file)
            except json.JSONDecodeError:
                maintenance_data = {}
    else:
        maintenance_data = {}

    maintenance_data[f"object_{pipe_id}"] = date

    with open(MAINTENANCE_FILE, 'w') as file:
        json.dump(maintenance_data, file, indent=4)

    return {"message": f"Maintenance date for object {pipe_id} updated to {date}."}

@app.post("/upload-data")
async def upload_data(file: UploadFile = File(...)):
    if file.content_type != 'application/json':
        raise HTTPException(status_code=400, detail="Invalid file type. Only JSON files are allowed.")
    
    try:
        contents = await file.read()
        data = json.loads(contents)
        
        with open('data.json', 'w') as f:
            json.dump(data, f)
        
        return {"message": "File uploaded successfully"}
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Error decoding JSON data")