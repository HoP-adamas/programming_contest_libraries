def binary_search(ok, ng, test):
    '''
    :param ok: the point which satisfies test(x) == True
    :param ng: the point which satisfies test(x) == False

    '''

    while abs(ok - ng) > 1:
        mid = (ok + ng) // 2
        if test(mid):
            ok = mid
        else:
            ng = mid
    return ok

def test(x):
    '''
    write the test function for the probrem
    '''

    return True

