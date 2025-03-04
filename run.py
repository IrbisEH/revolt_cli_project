from app.Modules.VMModule.VMController import VMController


if __name__ == '__main__':
    controller = VMController()

    vm_list = controller.get_running_vm_list()

    if len(vm_list):
        for vm in vm_list:
            controller.stop_vm(vm)


    vm = '/home/irbis-eh/Desktop/Vm/tacacs/tacacs.vmx'

    controller.start_vm(vm, verbose=True)




    # vm_list = controller.get_vm_list(verbose=True)
    #
    # for vm in vm_list:
    #     controller.start_vm(vm, verbose=True)
    #
    # controller.get_running_vm_list(verbose=True)
    #
    # for vm in vm_list:
    #     controller.stop_vm(vm, verbose=True)
    #
    # controller.get_running_vm_list(verbose=True)

    # vm_list = controller.get_running_vm_list(verbose=True)
    #
    # for vm in vm_list:
    #     controller.stop_vm(vm, verbose=True)
    #     controller.get_running_vm_list(verbose=True)
    #
    # for vm in vm_list:
    #     controller.start_vm(vm, verbose=True)
    #     controller.get_running_vm_list(verbose=True)
