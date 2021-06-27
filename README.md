# Data_Deduplication-
Data deduplication looks for redundancy of sequences of bytes across very large comparison windows. Sequences of data (over 8 KB long) are compared to the history of other such sequences. The first uniquely stored version of a sequence is referenced rather than stored again. This process is completely hidden from users and applications so the whole file is readable after it's written.