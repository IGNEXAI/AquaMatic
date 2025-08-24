from src.services.models import Parameter

def test_parameter_is_acceptable():
    """
    Tests the is_acceptable property of the Parameter class.
    """
    # Test with value within the accepted range
    param = Parameter(name="pH", value=7.0, unit="pH", min_accepted_val=6.5, max_accepted_val=8.5)
    assert param.is_acceptable is True

    # Test with value below the accepted range
    param = Parameter(name="pH", value=6.0, unit="pH", min_accepted_val=6.5, max_accepted_val=8.5)
    assert param.is_acceptable is False

    # Test with value above the accepted range
    param = Parameter(name="pH", value=9.0, unit="pH", min_accepted_val=6.5, max_accepted_val=8.5)
    assert param.is_acceptable is False

    # Test with value equal to the minimum accepted value
    param = Parameter(name="pH", value=6.5, unit="pH", min_accepted_val=6.5, max_accepted_val=8.5)
    assert param.is_acceptable is True

    # Test with value equal to the maximum accepted value
    param = Parameter(name="pH", value=8.5, unit="pH", min_accepted_val=6.5, max_accepted_val=8.5)
    assert param.is_acceptable is True

    # Test with no min_accepted_val
    param = Parameter(name="pH", value=6.0, unit="pH", max_accepted_val=8.5)
    assert param.is_acceptable is True

    # Test with no max_accepted_val
    param = Parameter(name="pH", value=9.0, unit="pH", min_accepted_val=6.5)
    assert param.is_acceptable is True

    # Test with no min or max accepted_val
    param = Parameter(name="pH", value=7.0, unit="pH")
    assert param.is_acceptable is True
