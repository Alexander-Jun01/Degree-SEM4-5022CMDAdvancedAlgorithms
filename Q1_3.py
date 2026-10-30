# Q1.3: Command-line inventory system
#
# ======================================================================
# WHAT THIS FILE DOES (Brief Q1 #3)
#   The pharmacy INVENTORY SYSTEM - a command-line menu on top of the
#   local storage from Q1_2.py.
#     Required by the brief : 1 Insert, 2 Search
#     Optional extras       : 3 Edit, 4 Delete
#     Helper for the VIVA   : 5 Display hash table
#
# HOW THE DATA FLOWS
#   create_inventory() (Q1_2) -> HashTable (Q1_1) with 3 medicines
#   Every menu choice works on that same `table` object, so changes stay
#   until the program closes (data is kept in memory, not saved to disk).
# ======================================================================

# Medicine = the entity class; create_inventory = the predefined storage.
from Q1_2 import Medicine, create_inventory

def main():
    # Obtain the populated storage built in Q1.2.
    table = create_inventory()

    # Repeat the menu until the exit branch reaches break.
    while True:
        print("\n=== Pharmacy Inventory ===")
        print("1. Insert product")
        print("2. Search product")
        print("3. Edit product")
        print("4. Delete product")
        print("5. Display hash table")
        print("0. Exit")
        # EDIT HERE: to add a menu option, add a print line above AND a
        # new `elif choice == "6":` branch below, and update the message
        # in the final else branch.
        # Read the choice as text and remove surrounding spaces.
        # The choice stays TEXT ("1"), so we compare with "1", not 1.
        choice = input("Enter choice: ").strip()

        # Allow the following operations to report invalid input without ending the menu.
        try:
            # ---------------------------------------------------------
            # 1. INSERT (required)
            #   Read 4 values -> build a Medicine (validates them) ->
            #   insert into the hash table using the ID as the key.
            # ---------------------------------------------------------
            # Insert a product.
            if choice == "1":
                # Read text and convert it to a whole-number ID.
                product_id = int(input("Product ID: "))
                # Read the name without leading or trailing spaces.
                name = input("Product name: ").strip()
                # Convert the entered price to a floating-point number.
                price = float(input("Price (RM): "))
                # Convert the stock quantity to a whole number.
                quantity = int(input("Stock quantity: "))
                # Validate the values and construct the product object.
                # If any value is invalid, Medicine() raises ValueError and
                # we jump straight to `except` - nothing is inserted.
                medicine = Medicine(product_id, name, price, quantity)
                # Insert the product and remember the slot used for the confirmation message.
                # old_size lets us detect automatic growth (11 -> 22 slots).
                old_size = table.size
                # insert() returns the slot number; it raises ValueError for
                # a duplicate ID.
                index = table.insert(product_id, medicine)
                if table.size != old_size:
                    print(f"Hash table resized from {old_size} to {table.size} slots.")
                print(f"Product inserted into slot {index}.")

            # ---------------------------------------------------------
            # 2. SEARCH (required)
            #   The hash table jumps to slot ID % size and probes from
            #   there - it does NOT check every record like an array.
            # ---------------------------------------------------------
            # Search for a product.
            elif choice == "2":
                # Read text and convert it to a whole-number ID.
                product_id = int(input("Product ID: "))
                # Find the product by ID, returning a Medicine object or None.
                medicine = table.search(product_id)
                # Handle a search that found no matching product.
                if medicine is None:
                    print("Product not found.")
                else:
                    # Call the found product's method to show its details.
                    medicine.display()

            # ---------------------------------------------------------
            # 3. EDIT (optional extra)
            #   The ID is NOT changed, because the ID decides the slot.
            #   (Changing an ID would mean delete + insert again.)
            # ---------------------------------------------------------
            # Edit a stored medicine, keeping its product ID unchanged.
            elif choice == "3":
                product_id = int(input("Product ID to edit: "))
                medicine = table.search(product_id)
                if medicine is None:
                    print("Product not found.")
                else:
                    # Show the current details first.
                    medicine.display()
                    name = input("New product name: ").strip()
                    price = float(input("New price (RM): "))
                    quantity = int(input("New stock quantity: "))
                    # Validate all new details before changing the stored object.
                    # VIVA: a TEMPORARY Medicine is built only to run the
                    # validation. If it fails, the stored record is untouched,
                    # so an invalid edit can never half-change a record.
                    updated = Medicine(product_id, name, price, quantity)
                    # Copy the checked values onto the object that is stored
                    # in the hash table (the same object, so no re-insert).
                    medicine.name = updated.name
                    medicine.price = updated.price
                    medicine.quantity = updated.quantity
                    print("Product updated.")
                    medicine.display()

            # ---------------------------------------------------------
            # 4. DELETE (optional extra)
            #   HashTable.delete() empties the slot and rebuilds the
            #   table so other colliding products can still be found.
            # ---------------------------------------------------------
            # Delete a stored medicine and preserve searches for other IDs.
            elif choice == "4":
                product_id = int(input("Product ID to delete: "))
                # delete() returns True if removed, False if not found.
                if table.delete(product_id):
                    print("Product deleted.")
                else:
                    print("Product not found.")

            # 5. DISPLAY: shows capacity, record count and every slot.
            # Display the current hash-table slots.
            elif choice == "5":
                table.display()

            # 0. EXIT
            # Exit the inventory menu.
            elif choice == "0":
                print("Goodbye.")
                # Leave the menu loop.
                break

            # When any of the conditions did not match.
            else:
                print("Choose a number from 0 to 5.")

        # Catch invalid numeric input or a validation error and keep the menu running.
        # Examples that land here: typing "abc" for an ID (int() fails),
        # a negative price (Medicine rejects it), a duplicate ID (insert
        # rejects it). The message is printed and the loop continues.
        except ValueError as error:
            print("Invalid entry:", error)

# Run the example only when this file is started directly.
if __name__ == "__main__":
    # Open the inventory menu and allow a terminal interruption to exit cleanly.
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nGoodbye.")
