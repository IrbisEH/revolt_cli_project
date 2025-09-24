from revolt_cli.managers.cli_manager import CliManager


def main():
    cli = CliManager()
    cli.run()


def debug_main():
    import pydevd_pycharm
    # pydevd_pycharm.settrace('10.10.0.1', port=9000, stdoutToServer=True, stderrToServer=True)
    pydevd_pycharm.settrace('10.10.0.10', port=9000, stdoutToServer=True, stderrToServer=True)
    main()


if __name__ == '__main__':
    main()
