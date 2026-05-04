def get_numbers():
    numbers = []
    print("Enter numbers (type 'done' to finish):")
    
    while True:
        user_input = input("> ")
        if user_input.lower() == 'done':
            break
        try:
            num = float(user_input)
            numbers.append(num)
        except ValueError:
            print("Invalid input! Please enter a number.")
    
    return numbers


def compute_stats(numbers):
    total = sum(numbers)
    count = len(numbers)
    avg = total / count if count > 0 else 0
    
    return total, count, avg


def main():
    numbers = get_numbers()
    
    if not numbers:
        print("No valid numbers entered.")
        return
    
    total, count, avg = compute_stats(numbers)
    
    print("\nResults:")
    print("Sum:", total)
    print("Count:", count)
    print("Average:", avg)


if __name__ == "__main__":
    main()
