#!/usr/bin/env python3

import hypervisor_api
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
import json
import sys
from loguru import logger
from dotenv import load_dotenv
load_dotenv()


# Get ENV variables
SERVER_PORT = os.getenv("SERVER_PORT")
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

# Node management APIs

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


# Template management APIs


@ironsight_api.get("/templates")
async def get_templates():
    return hypervisor.get_templates()


# VM management APIs

@ironsight_api.get("/vms")
async def get_vms():
    return hypervisor.get_vms()


@ironsight_api.get("/vms/{vm_name}")
async def get_vm_by_name(vm_name: str):
    return hypervisor.get_vm_by_name(vm_name)


@ironsight_api.post("/vms/{vm_name}/start")
async def start_vm(vm_name: str):
    return hypervisor.start_vm(vm_name)


@ironsight_api.post("/vms/{vm_name}/stop")
async def stop_vm(vm_name: str):
    return hypervisor.stop_vm(vm_name)


@ironsight_api.post("/vms/{vm_name}/toggle_power")
async def power_toggle_vm(vm_name: str):
    return hypervisor.power_toggle_vm(vm_name)


@ironsight_api.post("/vms/{vm_name}/reboot")
async def reboot_vm(vm_name: str):
    return hypervisor.reboot_vm(vm_name)


@ironsight_api.post("/vms/create")
async def create_vm(vm_name: str, template_name: str):
    return hypervisor.create_vm(vm_name, template_name)


@ironsight_api.post("/vms/{vm_name}/vnc")
async def configure_vnc(vm_name: str, port: int):
    return hypervisor.configure_vnc(vm_name, port)


@ironsight_api.get("/vms/{vm_name}/config")
async def get_vm_config(vm_name: str):
    return hypervisor.get_vm_config(vm_name)


@ironsight_api.get("/usage")
async def get_usage_graph():
    return hypervisor.get_usage_graph()


@ironsight_api.get("/usage/{node_name}")
async def get_usage_graph(node_name: str):
    return hypervisor.get_usage_graph(node_name)


@logger.catch
def main():
    uvicorn.run(ironsight_api, host="0.0.0.0", port=int((SERVER_PORT)))


if __name__ == "__main__":
    logger.add(
        sys.stderr, format="{time} {level} {message}", filter="my_module", level="INFO")
    main()
