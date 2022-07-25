#!/usr/bin/env python3

from fastapi import FastAPI
import os
import json
from dotenv import load_dotenv
load_dotenv()
import hypervisor_api

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
hypervisor = hypervisor_api.init_hypervisor(HYPERVISOR)

@ironsight_api.get("/")
async def root():
    return {"description": "Ironsight API", "api_version": API_VERSION, "hypervisor": hypervisor.get_summary()}


@ironsight_api.get("/health")
async def health():
    return {"status": "ok"}


@ironsight_api.get("/nodes")
async def get_nodes():
    return hypervisor.get_nodes()

@ironsight_api.get("/vms")
async def get_vms():
    return hypervisor.get_vms()
