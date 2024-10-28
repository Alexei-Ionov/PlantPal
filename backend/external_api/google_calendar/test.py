from datetime import datetime, timedelta

# Get the current UTC time
current_utc_time = datetime.utcnow()

# Calculate UTC time one week from now
one_week_later = current_utc_time + timedelta(weeks=1)

print("Current UTC Time:", current_utc_time)
print("UTC Time One Week From Now:", one_week_later)
