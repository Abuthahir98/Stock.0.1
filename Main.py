# Function to plot real and predicted data
def plot_data(real_data, simulated_data):
    plt.figure(figsize=(12, 8))
    
    # Plot real data
    plt.plot(real_data.index, real_data['Close'], label='Real Data', color='blue', marker='o')
    
    # Scatter plot for predicted values
    plt.scatter(simulated_data.index, simulated_data['Close'], c=simulated_data['predicted'], cmap='coolwarm', marker='s', s=100, label='Predicted Data')
    
    # Display predicted values as text
    for i in range(len(simulated_data)):
        plt.text(simulated_data.index[i], simulated_data['Close'].iloc[i], f'{simulated_data["Close"].iloc[i]:.2f}', ha='center', va='bottom', fontsize=8)
    
    plt.title('Real vs Predicted Data')
    plt.xlabel('Date')
    plt.ylabel('Closing Price')
    plt.legend()
    plt.show()

# Main function
def main():
    ticker = 'BTC-INR'  # Change to the desired cryptocurrency pair
    
    # Fetch real-time data every 1 minute for the last 1 day
    data = get_realtime_data(ticker)
    
    # Preprocess data
    data = preprocess_data(data)
    
    model = train_model(data)
    
    while True:
        # Fetch real-time data every 1 minute
        new_data = get_realtime_data(ticker)
        
        # Update the existing data with new data
        data = pd.concat([data, new_data])
        
        # Preprocess data
        data = preprocess_data(data)
        
        # Get the last 10 minutes of real data
        last_10_minutes_data = data.iloc[-10:]
        
        # Simulate trading for the next 5 minutes
        simulated_data = last_10_minutes_data.copy()
        for i in range(5):
            new_realtime_data = get_realtime_data(ticker).tail(1)
            simulated_data = pd.concat([simulated_data, new_realtime_data])
        
        simulated_data = preprocess_data(simulated_data)
        
        # Simulate trading
        final_balance = simulate_trading(model, simulated_data)
        
        # Print current balance
        print(f'Current Balance: {final_balance:.2f} Rupees')
        
        # Plot real and predicted data
        plot_data(last_10_minutes_data, simulated_data)
        
        # Wait for 1 minute before fetching new data
        time.sleep(60)

if __name__ == "__main__":
    main()
