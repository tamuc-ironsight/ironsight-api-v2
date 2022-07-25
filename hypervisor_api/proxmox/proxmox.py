#!/usr/bin/env python3
from lib2to3.pytree import Node
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

    def get_resource(self, resource):
        """_summary_
            Get a resource from the Proxmox API.

            Args:
                resource (str): Resource to get.

            Returns:
                dict: Result of the API call.
        """
        url = self.url_schema.format(
            hypervisor_url=self.hypervisor_url, resource=resource)
        response = requests.get(url, headers={
                                "Accept": "application/json", "Authorization": f"PVEAPIToken={self.hypervisor_token_id}={self.hypervisor_secret_key}"})
        return response.json()

    def get_summary(self):
        """_summary_
            Get summary from the hypervisor.

            Returns:
                dict: Summary of the hypervisor.
        """
        summary_response = {
            "hypervisor": "Proxmox",
            "hypervisor_url": self.hypervisor_url,
            "hypervisor_api_url": self.url_schema.format(hypervisor_url=self.hypervisor_url, resource=""),
            "version": self.get_version().get("data").get("version"),
        }
        return summary_response

    def get_version(self):
        """_summary_
            Get version information from the hypervisor.

            Returns:
                dict: Version information.
        """
        return self.get_resource("version")

    def get_nodes(self):
        """_summary_
            Get all nodes from the hypervisor.

            Returns:
                list: List of nodes.
        """
        return self.get_resource("nodes")

    def get_vms(self):
        """_summary_
            Get virtual machines from the hypervisor.

            Returns:
                list: List of virtual machines.
        """
        node_list = self.get_nodes()
        # Parse node list to pull out node names
        node_names = [node.get("node") for node in node_list.get("data")]
        # Get virtual machines from each node and merge into one list
        vm_list = []
        for node in node_names:
            vm_data = self.get_resource(f"nodes/{node}/qemu")
            vm_data = vm_data.get("data")
            # Append VM data to list
            for vm in vm_data:
                vm['node'] = node
                vm_list.append(vm)
        # Return VM list
        return vm_list
