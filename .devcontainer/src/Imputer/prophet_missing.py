import pandas as pd
from prophet import Prophet
import numpy as np
import matplotlib.pyplot as plt

def fill_missing_values_recursively_with_confidence(df):

    df = df.sort_values('ds')

    missing_data = df[df['y'].isna()]
    if missing_data.empty:
        print("No missing values found in the 'y' column.")
        return df, pd.DataFrame()  # If no missing values, return the original data
    
    print(f"Found {len(missing_data)} missing values in 'y' column.")

    model = Prophet()

    model.fit(df.dropna())  # Drop NaNs for fitting
    future = model.make_future_dataframe(periods=0)  # periods=0 means no additional future data points
    forecast = model.predict(future)
    print("Forecast structure (first few rows):")
    print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].head())

    forecasts = []

    for missing_index in df[df['y'].isna()].index:
        print(f"Processing missing value for index {missing_index}")  
        missing_date = df.loc[missing_index, 'ds']  

        forecast_row = forecast[forecast['ds'] == missing_date]

        if forecast_row.empty:
            print(f"Warning: No forecast data found for {missing_date}. Skipping this date.")
            continue
        # Extract the forecasted value and confidence intervals for this missing date
        predicted_value = forecast_row['yhat'].values[0]
        lower_bound = forecast_row['yhat_lower'].values[0]
        upper_bound = forecast_row['yhat_upper'].values[0]
        # Store the forecast and confidence intervals
        forecasts.append({
            'ds': missing_date,
            'yhat': predicted_value,
            'yhat_lower': lower_bound,
            'yhat_upper': upper_bound
        })

        # Fill the missing value with the predicted value
        df.loc[missing_index, 'y'] = predicted_value

    # Convert the forecasted values with confidence intervals into a DataFrame
    forecast_df = pd.DataFrame(forecasts)

    # Check if forecast_df has been populated
    print(f"Forecast with confidence intervals (first few rows):")
    print(forecast_df.head())

    return df, forecast_df

# # Example usage
# if __name__ == "__main__":
#     # Create a sample time series with missing values (NaNs)
#     data_=pd.read_csv('/home/qb/ML_Group_Assignment/sub_stations/df.csv')
#     data = data_[['date', 'so2']].rename(columns = {'date':'ds', 'so2':'y'})
#     data.ds= pd.to_datetime(data.ds)
#     # Introduce missing values (NaNs) at random places
#     np.random.seed(42)  # Set seed for reproducibility
#     missing_indices = np.random.choice(data.index, size=100, replace=False)
#     data.loc[missing_indices, 'y'] = np.nan

#     print("Data with missing values:")
#     print(data.head(10))  # Check first few rows to verify NaNs

#     # Fill missing values recursively using Prophet and get the forecast with confidence intervals
#     filled_data, forecast_with_confidence = fill_missing_values_recursively_with_confidence(data)

#     # Print the filled data and confidence intervals
#     print("\nData after filling missing values recursively:")
#     print(filled_data.head(10))  # Check the filled data

#     print("\nForecast with Confidence Intervals:")
#     print(forecast_with_confidence.head(10))  # Check forecast with confidence intervals

#     # Plot the filled data along with the forecast and confidence intervals
#     plt.figure(figsize=(10, 6))

#     # Plot the observed data
#     plt.plot(filled_data['ds'], filled_data['y'], label='Observed Data', color='blue')

    # Plot the predicted values with confidence intervals
        # if not forecast_with_confidence.empty:
        #     plt.plot(forecast_with_confidence['ds'], forecast_with_confidence['yhat'], label='Predicted (Filled)', color='green')
        #     plt.fill_between(forecast_with_confidence['ds'], forecast_with_confidence['yhat_lower'], forecast_with_confidence['yhat_upper'], color='gray', alpha=0.2, label='Confidence Interval')
    
        # # Add labels and title
        # plt.title('Time Series with Missing Values Filled and Confidence Intervals')
        # plt.xlabel('Date')
        # plt.ylabel('Value')
        # plt.legend()
        # plt.grid(True)
    
        # # Show the plot
        # plt.show()
