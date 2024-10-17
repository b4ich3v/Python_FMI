def sum_of_digits(number):
    sum = 0
    while(number is not 0):
        current_digit = number % 10
        sum +=  current_digit        
        number /= 10
    return sum
