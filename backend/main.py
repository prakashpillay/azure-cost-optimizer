
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.consumption import ConsumptionManagementClient
from datetime import datetime, timedelta
import pandas as pd

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SubscriptionRequest(BaseModel):
    subscriptionId: str

def get_resources(subscription_id):
    credential = DefaultAzureCredential()
    client = ResourceManagementClient(credential, subscription_id)
    resources = client.resources.list()
    return [{
        "name": r.name,
        "type": r.type,
        "location": r.location,
        "resource_group": r.id.split("/")[4],
        "id": r.id
    } for r in resources]

def get_usage(subscription_id, start_date, end_date):
    credential = DefaultAzureCredential()
    client = ConsumptionManagementClient(credential, subscription_id)
    usage = client.usage_details.list(
        expand="properties/meterDetails",
        start_date=start_date,
        end_date=end_date
    )
    data = []
    for item in usage:
        data.append({
            "resource_id": item.instance_id,
            "meter_category": item.meter_details.meter_category if item.meter_details else None,
            "usage_quantity": item.quantity,
            "cost": item.pretax_cost,
            "date": item.usage_start
        })
    return pd.DataFrame(data)

def create_prompt(df):
    summary = df.groupby(["type", "meter_category"]).agg({"cost": "sum", "usage_quantity": "sum"}).reset_index()
    prompt = "Here is a summary of Azure resource usage over the past 3 months:\n\n"
    for _, row in summary.iterrows():
        prompt += f"- Resource Type: {row['type']}, Category: {row['meter_category']}, Cost: ${row['cost']:.2f}, Usage: {row['usage_quantity']:.2f} units\n"
    prompt += "\nPlease suggest ways to optimize costs, including identifying idle or oversized resources, and opportunities for reserved pricing."
    return prompt

@app.post("/api/generate-prompt")
async def generate_prompt(req: SubscriptionRequest):
    sub_id = req.subscriptionId
    end_date = datetime.utcnow().date()
    start_date = end_date - timedelta(days=90)

    resources = get_resources(sub_id)
    usage_df = get_usage(sub_id, start_date.isoformat(), end_date.isoformat())
    res_df = pd.DataFrame(resources)
    combined = usage_df.merge(res_df, how="left", left_on="resource_id", right_on="id")

    prompt = create_prompt(combined)
    return {"prompt": prompt}
