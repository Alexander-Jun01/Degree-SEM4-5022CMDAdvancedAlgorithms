# Q1.1: Resizable open-addressed hash table with linear probing.
#
# ======================================================================
# WHAT THIS FILE DOES (Brief Q1 #1)
#   Builds a HASH TABLE that stores (key, value) pairs.
#   - Collision resolution: OPEN ADDRESSING with LINEAR PROBING.
#     If the home slot is taken, try the next slot, then the next, ...
#   - The table is RESIZABLE: when it is full it doubles its size.
#   - It is GENERIC: the value can be any object (a Medicine, a string...).
#     It does not know anything about pharmacy products.
#
# KEY WORDS FOR THE VIVA
#   slot        = one position in the table (index 0 .. size-1)
#   home slot   = key % size  (the first slot we try)
#   probe       = checking one slot
#   collision   = two keys want the same home slot
#   load factor = count / size (how full the table is)
#   rehash      = put every key again using the NEW size
# ======================================================================

# Keep keys and values in matching lists; integer keys can be negative.
class HashTable:
    # ------------------------------------------------------------------
    # __init__ : create an empty table.
    #   size  -> the starting number of slots (capacity).
    #   Example: HashTable(11) makes 11 empty slots, numbered 0..10.
    # ------------------------------------------------------------------
    # size is the starting capacity; the table can grow later.
    def __init__(self, size):
        # Reject invalid sizes before allocating either list.
        # type(size) is not int  -> blocks 2.5, "11" and also True/False.
        # size <= 0              -> a table needs at least one slot,
        #                           otherwise key % size divides by zero.
        if type(size) is not int or size <= 0:
            raise ValueError("Table size must be a positive integer.")
        # Save the current capacity and number of occupied slots.
        # size  = how many slots exist (capacity).
        # count = how many slots are actually used (number of records).
        # VIVA: size and count are different! 6 slots with 4 records
        #       means 2 slots are still free.
        self.size = size
        self.count = 0
        # None in the key list marks an unused slot.
        # SLOT STRUCTURE (Brief Q1.5(i)): two "parallel" lists.
        #   keys[i]   -> the key (product ID) stored in slot i
        #   values[i] -> the object stored with that key (e.g. a Medicine)
        #   [None] * size creates a list of `size` empty slots.
        # Why two lists? It is simple to read, simple to display, and each
        # slot holds exactly one key (no chains/linked lists needed).
        self.keys = [None] * size
        self.values = [None] * size

    # ------------------------------------------------------------------
    # resize : change the number of slots and REHASH every record.
    #   new_size -> the new capacity.
    #   Used automatically by insert() when the table is full, used by
    #   delete() to rebuild the table, and by menu option 5.
    #
    # VIVA: Why can't we just add empty slots at the end?
    #   Because the home slot is key % size. When size changes, the home
    #   slot of almost every key changes too. Example: key 11
    #   11 % 3 = 2 but 11 % 6 = 5. If we only copied the old lists,
    #   search would look in the wrong slot and fail to find the key.
    #   So every key must be inserted again using the new size.
    # ------------------------------------------------------------------
    # Rebuild every entry because key % size changes when capacity changes.
    def resize(self, new_size):
        # A smaller table must still have room for every existing record.
        # Rule 1: the new size must be a positive whole number.
        if type(new_size) is not int or new_size <= 0:
            raise ValueError("New capacity must be a positive integer.")
        # Rule 2: you cannot shrink below the number of stored records,
        # otherwise some records would have no slot.
        if new_size < self.count:
            raise ValueError("New capacity cannot be smaller than the record count.")
        # Save the old lists so their key/value pairs stay together.
        # (We keep a reference to the old lists before replacing them.)
        old_keys = self.keys
        old_values = self.values
        # Allocate both new lists before changing the current table.
        new_keys = [None] * new_size
        new_values = [None] * new_size
        # Switch the table over to the new, empty lists.
        self.size = new_size
        self.keys = new_keys
        self.values = new_values
        # Reinserting the survivors will rebuild the record count.
        # count goes back to 0 because insert() adds 1 for each record.
        self.count = 0
        # Scan old physical slots, preserving each original value object.
        # Go through every OLD slot; if it held a key, insert that key
        # (and the SAME value object) into the new table.
        # Cost: O(m) work in the normal case (m = number of slots),
        # up to O(m^2) if many keys collide into one long cluster.
        for i in range(len(old_keys)):
            if old_keys[i] is not None:
                self.insert(old_keys[i], old_values[i])

    # ------------------------------------------------------------------
    # insert : add a NEW key with its value.
    #   Returns the slot number where the key was stored.
    #   Raises ValueError for a non-integer key or a duplicate key.
    #
    # STEP BY STEP
    #   1. Check the key is an integer.
    #   2. If the table is full -> reject duplicates, then double the size.
    #   3. home = key % size.
    #   4. Try home, home+1, home+2, ... (wrapping round to 0).
    #   5. Same key found  -> duplicate -> error.
    #      Empty slot found -> store the key and value there.
    #
    # EXAMPLE (size 11): 1042 % 11 = 8 -> slot 8.
    #   1053 % 11 = 8 too (collision) -> slot 8 taken -> try 9 -> free.
    # ------------------------------------------------------------------
    # Add one distinct key; a full table doubles before the new insertion.
    def insert(self, key, value):
        # Only whole-number keys work with the % hash function.
        if type(key) is not int:
            raise ValueError("Keys must be integers.")
        # Is every slot already used? Then there is no space left.
        if self.count == self.size:
            # Reject a duplicate before allocating a larger table.
            # (No point growing the table for a key that already exists.)
            if key in self.keys:
                raise ValueError("This product ID already exists.")
            # EDIT HERE: this is the growth rule. "* 2" doubles the size.
            # To grow earlier (e.g. at 70% full) you would change the
            # condition above to: if self.count >= self.size * 0.7:
            self.resize(self.size * 2)
        # Use the current capacity after any automatic growth.
        # HASH FUNCTION: the remainder after dividing by the table size.
        # It always gives a number from 0 to size-1, i.e. a valid slot.
        home = key % self.size
        # probes counts how many slots we have moved away from home.
        probes = 0
        # Never check more than `size` slots -> the loop cannot run forever.
        while probes < self.size:
            # Linear probing wraps from the last slot back to zero.
            # (home + probes) moves forward one slot each time;
            # % self.size wraps past the last slot back to slot 0.
            # Example size 11: home 8 -> 8, 9, 10, 0, 1, ...
            index = (home + probes) % self.size
            # The same key is already stored -> do not store it twice.
            if self.keys[index] == key:
                raise ValueError("This product ID already exists.")
            # Found an empty slot -> store the pair here.
            if self.keys[index] is None:
                self.keys[index] = key
                self.values[index] = value
                # One more record is stored.
                self.count += 1
                # Tell the caller which slot was used (shown in the menu).
                return index
            # Slot is taken by a different key (a collision):
            # move on to the next slot = LINEAR probing (step size 1).
            probes += 1
        # This is a defensive check; growth provides space for valid insertions.
        # (Normally impossible because a full table grew above.)
        raise ValueError("No empty slot available.")

    # ------------------------------------------------------------------
    # search : find the value stored with a key.
    #   Returns the value, or None if the key is not in the table.
    #   It follows exactly the same probe path as insert().
    #
    # VIVA: Why can search stop at an empty (None) slot?
    #   insert() always uses the FIRST empty slot on the probe path.
    #   So if the key existed, it would be before this empty slot.
    #   Reaching None therefore proves the key is not stored.
    #   (This is only true because delete() rebuilds the table instead of
    #    leaving holes in the middle of a cluster.)
    # ------------------------------------------------------------------
    # Return the associated value, or None for an absent integer key.
    def search(self, key):
        if type(key) is not int:
            raise ValueError("Keys must be integers.")
        # Start at the same home slot that insert() used.
        home = key % self.size
        probes = 0
        # At most `size` checks, so searching a full table still ends.
        while probes < self.size:
            index = (home + probes) % self.size
            # Rehashing after deletion keeps this early stopping rule valid.
            # Empty slot -> the key cannot be further along -> not found.
            if self.keys[index] is None:
                return None
            # Match -> return the object stored in the matching value slot.
            if self.keys[index] == key:
                return self.values[index]
            # Different key here -> keep probing forward.
            probes += 1
        # Checked every slot and did not find it.
        return None

    # ------------------------------------------------------------------
    # delete : remove a key and its value.
    #   Returns True if it was deleted, False if it was not found.
    #
    # VIVA: Why not just set the slot back to None?
    #   Example: 1042, 1053, 1064 all hash to slot 8 and sit in 8, 9, 10.
    #   If we empty slot 9 (1053), a search for 1064 starts at 8, then
    #   reaches the empty slot 9 and wrongly stops with "not found".
    #   Fix used here: after emptying the slot, call resize(self.size),
    #   which re-inserts every remaining key so there are no gaps.
    #   (Another common fix is a "tombstone" marker - see Lab 5.3.)
    # ------------------------------------------------------------------
    # Remove one entry and rebuild its probe chain at the same capacity.
    def delete(self, key):
        if type(key) is not int:
            raise ValueError("Keys must be integers.")
        # Not stored at all -> nothing to delete.
        if key not in self.keys:
            return False
        # Find the slot that holds this key.
        index = self.keys.index(key)
        # Empty that slot (both the key and its matching value).
        self.keys[index] = None
        self.values[index] = None
        # One record fewer.
        self.count -= 1
        # Deletion does not automatically shrink the table.
        # Rebuild at the SAME size so every remaining key is placed on a
        # correct probe path again (removes the gap we just made).
        self.resize(self.size)
        return True

    # ------------------------------------------------------------------
    # display : print the capacity, number of records and every slot.
    #   Useful in the VIVA to SHOW where each key ended up.
    # ------------------------------------------------------------------
    # Show the current capacity, occupancy and every key slot.
    def display(self):
        print(f"Capacity: {self.size} | Records: {self.count}")
        # Print slot 0 .. size-1; an empty slot prints "None".
        for i in range(self.size):
            print(f"Slot {i}: {self.keys[i]}")

# ======================================================================
# MENU (only runs when this file is started directly)
#   Lets you test the generic table with your own integer keys and
#   text values. Every ValueError is caught and printed, so a wrong
#   input never crashes the program - the menu simply shows again.
# ======================================================================
# Let the user try the generic table with their own integer keys and text values.
def main():
    # --- Step 1: ask for the starting capacity (repeat until valid) ---
    while True:
        try:
            # .strip() removes spaces the user may type by accident.
            answer = input("Initial capacity (1-1000, Enter for 11, 0 to exit): ").strip()
            if answer == "0":
                print("Goodbye.")
                return
            # Pressing Enter (empty text) means "use the default of 11".
            # EDIT HERE: change 11 to use a different default capacity.
            size = 11 if answer == "" else int(answer)
            # EDIT HERE: the allowed range for the starting capacity.
            if size < 1 or size > 1000:
                raise ValueError("Use a capacity from 1 to 1000.")
            table = HashTable(size)
            # Valid capacity -> leave this loop and open the main menu.
            break
        except ValueError as error:
            # int("abc") or a bad range lands here; ask again.
            print("Invalid entry:", error)

    # --- Step 2: the main menu loop ---
    # Keep the same table between choices so later searches see earlier insertions.
    while True:
        print("\n=== Linear Probing Hash Table ===")
        print("1. Insert key and value")
        print("2. Search key")
        print("3. Delete key")
        print("4. Display hash table")
        print("5. Resize hash table")
        print("0. Exit")
        choice = input("Enter choice: ").strip()
        try:
            # 1. INSERT --------------------------------------------------
            if choice == "1":
                # int() turns the typed text into a whole number;
                # typing letters raises ValueError (caught below).
                key = int(input("Integer key: "))
                value = input("Text value: ").strip()
                if value == "":
                    raise ValueError("The value cannot be empty.")
                # Remember the size so we can tell the user if it grew.
                old_size = table.size
                index = table.insert(key, value)
                if table.size != old_size:
                    print(f"Hash table resized from {old_size} to {table.size} slots.")
                print(f"Key inserted into slot {index}.")
            # 2. SEARCH --------------------------------------------------
            elif choice == "2":
                key = int(input("Integer key: "))
                value = table.search(key)
                # search() returns None when the key is not stored.
                if value is None:
                    print("Key not found.")
                else:
                    print("Value:", value)
            # 3. DELETE --------------------------------------------------
            elif choice == "3":
                key = int(input("Integer key to delete: "))
                # delete() returns True (deleted) or False (not found).
                if table.delete(key):
                    print("Key deleted.")
                else:
                    print("Key not found.")
            # 4. DISPLAY -------------------------------------------------
            elif choice == "4":
                table.display()
            # 5. MANUAL RESIZE -------------------------------------------
            elif choice == "5":
                new_size = int(input("New capacity (1-100000, at least the record count): "))
                # A menu limit only, so the display stays readable.
                # (The resize() method itself has no upper limit.)
                if new_size > 100000:
                    raise ValueError("Use a capacity of at most 100000 for this display menu.")
                table.resize(new_size)
                print(f"Hash table resized to {table.size} slots.")
            # 0. EXIT ----------------------------------------------------
            elif choice == "0":
                print("Goodbye.")
                return
            else:
                print("Choose a number from 0 to 5.")
        # Any ValueError from int(), insert(), resize()... is shown here
        # and the while loop shows the menu again (no crash).
        except ValueError as error:
            print("Invalid entry:", error)


# Importing HashTable does not open the menu in another file.
# __name__ == "__main__" is only True when THIS file is run directly.
# When Q1_2.py does "from Q1_1 import HashTable", the menu does NOT start.
if __name__ == "__main__":
    try:
        main()
    # Ctrl+D / Ctrl+C (or input ending) closes the program politely.
    except (EOFError, KeyboardInterrupt):
        print("\nGoodbye.")
