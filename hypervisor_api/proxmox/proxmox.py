#!/usr/bin/env python3

import requests
import os
from loguru import logger
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
        self.hypervisor_auth = os.getenv("HYPERVISOR_AUTH")
        self.hypervisor_token = os.getenv("HYPERVISOR_TOKEN")
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
                                "Accept": "application/json", "Authorization": self.hypervisor_auth}, params=params)
        # Check for error in response
        if response.status_code != 200:
            logger.error(f"Error: {response.status_code}")
            logger.error(f"Response: {response.text}")
            return {"status": "error", "error": response.status_code, "response": response.text}
        response = response.json()
        response['status'] = "success"
        return response

    def post_resource(self, resource, data=None, params=None):
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
            "Accept": "application/json", "Authorization": self.hypervisor_auth, "CSRFPreventionToken": self.hypervisor_token}, data=data, params=params)
        # Check for error in response
        if response.status_code != 200:
            logger.error(f"Error: {response.status_code}")
            logger.error(f"Response: {response.text}")
            return {"status": "error", "error": response.status_code, "response": response.text}
        response = response.json()
        response['status'] = "success"
        return response

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

    def get_node(self, node_name):
        """_summary_
            Get a node from the hypervisor.

            Args:
                node_name (str): Name of the node.

            Returns:
                dict: Node status/details.
        """
        return self.get_resource(f"nodes/{node_name}/status")

    @logger.catch
    def get_vms(self):
        """_summary_
            Get virtual machines from the hypervisor.

            Returns:
                list: List of virtual machines.
        """
        node_list = self.get_nodes().get("data")
        # Parse node list to pull out node names
        try:
            node_names = [node.get("node") for node in node_list]
        except Exception as e:
            logger.error(e)
            return {"status": "error", "error": e, "data": []}
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
        return {"status": "success", "data": vm_list}

    def get_vms_on_node(self, node_name):
        """_summary_
            Get all virtual machines from a node.

            Args:
                node_name (str): Name of the node.

            Returns:
                list: List of virtual machines.
        """
        vm_list = self.get_resource(f"nodes/{node_name}/qemu")
        if vm_list.get("status") == "success":
            for vm in vm_list.get("data"):
                vm['node'] = node_name
                # Sort VM data by key
                vm = dict(sorted(vm.items()))
            return vm_list
        else:
            return {"status": "error", "error": vm_list.get("error"), "response": vm_list.get("response")}

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
            f"nodes/{node_name}/qemu/{vm_id}/status/current")
        if vm_data.get("status") == "error":
            return {"status": "error", "error": vm_data.get("error"), "response": vm_data.get("response")}
        vm_data = vm_data.get("data")
        vm_data['node'] = node_name
        return {"status": "success", "data": vm_data}

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
        vm_list = self.get_vms().get("data")
        for vm in vm_list:
            if vm.get("name") == vm_name:
                vm_data = self.get_vm_by_id(
                    vm.get("node"), vm.get("vmid")).get("data")
                return {"status": "success", "data": vm_data}
        return {"status": "error", "error": "VM not found"}

    def get_templates(self):
        """_summary_
            Get templates from the hypervisor.

            Returns:
                list: List of templates.
        """
        # Get list of VMs, if template=1 then it is a template
        vm_list = self.get_vms().get("data")
        template_list = [vm for vm in vm_list if vm.get("template") == 1]
        return template_list

    def start_vm(self, vm_name):
        """_summary_
            Power on a virtual machine.

            Args:
                vm_name (str): Name of the virtual machine.
        """
        try:
            vm_data = self.get_vm_by_name(vm_name).get("data")
            vm_id = vm_data.get("vmid")
            node_name = vm_data.get("node")
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
            vm_data = self.get_vm_by_name(vm_name).get("data")
            vm_id = vm_data.get("vmid")
            node_name = vm_data.get("node")
        except:
            print(f"Error: VM {vm_name} not found")
            return {"error": "VM not found"}
        print("Stopping VM...")
        print(f'"nodes/{node_name}/qemu/{vm_id}/status/stop')
        response = self.post_resource(
            f"nodes/{node_name}/qemu/{vm_id}/status/stop")
        return response

    def power_toggle_vm(self, vm_name):
        """_summary_
            Toggle power on/off a virtual machine.

            Args:
                vm_name (str): Name of the virtual machine.
        """
        try:
            vm_data = self.get_vm_by_name(vm_name).get("data")
            vm_id = vm_data.get("vmid")
            node_name = vm_data.get("node")
        except:
            print(f"Error: VM {vm_name} not found")
            return {"error": "VM not found"}
        # If VM is running, power off
        if vm_data.get("status") == "running":
            print(f"Powering off VM {vm_name}")
            response = self.post_resource(
                f"nodes/{node_name}/qemu/{vm_id}/status/stop")
        # Else power on
        else:
            print(f"Powering on VM {vm_name}")
            response = self.post_resource(
                f"nodes/{node_name}/qemu/{vm_id}/status/start")
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
        vm_list = self.get_vms().get("data")
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
        try:
            vm_id = self.get_vm_by_name(vm_name).get("vmid")
            node_name = self.get_vm_by_name(vm_name).get("node")
        except:
            print(f"Error: VM {vm_name} not found")
            return {"error": "VM not found"}
        # Subtract 5900 from the port, Proxmox adds 5900 to the arg
        port = int(port) - 5900
        params = {
            "args": "-vnc 0.0.0.0:{}".format(port)
        }
        response = self.post_resource(
            f"nodes/{node_name}/qemu/{vm_id}/config", params=params)
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

    def get_summary(self):
        """_summary_
            Get usage summary for all nodes/VMs (realtime).
        """
        response = self.get_resource("cluster/resources")
        return response

    def get_usage_graph(self, node_name=None):
        """_summary_
            Get usage graph for a node.
        """

        # Init in case something goes wrong
        graph_data = None

        # If node name is provided, get usage graph for a specific node
        if node_name:
            graph_data = self.get_resource(f"nodes/{node_name}/rrddata?timeframe=hour&cf=AVERAGE")
            if graph_data.get("status") == "error":
                logger.error(f"Error: Node {node_name} not found")
                return {"status": "error", "error": "Node not found", "data": []}
            graph_data["node"] = node_name
            response = graph_data

        # If no node name is provided, get usage graph for all nodes
        else:
            graph_data = []
            # Get a list of nodes
            node_list = self.get_nodes()
            if node_list.get("status") == "error":
                logger.error(f"Error: Node list could not be retrieved")
                return {"status": "error", "error": "Node list could not be retrieved", "data": []}
            else:
                node_list = node_list.get("data")
            # Get usage graph for each node
            for node in node_list:
                node_name = node.get("node")
                temp_data = {}
                temp_data["data"] = self.get_resource(f"nodes/{node_name}/rrddata?timeframe=hour&cf=AVERAGE").get("data")
                temp_data["node"] = node_name
                graph_data.append(temp_data)
            response = {"status": "success", "data": graph_data}
        
        return response

    def get_vm_usage_graph(self, vm_name=None):
        """_summary_
            Get usage graph for a virtual machine.
        """
        graph_data = None
        if vm_name:
            try:
                vm_id = self.get_vm_by_name(vm_name).get("data").get("vmid")
                node_name = self.get_vm_by_name(vm_name).get("data").get("node")
            except:
                print(f"Error: VM {vm_name} not found")
                return {"error": "VM not found"}
            graph_data = self.get_resource(
                f"nodes/{node_name}/qemu/{vm_id}/rrddata?timeframe=hour&cf=AVERAGE")
        else:
            # Get all of the VM graph usage and return it in a list
            graph_data = []
            vm_list = self.get_vms().get("data")
            for vm in vm_list:
                vm_id = vm.get("vmid")
                node_name = vm.get("node")
                temp_data = {}
                temp_data["data"] = self.get_resource(
                    f"nodes/{node_name}/qemu/{vm_id}/rrddata?timeframe=hour&cf=AVERAGE").get("data")
                temp_data["node"] = node_name
                temp_data["vm_name"] = vm.get("name")
                graph_data.append(temp_data)
        return graph_data