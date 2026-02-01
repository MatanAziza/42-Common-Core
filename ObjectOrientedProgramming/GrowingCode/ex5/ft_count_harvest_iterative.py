def ft_count_harvest_iterative():
    harvest_deadline = int(input("Days until harvest: "))
    for i in range(harvest_deadline):
        print(f"Day {i + 1}")
    print("Harvest time!")
