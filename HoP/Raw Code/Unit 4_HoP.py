import pandas as pd
import numpy as np
import json

# read in Players_Complete csv file
total_player_df = pd.read_csv('players_complete.csv')

# read purchase data json file
purchase_df = pd.read_json('purchase_data.json')
purchase2_df = pd.read_json('purchase_data2.json')
purchase3_df = pd.read_json('purchase_data_3.json~HEAD')

## Player Count
# Change Column Header from SN to Screen Name
total_player_df = total_player_df.rename(columns={'SN':'Screen Name'})
total_player_df.head()

## Player Count
# Count the total number of unique players
player_count = len(total_player_df['Screen Name'].unique())

total_players = pd.DataFrame({'Total Players':[player_count]})

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
gender_demographics = gender_demographics.round(2)

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
purchase_analysis_total = purchase_analysis_total.round(2)

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
purchase_analysis_gender = pd.DataFrame({"Male Purchase Count": [male_purchase_count],
                                   "Male Average Price": [male_avg_price],
                                   "Male Total Value": [male_revenue],
                                         "Female Purchase Count": [female_purchase_count],
                                   "Female Average Price": [female_avg_price],
                                   "Female Total Value": [female_revenue],
                                         "Other Purchase Count": [other_purchase_count],
                                   "Other Average Price": [other_avg_price],
                                   "Other Total Value": [other_revenue]
})