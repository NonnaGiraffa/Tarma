import os
import json

def isbn_check(code_string):
    code_string = code_string.replace("-", "").replace(" ", "")
    if len(code_string) != 10:
        return False
    if not code_string[0:8].isdigit() or not (code_string[9].isdigit() or code_string[9].lower() == "x"):
        return False
    result = 0
    for i in range(9):
        result = result + int(code_string[i]) * (10 - i)
    if code_string[9].lower() == "x":
        result += 10
    else:
        result += int(code_string[9])
    return result % 11 == 0

def build_dir(*dirs):
    builder = ""
    for dir in dirs:
        builder += dir + "/"
    return builder[:-1]

dirs = ("./Tarma", "data.json")
c_dirs = [build_dir(dirs[0], dirs[1])] #? Constructed dirs

def main():
    with open(c_dirs[0], "r") as f:
        data = json.load(f)

    selection = -1
    while selection > 5 or selection <  0:
        try:
            selection = int(input("What do you want to do?\n(0) → Quit.\n(1) → Read data.\n(2) → Write data.\n(3) → List registered data.\n(4) → Sort by rating.\n(5) → Clear data.\n> "))
        except:
            selection = -1
        if selection > 35 or selection <  0:
            print("! > Please, choose what to do.\n")

    if selection == 1 and len(data) != 0:
        print("Titles: ", end = "")
        for index, title in enumerate(data.keys()):
            print(f"{title}", end = "")
            if index != len(data.keys()) - 1:
                print(", ", end = "")
        print()
        while True:
            title = input("Insert title: ")
            try:
                data[title]
                break
            except KeyError:
                print("! > Unregistered title.")
        print("\nTitle:", data[title][0], "\nRating:", data[title][1], "\nDescription:", data[title][2], "\nBook:", data[title][3])
        if data[title][3]:
            print("ISBN:", data[title][4])
        else:
            print("Tag:", data[title][4])

    elif selection == 2:
        title = input("\nTitle: ")
        while True:
            try:
                rating = int(input("Rating: "))
                break
            except ValueError:
                print("! > Please, choose a valid rating (int)")
        description = input("Description: ")

        book = input("Is it a book? (Y/N): ")
        if book.lower()[0] in ("y"):
            book = True
            print("Insert ISBN (or leave empty).")
            while True:
                ISBN = input("ISBN: ")
                if ISBN == "" or isbn_check(ISBN):
                    break
                if input(f"!> Your ISBN Seems to be wrong ({ISBN}).\nDo you want to leave it anyway? (Y/N)\n> ").lower()[0] in ("y"):
                    break
            tag = ISBN
        else:
            book = False
            tag = input("Tag: ")
        data[title] = [title, rating, description, book, tag]
        with open(c_dirs[0], "w") as f:
            json.dump(data, f) 

    elif selection == 3:
        print("\nTitles: ", end = "")
        for index, title in enumerate(data.keys()):
            print(f"{title}", end = "")
            if index != len(data.keys()) - 1:
                print(", ", end = "")
        print()

    elif selection == 4:
        selection = -1
        while selection > 3 or selection <  0:
            try:
                selection = int(input("\nWhat do you want to do?\n(0) → Quit.\n(1) → Show Everything.\n(2) → Show Books Only.\n(3) → Show Non-Books only\n> "))
            except:
                selection = -1
        if selection == 1:
            elements = [(data[element][0], data[element][1]) for element in data]
        elif selection == 2:
            elements = [(data[element][0], data[element][1]) if data[element][3] else (None, False) for element in data]
        elif selection == 3:
            elements = [(data[element][0], data[element][1]) if not data[element][3] else (None, False) for element in data]
        if selection != 0:
            elements.sort(key = lambda x:x[1], reverse = True)
            for element in elements:
                if element[0] != None:
                    print(f"({element[1]}) {element[0]}")
        selection = 4

    elif selection == 5:
        print("\nTitles: ", end = "")
        for index, title in enumerate(data.keys()):
            print(f"{title}", end = "")
            if index != len(data.keys()) - 1:
                print(", ", end = "")
        print()
        while True:
            clearing = input("What do you want to clear?\nLeave empty if it was a mistake.\n> ")
            if clearing == "":
                break
            try:
                del data[clearing]
                break
            except:
                print("! > Title not found.")
        with open(c_dirs[0], "w") as f:
            json.dump(data, f)

    if selection != 0:
        input("\nPress enter.")
        main()
        
if __name__ == "__main__":
    #? Path and files generation
    if not os.path.exists(dirs[0]):
        os.mkdir(dirs[0])
    try:
        with open(c_dirs[0], 'x') as f:
            f.write("{}")
    except FileExistsError:
        pass
    main()
