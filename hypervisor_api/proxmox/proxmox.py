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

    def get_resource(self, resource, params=None):
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
                                "Accept": "application/json", "Authorization": f"PVEAPIToken={self.hypervisor_token_id}={self.hypervisor_secret_key}"}, params=params, verify=False)
        # Check for error in response
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            print(f"Response: {response.text}")
            return {"error": response.status_code, "response": response.text}
        return response.json()

    def post_resource(self, resource, data=None):
        """_summary_
            Post a resource to the Proxmox API.

            Args:
                resource (str): Resource to post.

            Returns:
                dict: Result of the API call.
        """
        url = self.url_schema.format(
            hypervisor_url=self.hypervisor_url, resource=resource)
        response = requests.post(url, headers={
            "Accept": "application/json", "Authorization": f"PVEAPIToken={self.hypervisor_token_id}={self.hypervisor_secret_key}"}, data=data, verify=False)
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
        return self.get_resource("nodes").get("data")

    def get_node(self, node_name):
        """_summary_
            Get a node from the hypervisor.

            Args:
                node_name (str): Name of the node.

            Returns:
                dict: Node status/details.
        """
        return self.get_resource(f"nodes/{node_name}/status").get("data")

    def get_vms(self):
        """_summary_
            Get virtual machines from the hypervisor.

            Returns:
                list: List of virtual machines.
        """
        node_list = self.get_nodes()
        # Parse node list to pull out node names
        node_names = [node.get("node") for node in node_list]
        # Get virtual machines from each node and merge into one list
        vm_list = []
        for node in node_names:
            vm_data = self.get_resource(f"nodes/{node}/qemu").get("data")
            # Append VM data to list
            for vm in vm_data:
                vm['node'] = node
                # Sort VM data by key
                vm = dict(sorted(vm.items()))
                vm_list.append(vm)
        # Return VM list
        return vm_list

    def get_vms_on_node(self, node_name):
        """_summary_
            Get all virtual machines from a node.

            Args:
                node_name (str): Name of the node.

            Returns:
                list: List of virtual machines.
        """
        vm_list = self.get_resource(f"nodes/{node_name}/qemu").get("data")
        for vm in vm_list:
            vm['node'] = node_name
            # Sort VM data by key
            vm = dict(sorted(vm.items()))
        return vm_list

    def get_vm_by_id(self, node_name, vm_id):
        """_summary_
            Get a virtual machine from the hypervisor by ID.

            Args:
                node_name (str): Name of the node.
                vm_id (int): ID of the virtual machine.

            Returns:
                dict: Virtual machine status/details.
        """
        vm_data = self.get_resource(
            f"nodes/{node_name}/qemu/{vm_id}/status/current").get("data")
        vm_data['node'] = node_name
        return vm_data

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
        # Cant get VM by name, so get all VMs and loop through them to get the ID
        vm_list = self.get_vms()
        for vm in vm_list:
            if vm.get("name") == vm_name:
                return self.get_vm_by_id(vm.get("node"), vm.get("vmid"))
        return None

    def get_templates(self):
        """_summary_
            Get templates from the hypervisor.

            Returns:
                list: List of templates.
        """
        # Get list of VMs, if template=1 then it is a template
        vm_list = self.get_vms()
        template_list = [vm for vm in vm_list if vm.get("template") == 1]
        return template_list

    def start_vm(self, vm_name):
        """_summary_
            Power on a virtual machine.

            Args:
                vm_name (str): Name of the virtual machine.
        """
        try:
            vm_id = self.get_vm_by_name(vm_name).get("vmid")
            node_name = self.get_vm_by_name(vm_name).get("node")
        except:
            print(f"Error: VM {vm_name} not found")
            return {"error": "VM not found"}
        response = self.post_resource(
            f"nodes/{node_name}/qemu/{vm_id}/status/start")
        return response

    def stop_vm(self, vm_name):
        """_summary_
            Power off a virtual machine.

            Args:
                vm_name (str): Name of the virtual machine.
        """
        try:
            vm_id = self.get_vm_by_name(vm_name).get("vmid")
            node_name = self.get_vm_by_name(vm_name).get("node")
        except:
            print(f"Error: VM {vm_name} not found")
            return {"error": "VM not found"}
        response = self.post_resource(
            f"nodes/{node_name}/qemu/{vm_id}/status/stop")
        return response

    def reboot_vm(self, vm_name):
        """_summary_
            Reboot a virtual machine.

            Args:
                vm_name (str): Name of the virtual machine.
        """
        try:
            vm_id = self.get_vm_by_name(vm_name).get("vmid")
            node_name = self.get_vm_by_name(vm_name).get("node")
        except:
            print(f"Error: VM {vm_name} not found")
            return {"error": "VM not found"}
        response = self.post_resource(
            f"nodes/{node_name}/qemu/{vm_id}/status/reboot")
        return response

    def create_vm(self, vm_name, template_name):
        """_summary_
            Create a virtual machine from a template.

            Args:
                template_name (str): Name of the template.
                vm_name (str): Name of the virtual machine.
        """
        try:
            template_vm_data = self.get_vm_by_name(template_name)
            template_id = template_vm_data.get("vmid")
            node_name = template_vm_data.get("node")
        except:
            print(f"Error: Template {template_name} not found")
            return {"error": "Template not found"}

        # Get a VMID not being used by any VM
        vm_list = self.get_vms()
        vm_ids = [vm.get("vmid") for vm in vm_list]
        vm_id = max(vm_ids) + 1

        # Parameters for creating a VM are newid, node and vmid
        params = {
            "newid": vm_id,
            "node": node_name,
            "vmid": template_id,
            "name": vm_name
        }

        response = self.post_resource(
            f"nodes/{node_name}/qemu/{template_id}/clone", params)
        return response

    def create_vnc_proxy(self, vm_name):
        """_summary_
            Create a VNC proxy for a virtual machine.

            Args:
                vm_name (str): Name of the virtual machine.
        """
        try:
            vm_id = self.get_vm_by_name(vm_name).get("vmid")
            node_name = self.get_vm_by_name(vm_name).get("node")
        except:
            print(f"Error: VM {vm_name} not found")
            return {"error": "VM not found"}
        response = self.post_resource(
            f"nodes/{node_name}/qemu/{vm_id}/vncproxy")
        return response

    def configure_vnc(self, vm_name, port):
        """_summary_
            Configure VNC for a virtual machine.

            Args:
                vm_name (str): Name of the virtual machine.
                port (int): VNC port.
                password (str): VNC password.
        """
        print("Configuring VNC")
        try:
            vm_id = self.get_vm_by_name(vm_name).get("vmid")
            node_name = self.get_vm_by_name(vm_name).get("node")
        except:
            print(f"Error: VM {vm_name} not found")
            return {"error": "VM not found"}
        params = {
            "args": "-vnc 0.0.0.0:{}".format(port)
        }
        response = self.post_resource(
            f"nodes/{node_name}/qemu/{vm_id}/config", params)
        return response

    def get_vm_config(self, vm_name):
        """_summary_
            Get configuration for a virtual machine.

            Args:
                vm_name (str): Name of the virtual machine.
        """
        try:
            vm_id = self.get_vm_by_name(vm_name).get("vmid")
            node_name = self.get_vm_by_name(vm_name).get("node")
        except:
            print(f"Error: VM {vm_name} not found")
            return {"error": "VM not found"}
        response = self.get_resource(
            f"nodes/{node_name}/qemu/{vm_id}/config")
        return response