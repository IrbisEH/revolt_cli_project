def test_get(arg):
    for i in range(0, 5):
        yield arg + i




x = test_get(22)

for _i in x:
    print(_i)