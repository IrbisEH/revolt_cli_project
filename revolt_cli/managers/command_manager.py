from typing import Tuple
import subprocess


class LinuxCommandManager:
    @classmethod
    def execute(cls, cmd: str, capture_output: bool = True, text: bool = True) -> Tuple[int, str, str]:
        try:
            result = subprocess.run(
                cmd,
                capture_output=capture_output,
                shell=True,
                check=False,
                text=text
            )
            return int(result.returncode), str(result.stdout.strip()), str(result.stderr.strip())
        except Exception as e:
            return 1, '', str(e)