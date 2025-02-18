import argparse
from app.CmdExecutor import CmdExecutor


VM_PATHS = {
    'dpiui2': '/home/irbis-eh/Desktop/Vm/dpiui2/'
}


def vm_run_command(vm_name):
    vm_path = None
    cmd = f'vmrun -T ws start {vm_path}'
    result = CmdExecutor().execute(cmd)

    if result and result.success:
        print(f'vm {vm_name} is running')
    else:
        print(result)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('command', type=str, help='Exec some single command')
    parser.add_argument('-n', '--vm_name', type=str, help='Name of vm')

    args = parser.parse_args()

    cmd = args.get('command', None)
    vm_name = args.get('name', None)

    if cmd and cmd == 'vm_run':
        if vm_name:
            pass
        else:
            print('Please specify vm_name')
    else:
        print('Please specify command')



if __name__ == '__main__':
    main()