import pandas as pd

def count_zero_values(df):
    zero_count = (df == 0).sum()  # Count zeros in each column
    total_count = df.count()  # Count total non-NaN values in each column
    zero_percentage = ((zero_count / total_count) * 100)  # Calculate percentage of zero values
     # Format percentage to 2 decimal places
    zero_percentage = zero_percentage.apply(lambda x: f"{x:.2f}%")


    # Create a result DataFrame with counts and percentages
    result = pd.DataFrame({
        'Zero Count': zero_count,
        'Zero Percentage': zero_percentage,
    })

    return result
