import subprocess


class VmManager:
    def __init__(self):
        pass

    def refresh_dev_items(self, dev_items):
        result = subprocess.run(['vmrun', 'list'], capture_output=True, text=True)

        if not result or not result.stdout:
            print("Warning! Can not get response from vmrun")
            return

        running = {
            l.strip()
            for l in result.stdout.splitlines()
            if l.endswith('.vmx')
        }

        for obj in [i for i in dev_items if i.type == 'vmx']:
            obj.is_running = str(obj.vmx_path) in running