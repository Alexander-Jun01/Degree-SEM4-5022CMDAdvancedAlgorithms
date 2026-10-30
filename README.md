All twelve Python files retain their menus. This separate version adds an interactive console menu to every Python file. Open this folder in PyCharm, right-click any .py file and choose Run. Enter choices in the Run console. Choose 0 to exit; in Q2.5's Advanced Features menu, 0 returns to University Courses.

Keep all code files together. Imports reuse classes and functions from neighbouring files without opening their menus. No launcher is needed. Each separately started program has its own in-memory data and resets on restart. Q2.5 shares changes between its own main and advanced menus.

| File | Brief item | What you can do |
| --- | --- | --- |
| Q1_1.py | 1.1 | Generic hash table with linear probing |
| Q1_2.py | 1.2 | Medicine class and predefined pharmacy storage |
| Q1_3.py | 1.3 | Complete pharmacy inventory menu |
| Q1_4.py | 1.4 | Hash-table and array search timing |
| Q2_1.py | 2.1 | Generic unweighted directed graph |
| Q2_2.py | 2.2 | Course entity and single-profile editor |
| Q2_3.py | 2.3 | Six course profiles and profile-list menu |
| Q2_4.py | 2.4 | Course prerequisite graph and relationship editor |
| Q2_5.py | 2.5 | University course main and advanced menus |
| Q3_2.py | 3.2 | Fibonacci function, shared input helpers and calculator |
| Q3_3.py | 3.3 | Three-worker threaded timing experiment |
| Q3_4.py | 3.4 | Sequential timing experiment |

Q1.1 asks for capacity before its menu. Press Enter for 11 slots, choose 1-1000, or enter 0 to exit. It starts empty so you can insert your own keys. Q1.2 and Q1.3 start with three predefined medicines in an eleven-slot table.

Q1.4 choice 1 runs 1000 records for ten rounds in 2003 slots. Choice 2 lets you enter 1-5000 records, 1-20 rounds and a target load of 0.1-1.0. Both methods search the same objects and queries.

Q2.5 choice 5 opens Advanced Features. Its choices are 1 Add course, 2 View profile by level, 3 Add prerequisite, 4 Remove prerequisite and 0 Return. There are initially six courses; additions stop at ten. Full details always show every field. Only the advanced profile view hides elective details except the name. For X requiring Y, the edge is Y -> X.

Q3.3 and Q3.4 choice 1 run the assignment inputs 35, 38 and 40 for ten rounds. Choice 2 accepts exactly three inputs from 0 to 1000 and 1-100 rounds. Use matching custom parameters in both files for a comparison. Each output includes per-round nanoseconds, total and average.

CODE_EXPLANATION_AND_EDITING_GUIDE.md explains the changes, menu options and every executable source line, with edit locations and parameter bounds. Personal details, repository URL and personal reflection must be completed with your own information in the portfolio.

## Resizable hash table

Q1_1.py now tracks size (current capacity) and count (stored records). Inserting a new distinct key into a full table doubles capacity and rehashes every existing record before insertion. Duplicate IDs are rejected without growth. Values remain the same objects, but their physical slots may change. The display header reports both capacity and record count.

Call table.resize(new_size) to grow or shrink manually. The API requires a positive integer with space for every current record. It has no configured upper bound. Deleting a record rebuilds probe chains at the current capacity and does not automatically shrink.

Q1_2.py still starts with three predefined medicines in eleven slots. With no deletions, the twelfth total distinct record grows the table to 22 slots. Q1_3.py reports the capacity change when an insertion causes growth; its existing 1-5 choices and 0 Exit remain the same.

The default Q1_4.py experiment still uses 1000 records, 2003 slots and ten rounds. That setup does not resize, and search timing excludes data insertion and rehashing.

Q1_1.py keeps its initial capacity prompt (1-1000, Enter for 11, 0 Exit). Its menu now includes 5 Resize, alongside 1 Insert, 2 Search, 3 Delete, 4 Display and 0 Exit. The manual resize menu permits 1-100000 slots and rejects capacities below count. This display-menu bound does not limit the reusable resize() API. Q1_2.py also reports automatic growth when adding a medicine. Custom Q1_4.py comparisons retain the selected initial load; the chosen capacity already holds all generated records.

Keep all twelve Python files in this one Portfolio_Code folder so neighbouring imports work.
