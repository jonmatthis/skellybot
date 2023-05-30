def returnTrue(num):
    try:
        return True
    except:
        return False


def test_test():
    """This is a tests of the tests framework.  It should always pass.
    To make your own tests, copy this function, change the name, and add your own assertions.
    """
    print("Running test_test")
    assert returnTrue(6) == True, "This should always pass - something is wrong with the tests framework"