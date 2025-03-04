import subprocess

# TODO: type notation in args

INDENT_CHAR = ' '
IN_DEEP_PROPS_INDENT = 2

class VMWareCmd:
    START = ''
    STOP = ''


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
        for key in ['stdout', 'stderr', 'error_msg']:
            value = kwargs.get(key, None)
            kwargs[key] = value.strip() if value and isinstance(value, str) else value

        self.success = False
        self.cmd = kwargs.get('cmd', None)
        self.stdout = kwargs.get('stdout', None)
        self.stderr = kwargs.get('stderr', None)

        if kwargs.get('error_msg', None) or kwargs.get('error_code', None):
            self.error = Error(
                msg=kwargs.get('error_msg', None),
                code=kwargs.get('error_code', None)
            )
        else:
            self.success = True
            self.error = None

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
    def execute(command: str, timeout: int=5) -> ExecuteResult:
        response = None
        result_dic = {'cmd': command}
        try:
            response = subprocess.run(command,
                                 shell=True,
                                 check=False,
                                 capture_output=True,
                                 text=True,
                                 timeout=timeout)

        except subprocess.CalledProcessError as e:
            result_dic.update(vars(e))
            result_dic.update({
                'error_msg': f'Error! Command [ {e.cmd} ] return non-zero code: {e.returncode}'
            })

        except subprocess.TimeoutExpired as e:
            result_dic.update(vars(e))
            result_dic.update({
                'error_msg': f'Error! Command [ {e.cmd} ] stopped by timeout: {e.timeout}'
            })

        except Exception as e:
            result_dic.update(vars(e))
            result_dic.update({
                'error_msg': f'Error! Unknown error: {e}'
            })

        if response:
            result_dic.update(vars(response))


        return ExecuteResult(**result_dic)
