#!/usr/bin/env python3

import hypervisor_api
from fastapi import FastAPI
import os
import json
from dotenv import load_dotenv
load_dotenv()

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


# Set up API routes
@ironsight_api.get("/")
async def root():
    return {"description": "Ironsight API", "api_version": API_VERSION, "hypervisor": hypervisor.get_summary()}


@ironsight_api.get("/health")
async def health():
    return {"status": "ok"}


# Set up hypervisor APIs
@ironsight_api.get("/nodes")
async def get_nodes():
    return hypervisor.get_nodes()


@ironsight_api.get("/nodes/{node_name}")
async def get_node(node_name: str):
    return hypervisor.get_node(node_name)


@ironsight_api.get("/nodes/{node_name}/vms")
async def get_vms(node_name: str):
    return hypervisor.get_vms_on_node(node_name)


@ironsight_api.get("/nodes/{node_name}/vms/{vm_id}")
async def get_vm(node_name: str, vm_id: int):
    return hypervisor.get_vm_by_id(node_name, vm_id)


@ironsight_api.get("/vms")
async def get_vms():
    return hypervisor.get_vms()


@ironsight_api.get("/vms/{vm_name}")
async def get_vm_by_name(vm_name: str):
    return hypervisor.get_vm_by_name(vm_name)
