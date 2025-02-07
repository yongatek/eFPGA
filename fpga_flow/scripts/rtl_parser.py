def extract_variables_info(input_string):
    # Check for arithmetic operations and adjust input_string if necessary
    if any(op in input_string for op in ['-', '+', '*']):
        # Extract the size range from the input string and evaluate the range
        left_bracket = input_string.find("[") + 1
        right_bracket = input_string.find("]")
        colon = input_string.find(":")
        start_index = int(eval(input_string[left_bracket:colon]))
        end_index = int(eval(input_string[colon + 1:right_bracket]))
        input_string = input_string[:left_bracket] + str(start_index) + ":" + str(end_index) + input_string[right_bracket:]

    # Extract size information from the range
    size_string = input_string[input_string.find("[") + 1:input_string.find("]")]
    start_size, end_size = map(int, size_string.split(":"))
    size = abs(end_size - start_size) + 1

    # Determine if the range is big-endian or little-endian
    big_endian = "false" if start_size > end_size else "true"

    # Extract variable names after the closing bracket "]"
    var_names_str = input_string[input_string.find("]") + 1:]
    if ';' in var_names_str:
        var_names = var_names_str.split(";")[0]
    else:
        var_names = var_names_str.split(",")[0]

    # Clean and return the result
    var_names = [name.strip().strip(";") for name in var_names.split(',')]
    return var_names, [size] * len(var_names), [big_endian] * len(var_names)
