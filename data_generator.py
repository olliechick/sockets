import random

chars = [i for i in "abcdefghijklmnopqrstuvwxyzABCDEDFGHIJKLMNOPQRSTUVWXYZ1234567890`"]
chars2 = [i for i in "~-=!@#$%^&*()_+<>,./;'[]{}|:?"]
chars = chars + chars2

file_name = input("Please enter file name eg data10.txt: ")
size = int(input("How many characters to create? "))

file = open(file_name, "w")

for i in range(size):
    c = random.choice(chars)
    file.write(c)