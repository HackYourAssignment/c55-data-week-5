# AI Assist Report

> Task 8: Fill in all three sections below. Your reflection should be specific —
> describe exactly what you asked, what the AI returned, and what you changed.
> "The AI fixed it" is not enough detail.

## The prompt I gave

After building the Docker image successfully, I received authentication errors when running the container. The pipeline worked locally, but inside Docker Azure authentication failed with DefaultAzureCredential. why Docker could not access the Azure data

## The code or suggestion it returned

ChatGPT first suggested using local sample CSV files instead of downloading data from Azure Blob Storage.

## What I changed after reviewing it

I reviewed the suggestions and decided to keep the Azure download functionality instead of switching to local sample data. I created a .env file and configured the Azure service-principal credentials so Docker could authenticate with Azure.
