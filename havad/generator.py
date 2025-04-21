with open("/home/ruz/backend-stuff/havad/file.txt", "r") as file:
    for line in file:
        words = line.split()
        for word in words:
            print(word)