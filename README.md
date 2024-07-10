Provided the Author ID in inspirehep database, the Python script indicates the number of entries and
the total number of citations. 
The script allows to save the record and the next time it is run, the script compares the number of citations,
both total and citations of individual entries.

The script is specially useful to track changes of citations of individual entries.

# How to use
Edit the file "InspirehepCitationsTracker.py" in a IDE or text editing software.
Near the end of the file, set the value of the variable `AUTHOR` to the Author ID in the INSPIREHEP
database (e.g. the default value is 'Stephen.W.Hawking.1' )

Run the script with an IDE with a python interpreter or directly from the command line using:

> Python InspirehepCitationsTracker.py

# Output
## First run
If there is no local save pf the record, the script will simply get the data from the INSPIREHEP database, indicating the number of entries and total citations.
The script will ask if the user wants to save the record to the disk. The standard name format is `AUTHORID_record.pkl` and the record is saved in the same directory of the script file.

**Note:** If the user wants to change the directory where the local record is saved, it simply needs to change the value of the variable `CURRENT_FILE_DIR`

## Further runs
If a record of the author's profile is found on the disk, the script will ask the user if it should compare with the online version.
If the users says yes, then the script will display:

 1. the current number of entries and total citations in the online database;
 2. the new entries that were not listed in the local record;
 3. the entries with updated citations and the change in the citations;
 4. indicate if no changes in the number of citations were detected.

The script will, lastly, ask the user if it wants to update the local record.

