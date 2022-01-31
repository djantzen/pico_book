file = open("main.txt", "w")
file.write("hello")
file.flush()

exec(open('scripts/lcd.py').read())
