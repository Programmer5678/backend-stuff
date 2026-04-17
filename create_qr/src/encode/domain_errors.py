from src.domain_error import DomainError

class InputValidationDE (DomainError):
    """Error given for the input values being files that dont match valid input
    expectation like dont exist , arent absolute etc. """
    pass

class TooMuchDataQRDE (DomainError):
    """Error given for the input values being files that dont match valid input
    expectation like dont exist , arent absolute etc. """
    pass

