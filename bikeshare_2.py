import time
import pandas as pd
import numpy as np
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

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
    print('\nHello! Let\'s explore some US bikeshare data!\n')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city = input('Would you like to see data for Chicago, New York City, or Washington? ').lower()
            test = CITY_DATA[city]
            break
        except KeyError:
            print('\nOops! That is an invalid entry. Please try again.\n')

    # prompt user to choose to filter by month, day, or nothing
    filter_val_dict = {'month': 1, 'day': 2, 'none': 3}
    while True:
        try:
            filter_val = input('\nWould you like to filter the data by month, day, or not at all? Type "none" for no time filter. ').lower()
            test = filter_val_dict[filter_val]
            break
        except KeyError:
            print('\nOops! That is an invalid entry. Please try again.')    

    if filter_val == 'month':
        month_dict = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6}
        # get user input for month (all, january, february, ... , june)
        while True:
            try:
                month = input('\nWhich month would you like to view? January, February, March, April, May, or June? Please type out the full month name. ').lower()
                test = month_dict[month]
                break
            except KeyError:
                print('\nOops! That is an invalid entry. Please try again.')         
        day = 'all'
        print('\nYou have chosen to filter by the month of {}\n.'.format(month.capitalize()))
    elif filter_val == 'day':
        day_dict = {'monday': 1, 'tuesday': 2, 'wednesday': 3, 'thursday': 4, 'friday': 5, 'saturday': 6, 'sunday': 7}
        # get user input for day of week (all, monday, tuesday, ... sunday)
        while True:
            try:
                day = input('\nWhich day of the week would you like to view? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday? Please type out the full day name. ').lower()
                test = day_dict[day]
                break
            except KeyError:
                print('\nOops! That is an invalid entry. Please try again.')         
        month = 'all'
        print('\nYou have chosen to filter by the day: {}\n.'.format(day.capitalize()))      
    elif filter_val == 'none':
        print('\nYou have chosen to not filter the data.\n')
        month = 'all'
        day = 'all'

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
    df['day_of_week'] = df['Start Time'].dt.dayofweek

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # use the index of the days list to get the corresponding int
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        day = days.index(day)
        
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    months = ['january', 'february', 'march', 'april', 'may', 'june']      
    popular_month = df['month'].mode()[0] - 1
    popular_month = months[popular_month].capitalize()
    
    print('Most popular month:', popular_month)

    # display the most common day of week
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    popular_day = df['day_of_week'].mode()[0]
    popular_day = days[popular_day].capitalize()
    
    print('Most popular day of the week:', popular_day)

    # display the most common start hour
    popular_start_hour = df['Start Time'].dt.hour.mode()[0]
    print('Most popular start hour:', popular_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most popular start station:', popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most popular end station:', popular_end_station)

    # display most frequent combination of start station and end station trip
    popular_start_end_station = df[['Start Station', 'End Station']].apply(tuple, 1).mode()[0]
    print('Most popular combination of start and end station: {} // {}'.format(popular_start_end_station[0], popular_start_end_station[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    travel_time_total = df['Trip Duration'].sum()
    print('Total travel time (seconds):', travel_time_total)

    # display mean travel time
    travel_time_mean = df['Trip Duration'].mean()
    print('Mean travel time (seconds):', travel_time_mean)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""
    
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('User Type Statistics')
    user_types = df['User Type'].value_counts()
    for i in range(len(user_types)):
        print('{}: {}'.format(user_types.index[i], user_types.iloc[i]))

    if city == 'chicago' or city == 'new york city':
        # Display counts of gender
        print('\nGender Statistics')
        gender = df['Gender'].value_counts()
        for i in range(len(gender)):
            print('{}: {}'.format(gender.index[i], gender.iloc[i]))
    
        # Display earliest, most recent, and most common year of birth
        print('\nBirth Year Statistics')
        earliest_dob = df['Birth Year'].min()
        recent_dob = df['Birth Year'].max()
        mode_dob = df['Birth Year'].mode()[0]
        print('Earliest birth year:', int(earliest_dob))
        print('Most recent birth year:', int(recent_dob))
        print('Most common birth year:', int(mode_dob))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def print_raw(df):
    """Displays raw data from selected bike share dataset"""
    
    user_input = input('\nWould you like to view the raw data? Enter yes or no. ').lower()
    print('\n')
    if user_input == 'yes':
        print(df.head())
    
    count = 5
    while True:
        user_input = input('\nWould you like to view more raw data? Enter yes or no. ').lower()
        if count < len(df):                
            if user_input == 'yes':
                print('\n')
                print(df.iloc[count:count+5])
                count += 5
            else:
                break   
        else:
            if user_input == 'yes':
                print('\n')
                print(df.iloc[count:])
                break
            else:
                break 
    

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        print_raw(df)

        restart = input('\nWould you like to restart? Enter yes or no. ')
        if restart.lower() != 'yes':
            print('\n')
            break


if __name__ == "__main__":
	main()
