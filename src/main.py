file = open("main.txt", "w")
file.write("hello")
file.flush()

exec(open('scripts/potentiometer.py').read())