#!/usr/bin/env python3

"""_summary_
    This is the Harvester HCI hypervisor communication interface for the Ironsight API.
    It is responsible for communicating with Harvester for VM and container management.
"""

# Create Harvester class
class Harvester:
    # Create function for getting Harvester version using Fast API
    def get_version(self):
        return "4.0.0"