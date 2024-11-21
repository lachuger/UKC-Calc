##WORK IN PROGRESS##

ukcMain.py is the original prototype for pulling tide tables. 

  -StationID pull request currently working with EXACT station name only.
  
  -Datum implementation is not enabled so any tide data requests are being bounced with a "Datum" error message.

ukcDatumFork.py is the current build in progress.

  -StationID search has *limited* functionality and isn't much better than the Single Station ID pull from the ukcMain file.
  
  -Currently in the process of debugging issue where stationID is being pulled but data isn't populating the "Datum" def correctly
