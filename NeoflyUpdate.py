import os

#Double check that sqlite3 is installed, if not pip install it
try:
    import sqlite3
except ImportError:
    os.system('pip install sqlite3')
    import sqlite3

#Python's version of a switch statement...using a dictionary
def functionSwitcher(arg):
    switch = {0: "exit()", 1: "profileTypeChoice()", 2: 'simpleUpdate("xp")', 3: 'simpleUpdate("cash")', 4: "giveQual()", 5: 'simpleUpdate("rank")'}
    return switch.get(arg, "invalid")


#SQL Connection and update
def updateTable(tableName, updateValue,setVal,largeCatUpdate):
    profName = input("Enter your Neofly profile name to update: ")

    if profName == "":
        print("\nNo profile name entered.")
        exit()

    try:
        #SQL Lite Connection
        sqlConnection = sqlite3.connect("C:\\ProgramData\\NeoFly\\common.db")
        cursor = sqlConnection.cursor()
        print("\nConnected to database. . .")

        if largeCatUpdate:
            for i in setVal:
                uString = 'UPDATE "' + tableName + '" SET ' + i + ' = "' + str(updateValue) + '" WHERE name = "' + profName + '";'

                # Execute update
                cursor.execute(uString)
                sqlConnection.commit()
        else:
            uString = 'UPDATE "' + tableName + '" SET ' + setVal + ' = ' + str(updateValue) + ' WHERE name = "' + profName + '";'

            #Execute update
            cursor.execute(uString)
            sqlConnection.commit()

        record = cursor.rowcount

        if record == 0:
            print("\nNo updates made.  Did you spell your profile name correctly?  It must match exactly to the Neofly profile select (This is case sensitive.)")
        else:
            print("\nRecord updated.")

        cursor.close()
    # Connection error
    except sqlite3.Error as error:
        print("\nError while connecting to database: ", error)
    # Close connection
    finally:
        if sqlConnection:
            sqlConnection.close()
            print("\nConnection to database has been closed.")


def profileTypeChoice():
    print("\nWhich profile type would you like?\n0. Custom \n1. Pro\n2. Survival")

    profType = int(input("Profile Type: "))
    if profType > 2:
        print("\nInvalid number selected.")
        exit()

    #Call update
    updateTable("career", profType, "profilMode", False)


def simpleUpdate(upOption):
    if upOption == "rank":
        print("\nThe ranks are as follows\n0. Cadet\n1. Second Officer\n2. Officer\n3. Captain\n4. Senior Captain")
    numIn = input("\nWhat would you like to set your " + upOption + " to? (Please enter a number) ")
    numIn = numIn.replace(",", "")
    numIn = round(numIn, 0)

    #Call update
    updateTable("career", int(numIn), upOption, False)


def giveQual():
    catArray = ("catB", "catC", "catD", "catE", "catF")
    print("Which qualification would you like?\n1.Cat B\n2. Cat C\n3. Cat D\n4. Cat E\n5. Cat F\n6. All!\n0. Exit")
    qualChoice = int(input("Choice: "))

    if qualChoice > 6:
        print("\nInvalid number entered.")
        exit()
    if qualChoice == 6:
        updateTable("career", "True",catArray, True)
    else:
        updateTable("career", "True", catArray[qualChoice-1], False)


if __name__ == "__main__":
    print("\nIMPORTANT: Please make sure to close Neofly before making any changes here!\n")
    print("\nEnter the number corresponding to your choice\n1. Update Profile Type (Custom/Pro/Survival)\n2. Cheats\n0. Exit.")
    oChoice = input("Choice: ")

    if oChoice != "0":
        if oChoice == "2":
            print("\nHey no judge.  What are you looking to do?\n1. Set XP\n2. Set Cash\n3. Give Qualification License(s)\n4. Set rank\n0. Exit. ")
            choice = input("Choice: ")
        func = functionSwitcher(int(oChoice) if oChoice != "2" else int(choice)+1)
        if func == "invalid":
            print("\nInvalid number selected.")
            exit()
        eval(func)
