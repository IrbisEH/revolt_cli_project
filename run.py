from app.CmdExecutor import CmdExecutor

cmd = 're ok'
executor = CmdExecutor()

result = executor.execute(cmd)

print(result)