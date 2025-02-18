import subprocess

# TODO: type notation in args

INDENT_CHAR = ' '
IN_DEEP_PROPS_INDENT = 2

class Error:
    def __init__(self, msg=None, code=None) -> None:
        self.msg = msg
        self.code = code

    def __str__(self, indent_multi=0) -> str:
        res = ''
        for key in self.__dict__.keys():
            value = getattr(self, key)
            res += f'{INDENT_CHAR * indent_multi}{key}: {value}'
            res += '\n'

        return res


class ExecuteResult:
    def __init__(self, **kwargs: dict) -> None:
        self.cmd = kwargs.get('cmd', None)
        self.stdout = kwargs.get('stdout', None)
        self.stderr = kwargs.get('stderr', None)

        if kwargs.get('error_msg', None) or kwargs.get('error_code', None):
            self.error = Error(
                msg=kwargs.get('error_msg', None),
                code=kwargs.get('error_code', None)
            )
        else:
            self.error = None

        for key in ['stdout', 'stderr']:
            prop = getattr(self, key)
            prop = prop.strip() if prop else None
            setattr(self, key, prop)

    def __str__(self, indent_multi=0) -> str:
        res = ''
        for key in self.__dict__.keys():
            value = getattr(self, key)
            if isinstance(value, Error):
                res += f'{INDENT_CHAR * indent_multi}{key}:\n'
                _indent = indent_multi + len(key) + IN_DEEP_PROPS_INDENT
                res += value.__str__(_indent)
            else:
                res += f'{INDENT_CHAR * indent_multi}{key}: {value}'

            res += '\n'

        return res


class CmdExecutor:
    @staticmethod
    def execute(command: str) -> ExecuteResult:
        try:
            res = subprocess.run(command,
                                 shell=True,
                                 check=True,
                                 capture_output=True,
                                 text=True,
                                 timeout=2)

            res = vars(res)
            res.update({'cmd': command})

        except subprocess.CalledProcessError as e:
            res = vars(e)
            res.update({
                'cmd': command,
                'error_msg': f'Error! Command [ {e.cmd} ] return non-zero code: {e.returncode}',
                'error_code': e.returncode
            })

        except subprocess.TimeoutExpired as e:
            res = vars(e)
            res.update({
                'cmd': command,
                'error_msg': f'Error! Command [ {e.cmd} ] stopped by timeout: {e.timeout}',
                'error_code': None
            })

        except Exception as e:
            res = vars(e)
            res.update({
                'cmd': command,
                'error_msg': f'Error! Unknown error: {e}',
                'error_code': None
            })

        return ExecuteResult(**res)
