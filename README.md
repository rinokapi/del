feature:
- output: last usn
- recursive
- verbose: attribute, usn, reason
- hardlink
- full path
- sorted

default:
```
$ python3 del.py -t 1 -f mftecmd.csv
. (id: 5, seq: 5)
   cat.jpg (id: 36, seq: 1)
   $RECYCLE.BIN (id: 37, seq: 1)
   target.jpg (id: 40, seq: 1)
   secret.txt (id: 41, seq: 1)
   password.txt (id: 41, seq: 2)
   folder1 (id: 41, seq: 3)
(id: 33, seq: 1)
   WPSettings.dat (id: 40, seq: 2)
(id: 90, seq: 1)
   folder5 (id: 56, seq: 1)
   folder7 (id: 65, seq: 1)
(id: 80, seq: 1)
   Folder7(2) (id: 65, seq: 1)
   Folder8 (id: 66, seq: 1)
```
parent reference:
```
$ python3 del.py -t 1 -f ../mftecmd.csv -p 47 1
PATH: .\folder1\folder2

folder2 (id: 47, seq: 1)
   text1.txt (id: 48, seq: 1)
   text2.txt (id: 49, seq: 1)
   text3.txt (id: 50, seq: 1)
   folder3 (id: 51, seq: 1)
```
recursive:
```
$ python3 del.py -t 1 -f ../mftecmd.csv -p 47 1 -r
PATH: .\folder1\folder2

folder2 (id: 47, seq: 1)
   text1.txt (id: 48, seq: 1)
   text2.txt (id: 49, seq: 1)
   text3.txt (id: 50, seq: 1)
   folder3 (id: 51, seq: 1)
      text1.txt (id: 52, seq: 1)
      text2.txt (id: 53, seq: 1)
      text3.txt (id: 54, seq: 1)
      folder4 (id: 55, seq: 1)
```
verbose:
```
$ python3 del.py -t 1 -f ../mftecmd.csv -p 47 1 -r -v
PATH: .\folder1\folder2

folder2 (id: 47, seq: 1) Directory, 9464, ObjectIdChange|Close
   text1.txt (id: 48, seq: 1) Archive, 10096, ObjectIdChange|Close
   text2.txt (id: 49, seq: 1) Archive, 10728, ObjectIdChange|Close
   text3.txt (id: 50, seq: 1) Archive, 11360, ObjectIdChange|Close
   folder3 (id: 51, seq: 1) Directory, 11920, ObjectIdChange|Close
      text1.txt (id: 52, seq: 1) Archive, 12632, ObjectIdChange|Close
      text2.txt (id: 53, seq: 1) Archive, 13264, ObjectIdChange|Close
      text3.txt (id: 54, seq: 1) Archive, 13896, ObjectIdChange|Close
      folder4 (id: 55, seq: 1) Directory, 13897, ObjectIdChange|Close
```
options:
```
$ python3 del.py -h
usage: del.py [-h] -t {1,2,3} -f FILE [-p NUM NUM] [-r] [-v]

options:
  -h, --help  show this help message and exit
  -t {1,2,3}  tool used for parsing USN Journal (1 = MFTECmd, 2 = UsnJrnl2Csv(dump everything), 3 = ntfs_parse)
  -f FILE     parsed USN Journal (CSV file)
  -p NUM NUM  parent refrence (-p [ParentId] [ParentSeq])
  -r          recursive
  -v          verbose
```