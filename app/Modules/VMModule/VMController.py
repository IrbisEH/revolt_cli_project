import os
from pathlib import Path
from app.CmdExecutor import CmdExecutor


# TODO: попробовать -T ws

class VMController:
    VM_ROOT_FOLDERS = [
        '/home/irbis-eh/Desktop/Vm',
        '/home/irbis-eh/vmware'
    ]

    VM_FILE_EXT = '.vmx'

    CMD_TIMEOUT = 120

    def __init__(self):
        self.executor = CmdExecutor

    def get_running_vm_list(self, verbose=False):
        response = self.executor.execute(
            ['vmrun' 'list']
        )

        if verbose:
            print(response)

        if response.success:
            return response.stdout.splitlines()[1:]     # first line indicate total running VM

        return []

    def get_vm_list(self, verbose=False):
        vm_files = []
        for root_folder in self.VM_ROOT_FOLDERS:
            for root, _, files in os.walk(root_folder):
                for file in files:
                    if file.endswith(self.VM_FILE_EXT):
                        vm_files.append(os.path.join(root, file))

        if verbose:
            for file in vm_files:
                print(file)

        return vm_files

    def start_vm(self, vm_path, verbose=False):
        response = self.executor.execute(
            ['vmrun', 'start', vm_path, 'nogui'],
            non_blocking_mode=True,
            timeout=self.CMD_TIMEOUT
        )

        if verbose:
            print(response)

        return None

    def stop_vm(self, vm_path, verbose=False):
        response = self.executor.execute(
            ['vmrun', 'stop', vm_path],
            timeout=self.CMD_TIMEOUT
        )

        if verbose:
            print(response)

    def reload_vm(self, verbose=False):
        pass

    def clone_vm(self, verbose=False):
        pass

    def delete_vm(self, verbose=False):
        pass

    def take_snapshot(self, verbose=False):
        pass

    def get_snapshot_list(self, verbose=False):
        pass

    def go_to_snapshot(self, verbose=False):
        pass