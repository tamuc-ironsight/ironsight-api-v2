#!/usr/bin/env python3

import requests
import os
from dotenv import load_dotenv
load_dotenv()

"""_summary_
    This is a template hypervisor communication interface for the Ironsight API.
    It is responsible for communicating with (hypervisor here) for VM and container management.
"""

# Create HypervisorTemplate class


class HypervisorTemplate:

    # Initialize HypervisorTemplate class
    def __init__(self):
        # Get hypervisor URL from class constructor
        self.hypervisor_url = os.getenv("HYPERVISOR_URL")
        # Get hypervisor API key from class constructor
        self.hypervisor_token_id = os.getenv("HYPERVISOR_TOKEN_ID")
        self.hypervisor_secret_key = os.getenv("HYPERVISOR_SECRET_KEY")
        # Set up hypervisor URL / URL schema
        self.url_schema = "{hypervisor_url}/{resource}"

    def get_resource(self, resource, params=None):
        """_summary_
            Get a resource from the HypervisorTemplate API.

            Args:
                resource (str): Resource to get.

            Returns:
                dict: Result of the API call.
        """
        url = self.url_schema.format(
            hypervisor_url=self.hypervisor_url, resource=resource)
        response = requests.get(url, headers={
                                "Accept": "application/json", "Authorization": ""}, params=params)
        # Check for error in response
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            print(f"Response: {response.text}")
            return {"error": response.status_code, "response": response.text}
        return response.json()

    def post_resource(self, resource, data=None):
        """_summary_
            Post a resource to the HypervisorTemplate API.

            Args:
                resource (str): Resource to post.

            Returns:
                dict: Result of the API call.
        """
        url = self.url_schema.format(
            hypervisor_url=self.hypervisor_url, resource=resource)
        response = requests.post(url, headers={
            "Accept": "application/json", "Authorization": ""}, data=data)
        # Check for error in response
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            print(f"Response: {response.text}")
            return {"error": response.status_code, "response": response.text}
        return response.json()

    def get_summary(self):
        """_summary_
            Get summary from the hypervisor.

            Returns:
                dict: Summary of the hypervisor.
        """
        return None

    def get_version(self):
        """_summary_
            Get version information from the hypervisor.

            Returns:
                dict: Version information.
        """
        return None

    def get_nodes(self):
        """_summary_
            Get all nodes from the hypervisor.

            Returns:
                list: List of nodes.
        """
        return None

    def get_node(self, node_name):
        """_summary_
            Get a node from the hypervisor.

            Args:
                node_name (str): Name of the node.

            Returns:
                dict: Node status/details.
        """
        return None

    def get_vms(self):
        """_summary_
            Get virtual machines from the hypervisor.

            Returns:
                list: List of virtual machines.
        """
        return None

    def get_vms_on_node(self, node_name):
        """_summary_
            Get all virtual machines from a node.

            Args:
                node_name (str): Name of the node.

            Returns:
                list: List of virtual machines.
        """
        return None

    def get_vm_by_id(self, node_name, vm_id):
        """_summary_
            Get a virtual machine from the hypervisor by ID.

            Args:
                node_name (str): Name of the node.
                vm_id (int): ID of the virtual machine.

            Returns:
                dict: Virtual machine status/details.
        """
        return None

    def get_vm_by_name(self, vm_name):
        """_summary_
            Get a virtual machine from the hypervisor by name.
            (Warning, this is more expensive than getting by ID due to looping through all VMs/nodes.)

            Args:
                node_name (str): Name of the node.
                vm_name (str): Name of the virtual machine.

            Returns:
                dict: Virtual machine status/details.
        """
        return None

    def get_templates(self):
        """_summary_
            Get templates from the hypervisor.

            Returns:
                list: List of templates.
        """
        return None

    def start_vm(self, vm_name):
        """_summary_
            Power on a virtual machine.

            Args:
                vm_name (str): Name of the virtual machine.
        """
        return None

    def stop_vm(self, vm_name):
        """_summary_
            Power off a virtual machine.

            Args:
                vm_name (str): Name of the virtual machine.
        """
        return None

    def reboot_vm(self, vm_name):
        """_summary_
            Reboot a virtual machine.

            Args:
                vm_name (str): Name of the virtual machine.
        """
        return None

    def create_vm(self, vm_name, template_name):
        """_summary_
            Create a virtual machine from a template.

            Args:
                template_name (str): Name of the template.
                vm_name (str): Name of the virtual machine.
        """
        return None

    def create_vnc_proxy(self, vm_name):
        """_summary_
            Create a VNC proxy for a virtual machine.

            Args:
                vm_name (str): Name of the virtual machine.
        """
        return None

    def configure_vnc(self, vm_name, port):
        """_summary_
            Configure VNC for a virtual machine.

            Args:
                vm_name (str): Name of the virtual machine.
                port (int): VNC port.
                password (str): VNC password.
        """
        return None

    def get_vm_config(self, vm_name):
        """_summary_
            Get configuration for a virtual machine.

            Args:
                vm_name (str): Name of the virtual machine.
        """
        return None