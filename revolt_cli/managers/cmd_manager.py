class CmdManager:
    SEP = ' '

    def __init__(self):
        self.modules = []

    def parse_cmd(self, line):
        line = line.strip()
        if line == '':
            return []
        return line.split(self.SEP)

    def exec(self, line):
        args = self.parse_cmd(line)
        try:
            if not len(args):
                raise AttributeError('No arguments provided.')

            command = args.pop(0)

            if not hasattr(self, command) or not callable(getattr(self, command)):
                raise AttributeError(f'Unknown command: {command}')

            action = getattr(self, command)
            response = action(args)
            result = 0, response

        except AttributeError as e:
            response = f'Error! {e}'
            result = 0, response
        except Exception as e:
            response = f'Error! Failed to execute command "{args}" Exception: {e}'
            result = 1, response


        return result

    def exit(self, *args, **kwargs):
        exit(0)