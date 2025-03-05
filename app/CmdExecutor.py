import os
import time
import errno
import fcntl
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

        if kwargs.get('error_msg', None) or kwargs.get('return_code', None):
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
    def execute(command: list, non_blocking_mode=False, timeout: int=5) -> ExecuteResult:
        result_dic = {'cmd': command}
        process = None

        # TODO: Как добавить timeout

        try:
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            process.wait()

            if non_blocking_mode:
                CmdExecutor.make_non_blocking(process.stdout)
                CmdExecutor.make_non_blocking(process.stderr)

            result_dic.update({
                'stdout': process.stdout.read(),
                'stderr': process.stderr.read(),
                'return_code': process.returncode
            })

        except OSError as e:
            if e.errno == errno.EAGAIN:
                stderr_data = ''
            else:
                raise

        except Exception as e:
            result_dic.update(vars(e))
            result_dic.update({
                'error_msg': f'Error! Unknown error: {e}'
            })
        finally:
            # TODO
            if process:
                process.stdout.close()
                process.stderr.close()


        return ExecuteResult(**result_dic)

    @staticmethod
    def make_non_blocking(file_obj):
        fd = file_obj.fileno()
        flags = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, flags | os.O_NONBLOCK)

    # @staticmethod
    # def read_non_blocking(file_obj):
    #     output = ''
    #
    #     try:
    #         for lin in
    #     except OSError as e:
    #         if e.errno != errno.EAGAIN:
    #             raise
    #
    #     return output