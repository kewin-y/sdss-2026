# import duckdb
# import polars as pl
# import geoscript
import pandas as pd
# import openpyxl
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
from shapely.geometry import Point
import matplotlib.patches as mpatches
import numpy as np

import seaborn as sns
import matplotlib.pyplot as plt

def plot_strain_distribution(df):
    plt.figure(figsize=(10, 10))
    
    # Create the plot
    sns.histplot(df['strain_score'], bins=100, kde=True, color='teal')
    
    # Add labels and styling
    plt.title('Distribution of Service Strain Scores', fontsize=15)
    plt.xlabel('Strain Score (Capped at 1.0)', fontsize=12)
    plt.ylabel('Frequency (Count of Facilities)', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    plt.savefig("strain_distribution.png", dpi=300)

# Sectoral strain
# TODO Fix
def plot_strain_by_sector(df):
    plt.figure(figsize=(10, 10))
    
    # Create a box plot to see distribution across different sectors
    sns.boxplot(data=df, x='SECTOR', y='strain_score', palette='viridis')
    
    plt.xticks(rotation=45)
    plt.title(f'Strain Score Distribution by sector', fontsize=15)
    plt.ylim(0, 1.1) # Keep the focus on the 0-1 range
    
    plt.tight_layout()
    plt.savefig("strain_by_sector.png", dpi=300)

def sectoral_strain(df):
    # Grouping by sector, aggregate and calculate strain score
    
    sectoral_strain = (
        df.groupby('SECTOR')['strain_score']
        .mean()
        .reset_index() # This turns the index back into a column
        .sort_values(by='strain_score', ascending=False)
    )

    print(sectoral_strain.head())

    plot_strain_by_sector(sectoral_strain)
    
    return sectoral_strain

# Geo strain
def geo_strain(df):
    # Grouping by postal code, aggregate and calculate strain score
    # Create new column for more general neighbourhood
    df['POSTAL_CODE_FSA'] = df['LOCATION_POSTAL_CODE'].str[:3]

    regional_strain = (
        df.groupby('POSTAL_CODE_FSA')['strain_score']
        .mean()
        .reset_index() # This turns the index back into a column
        .sort_values(by='strain_score', ascending=False)
    )

    print(regional_strain.head())

    return regional_strain

def plot_strain_heatmap(df):
    """
    Creates a geographical heatmap where color intensity represents strain score.
    """
    # Recalculate or ensure strain_score exists (capped at 1.0)
    denominator = df['ACTUAL_CAPACITY'].replace(0, np.nan)
    df['strain_score'] = ((df['OCCUPIED_CAPACITY'] + df['UNAVAILABLE_CAPACITY']) / denominator).clip(upper=1.0).fillna(0)

    plt.figure(figsize=(10, 10))
    
    # Use a scatter plot where 'c' (color) is mapped to 'strain_score'
    # 'YlOrRd' is great for heatmaps (Yellow = low strain, Red = high strain)
    scatter = plt.scatter(
        df['LONG'], 
        df['LAT'], 
        c=df['strain_score'], 
        cmap='YlOrRd', 
        alpha=0.7, 
        s=40, 
        edgecolors='grey', 
        linewidth=0.2
    )

    # Add a colorbar to explain the scale
    cbar = plt.colorbar(scatter)
    cbar.set_label('Strain Score (0.0 = Empty, 1.0 = Full)', rotation=270, labelpad=15)

    plt.title('Geographical Heatmap of Service Strain', fontsize=16)
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.grid(True, linestyle='--', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig("strain_heatmap.png", dpi=300)
    
# Geo-based info plotting
# TODO Fix the colours
def plot_geoinfo(ax, df, category):
    df['_cat_code'] = df[category].astype('category').cat.codes
    codes = df['_cat_code']
    categories = df[category].astype('category').cat.categories

     # Use the modern Colormap API (discrete colors)
    cmap = matplotlib.colormaps['tab20']  # Colormap object
    n_colors = len(categories)
    
    # Map integer codes to the discrete colormap indices
    # colors = [cmap(i % cmap.N) for i in range(n_colors)]


    scatter = ax.scatter(df['LONG'], df['LAT'], 
                         c=codes, cmap=cmap, alpha=0.6, s=10, rasterized=True)
    ax.set_title('Geographical Distribution of ' + category)
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')

    # Build legend
    import matplotlib.patches as mpatches
    patches = [mpatches.Patch(color=cmap(i), label=cat) for i, cat in enumerate(categories)]
    ax.legend(handles=patches, bbox_to_anchor=(1.05, 1), loc='upper left', title=category)

def execute_plot(df):
    categories = ["SECTOR", "OVERNIGHT_SERVICE_TYPE", "PROGRAM_MODEL", "PROGRAM_AREA", "CAPACITY_TYPE"]
    
    fig, axs = plt.subplots(len(categories), 1, figsize=(12, 8*len(categories)))

    for i, category in enumerate(categories):
        plot_geoinfo(axs[i], df, category)

    plt.tight_layout()
    plt.savefig("map.png", dpi=300)

# Data summary
def data_summary(df):

    print("Summary of data set\n")

    print("Column names:")
    print(df.columns)
    print("\n")

    df.info()
    print("\n")

    print(df.describe())
    print("\n")

    print(df.head())

def compute_strain(df):
    raw_ratio = (df['OCCUPIED_CAPACITY'] + df['UNAVAILABLE_CAPACITY']) / df['ACTUAL_CAPACITY'].replace(0, np.nan)
    # raw_ratio = (df['OCCUPIED_CAPACITY']*(df['UNAVAILABLE_CAPACITY']+1))/df['ACTUAL_CAPACITY']
    df['strain_score'] = raw_ratio.clip(upper=1.0).fillna(0).replace([np.inf, -np.inf], 0)
    # df['strain_score'] = raw_ratio.clip(upper=50).fillna(0).replace([np.inf, -np.inf], 0)

    df['is_resilient'] = (df['strain_score'] < 0.9).astype(int)

    return df


def compute_resilience(df):
    return sum(df['is_resilient'])/len(df)