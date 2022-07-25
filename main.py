#!/usr/bin/env python3

from fastapi import FastAPI
import os
import json
from dotenv import load_dotenv
load_dotenv()
import hypervisors

# Get ENV variables
HYPERVISOR = os.getenv("HYPERVISOR")


# Get build information
with open("build_info.json", "r") as f:
    BUILD_INFO = f.read()
BUILD_INFO = json.loads(BUILD_INFO)
API_VERSION = BUILD_INFO["api_version"]

# Set up API
ironsight_api = FastAPI()

# Set up hypervisor object
hypervisor = hypervisors.init_hypervisor(HYPERVISOR)

@ironsight_api.get("/")
async def root():
    return {"description": "Ironsight API", "api_version": API_VERSION, "hypervisor": hypervisor.get_summary()}


@ironsight_api.get("/health")
async def health():
    return {"status": "ok"}
