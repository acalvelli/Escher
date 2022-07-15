def genProgram():
    def program1(x):
        if(x < 10):
            return 2*x + 10
        elif (x < 35):
            return x*x + 23
        elif(x < 60):
            return 3*x + 12
        else:
            return 2*x
    def program2(x):
        if(x < 50):
            return x*x + 23
        elif (x < 75):
            return 2*x + 10
        elif(x < 90):
            return 3*x + 16
        else:
            return 3*x + 10
    def program3(x):
        if(x < 5):
            return 3*x + 7
        elif (x < 25):
            return x*x + 25
        elif(x < 28):
            return 2*x + 5
        else:
            return x*x + 9
    def program4(x):
        if(x < 40):
            return 3*x + 10
        elif (x < 55):
            return x*x + 23
        elif(x < 80):
            return 3*x + 23
        else:
            return x*x + 10
    return program1
