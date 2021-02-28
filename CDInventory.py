#------------------------------------------#
# Title: CDInventory.py (Assignment_07)
# Desc: CD Inventory Program.
# Change Log: 
#    2/20/21, Eric Hoyle, consolidated code into functions under classes
#             updated main to incorporate new class and function calls. 
#    2/27/21, Eric Hoyle, Incorporated exception handling and data serialization.
#             Further consolidation of main into functions. Minor corrections
#             function arguments.
# DBiesinger, 2030-Jan-01, Created File
#------------------------------------------#
import pickle
# -- DATA -- #
strChoice = '' # User input
lstTbl = []  # list of lists to hold data
dicRow = {}  # dictionary of data row
datFileName = 'CDInventory.dat'  # data storage file
objFile = None  # file object
cdData = None

# -- PROCESSING -- #
class DataProcessor:
    """Processing data supplied by the user"""
   
    @staticmethod   
    def table_append(cdData, table):
        """Appends new cd entry as dictionary to a list of dictionaries
        
        Args: 
            cdData: Information aboout the CD 
            table: The list that the new dictionary is appended to
        
        Returns: 
            List of dictionaries with new dictionary appended to the list
        
        """
        dicRow = {'ID': cdData[0], 'Title': cdData[1], 'Artist': cdData[2]}
        table.append(dicRow)
        return table

    @staticmethod
  
    def cd_remove(intIDDel, table):
        """Removes the dictionary with ID key value specified by user in 
        intIDDel from the list of dictionaries.
        
        Args:
            intIDDel (int): value for key ID specified by the user
            table: list of dictionaries the entry is removed from.
            
        Returns:
            Boolean value of cd removal status.
            """
        intRowNr = -1
        blnCDRemoved = False
        # for row in lstTbl:
        for row in table:
            intRowNr += 1
            if row['ID'] == intIDDel:
                # del lstTbl[intRowNr]
                del table[intRowNr]
                blnCDRemoved = True
                break
        return blnCDRemoved
    
   
class FileProcessor:
    """Processing the data to and from text file"""

    @staticmethod
    def read_file(file_name, table):
        """Function to manage data ingestion from file to a list of 
        dictionaries

        Reads the data from file identified by file_name into a 2D table
        (list of dicts) table one line in the file represents one dictionary 
        row in table.

        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds
            the data during runtime

        Returns:
            None.
        """
        try:     
            table.clear()  # this clears existing data and allows to load data from file
            with open(file_name, 'rb') as dataread:
                picdata = pickle.load(dataread)
                for line in picdata:
                    table.append(line)
        except FileNotFoundError as e:
            print('\n{:*^66}'.format((e.__doc__).upper()),
                  '\n{:^66}'.format(' WARNING: Data not loaded').upper())

    @staticmethod
    def write_file(file_name, table):
        """Function to manage data output from a list of dictionaries to a file 

        Writes the data from a 2D table (lstTbl) to a file identified by 
        file_name, one dictionary per row.
        
        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (lstTbl) that holds the 
            data during runtime

        Returns:
            None.
        """
        try:
            with open(file_name, 'wb') as datastore:
                pickle.dump(table, datastore)
        except FileNotFoundError as e:
            print('\n{:*^66}'.format((e.__doc__).upper()),
                  '\n{:^66}'.format(' WARNING: Data not saved').upper())

# -- PRESENTATION (Input/Output) -- #

class IO:
    """Handling Input / Output"""
    @staticmethod
    def add_cd():
        """Ask user for new ID, CD Title and Artist
        
        Args: 
            None.
            
        Returns:
            list of information (ID, Title, and Artist) for a new CD entry"""
        
        print('Please enter info for the CD you would like to add:\n')
        strID = ''
        n=3
        while strID == '':
            
            try:
                strID = int(input('Enter ID: ').strip())
            except ValueError:
                print('\n* Don\'t be a dummy! ID must be a number. Please try again *\n'.upper())
                n-=1
                if n==0:
                    input('You seem to be pretty dense. Let\'s get you back to the main menu.')
                    break
                continue
            strTitle = input('What is the CD\'s title? ').strip()
            strArtist = input('What is the Artist\'s name? ').strip()
            cdData =[strID, strTitle, strArtist]
        return cdData
               
            
    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """

        print('\n\n')
        print('{:-^66}'.format(' Menu '),'\n{:<}'.format('[l] Load Inventory from'),datFileName,
             '\n{:<30}'.format('[a] Add CD'),'\n{:<30}'.format('[i] Display Current Inventory'),
             '\n{:<30}'.format('[d] Delete CD from Inventory'),
             '\n{:<}'.format('[s] Save Inventory to'),datFileName,
             '\n{:<30}'.format('[x] Exit'),
             '\n{:-^66}'.format('-'))

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, i, d, s or x

        """
        choice = ' '
        while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
            choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
        print()  
        return choice

    @staticmethod
    def show_inventory(table):
        """Displays current inventory table


        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.

        """
        print('\n\n')
        print('{:=^66}'.format(' The Current Inventory '))
        print('{:<6}{:30}{:30}'.format('ID','Title','Artist'))
        print('{:-^66}'.format('-'))
        for row in table:
            print('{:<6}{:30}{:30}'.format(*row.values()))
        print('{:=^66}'.format('='))
    
    @staticmethod
    def cd_removed_conf(removed):
        """ uses the status (True/False) of the boolean flag in the cd_remove
        function to return a printed statement of the status to the user.
        
        Args:
            None
        
        Returns:
            None
        """
        print()
        if removed:
            print('The CD was removed\n')
        else:
            print('Could not find this CD!\n')

    @staticmethod
    def del_choice():
        n=3
        while n > 0:
            try:
                delID = int(input('Which ID would you like to delete? ').strip())
            except ValueError:
                    print('\n* Don\'t be a dummy! ID must be a number. Please try again *\n'.upper())
                    n-=1
                    if n==0:
                        input('You seem to be pretty dense. Let\'s get you back to the main menu.')
                        break
                    continue
            else:
                return delID

# 1. When program starts, read in the currently saved Inventory
FileProcessor.read_file(datFileName, lstTbl)

# 2. start main loop
while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()

    # 3. Process menu selection
    try:
        if strChoice == 'x':# 3.1 process exit first
            break
        # 3.2 process load inventory
        if strChoice == 'l':
            print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
            strYesNo = input('Type \'yes\' to continue and reload from {}. \nPress any key to cancel: '.format(datFileName))
            if strYesNo.lower() == 'yes':
                print('reloading...')
                FileProcessor.read_file(datFileName, lstTbl)
                IO.show_inventory(lstTbl)
            else:
                input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
                IO.show_inventory(lstTbl)
            continue
        # 3.3 process add a CD
        elif strChoice == 'a':
            cdData = IO.add_cd()
            lstTbl = DataProcessor.table_append(cdData, lstTbl)
            IO.show_inventory(lstTbl)
            continue  
        # 3.4 process display current inventory
        elif strChoice == 'i':
            IO.show_inventory(lstTbl)
            continue
        # 3.5 process delete a CD
        elif strChoice == 'd':
            # 3.5.1 get Userinput for which CD to delete
            # 3.5.1.1 display Inventory to user
            IO.show_inventory(lstTbl)
            # 3.5.1.2 ask user which ID to remove
            intIDDel = IO.del_choice()
            # 3.5.2 search thru table and delete CD
            removed = DataProcessor.cd_remove(intIDDel, lstTbl)
            IO.cd_removed_conf(removed)
            IO.show_inventory(lstTbl)
            continue
        # 3.6 process save inventory to file
        elif strChoice == 's':
            # 3.6.1 Display current inventory and ask user for confirmation to save
            IO.show_inventory(lstTbl)
            strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
            # 3.6.2 Process choice
            if strYesNo == 'y':
                # 3.6.2.1 save data
                FileProcessor.write_file(datFileName, lstTbl)
            else:
                input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
            continue
        # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be save:
        else:
            print('General Error')
    except Exception as e: #Exception for exceptions the propogate beyong function level
        print(e.__doc__)



