def type_check(arg_type):

    def type_decorator(*expected_types):

        def type_wrapper(function):

            def type_validator(*args, **kwargs):

                def print_error():
                    expected_types_str = ', '.join(map(str, expected_types))
                    if arg_type == "in":
                        print(f"Invalid input arguments, expected {expected_types_str}!")
                    elif arg_type == "out":
                        print(f"Invalid output value, expected {expected_types_str}!")

                if arg_type == "in":
                    invalid_args = [current_arg for current_arg in args if type(current_arg) not in expected_types]
                    invalid_kwargs = [current_value for current_value in kwargs.values() if type(current_value) not in expected_types]
                    if invalid_args or invalid_kwargs:
                        print_error()

                result = function(*args, **kwargs)

                if arg_type == "out" and type(result) not in expected_types:
                    print_error()

                return result

            return type_validator

        return type_wrapper

    return type_decorator

