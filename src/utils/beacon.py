from datetime import datetime
from datetime import datetime
import pytz

def ping_status():
    # Prints 'RealmForge Systems Nominal' along with the current UTC timestamp.
    current_time = datetime.now(pytz.utc)
    print(f'RealmForge Systems Nominal - {current_time}')

# Example usage:
if __name__ == '__main__':
    ping_status()