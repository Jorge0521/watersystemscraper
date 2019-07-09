# Water System Data

This is the format of the data retrieved from:
> with other columns added
https://enviro.epa.gov/enviro/sdw_query_v3.get_list?wsys_name=&fac_search=fac_beginning&fac_county=&fac_city=&pop_serv=500&pop_serv=3300&pop_serv=10000&pop_serv=100000&pop_serv=100001&sys_status=active&pop_serv=&wsys_id=&fac_state=AK&last_fac_name=&page=1&query_results=&total_rows_found=:


| Water System name | County served | City served | Pop served | Primary water source type | PWS Activity | Water System ID | Provided City | Got Data | Data for geojson | Data for bounding box |
| ----------------- | ------------- | ----------- | ---------- | ------------------------- | ------------ | --------------- | ------------- | -------- | ---------------- | --------------------- |

Fields that are modIfied when I collected the data and new Fields that I added:

**City Served**
- Its an array that stores all cities served by that water system

**Provided City**
- Boolean where
  - True = A city was provided in the data,
  - False = No city Provided

**Got Data**
 - Boolean where
   - True = Data for geojson/bounding box provided,
   - By default false if city is not provided

**Data for geojson**
- If there are multiple cities then the data is stored in an array [[{type}],[{type}]]
- This column is geojson objects

**Data for bounding box**
- Bounding box data stored in array, format for multiple bounding box = [[], [], []]

The data for `geojson` and `bounding box` is collected from [here](https://nominatim.openstreetmap.org)

Its collected at the same time I collect the data from EPA.

This data is saved in CSV files for every single state, the reason for this is because scraping was taking too long and if an error occurred progress would be lost

Right now all the states except for NY and DC are scra8ped. Theres is an issue with NY where itsnot  proceding to the next 10 systems unless 5-10 min have passed. Im going let it run overnightand upload the file to the repo once its done

One thing to note there were a few states that only provided what county the water system provides water to.

AR, TX, OH, UT, LA, MS,OR, PA, WA are the states that I am aware have this issue.

Assumption: Maybe that is the only water system that provides water to that county?

If so I found a file of the boundaries for counties across the US.

It’s in the code baseIf you need all the files as one CSV file we can merge them, shouldn’t be an issue.

## Violations

For Violations I went to: https://ofmpub.epa.gov/apex/sfdw/f?p=108:11:::NO:RP,RIR::

Here they give us the option to download their tables as CSV files. I downloaded all the Violations for the past 4-5 years(every quarter).
These files are big(50.1Mb ~ each) with 150,000 columns each
- Level detected for contaminant is not in these CSV, they only tell us the type
  - Possible Solution: Still Looking for this Info
- The number of violations is not in these CSV
  - Possible Solution: Iterate through the data collected and count how many times aspecific water system id is listed per quarter.


If you want to run the scraper I have a repository set up [here](https://github.com/Jorge0521/watersystemscraper)

The command needed to run is:

```sh
python3 scrapewater.pyThen
```

it may prompt you to `pip install selenium` and `pandas`.

If you are getting errors about permissions, redownload the [chromedriver](https://sites.google.com/a/chromium.org/chromedriver/downloadsVersion)


ChromeDriver 75.0.3770.8