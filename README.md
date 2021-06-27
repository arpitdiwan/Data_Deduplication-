# Data_Deduplication-
Data deduplication looks for redundancy of sequences of bytes across very large comparison windows. Sequences of data (over 8 KB long) are compared to the history of other such sequences. The first uniquely stored version of a sequence is referenced rather than stored again. This process is completely hidden from users and applications so the whole file is readable after it's written.

Who uses data deduplication and why?

Deduplication is ideal for highly redundant operations like backup, which requires repeatedly copying and storing the same data set multiple times for recovery purposes over 30- to 90-day periods. As a result, enterprises of all sizes rely on backup and recovery with deduplication for fast, reliable, and cost-effective backup and recovery.

Main Libraries used in this application are PyQt5 for GUI, Sockets for establishing the TCP, hashlib for generating hash values and Sqlite For the database

First start the server_core.py in server folder
then start the client_log.py

