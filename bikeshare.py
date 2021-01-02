import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'nyc': 'new_york_city.csv',
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
    city = input("Would you like to see data for Chicago, NYC, or Washington?\n").lower()
    while city not in ["chicago", "nyc", "washington"]:
        city = input("Invalid response! Please choose only one of the following: Chicago, NYC, or Washington\n").lower()

    # get user input for month (all, january, february, ... , june)
    month = input("What month would you like information about? Choose from january to june (please type 'all' to get all months)\n").lower()
    while month not in ["january", "february", "march", "april", "may", "june", "all"]:
        month = input("Invalid response! Please choose one of the following: january, february, march, april, may, june, or all\n").lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("What day would you like information about? Please type 'all' to get all days\n").lower()
    while day not in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "all"]:
        day = input("Invalid response! Please choose one of the following: monday, tuesday, wednesday, thursday, friday, saturday, sunday, or all\n").lower()

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
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month

    print("Most common month (mind the month filter chosen!): ", pd.to_datetime(df['month'], format='%m').dt.month_name().mode())

    # display the most common day of week
    print("Most common day of week (mind the day of the week filter chosen!): ", df['day_of_week'].mode())

    # display the most common start hour
    df['start_hour'] = df['Start Time'].dt.hour
    print("Most common start hour: ", df['start_hour'].mode())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("Most commonly used start station: ", df['Start Station'].value_counts().idxmax())

    # display most commonly used end station
    print("Most commonly used end station: ", df['End Station'].value_counts().idxmax())

    # display most frequent combination of start station and end station trip
    df['combined_stations'] = 'Start: ' + df['Start Station'] + ' , End: ' + df['End Station']
    print("Most commonly used combination of start and end station: ", df['combined_stations'].mode())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("Total travel time: ", pd.to_numeric(df['Trip Duration']).sum())

    # display mean travel time
    print("Mean travel time: ", pd.to_numeric(df['Trip Duration']).mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("User type counts:\n", df['User Type'].value_counts())

    # Display counts of gender
    try:
        print("Gender counts:\n", df['Gender'].value_counts())
    except:
        print('Gender data not available')


    # Display earliest, most recent, and most common year of birth
    try:
        print("Earliest year of birth: ", pd.to_numeric(df['Birth Year']).min())
        print("Most recent year of birth: ", pd.to_numeric(df['Birth Year']).max())
        print("Most common year of birth: ", df['Birth Year'].mode())
    except:
        print('Year of birth data not available')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        additional_data = input('\nIf you would like to see raw data please type "yes"\n').lower()
        initial_row = 0
        last_row = 5
        while additional_data == 'yes':
            print(df[initial_row:last_row][:])
            additional_data = input('\nIf you would like to see more raw data please type "yes"\n').lower()
            initial_row += 5
            last_row += 5

        restart = input('\nIf you would like to restart please type "yes"\n').lower()
        if restart != 'yes':
            break


if __name__ == "__main__":
	main()
