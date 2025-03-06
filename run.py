from app.Modules.VMModule.VMController import VMController


def check_all():
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


def check_sequentially_tasks(controller, vm_list, type):

    exec_type = {
        'start': lambda x: (x, controller.start_vm),
        'stop': lambda x: (x, controller.stop_vm)
    }

    tasks = list(map(exec_type[type], vm_list))
    controller.run_sequentially(tasks, verbose=True)

if __name__ == '__main__':
    # check_all()


    controller = VMController()
    vm_list = controller.get_running_vm_list()
    if len(vm_list):
        check_sequentially_tasks(controller, vm_list, 'stop')


    vm_list = controller.get_vm_list(verbose=True)
    check_sequentially_tasks(controller, vm_list[12:], 'start')

