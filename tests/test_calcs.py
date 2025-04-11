import pytest

@pytest.fixture
def my_fixture():
    print("in my_fixture")
    return 5

def add(x, y):
    return x + y

@pytest.mark.parametrize ( "x, y, r" ,  [
    ( 3, 4, 7 ),
    ( 1, 9, 10),
    ( 2, 2, 4)
] )
def test_add(x, y, r):
    print("SIUU")
    assert x + y == r
    
    
@pytest.mark.parametrize ( "x, y, r" , [
    ( 3, 4, 7 ),
    ( 1, 9, 10),
    ( 2, 2, 4)
] )
def test_mul(x, y, r):
    assert x*y == r
    
class Bank:

    def __init__(self, amount = 0):
        self.amount = amount
        
    def deposit(self, n):
        self.amount += n
        
    def withdraw(self, n):
        self.amount -= n
        
        
def test_default_amount():
    b = Bank()
    assert b.amount == 0
    

@pytest.mark.parametrize( "start, dep, expected", 
                         [
                             (20, 9, 29),
                             (3, 0, 3),
                             (100, 100, 200)
                         ])
def test_deposit_amount(start, dep, expected):
    b = Bank(start)
    b.deposit( dep )
    
    assert b.amount == expected
    
    
    
@pytest.mark.parametrize( "start, withdrawal, expected", 
                         [
                             (20, 9, 11),
                             (3, 0, 11),
                             (100, 100, 0)
                         ])
def test_withdraw_amount(start, withdrawal, expected):
    b = Bank(start)
    b.withdraw( withdrawal )
    
    assert b.amount == expected
    
    
def test_example( my_fixture ):
    print("in test_example")
    assert my_fixture == 5
    
    
    
class Exy(Exception):
    pass
    
def test_expecting_error() :
    
    with pytest.raises(Exy):
        raise Exy("tsup")        