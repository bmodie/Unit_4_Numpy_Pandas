
# Heroes of Pymoli Data Analysis

#3 Observed Trends

-  Heroes of Pymoli is largely dominated by males players (i.e., Males: 82%, Females: 16%, Other: 2%)
-  In-game purchases are broken out in nearly the same ratio as the gender percentages. 
-  In-game purchases are not a huge money maker. Only 4,879 dollars have been spent on in-game items and no one player has spent more than 20 dollars.
-  Of the in-game items, the Bone Crushing Silver Skewer is most profitable, having generated roughly 68 dollars in total purchase value.


```python
import pandas as pd
import numpy as np
import json
```


```python
# read in Players_Complete csv file
total_player_df = pd.read_csv('players_complete.csv')

# read purchase data json file
purchase_df = pd.read_json('purchase_data.json')
purchase2_df = pd.read_json('purchase_data2.json')
purchase3_df = pd.read_json('purchase_data_3.json~HEAD')

# read in items inventory
items_inventory = pd.read_csv('items_complete.csv')
```


```python
## Player Count
# Change Column Header from SN to Screen Name
total_player_df = total_player_df.rename(columns={'SN':'Screen Name'})
total_player_df.head()
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Player ID</th>
      <th>Screen Name</th>
      <th>Age</th>
      <th>Gender</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0</td>
      <td>Marughi89</td>
      <td>21</td>
      <td>Male</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>Lirtedy26</td>
      <td>40</td>
      <td>Male</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2</td>
      <td>Chamistast30</td>
      <td>7</td>
      <td>Male</td>
    </tr>
    <tr>
      <th>3</th>
      <td>3</td>
      <td>Lisirra25</td>
      <td>24</td>
      <td>Male</td>
    </tr>
    <tr>
      <th>4</th>
      <td>4</td>
      <td>Lirtim36</td>
      <td>23</td>
      <td>Male</td>
    </tr>
  </tbody>
</table>
</div>




```python
## Player Count
# Count the total number of unique players
player_count = len(total_player_df['Screen Name'].unique())

total_players = pd.DataFrame({'Total Players':[player_count]})
total_players
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Total Players</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1161</td>
    </tr>
  </tbody>
</table>
</div>




```python
## Gender Demographics
# Identify percentage of male, female, and other/non-disclosed players

male_players = total_player_df['Gender'].value_counts()['Male']
perc_male = (male_players / player_count) * 100

female_players = total_player_df['Gender'].value_counts()['Female']
perc_female = (female_players / player_count) * 100

other_players = player_count - male_players - female_players
perc_other = (other_players / player_count) * 100

gender_demographics = pd.DataFrame({"Male Players": [male_players],
                                   "Percent Male": [perc_male],
                                   "Female Players": [female_players],
                                   "Percent Female": [perc_female],
                                   "Other Players": [other_players],
                                   "Percent Other":[perc_other],
})

gender_demographics = gender_demographics[['Male Players','Percent Male','Female Players','Percent Female','Other Players','Percent Other']]
#gender_demographics = gender_demographics.round(2)
gender_demographics.style.format({"Percent Male": "{:.2f}%", "Percent Female": "{:.2f}%", "Percent Other": "{:.2f}%"})

```




<style  type="text/css" >
</style>  
<table id="T_a9bb3f28_184a_11e8_824a_bc8385f28f74" > 
<thead>    <tr> 
        <th class="blank level0" ></th> 
        <th class="col_heading level0 col0" >Male Players</th> 
        <th class="col_heading level0 col1" >Percent Male</th> 
        <th class="col_heading level0 col2" >Female Players</th> 
        <th class="col_heading level0 col3" >Percent Female</th> 
        <th class="col_heading level0 col4" >Other Players</th> 
        <th class="col_heading level0 col5" >Percent Other</th> 
    </tr></thead> 
<tbody>    <tr> 
        <th id="T_a9bb3f28_184a_11e8_824a_bc8385f28f74level0_row0" class="row_heading level0 row0" >0</th> 
        <td id="T_a9bb3f28_184a_11e8_824a_bc8385f28f74row0_col0" class="data row0 col0" >954</td> 
        <td id="T_a9bb3f28_184a_11e8_824a_bc8385f28f74row0_col1" class="data row0 col1" >82.17%</td> 
        <td id="T_a9bb3f28_184a_11e8_824a_bc8385f28f74row0_col2" class="data row0 col2" >187</td> 
        <td id="T_a9bb3f28_184a_11e8_824a_bc8385f28f74row0_col3" class="data row0 col3" >16.11%</td> 
        <td id="T_a9bb3f28_184a_11e8_824a_bc8385f28f74row0_col4" class="data row0 col4" >20</td> 
        <td id="T_a9bb3f28_184a_11e8_824a_bc8385f28f74row0_col5" class="data row0 col5" >1.72%</td> 
    </tr></tbody> 
</table> 




```python
## Purchasing Analysis (TOTAL)
# Concatenate the 3 json files
all_purchases = pd.concat([purchase_df, purchase2_df, purchase3_df], ignore_index=True)

# Number of Unique Items
#unique_items = all_purchase['Item Name'].count()
unique_items = len(all_purchases["Item Name"].unique())

# Average purchase price
avg_purchase_price = all_purchases['Price'].mean()

# Total purchases
total_purchases = len(all_purchases)

# Total revenue
total_revenue = all_purchases['Price'].sum()

# Create DataFrame
purchase_analysis_total = pd.DataFrame({"Number of Unique Items": [unique_items],
                                   "Average Price": [avg_purchase_price],
                                   "Number of Purchases": [total_purchases],
                                   "Total Revenue": [total_revenue]
})

purchase_analysis_total = purchase_analysis_total[['Number of Unique Items', 'Average Price', 'Number of Purchases', 'Total Revenue']]
purchase_analysis_total.style.format({"Average Price": "${:.2f}", "Total Revenue": "${:.2f}"})


```




<style  type="text/css" >
</style>  
<table id="T_2dac39f8_184a_11e8_a49f_bc8385f28f74" > 
<thead>    <tr> 
        <th class="blank level0" ></th> 
        <th class="col_heading level0 col0" >Number of Unique Items</th> 
        <th class="col_heading level0 col1" >Average Price</th> 
        <th class="col_heading level0 col2" >Number of Purchases</th> 
        <th class="col_heading level0 col3" >Total Revenue</th> 
    </tr></thead> 
<tbody>    <tr> 
        <th id="T_2dac39f8_184a_11e8_a49f_bc8385f28f74level0_row0" class="row_heading level0 row0" >0</th> 
        <td id="T_2dac39f8_184a_11e8_a49f_bc8385f28f74row0_col0" class="data row0 col0" >180</td> 
        <td id="T_2dac39f8_184a_11e8_a49f_bc8385f28f74row0_col1" class="data row0 col1" >$2.98</td> 
        <td id="T_2dac39f8_184a_11e8_a49f_bc8385f28f74row0_col2" class="data row0 col2" >1638</td> 
        <td id="T_2dac39f8_184a_11e8_a49f_bc8385f28f74row0_col3" class="data row0 col3" >$4879.60</td> 
    </tr></tbody> 
</table> 




```python
## Purchasing Analysis (GENDER) 
# Identify purchase count by M/F/O
male_purchase_count = all_purchases['Gender'].value_counts()['Male']
female_purchase_count = all_purchases['Gender'].value_counts()['Female']
other_purchase_count = total_purchases - male_purchase_count - female_purchase_count

# Average Purchase Price and Total Revenue by M/F/O
# males
male_purchases = all_purchases.loc[all_purchases['Gender'] == 'Male', :]
male_avg_price = male_purchases['Price'].mean()
male_revenue = male_purchases['Price'].sum()

# females
female_purchases = all_purchases.loc[all_purchases['Gender'] == 'Female', :]
female_avg_price = female_purchases['Price'].mean()
female_revenue = female_purchases['Price'].sum()

#others
other_purchases_minus_female = all_purchases.loc[all_purchases['Gender'] != 'Female', :]
other_purchases = other_purchases_minus_female.loc[other_purchases_minus_female['Gender'] != 'Male', :]
other_avg_price = other_purchases['Price'].mean()
other_revenue = total_revenue - male_revenue - female_revenue

# Normalized Totals of M/F/O

# Create DataFrame
purchase_analysis_gender = pd.DataFrame({"Gender":['Male','Female','Other'],
                                         "Purchase Count":[male_purchase_count,female_purchase_count,other_purchase_count],
                                         "Average Price":[male_avg_price,female_avg_price, other_avg_price],
                                         "Total Value":[male_revenue, female_revenue, other_revenue]})

purchase_analysis_gender = purchase_analysis_gender[['Gender','Purchase Count','Average Price','Total Value']]
purchase_analysis_gender.style.format({"Average Price": "${:.2f}", "Total Value": "${:.2f}"})
|
```




<style  type="text/css" >
</style>  
<table id="T_01cdb568_184a_11e8_9f2f_bc8385f28f74" > 
<thead>    <tr> 
        <th class="blank level0" ></th> 
        <th class="col_heading level0 col0" >Gender</th> 
        <th class="col_heading level0 col1" >Purchase Count</th> 
        <th class="col_heading level0 col2" >Average Price</th> 
        <th class="col_heading level0 col3" >Total Value</th> 
    </tr></thead> 
<tbody>    <tr> 
        <th id="T_01cdb568_184a_11e8_9f2f_bc8385f28f74level0_row0" class="row_heading level0 row0" >0</th> 
        <td id="T_01cdb568_184a_11e8_9f2f_bc8385f28f74row0_col0" class="data row0 col0" >Male</td> 
        <td id="T_01cdb568_184a_11e8_9f2f_bc8385f28f74row0_col1" class="data row0 col1" >1339</td> 
        <td id="T_01cdb568_184a_11e8_9f2f_bc8385f28f74row0_col2" class="data row0 col2" >$2.99</td> 
        <td id="T_01cdb568_184a_11e8_9f2f_bc8385f28f74row0_col3" class="data row0 col3" >$3997.79</td> 
    </tr>    <tr> 
        <th id="T_01cdb568_184a_11e8_9f2f_bc8385f28f74level0_row1" class="row_heading level0 row1" >1</th> 
        <td id="T_01cdb568_184a_11e8_9f2f_bc8385f28f74row1_col0" class="data row1 col0" >Female</td> 
        <td id="T_01cdb568_184a_11e8_9f2f_bc8385f28f74row1_col1" class="data row1 col1" >279</td> 
        <td id="T_01cdb568_184a_11e8_9f2f_bc8385f28f74row1_col2" class="data row1 col2" >$2.94</td> 
        <td id="T_01cdb568_184a_11e8_9f2f_bc8385f28f74row1_col3" class="data row1 col3" >$820.09</td> 
    </tr>    <tr> 
        <th id="T_01cdb568_184a_11e8_9f2f_bc8385f28f74level0_row2" class="row_heading level0 row2" >2</th> 
        <td id="T_01cdb568_184a_11e8_9f2f_bc8385f28f74row2_col0" class="data row2 col0" >Other</td> 
        <td id="T_01cdb568_184a_11e8_9f2f_bc8385f28f74row2_col1" class="data row2 col1" >20</td> 
        <td id="T_01cdb568_184a_11e8_9f2f_bc8385f28f74row2_col2" class="data row2 col2" >$3.09</td> 
        <td id="T_01cdb568_184a_11e8_9f2f_bc8385f28f74row2_col3" class="data row2 col3" >$61.72</td> 
    </tr></tbody> 
</table> 




```python
## Age Demographics
# Create bins of 4 years
# By bin identify: Purchase Count, Avg Purch Price, Total Purch Value, Normalized Totals
bins = [0,4,8,12,16,20,24,28,32,36,40,44,48,52]
group_names = ['0 to 4','4 to 8','8 to 12','12 to 16','16 to 20','20 to 24','24 to 28','28 to 32','32 to 36','36 to 40','40 to 44','44 to 48','48 to 52']
pd.cut(all_purchases['Age'], bins, labels=group_names)
all_purchases['Age Bracket'] = pd.cut(all_purchases['Age'], bins, labels=group_names)

purchase_groups = all_purchases[['Age Bracket','Price','Item Name']]

group_total_purchase = purchase_groups.groupby('Age Bracket')['Price'].sum().to_frame()
group_purchase_count = purchase_groups.groupby('Age Bracket')['Item Name'].count().to_frame()
group_purchase_avg = purchase_groups.groupby('Age Bracket')['Price'].mean().to_frame()

group_total_purchase.columns=["Age Bracket"]
join_one = group_total_purchase.join(group_purchase_count, how="left")
join_one.columns=["Total Purchase Value", "Purchase Count"]

join_two = join_one.join(group_purchase_avg, how="inner")
join_two.columns=["Total Purchase Value", "Purchase Count", "Average Purchase Price"]

age_demo_df = join_two[["Total Purchase Value","Purchase Count", "Average Purchase Price"]]
age_demo_final = age_demo_df.sort_values('Total Purchase Value', ascending=False).head()
age_demo_final.style.format({"Average Purchase Price": "${:.2f}", "Total Purchase Value": "${:.2f}"})

```




<style  type="text/css" >
</style>  
<table id="T_e91fdb82_184a_11e8_a7c1_bc8385f28f74" > 
<thead>    <tr> 
        <th class="blank level0" ></th> 
        <th class="col_heading level0 col0" >Total Purchase Value</th> 
        <th class="col_heading level0 col1" >Purchase Count</th> 
        <th class="col_heading level0 col2" >Average Purchase Price</th> 
    </tr>    <tr> 
        <th class="index_name level0" >Age Bracket</th> 
        <th class="blank" ></th> 
        <th class="blank" ></th> 
        <th class="blank" ></th> 
    </tr></thead> 
<tbody>    <tr> 
        <th id="T_e91fdb82_184a_11e8_a7c1_bc8385f28f74level0_row0" class="row_heading level0 row0" >20 to 24</th> 
        <td id="T_e91fdb82_184a_11e8_a7c1_bc8385f28f74row0_col0" class="data row0 col0" >$1494.48</td> 
        <td id="T_e91fdb82_184a_11e8_a7c1_bc8385f28f74row0_col1" class="data row0 col1" >503</td> 
        <td id="T_e91fdb82_184a_11e8_a7c1_bc8385f28f74row0_col2" class="data row0 col2" >$2.97</td> 
    </tr>    <tr> 
        <th id="T_e91fdb82_184a_11e8_a7c1_bc8385f28f74level0_row1" class="row_heading level0 row1" >16 to 20</th> 
        <td id="T_e91fdb82_184a_11e8_a7c1_bc8385f28f74row1_col0" class="data row1 col0" >$981.50</td> 
        <td id="T_e91fdb82_184a_11e8_a7c1_bc8385f28f74row1_col1" class="data row1 col1" >332</td> 
        <td id="T_e91fdb82_184a_11e8_a7c1_bc8385f28f74row1_col2" class="data row1 col2" >$2.96</td> 
    </tr>    <tr> 
        <th id="T_e91fdb82_184a_11e8_a7c1_bc8385f28f74level0_row2" class="row_heading level0 row2" >24 to 28</th> 
        <td id="T_e91fdb82_184a_11e8_a7c1_bc8385f28f74row2_col0" class="data row2 col0" >$700.17</td> 
        <td id="T_e91fdb82_184a_11e8_a7c1_bc8385f28f74row2_col1" class="data row2 col1" >232</td> 
        <td id="T_e91fdb82_184a_11e8_a7c1_bc8385f28f74row2_col2" class="data row2 col2" >$3.02</td> 
    </tr>    <tr> 
        <th id="T_e91fdb82_184a_11e8_a7c1_bc8385f28f74level0_row3" class="row_heading level0 row3" >12 to 16</th> 
        <td id="T_e91fdb82_184a_11e8_a7c1_bc8385f28f74row3_col0" class="data row3 col0" >$467.25</td> 
        <td id="T_e91fdb82_184a_11e8_a7c1_bc8385f28f74row3_col1" class="data row3 col1" >160</td> 
        <td id="T_e91fdb82_184a_11e8_a7c1_bc8385f28f74row3_col2" class="data row3 col2" >$2.92</td> 
    </tr>    <tr> 
        <th id="T_e91fdb82_184a_11e8_a7c1_bc8385f28f74level0_row4" class="row_heading level0 row4" >28 to 32</th> 
        <td id="T_e91fdb82_184a_11e8_a7c1_bc8385f28f74row4_col0" class="data row4 col0" >$384.69</td> 
        <td id="T_e91fdb82_184a_11e8_a7c1_bc8385f28f74row4_col1" class="data row4 col1" >127</td> 
        <td id="T_e91fdb82_184a_11e8_a7c1_bc8385f28f74row4_col2" class="data row4 col2" >$3.03</td> 
    </tr></tbody> 
</table> 




```python
## Top Spenders
# Identify the top 5 spenders in the game by total purchase value (list: SN, Purch Count, Avg Purch Price, Total Purch. Price)
top_spenders = all_purchases[['Price','SN']]

sn_total_purchase = top_spenders.groupby('SN')['Price'].sum().to_frame()
sn_purchase_count = top_spenders.groupby('SN')['Price'].count().to_frame()
sn_purchase_avg = top_spenders.groupby('SN')['Price'].mean().to_frame()

sn_total_purchase.columns=["Total Purchase Value"]
join_one = sn_total_purchase.join(sn_purchase_count, how="left")
join_one.columns=["Total Purchase Value", "Purchase Count"]

join_two = join_one.join(sn_purchase_avg, how="inner")
join_two.columns=["Total Purchase Value", "Purchase Count", "Average Purchase Price"]

top_spenders_df = join_two[["Total Purchase Value", "Purchase Count", "Average Purchase Price"]]
top_spenders_final = top_spenders_df.sort_values('Total Purchase Value', ascending=False).head()
top_spenders_final.style.format({"Average Purchase Price": "${:.2f}", "Total Purchase Value": "${:.2f}"})

```




<style  type="text/css" >
</style>  
<table id="T_0b1b2c3e_184b_11e8_99b0_bc8385f28f74" > 
<thead>    <tr> 
        <th class="blank level0" ></th> 
        <th class="col_heading level0 col0" >Total Purchase Value</th> 
        <th class="col_heading level0 col1" >Purchase Count</th> 
        <th class="col_heading level0 col2" >Average Purchase Price</th> 
    </tr>    <tr> 
        <th class="index_name level0" >SN</th> 
        <th class="blank" ></th> 
        <th class="blank" ></th> 
        <th class="blank" ></th> 
    </tr></thead> 
<tbody>    <tr> 
        <th id="T_0b1b2c3e_184b_11e8_99b0_bc8385f28f74level0_row0" class="row_heading level0 row0" >Aerithllora36</th> 
        <td id="T_0b1b2c3e_184b_11e8_99b0_bc8385f28f74row0_col0" class="data row0 col0" >$19.14</td> 
        <td id="T_0b1b2c3e_184b_11e8_99b0_bc8385f28f74row0_col1" class="data row0 col1" >6</td> 
        <td id="T_0b1b2c3e_184b_11e8_99b0_bc8385f28f74row0_col2" class="data row0 col2" >$3.19</td> 
    </tr>    <tr> 
        <th id="T_0b1b2c3e_184b_11e8_99b0_bc8385f28f74level0_row1" class="row_heading level0 row1" >Sondim43</th> 
        <td id="T_0b1b2c3e_184b_11e8_99b0_bc8385f28f74row1_col0" class="data row1 col0" >$17.81</td> 
        <td id="T_0b1b2c3e_184b_11e8_99b0_bc8385f28f74row1_col1" class="data row1 col1" >5</td> 
        <td id="T_0b1b2c3e_184b_11e8_99b0_bc8385f28f74row1_col2" class="data row1 col2" >$3.56</td> 
    </tr>    <tr> 
        <th id="T_0b1b2c3e_184b_11e8_99b0_bc8385f28f74level0_row2" class="row_heading level0 row2" >Rinallorap73</th> 
        <td id="T_0b1b2c3e_184b_11e8_99b0_bc8385f28f74row2_col0" class="data row2 col0" >$17.50</td> 
        <td id="T_0b1b2c3e_184b_11e8_99b0_bc8385f28f74row2_col1" class="data row2 col1" >5</td> 
        <td id="T_0b1b2c3e_184b_11e8_99b0_bc8385f28f74row2_col2" class="data row2 col2" >$3.50</td> 
    </tr>    <tr> 
        <th id="T_0b1b2c3e_184b_11e8_99b0_bc8385f28f74level0_row3" class="row_heading level0 row3" >Undirrala66</th> 
        <td id="T_0b1b2c3e_184b_11e8_99b0_bc8385f28f74row3_col0" class="data row3 col0" >$17.06</td> 
        <td id="T_0b1b2c3e_184b_11e8_99b0_bc8385f28f74row3_col1" class="data row3 col1" >5</td> 
        <td id="T_0b1b2c3e_184b_11e8_99b0_bc8385f28f74row3_col2" class="data row3 col2" >$3.41</td> 
    </tr>    <tr> 
        <th id="T_0b1b2c3e_184b_11e8_99b0_bc8385f28f74level0_row4" class="row_heading level0 row4" >Arithllorin55</th> 
        <td id="T_0b1b2c3e_184b_11e8_99b0_bc8385f28f74row4_col0" class="data row4 col0" >$16.80</td> 
        <td id="T_0b1b2c3e_184b_11e8_99b0_bc8385f28f74row4_col1" class="data row4 col1" >4</td> 
        <td id="T_0b1b2c3e_184b_11e8_99b0_bc8385f28f74row4_col2" class="data row4 col2" >$4.20</td> 
    </tr></tbody> 
</table> 




```python
## Most Popular Items
# Identify the top 5 items by purchase count (list: Name, Purch Count, Price, Total Purch Value)
popular_items = all_purchases[['Item ID','Item Name','Price']]

item_purchase_count = popular_items.groupby('Item ID')['Item Name'].count().to_frame()
item_total_purchase = popular_items.groupby('Item ID')['Price'].sum().to_frame()
item_price = popular_items.groupby('Item ID')['Price'].head().to_frame()
item_name = popular_items.groupby('Item ID')['Item Name'].head().to_frame()

item_purchase_count.columns=["Item Purchase Count"]
join_one = item_purchase_count.join(item_total_purchase, how="left")
join_one.columns=["Item Purchase Count", "Total Purchase Value"]

join_two = join_one.join(item_price, how="inner")
join_two.columns=["Item Purchase Count", "Total Purchase Value", "Item Price"]

join_three = join_two.join(item_name, how="inner")
join_three.columns=["Item Purchase Count", "Total Purchase Value", "Item Price","Item Name"]

popular_items_df = join_three[["Item Name","Item Purchase Count","Total Purchase Value", "Item Price"]]
popular_items_final = popular_items_df.sort_values('Item Purchase Count', ascending=False).head()
popular_items_final.style.format({"Total Purchase Value": "${:.2f}", "Item Price": "${:.2f}"})


```




<style  type="text/css" >
</style>  
<table id="T_97ef4e50_1846_11e8_bc91_bc8385f28f74" > 
<thead>    <tr> 
        <th class="blank level0" ></th> 
        <th class="col_heading level0 col0" >Item Name</th> 
        <th class="col_heading level0 col1" >Item Purchase Count</th> 
        <th class="col_heading level0 col2" >Total Purchase Value</th> 
        <th class="col_heading level0 col3" >Item Price</th> 
    </tr></thead> 
<tbody>    <tr> 
        <th id="T_97ef4e50_1846_11e8_bc91_bc8385f28f74level0_row0" class="row_heading level0 row0" >111</th> 
        <td id="T_97ef4e50_1846_11e8_bc91_bc8385f28f74row0_col0" class="data row0 col0" >Azurewrath</td> 
        <td id="T_97ef4e50_1846_11e8_bc91_bc8385f28f74row0_col1" class="data row0 col1" >16</td> 
        <td id="T_97ef4e50_1846_11e8_bc91_bc8385f28f74row0_col2" class="data row0 col2" >$62.23</td> 
        <td id="T_97ef4e50_1846_11e8_bc91_bc8385f28f74row0_col3" class="data row0 col3" >$2.22</td> 
    </tr>    <tr> 
        <th id="T_97ef4e50_1846_11e8_bc91_bc8385f28f74level0_row1" class="row_heading level0 row1" >31</th> 
        <td id="T_97ef4e50_1846_11e8_bc91_bc8385f28f74row1_col0" class="data row1 col0" >Shadow Strike, Glory of Ending Hope</td> 
        <td id="T_97ef4e50_1846_11e8_bc91_bc8385f28f74row1_col1" class="data row1 col1" >16</td> 
        <td id="T_97ef4e50_1846_11e8_bc91_bc8385f28f74row1_col2" class="data row1 col2" >$35.16</td> 
        <td id="T_97ef4e50_1846_11e8_bc91_bc8385f28f74row1_col3" class="data row1 col3" >$1.93</td> 
    </tr>    <tr> 
        <th id="T_97ef4e50_1846_11e8_bc91_bc8385f28f74level0_row2" class="row_heading level0 row2" >92</th> 
        <td id="T_97ef4e50_1846_11e8_bc91_bc8385f28f74row2_col0" class="data row2 col0" >Reaper's Toll</td> 
        <td id="T_97ef4e50_1846_11e8_bc91_bc8385f28f74row2_col1" class="data row2 col1" >15</td> 
        <td id="T_97ef4e50_1846_11e8_bc91_bc8385f28f74row2_col2" class="data row2 col2" >$30.34</td> 
        <td id="T_97ef4e50_1846_11e8_bc91_bc8385f28f74row2_col3" class="data row2 col3" >$4.56</td> 
    </tr>    <tr> 
        <th id="T_97ef4e50_1846_11e8_bc91_bc8385f28f74level0_row3" class="row_heading level0 row3" >91</th> 
        <td id="T_97ef4e50_1846_11e8_bc91_bc8385f28f74row3_col0" class="data row3 col0" >Malice, Legacy of the Queen</td> 
        <td id="T_97ef4e50_1846_11e8_bc91_bc8385f28f74row3_col1" class="data row3 col1" >15</td> 
        <td id="T_97ef4e50_1846_11e8_bc91_bc8385f28f74row3_col2" class="data row3 col2" >$41.74</td> 
        <td id="T_97ef4e50_1846_11e8_bc91_bc8385f28f74row3_col3" class="data row3 col3" >$2.38</td> 
    </tr>    <tr> 
        <th id="T_97ef4e50_1846_11e8_bc91_bc8385f28f74level0_row4" class="row_heading level0 row4" >84</th> 
        <td id="T_97ef4e50_1846_11e8_bc91_bc8385f28f74row4_col0" class="data row4 col0" >Thorn, Satchel of Dark Souls</td> 
        <td id="T_97ef4e50_1846_11e8_bc91_bc8385f28f74row4_col1" class="data row4 col1" >15</td> 
        <td id="T_97ef4e50_1846_11e8_bc91_bc8385f28f74row4_col2" class="data row4 col2" >$43.89</td> 
        <td id="T_97ef4e50_1846_11e8_bc91_bc8385f28f74row4_col3" class="data row4 col3" >$4.51</td> 
    </tr></tbody> 
</table> 




```python
## Most Profitable Items
# Identify the top 5 items by purchase value (list: Name, Purch Count, Price, Total Purch Value)
profitable_items = all_purchases[['Item ID','Item Name','Price']]

profit_item_purchase_count = profitable_items.groupby('Item ID')['Item Name'].count().to_frame()
profit_item_total_purchase = profitable_items.groupby('Item ID')['Price'].sum().to_frame()
profit_item_price = profitable_items.groupby('Item ID')['Price'].head().to_frame()
profit_item_name = profitable_items.groupby('Item ID')['Item Name'].head().to_frame()

profit_item_total_purchase.columns=['Total Purchase Value']
join_one = profit_item_purchase_count.join(profit_item_total_purchase, how="left")
join_one.columns=["Item Purchase Count", "Total Purchase Value"]

join_two = join_one.join(profit_item_price, how="inner")
join_two.columns=["Item Purchase Count", "Total Purchase Value", "Item Price"]

join_three = join_two.join(profit_item_name, how="inner")
join_three.columns=["Item Purchase Count", "Total Purchase Value", "Item Price","Item Name"]

profitable_items_df = join_three[["Item Name","Total Purchase Value","Item Purchase Count", "Item Price"]]
profitable_items_final = profitable_items_df.sort_values('Total Purchase Value', ascending=False).head()
profitable_items_final.style.format({"Total Purchase Value": "${:.2f}", "Item Price": "${:.2f}"})

```




<style  type="text/css" >
</style>  
<table id="T_1028e90a_1848_11e8_a01d_bc8385f28f74" > 
<thead>    <tr> 
        <th class="blank level0" ></th> 
        <th class="col_heading level0 col0" >Item Name</th> 
        <th class="col_heading level0 col1" >Total Purchase Value</th> 
        <th class="col_heading level0 col2" >Item Purchase Count</th> 
        <th class="col_heading level0 col3" >Item Price</th> 
    </tr></thead> 
<tbody>    <tr> 
        <th id="T_1028e90a_1848_11e8_a01d_bc8385f28f74level0_row0" class="row_heading level0 row0" >52</th> 
        <td id="T_1028e90a_1848_11e8_a01d_bc8385f28f74row0_col0" class="data row0 col0" >Bone Crushing Silver Skewer</td> 
        <td id="T_1028e90a_1848_11e8_a01d_bc8385f28f74row0_col1" class="data row0 col1" >$68.05</td> 
        <td id="T_1028e90a_1848_11e8_a01d_bc8385f28f74row0_col2" class="data row0 col2" >15</td> 
        <td id="T_1028e90a_1848_11e8_a01d_bc8385f28f74row0_col3" class="data row0 col3" >$3.37</td> 
    </tr>    <tr> 
        <th id="T_1028e90a_1848_11e8_a01d_bc8385f28f74level0_row1" class="row_heading level0 row1" >93</th> 
        <td id="T_1028e90a_1848_11e8_a01d_bc8385f28f74row1_col0" class="data row1 col0" >Netherbane</td> 
        <td id="T_1028e90a_1848_11e8_a01d_bc8385f28f74row1_col1" class="data row1 col1" >$63.42</td> 
        <td id="T_1028e90a_1848_11e8_a01d_bc8385f28f74row1_col2" class="data row1 col2" >14</td> 
        <td id="T_1028e90a_1848_11e8_a01d_bc8385f28f74row1_col3" class="data row1 col3" >$1.48</td> 
    </tr>    <tr> 
        <th id="T_1028e90a_1848_11e8_a01d_bc8385f28f74level0_row2" class="row_heading level0 row2" >111</th> 
        <td id="T_1028e90a_1848_11e8_a01d_bc8385f28f74row2_col0" class="data row2 col0" >Azurewrath</td> 
        <td id="T_1028e90a_1848_11e8_a01d_bc8385f28f74row2_col1" class="data row2 col1" >$62.23</td> 
        <td id="T_1028e90a_1848_11e8_a01d_bc8385f28f74row2_col2" class="data row2 col2" >16</td> 
        <td id="T_1028e90a_1848_11e8_a01d_bc8385f28f74row2_col3" class="data row2 col3" >$2.22</td> 
    </tr>    <tr> 
        <th id="T_1028e90a_1848_11e8_a01d_bc8385f28f74level0_row3" class="row_heading level0 row3" >49</th> 
        <td id="T_1028e90a_1848_11e8_a01d_bc8385f28f74row3_col0" class="data row3 col0" >Severance</td> 
        <td id="T_1028e90a_1848_11e8_a01d_bc8385f28f74row3_col1" class="data row3 col1" >$58.03</td> 
        <td id="T_1028e90a_1848_11e8_a01d_bc8385f28f74row3_col2" class="data row3 col2" >13</td> 
        <td id="T_1028e90a_1848_11e8_a01d_bc8385f28f74row3_col3" class="data row3 col3" >$1.85</td> 
    </tr>    <tr> 
        <th id="T_1028e90a_1848_11e8_a01d_bc8385f28f74level0_row4" class="row_heading level0 row4" >107</th> 
        <td id="T_1028e90a_1848_11e8_a01d_bc8385f28f74row4_col0" class="data row4 col0" >Spectral Diamond Doomblade</td> 
        <td id="T_1028e90a_1848_11e8_a01d_bc8385f28f74row4_col1" class="data row4 col1" >$52.87</td> 
        <td id="T_1028e90a_1848_11e8_a01d_bc8385f28f74row4_col2" class="data row4 col2" >13</td> 
        <td id="T_1028e90a_1848_11e8_a01d_bc8385f28f74row4_col3" class="data row4 col3" >$4.25</td> 
    </tr></tbody> 
</table> 


