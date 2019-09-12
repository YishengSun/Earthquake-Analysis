"""
Yisheng Sun(NetID:yisheng4) completed this assignment7 independently.
I chose to compare earthquakes happened in China and Japan,
and the standard to add in is only what the description/text writes.
For example, "8km SE of Shiraoi, Japan", I would count it in Japan's earthquakes.
"""

import requests
import lxml.html
import pandas as pd
from time import sleep
from prettytable import PrettyTable


def get_tree(year=None) -> lxml.etree:
    """ Get the XML tree by entering the year.

    :param year: The year you want to search.
    :return: The tree of search result of this year.
    """
    url = 'https://earthquake.usgs.gov/fdsnws/event/1/query.quakeml?starttime=' \
            + year + '-01-01%2000:00:00&endtime=' + year \
            + '-12-31%2023:59:59&maxlatitude=53.966&minlatitude=9.102&maxlongitude=155.039&' \
            + 'minlongitude=71.543&minmagnitude=4&orderby=time'

    # Fetch the url web page, and convert the response into an HTML document tree:
    tree = None
    while tree is None:
        try:
            r = requests.get(url)
            tree = lxml.html.fromstring(r.content)
            break
        except (ConnectionError, ConnectionRefusedError) as e:
            print('Error retrieving web page.  Retrying in 10 seconds...')
            sleep(10)
    return tree


df_result_CN = pd.DataFrame(columns=['region_revised', 'magnitude', 'year'])
df_result_JP = pd.DataFrame(columns=['region_revised', 'magnitude', 'year'])

for i in range(1950, 2020):
    result_tree = get_tree(str(i))
    region = result_tree.xpath('//description/text/text()')
    magnitude = result_tree.xpath('//mag/value/text()')
    result_per_year = {'region': region, 'magnitude': magnitude}
    df_result_per_year_og = pd.DataFrame(result_per_year)
    df_result_per_year_og.loc[:, 'focus'], df_result_per_year_og.loc[:, 'region_revised'] = df_result_per_year_og['region'].str.split(', ', 1).str
    df_result_per_year_r1 = df_result_per_year_og.loc[:, ['region_revised', 'magnitude']]
    df_result_per_year_r1['year'] = str(i)
    df_result_per_year_CN = df_result_per_year_r1.loc[df_result_per_year_r1.region_revised == "China"].reset_index(drop=True)
    df_result_CN = pd.concat([df_result_CN, df_result_per_year_CN], axis=0, ignore_index=True)
    df_result_per_year_JP = df_result_per_year_r1.loc[df_result_per_year_r1.region_revised == "Japan"].reset_index(drop=True)
    df_result_JP = pd.concat([df_result_JP, df_result_per_year_JP], axis=0, ignore_index=True)


df_result_JP[['year']] = df_result_JP[['year']].astype(int)
df_result_CN[['year']] = df_result_CN[['year']].astype(int)
df_result_JP[['magnitude']] = df_result_JP[['magnitude']].astype(float)
df_result_CN[['magnitude']] = df_result_CN[['magnitude']].astype(float)
JP_per_decade = []
JP_per_mag_range = []
CN_per_decade = []
CN_per_mag_range = []

for i in range(0, 7):
    JP_per_decade.append(len(df_result_JP.loc[df_result_JP['year'].isin(range(1950 + i * 10, 1960 + i * 10))]))
    CN_per_decade.append(len(df_result_CN.loc[df_result_CN['year'].isin(range(1950 + i * 10, 1960 + i * 10))]))
JP_per_decade.append(sum(JP_per_decade))
CN_per_decade.append(sum(CN_per_decade))

for i in range(0, 6):
    JP_per_mag_range.append(len(df_result_JP.loc[df_result_JP['magnitude'] < 5+i].loc[df_result_JP['magnitude'] >= 4+i]))
    CN_per_mag_range.append(len(df_result_CN.loc[df_result_CN['magnitude'] < 5+i].loc[df_result_CN['magnitude'] >= 4+i]))
JP_per_mag_range.append(sum(JP_per_mag_range))
CN_per_mag_range.append(sum(CN_per_mag_range))


sum_per_decade = []
for i in range(0, len(JP_per_decade)):
    sum1 = JP_per_decade[i]+CN_per_decade[i]
    sum_per_decade.append(sum1)

sum_per_mag_range = []
for i in range(0, len(JP_per_mag_range)):
    sum2 = JP_per_mag_range[i]+CN_per_mag_range[i]
    sum_per_mag_range.append(sum2)


percentage_JP_per_decade = []
percentage_CN_per_decade = []
for i in range(0, len(JP_per_decade)):
    p_JP = str(round((JP_per_decade[i]/sum_per_decade[i])*100))+'%'
    p_CN = str(round((CN_per_decade[i]/sum_per_decade[i])*100))+'%'
    percentage_JP_per_decade.append(p_JP)
    percentage_CN_per_decade.append(p_CN)

percentage_JP_per_mag_range = []
percentage_CN_per_mag_range = []
for i in range(0, len(JP_per_mag_range)):
    pm_JP = str(round((JP_per_mag_range[i]/sum_per_mag_range[i])*100))+'%'
    pm_CN = str(round((CN_per_mag_range[i]/sum_per_mag_range[i])*100))+'%'
    percentage_JP_per_mag_range.append(pm_JP)
    percentage_CN_per_mag_range.append(pm_CN)

table1 = PrettyTable()
table1.align = "l"
Decade = ["1950s", "1960s", "1970s", "1980s", "1990s", "2000s", "2010s", "Total"]
table1.add_column("Decade", Decade)
table1.add_column("China", CN_per_decade)
table1.add_column("Percentage", percentage_CN_per_decade)
table1.add_column("Japan", JP_per_decade)
table1.add_column("Percentage", percentage_JP_per_decade)
print("Total earthquakes per region per decade with magnitude >= 4:")
print(table1)

table2 = PrettyTable()
table2.align = "l"
Mag_range = ["4.0-4.99", "5.0-5.99", "6.0-6.99", "7.0-7.99", "8.0-8.99", "9.0-9.99", "Total"]
table2.add_column("Magnitude", Mag_range)
table2.add_column("China", CN_per_mag_range)
table2.add_column("Percentage", percentage_CN_per_mag_range)
table2.add_column("Japan", JP_per_mag_range)
table2.add_column("Percentage", percentage_JP_per_mag_range)
print("Total earthquakes per region per magnitude range:")
print(table2)

