# Q1.2: Pharmacy entity and local storage
#
# ======================================================================
# WHAT THIS FILE DOES (Brief Q1 #2)
#   1. Defines the ENTITY CLASS `Medicine` - one pharmacy product.
#   2. create_inventory() makes the pharmacy's LOCAL STORAGE: a hash table
#      from Q1_1.py with 3 PRE-DEFINED medicine records inserted.
#   3. main() is a small menu to look at / add to that storage.
#
# HOW IT CONNECTS
#   Q1_1.py (HashTable) -> used here
#   Q1_3.py (inventory menu) and Q1_4.py (experiment) import from here.
# ======================================================================

# math is needed for math.isfinite() (checks a price is a real number).
import math
# Reuse the hash table written in Q1.1 (the files must stay together).
from Q1_1 import HashTable

# ----------------------------------------------------------------------
# ENTITY CLASS (Brief Q1.5(ii): explain the attributes and data types)
#   product_id : int   -> unique ID and the HASH KEY (key % size needs int)
#   name       : str   -> readable product name
#   price      : float -> price in RM, shown with 2 decimal places
#   quantity   : int   -> stock is counted in whole units
#
# VIVA: Why float for price and not Decimal?
#   float is simple and fine for DISPLAYING prices. It cannot store every
#   decimal exactly (e.g. 0.1), so a real shop doing money calculations
#   would store whole sen as an int, or use Decimal.
# ----------------------------------------------------------------------
# Represent one pharmacy product and its details.
class Medicine:
    # Construct and validate one medicine. self refers to the object being created.
    # VALIDATION FIRST: bad data is rejected BEFORE anything is stored,
    # so an invalid Medicine object can never exist.
    def __init__(self, product_id, name, price, quantity):
        # Reject a negative ID or a name that is empty after removing surrounding spaces.
        # name.strip() == "" catches "" and "   " (only spaces).
        if product_id < 0 or name.strip() == "":
            # Stop this operation and pass the explanatory error message to the caller.
            raise ValueError("Enter a non-negative ID and a product name.")
        # Reject non-finite prices, negative prices and negative stock quantities.
        # math.isfinite() is False for infinity ("inf") and NaN ("nan"),
        # which float() would otherwise accept.
        # EDIT HERE: add more rules, e.g. "or price > 10000" for a price cap.
        if not math.isfinite(price) or price < 0 or quantity < 0:
            # Stop this operation and pass the explanatory error message to the caller.
            raise ValueError("Enter a valid price and a non-negative quantity.")
        # All checks passed -> store the four attributes on this object.
        # Save the ID on this Medicine object. self refers to the current object.
        self.product_id = product_id
        # Save the product name on this object.
        self.name = name
        # Store the price as a float; this does not make decimal arithmetic exact.
        self.price = price
        # Save the stock quantity on this object.
        self.quantity = quantity
        # EDIT HERE: to add a new attribute (e.g. expiry date):
        #   1. add a parameter to __init__ (e.g. expiry)
        #   2. validate it above
        #   3. save it: self.expiry = expiry
        #   4. print it in display() below
        #   5. update every place that creates Medicine(...) (this file,
        #      Q1_3.py and Q1_4.py) to pass the new value.

    # Print the details belonging to this medicine.
    # Keeping the printing inside the class means every menu shows a
    # medicine in the same format.
    def display(self):
        print(f"ID: {self.product_id} | Name: {self.name}")
        # Display the price with two decimal places; the stored float is unchanged.
        # :.2f -> 2 digits after the decimal point (5.9 shows as 5.90).
        print(f"Price: RM{self.price:.2f} | Stock: {self.quantity}")



# ----------------------------------------------------------------------
# create_inventory : build the pharmacy's local storage.
#   Returns a HashTable with 11 slots holding 3 medicines.
#
# VIVA: Why these three IDs?
#   1042 % 11 = 8, 1053 % 11 = 8, 1064 % 11 = 8  -> all COLLIDE at slot 8.
#   Linear probing therefore puts them in slots 8, 9 and 10.
#   This was chosen on purpose so the collision handling is visible.
#   Inserting another ID that hashes to 8 (e.g. 1075) wraps round to 0.
# ----------------------------------------------------------------------
# Build the pharmacy storage with predefined medicine records.
def create_inventory():
    # Create the smaller table used by the interactive inventory.
    # EDIT HERE: the starting capacity. The table still grows automatically
    # (11 -> 22) when it is full, so 11 is not a permanent limit.
    table = HashTable(11)
    # All three IDs hash to slot 8, demonstrating linear probing.
    # The KEY passed to insert() is the product ID; the VALUE is the whole
    # Medicine object, so a search by ID returns the full record.
    # EDIT HERE: add or change predefined records with more lines like these.
    # This ID hashes to slot 8 and is inserted there.
    table.insert(1042, Medicine(1042, "Paracetamol 500mg", 5.90, 120))
    # This ID also hashes to 8, so it probes forward to slot 9.
    table.insert(1053, Medicine(1053, "Cetirizine 10mg", 8.50, 45))
    # This ID also hashes to 8 and skips the occupied slots to use slot 10.
    table.insert(1064, Medicine(1064, "Antacid tablets", 6.20, 60))

    # Return the populated hash table to the caller.
    return table

# ======================================================================
# MENU (only runs when this file is started directly)
# ======================================================================
# Explore the Medicine class and the local storage built above.
def main():
    # Start with the 3 predefined medicines.
    table = create_inventory()
    while True:
        print("\n=== Pharmacy Local Storage ===")
        print("1. Display all medicines")
        print("2. Search medicine")
        print("3. Add medicine")
        print("4. Display hash table")
        print("0. Exit")
        choice = input("Enter choice: ").strip()
        try:
            # 1. Show every stored medicine --------------------------------
            if choice == "1":
                # Each occupied value slot contains a Medicine object.
                # Empty slots hold None, so they are skipped.
                for medicine in table.values:
                    if medicine is not None:
                        medicine.display()
            # 2. Search by ID ---------------------------------------------
            elif choice == "2":
                product_id = int(input("Product ID: "))
                medicine = table.search(product_id)
                if medicine is None:
                    print("Product not found.")
                else:
                    medicine.display()
            # 3. Add a new medicine ----------------------------------------
            elif choice == "3":
                # Read each field and convert it to the right data type.
                product_id = int(input("Product ID: "))
                name = input("Product name: ").strip()
                price = float(input("Price (RM): "))
                quantity = int(input("Stock quantity: "))
                # Validate all details before changing the table.
                # (If Medicine() raises ValueError, nothing is inserted.)
                medicine = Medicine(product_id, name, price, quantity)
                # Compare the size before and after to report automatic growth.
                old_size = table.size
                index = table.insert(product_id, medicine)
                if table.size != old_size:
                    print(f"Hash table resized from {old_size} to {table.size} slots.")
                print(f"Product inserted into slot {index}.")
                medicine.display()
            # 4. Show the slots ---------------------------------------------
            elif choice == "4":
                table.display()
            # 0. Exit -------------------------------------------------------
            elif choice == "0":
                print("Goodbye.")
                return
            else:
                print("Choose 0, 1, 2, 3 or 4.")
        # Wrong number format, invalid medicine data or a duplicate ID:
        # print the message and show the menu again.
        except ValueError as error:
            print("Invalid entry:", error)


# Other files can import Medicine and create_inventory without opening this menu.
if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nGoodbye.")
