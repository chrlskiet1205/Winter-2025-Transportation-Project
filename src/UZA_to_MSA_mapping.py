import pandas as pd
import os

# This dictionary includes top 20 MSA names, correlated UZA names, and its UACE codes
uza_to_msa = {
    "MSA_Name": [
        "New York–Newark–Jersey City, NY-NJ",
        "Los Angeles–Long Beach–Anaheim, CA",
        "Chicago–Naperville–Elgin, IL-IN",
        "Dallas–Fort Worth–Arlington, TX",
        "Houston–Pasadena–The Woodlands, TX",
        "Miami–Fort Lauderdale–West Palm Beach, FL",
        "Washington–Arlington–Alexandria, DC-VA-MD-WV",
        "Atlanta–Sandy Springs–Roswell, GA",
        "Philadelphia–Camden–Wilmington, PA-NJ-DE-MD",
        "Phoenix–Mesa–Chandler, AZ",
        "Boston–Cambridge–Newton, MA-NH",
        "Riverside–San Bernardino–Ontario, CA",
        "San Francisco–Oakland–Fremont, CA",
        "Detroit–Warren–Dearborn, MI",
        "Seattle–Tacoma–Bellevue, WA",
        "Minneapolis–St. Paul–Bloomington, MN-WI",
        "Tampa–St. Petersburg–Clearwater, FL",
        "San Diego–Chula Vista–Carlsbad, CA",
        "Denver–Aurora–Centennial, CO",
        "Orlando–Kissimmee–Sanford, FL"
    ],
    "UZA_Name": [
        "New York–Newark–Jersey City, NY-NJ",
        "Los Angeles–Long Beach–Anaheim, CA",
        "Chicago, IL-IN",
        "Dallas–Fort Worth–Arlington, TX",
        "Houston–Pasadena–The Woodlands, TX",
        "Miami–Fort Lauderdale, FL",
        "Washington–Arlington, DC-VA-MD-WV",
        "Atlanta, GA",
        "Philadelphia, PA-NJ-DE-MD",
        "Phoenix–Mesa–Scottsdale, AZ",
        "Boston, MA-NH",
        "Riverside–San Bernardino, CA",
        "San Francisco–Oakland, CA",
        "Detroit, MI",
        "Seattle–Tacoma, WA",
        "Minneapolis–St. Paul, MN",
        "Tampa–St. Petersburg, FL",
        "San Diego–Chula Vista–Carlsbad, CA",
        "Denver–Aurora, CO",
        "Orlando, FL"
    ],
    "UACE_Code": [
        "63217",
        "51445",
        "16264",
        "22042",
        "40429",
        "56602",
        "92242",
        "03817",
        "69076",
        "69184",
        "09271",
        "75340",
        "78904",
        "23824",
        "80389",
        "57628",
        "86599",
        "78661",
        "23527",
        "65863"
    ]
}

uza_to_msa_df = pd.DataFrame(data=uza_to_msa)

#Output the DataFrame
output_folder = 'data/raw/transportation/output'
output_path = os.path.join(output_folder, 'uza_to_msa.csv')

uza_to_msa_df.to_csv(output_path, index=False)