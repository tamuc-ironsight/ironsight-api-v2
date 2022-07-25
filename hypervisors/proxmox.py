#!/usr/bin/env python3
import requests
import os
from dotenv import load_dotenv
load_dotenv()

"""_summary_
    This is the Proxmox hypervisor communication interface for the Ironsight API.
    It is responsible for communicating with Proxmox for VM and container management.
"""

# Create Proxmox class
class Proxmox:

    # Initialize Proxmox class
    def __init__(self):
        # Get hypervisor URL from class constructor
        self.hypervisor_url = os.getenv("HYPERVISOR_URL")
        # Get hypervisor API key from class constructor
        self.hypervisor_token_id = os.getenv("HYPERVISOR_TOKEN_ID")
        self.hypervisor_secret_key = os.getenv("HYPERVISOR_SECRET_KEY")
        # Set up hypervisor URL / URL schema
        self.url_schema = "{hypervisor_url}/api2/json/{resource}"

    def get_json(self, url):
        # Get JSON from Proxmox API
        response = requests.get(url, headers={"Accept": "application/json", "Authorization": f"PVEAPIToken={self.hypervisor_token_id}={self.hypervisor_secret_key}"})
        # Return JSON
        return response.json()

    # Get resource from Proxmox API
    def get_resource(self, resource):
        return self.get_json(self.url_schema.format(hypervisor_url=self.hypervisor_url, resource=resource))

    # Get Proxmox summary from Proxmox API
    def get_summary(self):
        summary_response = {
            "hypervisor": "Proxmox",
            "hypervisor_url": self.hypervisor_url,
            "hypervisor_api_url": self.url_schema.format(hypervisor_url=self.hypervisor_url, resource=""),
            "version": self.get_version().get("data").get("version"),
        }
        return summary_response
    # Get version from Proxmox API
    def get_version(self):
        return self.get_resource("version")

    # Get VMs from Proxmox API
    def get_vms(self):
        return self.get_resource("nodes/{node}/qemu")
