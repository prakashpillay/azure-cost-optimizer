# Azure Cost Optimizer

This project helps analyze Azure resource usage over the past 3 months and generates a prompt that can be sent to an OpenAI model for actionable cost optimization suggestions.

## Components

- **Backend**: Python (FastAPI) deployed to Azure Web App
- **Frontend**: React + Tailwind UI deployed via Vercel

## Features

- Fetches all Azure resources and usage data using Azure SDKs
- Summarizes cost and usage by service
- Generates structured prompt for AI-based cost saving recommendations
- API-first design with GitHub Actions CI/CD ready

## Deployment Targets

- **API**: Azure Web App (Python 3.11, Linux)
- **Frontend**: Vercel (React)

## Usage

1. Clone this repo
2. Deploy the backend to Azure using GitHub Actions or CLI
3. Connect the frontend to the deployed API

