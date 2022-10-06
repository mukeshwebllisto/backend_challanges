def compress(string: str) -> str:
    """
    Compress the given string and returns it

    Args
        - string

    Returns
        - compressed_string

    Rules
        - shorten the string by replacing contineous repeating characters with `{char}{no_of_repeation}`
        - if no repeation of character, ignore it.

    Examples
        - bbcceeee -> b2c2e4
        - aaabbbcccaaa -> a3b3c3a3
        - a -> a

    Time Complexity - O(n), we need to iterate over each char in string
    Space complexity - O(n), new list and str required to store compressed and count string

    """
    char_repeation_with_count = []
    char_repeat_count = 1

    for index, char in enumerate(string):
        if index < len(string) - 1 and char == string[index + 1]:
            char_repeat_count += 1
        else:
            char_repeation_with_count.append([char, char_repeat_count])
            char_repeat_count = 1

    compressed_string = ""
    for char, repeat_count in char_repeation_with_count:
        compressed_string += char
        if repeat_count > 1:
            compressed_string += str(repeat_count)

    return compressed_string
