def type_check(arg_type):

    def type_decorator(*expected_types):

        def type_wrapper(function):

            def type_validator(*args, **kwargs):

                def print_error(message_type):
                    expected_types_str = ', '.join(map(str, expected_types))
                    print(f"Invalid {message_type} arguments, expected {expected_types_str}!")

                if arg_type == "in":
                    invalid_args = [current_arg for current_arg in args if type(current_arg) not in expected_types]
                    invalid_kwargs = [current_value for current_value in kwargs.values() if type(current_value) not in expected_types]
                    if invalid_args or invalid_kwargs:
                        print_error("in")

                result = function(*args, **kwargs)

                if arg_type == "out" and type(result) not in expected_types:
                    print_error("out")

                return result

            return type_validator

        return type_wrapper

    return type_decorator
