from app.Modules.VMModule.VMController import VMController
import subprocess
import os
import fcntl

def make_non_blocking(file_obj):
    fd = file_obj.fileno()
    flags = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, flags | os.O_NONBLOCK)

if __name__ == '__main__':
    controller = VMController()

    vm_list = controller.get_vm_list(verbose=True)

    for vm in vm_list:
        controller.start_vm(vm, verbose=True)

    controller.get_running_vm_list(verbose=True)

    for vm in vm_list:
        controller.stop_vm(vm, verbose=True)

    controller.get_running_vm_list(verbose=True)

    vm_list = controller.get_running_vm_list(verbose=True)

    for vm in vm_list:
        controller.stop_vm(vm, verbose=True)
        controller.get_running_vm_list(verbose=True)

    for vm in vm_list:
        controller.start_vm(vm, verbose=True)
        controller.get_running_vm_list(verbose=True)
