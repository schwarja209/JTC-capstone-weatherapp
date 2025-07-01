'''
Single function utilities for the Weather Dashboard application.
'''

def display_fallback_status(fallback_used):
    '''Returns fallback status label for display based on boolean.'''
    return "(Simulated)" if fallback_used else ""

def describe_fallback_status(fallback_used):
    '''Returns descriptive fallback status for logging based on boolean.'''
    return "(Simulated)" if fallback_used else "Live"

def is_fallback(data):
    '''Returns True if the data was generated as a fallback.'''
    return data.get('source') == 'simulated'

def normalize_city_name(name):
    '''Strips whitespace and capitalizes each word of the city name.'''
    return name.strip().title()

def city_key(name):
    '''Generates a normalized key for city name to ensure consistent API calls and logging.'''
    return normalize_city_name(name).lower().replace(" ", "_")