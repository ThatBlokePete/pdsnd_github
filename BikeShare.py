import time
import calendar
import pandas as pd
import datetime as d

CITY_DATA = {'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv'}

# Internal flag for printing addittional information
debug_flag = True

def get_user_input(choice_list,data_name):
    """
    Used to get data from the user to analyze.

    Returns:
        (str) - selection from user based on choice_list
    """
    # ref https://stackoverflow.com/questions/58449700/how-to-create-a-sub-program-that-takes-user-input

    input_num = 0

    while True:
        # print out the options
        for i in range(len(choice_list)):
            print(str(i+1)+":", choice_list[i])
        # try to get the user to select an option
        try:
            input_num = int(input("Enter the number that represents the {0}:".format(data_name)))
            if input_num in range(1, len(choice_list)+1):
                return_value = choice_list[input_num-1]
                print('Great, you have choosen the ' + data_name + ": " + return_value + '\n')
                return return_value
            else:
                print("invalid choice, please try again")
        except ValueError:
            print('Thats not a valid number please try again')
            continue


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!\n')

    # ref https://stackabuse.com/getting-user-input-in-python/

    # Get user input for city (chicago, new york city, washington).
    cities = ['Chicago', 'New York city', 'Washington']
    city = get_user_input(cities,"city")

    # Get user input for month (all, january, february, ... , june)
    months = ['All', 'Jan', 'Feb', 'Mar', 'Apr', 'Jun']
    month = get_user_input(months,"month")

    # Get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['All', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day = get_user_input(days,"day")

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
    # Make sure the city name is correct
    city_name = city.lower()

    if debug_flag:
            print(city_name)

    try:
        print('getting data from: ', CITY_DATA[city_name])
        df = pd.read_csv(CITY_DATA[city_name])
    except OSError as e:
        print("Error: cannot find the data files")
        print("       Please make sure they are available in the root folder")
        print("       and restart the program\n")
    finally:
        exit()


    try:
        # Build data frame columns:
        # Convert start time column to date time so we can work with it
        df['Start Time'] = pd.to_datetime(df['Start Time'])

        # Build month (num) column from "start time"
        df['Month'] = df['Start Time'].dt.month

        # Use start date to calculate start day (i.e. tuesday) column
        df['Start Day'] = df['Start Time'].dt.day_name()

        # build hour column from start day column
        df['Hour'] = df['Start Time'].dt.hour

    except:
        print ("Unexpected error")

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    # ref: https://stackoverflow.com/questions/48590268/pandas-get-the-most-frequent-values-of-a-column
    print('\nCalculating The Most Frequent Times of Travel...\n')

    start_time = time.time()

    # Display the most popular month
    most_popular_month =  df['Month'].mode()[0]
    print ('The most popular rental month: {0}'.format(calendar.month_name[most_popular_month]))

    # print most popular day
    most_popular_day = df['Start Day'].mode()[0]
    print ('The most popular start day of the week: {0}'.format(most_popular_day))

    # most popular hour
    most_popular_hour = df['Hour'].mode()[0]
    print ('The most popular rental hour is: {0}'.format(most_popular_hour))

    # ref: https://stackoverflow.com/questions/29645153/remove-name-dtype-from-pandas-output
    top_2_days = df['Start Day'].value_counts()[0:2]
    print ('The top 2 most popular rental days are:\n{0}'.format(top_2_days.to_string()))

    top_3_hours = df['Hour'].value_counts()[0:3]
    print ('The top 3 most popular rental hours are:\n{0}'.format(top_3_hours.to_string()))

    print('-'*40)

    ###### try plottling some info ####################
    # plot via pandas
    #pd.value_counts(df['Month']).plot.bar()
    #pd.value_counts(df['Start Day']).plot.bar()
    #pd.value_counts(df['Hour']).plot.bar()

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df['Start Station'].value_counts().idxmax()
    print('Most Commonly used start station:\n', start_station)

    # display most commonly used end station
    end_station = df['End Station'].value_counts().idxmax()
    print('\nMost Commonly used end station:\n', end_station)

    # display most frequent combination of start station and end station trip
    combined_trip = df['Start Station'] + " --> " + df['End Station']
    most_common_trip = combined_trip.value_counts().idxmax()
    print('\nMost Commonly used combination of start station and end station is:\n', most_common_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def ConvertSectoDay(n):
    """Converts seconds into days / hours / mins / secs."""
    # ref: https://www.geeksforgeeks.org/converting-seconds-into-days-hours-minutes-and-seconds/
    day = n // (24 * 3600)

    n = n % (24 * 3600)
    hour = n // 3600

    n %= 3600
    minutes = n // 60

    n %= 60
    seconds = n

    day = int(day)
    hour = int(hour)
    minutes = int(minutes)
    seconds = int(seconds)

    print(day, "days", hour, "hours",
          minutes, "minutes",
          seconds, "seconds\n")


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_trip_duration = sum(df['Trip Duration'])
    print("Total of trip duration is:")
    ConvertSectoDay(total_trip_duration)

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('The mean travel is:')
    ConvertSectoDay(mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    # ref: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_string.html
    print('User types:')
    print(user_types.to_string()+'\n')

    # Display counts of gender
    # Some csv files dont contain this data
    if 'Gender' in df.columns:
        genders = df['Gender'].value_counts()
        print('User Genders:\n', genders.to_string()+"\n")
    else:
        print('Sorry, Gender info is not available in the selected dataframe')

    # Display earliest, most recent, and most common year of birth
    # Some csv files dont contain this data
    if 'Birth Year' in df.columns:
        oldest_user = int(df['Birth Year'].min())
        youngest_user = int(df['Birth Year'].max())
        most_common_user = int(df['Birth Year'].mode()[0])
        print("The oldest user was born in {0} and is approx {1} years old".format(oldest_user,calculateAgeInYears(oldest_user)))
        print("The youngest user was born in {0} and is approx {1} years old".format(youngest_user,calculateAgeInYears(youngest_user)))
        print("The most common birth year of our users is {0} with an approx age of {1} years ".format(most_common_user,calculateAgeInYears(most_common_user)))

    else:
        print('Sorry, Birth date info is not available in the selected dataframe')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def calculateAgeInYears(year_born):
    """Calculates age in years from birth year"""
    # ref https://stackoverflow.com/questions/4436957/pythonic-difference-between-two-dates-in-years
    current_year = int(d.datetime.now().year)
    difference_in_years = abs(current_year - year_born)
    return int(difference_in_years)


def raw_data(df):
    """
    Checks with the user to display 5 rows of
    raw data with a (Y/N) question to continue
    """

    print('would you like to see the current datasets raw data?')
    user_input = input('y or n\n')
    line_num = 0

    while True:
        if user_input.lower() == "y":
            print(df.iloc[line_num : line_num + 5])
            line_num += 5
            print('\nwould you like to continue?')
            user_input = input('y or n\n')
        else:
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        print('\nwould you like to start from the beginning?')
        restart = input('y or n\n')
        if restart.lower() == 'n':
            break


if __name__ == "__main__":
	main()
