##WORK IN PROGRESS##

ukcMain.py is the original prototype for pulling tide tables.

-StationID pull request currently working with EXACT station name only.

-Datum implementation is not enabled so any tide data requests are being bounced with a "Datum" error message.

ukcDatumFork.py is the current build in progress.

-StationID search has _limited_ functionality and isn't much better than the Single Station ID pull from the ukcMain file.

-Currently in the process of debugging issue where stationID is being pulled but data isn't populating the "Datum" def correctly

-(NEW)Added a validation step that doesn't seem to be working properly

https://tidesandcurrents.noaa.gov/datum-updates/ntde/#:~:text=The%20National%20Tidal%20Datum%20Epoch,%2C%20mean%20lower%20low%20water)
