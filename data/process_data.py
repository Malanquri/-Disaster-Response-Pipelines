import sys
# import libraries
import pandas as pd
import numpy as np
import sqlalchemy
from sqlalchemy import create_engine

def load_data(messages_filepath, categories_filepath):
    """Load data from two csv files into pandas dataframes and
    merge them into one.
    Parameters:
    messages_filepath : string
        path of the messages csv file
    categories_filepath : string
        path of the categories csv file
    
    Output:
    df : pandas.DataFrame
        The merged dataframe
    """    
    messages = pd.read_csv(messages_filepath)
    categories = pd.read_csv(categories_filepath)
    df = messages.merge(categories, on='id')
    return df

def clean_data(df):
    """Clean the data
    Parameters:
    df : pandas.DataFrame
        dataframe to be processed
    
    Output:
    df : pandas.DataFrame
        The processed dataframe
    """   
    categories = df['categories'].str.split(";", expand=True)
    row = categories.loc[0,:]
    category_colnames = row.apply(lambda x:x.split('-')[0])
    categories.columns = category_colnames

    for column in categories:
        # set each value to be the last character of the string
        categories[column] = categories[column].apply(lambda x:x.split('-')[1])

        # convert column from string to numeric
        categories[column] = categories[column].astype(int)
    df.drop('categories', axis=1, inplace=True)
    df = pd.concat([df,categories], axis=1)
    df.drop_duplicates(inplace=True)
    return df
    


def save_data(df, database_filename):
    """Save the data
    Parameters:
    df : pandas.DataFrame
        dataframe to be written
    
    database_filename: string
        The filename of the database 
   
   Output:
   None
    """       
    engine = create_engine('sqlite:///' + database_filename)
    df.to_sql('df', engine, index=False)    
    pass  


def main():
    if len(sys.argv) == 4:

        messages_filepath, categories_filepath, database_filepath = sys.argv[1:]

        print('Loading data...\n    MESSAGES: {}\n    CATEGORIES: {}'
              .format(messages_filepath, categories_filepath))
        df = load_data(messages_filepath, categories_filepath)

        print('Cleaning data...')
        df = clean_data(df)
        
        print('Saving data...\n    DATABASE: {}'.format(database_filepath))
        save_data(df, database_filepath)
        
        print('Cleaned data saved to database!')
    
    else:
        print('Please provide the filepaths of the messages and categories '\
              'datasets as the first and second argument respectively, as '\
              'well as the filepath of the database to save the cleaned data '\
              'to as the third argument. \n\nExample: python process_data.py '\
              'disaster_messages.csv disaster_categories.csv '\
              'DisasterResponse.db')


if __name__ == '__main__':
    main()