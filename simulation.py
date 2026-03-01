import pandas as pd
import exploratory
import seaborn as sns
import matplotlib.pyplot as plt

def amplify_demand(df):
    multipliers = []

    multipliers = list(range(100, 500, 5))

    results = []

    df_temp = df.copy()

    for multiplier in multipliers:
        df_temp['OCCUPIED_CAPACITY'] = df['OCCUPIED_CAPACITY'] * (multiplier / 100)
        df_temp['OCCUPIED_CAPACITY'] = df_temp['OCCUPIED_CAPACITY'].clip(upper=df_temp['ACTUAL_CAPACITY'])
        df_temp = exploratory.compute_strain(df_temp)
        resilience = exploratory.compute_resilience(df_temp)

        results.append({'multiplier': multiplier, 'resilience': resilience})

    return pd.DataFrame(results)

def plot_resilience_test(resilience_test_df):
    plt.figure(figsize=(12, 6))

    resilience_test_df['multiplier'] = resilience_test_df['multiplier'] - 100
    
    # Plot the line
    sns.lineplot(data=resilience_test_df, x='multiplier', y='resilience', 
                 marker='o', color='royalblue', linewidth=2)
    
    # Formatting
    plt.title('System Resilience Stress Test: Scaling Demand', fontsize=14)
    plt.xlabel('Demand Multiplier (% of Original Occupancy)', fontsize=12)
    plt.ylabel('Resilience Score (% of Sites < 90% Full)', fontsize=12)
    
    # Set Y-axis to percentage
    # plt.ylim(0, 0.125)
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    plt.tight_layout()
    plt.savefig("resilience_stress_test.png", dpi=300)
    plt.show()    