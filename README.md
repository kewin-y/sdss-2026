# Toronto Shelter System – Case Summary

Toronto's shelter system serves thousands nightly but faces constant pressure from demand fluctuations, capacity limits, and seasonal spikes. The task uses daily 2024–2025 operational data to analyze capacity utilization, system pressure, and risk across programs.

**Key questions:** where is the system most strained, and how does pressure differ across populations?

The goal is to deliver data-driven recommendations to improve planning and build a more resilient shelter system. Each team member wrote the code and generated the graphs for the section they presented in the video.

## Overview of Solutions

- Comparing the average and maximums of occupancy rates, showing that the men's sector is the least resilient, whereas the youth's sector is more resilient
- Looking at the trend in (monthly) average occupancy rate over time by overnight service type and program area, and types of programs with high occupancy rates
- Measuring fragility (the volatility of resources) with the standard deviation of the unavailability ratio, a metric for how much capacity is unavailable at a shelter
- Analyzing heatmaps, indexing by service capacity and occupancy rate
- Quantifying "strain" and "system resilience" using occupancy data, simulating how operational scenarios such as modest increases in demand can push the system to its breakpoint

## Dependencies

- ipykernel
- jupyterlab
- matplotlib
- numpy
- fastexcel
- fastparquet
- pandas
- seaborn
- scikit-learn
- plotly
- polars
- pyarrow
