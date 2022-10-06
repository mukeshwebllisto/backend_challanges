from challange_1.challange_1a import compress


def test_string_compression():
    assert compress("bbcceeee") == "b2c2e4"
    assert compress("aaabbbcccaaa") == "a3b3c3a3"
    assert compress("a") == "a"
