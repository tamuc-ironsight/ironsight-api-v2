#!/usr/bin/env python3

"""_summary_
    This is the hypervisor interface for the Ironsight API.
    It is responsible for communicating with the hypervisor.
    This allows for the hypervisor to be swapped out without
    having to change the code.
"""

def init_hypervisor(hypervisor):
    """_summary_
        This function gets the hypervisor from the environment
        variables.
    """
    try:
        if hypervisor == "proxmox":
            from hypervisor_api.proxmox.proxmox import Proxmox
            return Proxmox()
        else:
            raise Exception("Hypervisor not found.")
    except Exception as e:
        print(e)
        return None
