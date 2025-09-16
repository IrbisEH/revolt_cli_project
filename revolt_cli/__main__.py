from revolt_cli.managers.cli_manager import CliManager


def main():
    cli = CliManager()
    cli.run()


def debug_main():
    import pydevd_pycharm
    pydevd_pycharm.settrace('192.168.1.49', port=9000, stdoutToServer=True, stderrToServer=True)
    main()


if __name__ == '__main__':
    main()
