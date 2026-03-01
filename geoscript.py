import pandas as pd

def extract_geoinfo(df):
    """
    This function extracts the latitude of longitude of each location given the postal code information, 
    and modfiy the dataset accordingly   
    """

    pccf = pd.read_csv("PCCF_FCCP_V2503_2021.tab", sep="\t")
    pccf_subset = pccf[['PC', 'LAT', 'LONG']]

    df = df.merge(
        pccf_subset,
        left_on="LOCATION_POSTAL_CODE",
        right_on="PC",
        how="left"
    )

    df.rename(columns={
        "latitude": "latitude",
        "longitude": "longitude"
        }, inplace=True)
    
    df.drop(columns=["PC"], inplace=True)
    
    return df