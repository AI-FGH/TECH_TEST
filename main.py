# Modularized version of the figure generation part of the `main.py` file
import argparse
import pandas as pd
import seaborn as sns
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from googletrans import Translator

from llm import main as llm_main


def generate_heatmap(sales_data):
    """
    Generates a heatmap showing the correlation between various features in the sales data.
    """
    plt.figure(figsize=(30, 30))
    sns.heatmap(sales_data.corr(method='pearson'), annot=True, vmin=-1, vmax=1, cmap='YlGnBu')
    plt.subplots_adjust(left=0.3, bottom=0.2)
    plt.show()



def generate_top10_sales_barplot(day_sales_insights):
    """
    Generates a bar plot showing the top 10 sales amounts by date.
    """
    sns.set(style='darkgrid')
    top10sales = (day_sales_insights.groupby('Invoice_Date').sum(numeric_only=True).sort_values('Sales Amount', ascending=False).head(10))
    top10sales = top10sales.reset_index()
    sns.catplot(y = 'Sales Amount', x = 'Invoice_Date', data = top10sales, aspect = 2,palette='turbo',kind="bar")
    plt.title('Top 10 Days When Sales Were Highest')
    top10sales[['Sales Amount']]
    plt.show()
    return  top10sales


def generate_pie_plot(t):
    plt.figure(figsize=(20, 20))
    # Create a pie chart using actual values and labels
    plt.pie(t['Sales Amount'],  labels=t['Invoice_Date'],  # Use the 'Invoice_Date' values as labels
            autopct='%1.2f%%',
            shadow=True,
            startangle=90)
    plt.axis('equal')  # Ensure the pie chart is a circle
    plt.title('Contribution Of Sales Amount Among 10 Days')
    # Add a legend with rounded sales amounts
    plt.legend([round(val, 2) for val in t['Sales Amount']], loc='center left', fontsize='x-large',bbox_to_anchor=(1, 0.5))
    plt.subplots_adjust(right=0.7)
    plt.show()


def main(data_file):
    # Load the data
    sales_data = pd.read_csv(data_file, parse_dates=['DateKey', 'Invoice Date', 'Promised Delivery Date'])

    # Preprocess the data (this is extracted from the original script)
    sales_data01 = sales_data.dropna(subset=['Discount Amount', 'Sales Price', 'Item Number', 'Item Class'])
    sales_data02 = sales_data01.copy()
    sales_data01['Invoice_Year'] = sales_data['Invoice Date'].dt.year
    sales_data01['Invoice_Month'] = sales_data['Invoice Date'].dt.month
    sales_data01['Invoice_Quarter'] = sales_data['Invoice Date'].dt.quarter
    sales_data01['Invoice_Day'] = sales_data['Invoice Date'].dt.day
    # Convert columns to int64
    sales_data01['Invoice_Year'] = sales_data01['Invoice_Year'].astype('int64')
    sales_data01['Invoice_Month'] = sales_data01['Invoice_Month'].astype('int64')
    sales_data01['Invoice_Quarter'] = sales_data01['Invoice_Quarter'].astype('int64')
    sales_data01['Invoice_Day'] = sales_data01['Invoice_Day'].astype('int64')
    sales_data01 = sales_data01.drop(['DateKey', 'Item', 'Invoice Number', 'Item Class', 'Item Number', 'Line Number', 'Order Number','Promised Delivery Date', 'U/M'], axis=1)

    # Generate the heatmap
    generate_heatmap(sales_data01)

    # Prepare and generate the barplot
    day_sales_insights = sales_data02[['Invoice Date', 'Sales Amount']]
    print(sales_data[ 'Sales Amount'])
    day_sales_insights['Invoice_Date'] = pd.to_datetime(sales_data['Invoice Date']).dt.date
    r = generate_top10_sales_barplot(day_sales_insights)
    # Prepare and generate the pieplot
    generate_pie_plot(r)

    print("-----------------------------------------------------------------------------------------")
    # Sort the sales data by Discount Amount in descending order
    sorted_items = sales_data02.sort_values(by='Discount Amount', ascending=False)

    # Initialize an empty list to hold the unique items
    unique_discounted_items = []
    seen_item_names = set()

    # Iterate over the sorted items and collect unique items
    for _, row in sorted_items.iterrows():
        item_name = row['Item']
        if item_name not in seen_item_names:
            unique_discounted_items.append(row)
            seen_item_names.add(item_name)
        if len(unique_discounted_items) == 10:  # Stop when we have 10 unique items
            break

    # Convert the list of rows to a DataFrame
    top_10_unique_discounted_items = pd.DataFrame(unique_discounted_items)

    # Display the top 10 unique most discounted items
    print("Top 10 unique most discounted items:")
    print(top_10_unique_discounted_items[['Item Number', 'Item', 'Discount Amount', 'Sales Amount']])
    print("-----------------------------------------------------------------------------------------")

    number = int(input("چندمین محصول پر تخفیف را می خواهید؟لطفا بین 1 تا 10 انتخاب کنید و سپس enter  را بزنید"))
    print("-----------------------------------------------------------------------------------------")
    # Check if the number is within the valid range
    if 1 <= number <= 10:
        # Convert the number to a range of 0 to 9
        z = number - 1

        # Initialize the translator
        translator = Translator()
        # Define the text you want to translate
        first_space_index = top_10_unique_discounted_items['Item'].iloc[z].find(" ")
        # Get the part after the first space
        part_after_space = top_10_unique_discounted_items['Item'].iloc[z][
                           first_space_index + 1:] if first_space_index != -1 else ""
        text_to_translate = part_after_space
        # Perform the translation
        translated = translator.translate(text_to_translate, src='en', dest='fa')

        # Print the original and translated text
        print(f"Original: {text_to_translate}")
        print(f"Translated: {translated.text}")

    else:
        print("Please enter a valid number between 1 and 10.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate figures from sales data")
    parser.add_argument('data_file', type=str, help='Path to the sales data CSV file')
    args = parser.parse_args()

    # Call the main function
    main(args.data_file)
    llm_main( )