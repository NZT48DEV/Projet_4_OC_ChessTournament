

def get_valid_input(prompt, formatter, validator, message_error):
    while True:
        user_input = input(prompt)
        formatted_input = formatter(user_input)

        if validator(formatted_input):
            return formatted_input
        else:
            message_error()