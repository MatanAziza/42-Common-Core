def ft_count_harvest_recursive():
    harvest_deadline = int(input("Days until harvest:   "))

    def recursion(nbr: int, max: int):
        if nbr <= max:
            print(f"Day {nbr}")
            recursion(nbr + 1, max)
        else:
            print("Harvest time!")

    recursion(1, harvest_deadline)
