"""Name: Ryan Bailis
    CSCI204 P1 Phase 1
"""

import csv

def readCSV(filename):
    """takes in the name of a csv and returns the \
    csv in a list (each line in a separate list)"""
    with open(filename, "r") as f:
        reader = csv.reader(f)
        data = list(reader)
        data = data[1:]
        return data

class Item():
    """the most basic type of item in inventory. Has name, date, price, and quantity attributes"""
    def __init__(self,name,date,price,quantity):
        """constructor. creates name,date,price,and qunatity"""
        self.name = name
        self.date = date
        self.price = price
        self.quantity = quantity
        
    def __str__(self):
        """string method"""
        return "Name: " + self.name + "\nDate: " + self.date + "\nPrice: $" \
               + self.price + "\nQunatity: " + self.quantity

class Book(Item):
    """book is one type of item in inventory"""
    def __init__(self,name,date,price,quantity,publisher,author,ISBN):
        """constructor. inherits Item attributes and adds publisher, author, and ISBN as attributes"""
        super().__init__(name,date,price,quantity)
        self.publisher = publisher
        self.author = author
        self.ISBN = ISBN

    def __str__(self):
        """string method"""
        return super().__str__() + "\nPublisher: " + self.publisher + \
               "\nAuthor: " + self.author + "\nISBN: " + self.ISBN
        
class CD(Item):
    """CD is one type of item in inventory"""
    def __init__(self,name,date,price,quantity,artist,label,ASIN):
        """constructor. inherits item attributes and adds artist, label, and ASIN as attributes"""
        super().__init__(name,date,price,quantity)
        self.artist = artist
        self.label = label
        self.ASIN = ASIN

    def __str__(self):
        """string method"""
        return super().__str__() + "\nArtist: " + self.artist + \
               "\nLabel: " + self.label + "\nASIN: " + self.ASIN

class Collectable(Item):
    """collectable is one type of item in inventory"""
    def __init__(self,name,date,price,quantity,owner):
        """constructor. inherits item attributes and adds owner attribute"""
        super().__init__(name,date,price,quantity)
        self.owner = owner

    def __str__(self):
        """string method"""
        return super().__str__() + "\nOwner: " + self.owner 
        
class Ebay(Item):
    """ebay is one type of classes that inherits item and will be inherited by electronics, home_garden, and fashion"""
    def __init__(self,name,date,price,quantity,manufacturer):
        """constructor. inherits item attributes and adds manufacturer attribute"""
        super().__init__(name,date,price,quantity)
        self.manufacturer = manufacturer

    def __str__(self):
        """string method"""
        return super().__str__() + "\nManufacturer : " + self.manufacturer 
        
class Fashion(Ebay):
    """inherits ebay class and has the same exact attributes"""
    pass
        
class HomeGarden(Ebay):
    """inherits ebay class and has the same exact attributes"""
    pass
        
class Electronics(Ebay):
    """inherits ebay class and has the same exact attributes"""
    pass

class Inventory():
    """creates the list of all items in inventory and contains analysis methods (print, sum, check type)"""
    def __init__(self):
        """create the object 'items' and make it contain all the individual objects"""
        self.items = []
            
        for i in readCSV("book.csv"):
            self.items.append(Book(i[0],i[1],i[4],i[6],i[2],i[3],i[5]))
        for i in readCSV("cd_vinyl.csv"):
            self.items.append(CD(i[0],i[4],i[5],i[6],i[1],i[2],i[3]))
        for i in readCSV("collectible.csv"):
            self.items.append(Collectable(i[0],i[2],i[1],i[4],i[3]))
        for i in readCSV("electronics.csv"):
            self.items.append(Electronics(i[0],i[2],i[1],i[4],i[3]))
        for i in readCSV("fashion.csv"):
            self.items.append(Fashion(i[0],i[2],i[1],i[4],i[3]))
        for i in readCSV("home_garden.csv"):
            self.items.append(HomeGarden(i[0],i[2],i[1],i[4],i[3]))

        self.count = len(self.items)
            
    def print_inventory(self,begin=0,end=-1):
        """prints the inventory from 'begin' to 'end'"""
        for item in self.items[begin:end]:
           print(item)
           print()
           
    def check_type(self, item):
        """determine the type of the given item and return a string"""
        if isinstance(item,Book):
            return "book"
        elif isinstance(item,CD):
            return "CD"
        elif isinstance(item,Collectable):
            return "collectable"
        elif isinstance(item,Fashion):
            return "fashion"
        elif isinstance(item,HomeGarden):
            return "home and garden"
        elif isinstance(item,Electronics):
            return "electronics"
        
    def compute_inventory(self):
        """determine the total dollar value of the inventory."""
        total = 0
        for item in self.items:
            total += float(item.quantity)*float(item.price)
        return total
            
    def print_category(self, cat_name):
        """given a category, return all the items in that category."""
        if cat_name.lower() == "fashion":
            for item in self.items:
                if isinstance(item,Fashion):
                    print(item)
                    print()
        elif cat_name.lower() == "book":
            for item in self.items:
                if isinstance(item,Book):
                    print(item)
                    print()
        elif cat_name.lower() == "home_garden":
            for item in self.items:
                if isinstance(item,HomeGarden):
                    print(item)
                    print()
        elif cat_name.lower() == "electronics":
            for item in self.items:
                if isinstance(item,Electronics):
                    print(item)
                    print()
        elif cat_name.lower() == "cd":
            for item in self.items:
                if isinstance(item,CD):
                    print(item)
                    print()
        elif cat_name.lower() == "collectable":
            for item in self.items:
                if isinstance(item,Collectable):
                    print(item)
                    print()
        else:
            print("That is not a category name.")

    def search_item(self, item_name):
        """simplistic search function. checks to see if a sub sting is contained \
        within the name of the object"""
        print("NOW SEARCHING FOR: " + item_name)
        for item in self.items:
            if item_name in item.name:
                print(item)
                print()


        
