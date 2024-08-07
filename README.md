# Scraper for Irish diplomatic missions abroad

The scraper uses HTTPX and Selectolax to scrape the data from
Ireland's [Department of Foreign Affairs (DFA)](https://www.ireland.ie/en/dfa/embassies) and separates it into:
Countries,
Diplomats, Embassies, Consulates and Representations.

My objective is to have faster access to specific information, which is slow and cumbersome to find in the current
collapsible accordion format provided by DFA's website; and to have a foundation onto which more data can be added for
analysis.

## Stored Data

The scraped data has been stored in a MongoDB database, and can be accessed [through this API](#).

## Caveat

The current data was scraped in July 2024 and should not be considered to be neither accurate nor up-to-date unless the
data is re-scraped after any updates have been made (diplomatic appointments are normally announced in Augus/September),
and it is verified against an official publication.