# Standard Python library imports
from datetime import datetime, timedelta
import re

# Third party libraries imports
from dateutil.relativedelta import relativedelta


def format_current_date():
    """
    Formats the current date as 'MM-YYYY'.

    Returns
    -------
    str
        The current date in 'MM-YYYY' format.
    """
    current_date = datetime.now()
    return current_date.strftime("%m-%Y")

def convert_date_to_mm_aaaa(date_str):
    """
    Converts a date string to 'MM-YYYY' format.

    Parameters
    ----------
    date_str : str
        The date string to be converted.

    Returns
    -------
    str or None
        The date in 'MM-YYYY' format, or None if the conversion fails.
    """
    # Check for recent time patterns
    recent_patterns = {
        "now": datetime.now(),
        "sec": timedelta(seconds=1),
        "seconds": timedelta(seconds=1),
        "min": timedelta(minutes=1),
        "minutes": timedelta(minutes=1),
        "hour": timedelta(hours=1),
        "hours": timedelta(hours=1),
        "day": timedelta(days=1)
    }
    
    for pattern, delta in recent_patterns.items():
        if re.match(fr"\b\d+\s*{pattern}\b", date_str):
            return (datetime.now() - delta).strftime("%m-%Y")

    # Map of month abbreviations to full month names
    month_map = {
        "Jan.": "January", "Jan": "January",
        "Feb.": "February", "Feb": "February",
        "March": "March", "Mar": "March",
        "April": "April", "Apr": "April",
        "May": "May",
        "June": "June", "Jun": "June",
        "July": "July", "Jul": "July", 
        "Aug.": "August", "Aug": "August",
        "Sept.": "September", "Sep": "September",
        "Oct.": "October", "Oct": "October",
        "Nov.": "November", "Nov": "November",
        "Dec.": "December", "Dec": "December"
    }
    
    # Replace month abbreviation with full name
    for abbr, full in month_map.items():
        if abbr in date_str:
            date_str = date_str.replace(abbr, full)
            break

    # Possible date formats
    possible_formats = ["%B. %d, %Y", "%B %d, %Y"]
    
    # Try parsing with each format
    for fmt in possible_formats:
        try:
            date_obj = datetime.strptime(date_str, fmt)
            return date_obj.strftime("%m-%Y")
        except ValueError:
            pass
    
    return None

def word_counter(text_to_match, search_phrase):
    """
    Counts the occurrences of a search phrase in a given text.

    Parameters
    ----------
    text_to_match : str
        The text to search within.
    search_phrase : str
        The search phrase to count.

    Returns
    -------
    int
        The number of occurrences of the search phrase in the text.
    """
    text_to_match = text_to_match.lower()
    search_phrase = search_phrase.lower()

    # Create a regular expression that searches for the word within other words
    pattern = re.compile(r'\b\w*' + re.escape(search_phrase) + r'\w*\b')

    # Find all occurrences that match the pattern
    matches = pattern.findall(text_to_match)

    # Return the number of matches found
    return len(matches)

def does_it_contain_money(text_to_match):
    """
    Checks if the text contains any monetary values.

    Parameters
    ----------
    text_to_match : str
        The text to check.

    Returns
    -------
    bool
        True if the text contains monetary values, False otherwise.
    """
    patron_dinero = r'\$[0-9]+(\.[0-9]+)?(\,[0-9]+)?(\s(dollars|usd))?'
    return bool(re.search(patron_dinero, text_to_match, re.IGNORECASE))

def calculate_months_to_consider(num_months):
    """
    Calculates a list of months to consider based on the current date and a given number of months.

    Parameters
    ----------
    num_months : int
        The number of months to consider.

    Returns
    -------
    list of str
        List of months in 'MM-YYYY' format.

    Raises
    ------
    ValueError
        If num_months is not a positive integer.
    """
    # We do not accept strings or negative numbers
    if not isinstance(num_months, int) or num_months <= 0:
        raise ValueError("num_months must be a positive integer.")

    # We find current date and obtain the current month and year
    current_date = datetime.now()
    months_years = [current_date.strftime("%m-%Y")]

    # Then, we find the possible month and years to consider for the search
    for i in range(1, num_months):
        date_to_add = current_date - relativedelta(months=i)
        months_years.append(date_to_add.strftime("%m-%Y"))
    return months_years
