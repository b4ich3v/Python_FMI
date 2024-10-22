def type_check(type):
    def type_decorator(*expected_types):
        def type_wrapper(function):
            def type_checker(*args, **kwargs):
                def print_error(message_type):
                    expected_types_str = ''
                    for i in range(len(expected_types)):
                        expected_types_str += str(expected_types[i])
                        if i < len(expected_types) - 1:
                            expected_types_str += ', '
                    print(f"Invalid {message_type} arguments, expected {expected_types_str}!")

                if type == "in":
                    invalid_args = [current_arg for current_arg in args if current_arg not in expected_types]
                    if len(invalid_args) > 0:
                        print_error("in")

                result = function(*args, **kwargs)

                if type == "out" and result not in expected_types:
                    print_error("out")

                return result

            return type_checker

        return type_wrapper

    return type_decorator
