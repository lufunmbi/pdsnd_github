import time
import pandas as pd
import numpy as np

"""
The data files are defined below but they may be absent from the git repo 
due to their largeness.
"""

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ""
    while city not in CITY_DATA.keys():
        city = input("Would you like to see data for chicago, new york city or washington? kindly note that the city name should be entered in lower case:").lower()
        if city not in CITY_DATA.keys():
            print("Incorrect input format. Kindly ensure you type in lower case")
    print("You have chosen to see data from {0}".format(city.title()))

    # get user input for month (all, january, february, ... , june)
    #I created a dictionary for the acceptable months
    MONTH_DATA = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6, 'all': 7}
    month = ""
    while month not in MONTH_DATA.keys():
        month = input("Which month will you like to filter the data by january, february, march, april, may or june? Type 'all' to select all the data:").lower()
        if month not in MONTH_DATA.keys():
            print("You have entered an invalid value. Kindly ensure that the month is in lower case")
    print("The month chosen is {0}".format(month.title()))

    # get user input for day of week (all, monday, tuesday, ... sunday)
    DAY_DATA = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all']
    day = ""
    while day not in DAY_DATA:
        day = input("Which day you like to filter the data by sunday, monday, tuesday...? Type 'all' to select all the data: ").lower()
        if day not in DAY_DATA:
            print("You have entered an invalid value. Kindly ensure that the day is in lower case")
    print("The month chosen is {0}".format(month.title()))

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    #df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]
        #df = df.loc[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
        #df = df.loc[df['day_of_week'] == month]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    #popular_month = df.loc[:, "month"].mode()
    print("1 = January, 2 = february....3 = June. Therefore, The commonly travelled month is: ", popular_month)

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    #popular_day = df.loc[:, "day_of_week"].mode()
    print("The commonly travelled day of the week is: ", popular_day)

    # display the most common start hour
    #first we extract the hour from the day of the week
    df['hourdf'] = df['Start Time'].dt.hour
    popular_hour = df['hourdf'].mode()[0]
    print("The commonly travelled start hour is: ", popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_startstation = df['Start Station'].mode()[0]
    print("The commonly used start station is", popular_startstation)

    # display most commonly used end station
    popular_endstation = df['End Station'].mode()[0]
    print("The commonly used end station is", popular_endstation)

    # display most frequent combination of start station and end station trip
    df['newdf'] = df['Start Station'].str.cat(df['End Station'], sep=' - ')
    popular_combination = df['newdf'].mode()[0]
    print("The commonly used end station is", popular_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    sum_traveltime = df['Trip Duration'].sum()
    print("The total travel time is: ", sum_traveltime)

    # display mean travel time
    mean_traveltime = df['Trip Duration'].mean()
    print("The average/mean travel time is: ", mean_traveltime)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("The number of people by user types is: ", user_types)

    # Display counts of gender
    #Because not all rows have the gender column, we need to use the try catch block to handle future exceptions
    try:
        gender = df['Gender'].value_counts()
        print("The number of people by gender is: ", gender)
    except:
        print("There is no gender value for this input")

    # Display earliest, most recent, and most common year of birth
    #Again, not all the values in the dataframe have birth year, so we employ the try-catch for exception handling here too
    try:
        earliest_birthyear = df['Birth Year'].min()
        print("The earliest birth year is: ", earliest_birthyear)

        most_recent = df['Birth Year'].max()
        print("The most recent birth year is: ", most_recent)

        most_common = int(df['Birth Year'].mode())
        print("The most common birth year is: ", most_common)
    except:
        print("No birth year value exists for this input")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#Function to display raw data
def returnRawData(df):
    """

    :param df: The dataframe that the user passes into the function
    :return: raw data similar to using a .head() in pandas
    """
    User_response = ["yes", "no"]
    retrieved_data = ""
    #Because we want to retrieve 5 values, we have to use a counter to monitor the count
    counter = 0
    while retrieved_data not in User_response:
        retrieved_data = input("Do you want to retreive raw data? Kindly answer yes or no: ").lower()
        if retrieved_data == "yes":
            print(df.head())
        elif retrieved_data not in User_response:
            print("Invalid response provided. Kindly respond correctly.")
    #What if user wishes to view more data as in the case of head(10) to view up to 10 rows?
    while retrieved_data == "yes":
        retrieved_data = input("Do you wish to view more data? Kindly answer yes or no: ").lower()
        counter += 5
        if retrieved_data == "yes":
            print(df[counter:counter+5])
        elif retrieved_data != "yes":
            break
    print('-'*40)
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        returnRawData(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
