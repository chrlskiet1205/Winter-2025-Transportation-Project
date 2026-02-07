<div align ="center">

# A Comparative Analysis of Public Transit Need and Supply in the 20 Largest U.S. Metropolitan Statistical Areas (MSAs)

[![License](https://img.shields.io/badge/license-MIT-red)]()

</div>

<hr>

## I. Motivation & Background
Public transportation plays a critical role in urban mobility in the United States, supporting billions of passenger trips each year and providing essential access to employment, education, and services—particularly for households without reliable access to private vehicles. Ensuring that transit service is aligned with underlying need remains an important challenge for large metropolitan regions.

In practice, the distribution of public transit service across metropolitan areas does not always reflect socioeconomic indicators of transit dependence, such as income, vehicle availability, and commuting patterns. Comparing transit need and supply is further complicated by fragmented data structures: measures of transit demand are typically reported at the metropolitan level, while transit service metrics
are reported at the urbanized area level. This project is motivated by the need for a transparent, data-driven framework to compare public transit need and supply across major U.S. metropolitan statistical areas.

## II. Research Question
Which of the 20 largest U.S. metropolitan statistical areas exhibit the largest gaps between public transit need and public transit supply?

## III. Data Sources
This project uses publicly available datasets from the United States Census Bureau and the Federal Transit Administration.    
### 1. American Community Survey (ACS)  
- [Table B01003: Total Population - Census Bureau Table](https://data.census.gov/table/ACSDT1Y2024.B01003?q=B01003&g=010XX00US$3140000&moe=false)
- [Table B08301: Means of Transportation to Work](https://data.census.gov/table/ACSDT1Y2024.B08301?q=B08301:+Means+of+Transportation+to+Work&moe=false)
- [Table B08201: Household Size by Vehicles Available](https://data.census.gov/table/ACSDT1Y2024.B08201?q=b08201&g=010XX00US$31000M1&moe=false)
- [Table S1903: Median Income in the Past 12 Months (in 2024 Inflation-Adjusted Dollars)](https://data.census.gov/table/ACSST1Y2024.S1903?q=S1903&g=010XX00US$31000M1&moe=false)

### 2. Federal Transit Administration
- [National Transit Dataset - Service (by Mode and Time Period)](https://catalog.data.gov/dataset/service-flat-file)
- [Annual Database Agency Information](https://www.transit.dot.gov/ntd/data-product/2024-annual-database-agency-information)

### 3. United States Census Bureau
- [Metropolitan Statistical Areas (MSA) References Files](https://www.census.gov/geographies/reference-files/time-series/demo/metro-micro/delineation-files.html)
  
## IV. Unit of Analysis

## V. Methodology
### 1. Transit Need Index
Transit need was approximated using the following variables:

- Percentage of households with no vehicle available
- Percentage of workers commuting via public transit
- Mean household income (inverted to reflect higher need at lower incomes)

Each variable was standardized using a **robust z-score** based on the median and interquartile range (IQR).
The final Transit Need Index is calculated as the unweighted mean of the standardized variables:

$$ Transit Need Index = \frac{Z_{noVehicle} + Z_{transitCommute} − Z_{income}}{3}$$
### 2. Transit Supply Index
Transit supply was measured using National Transit Database service metrics:

- Vehicle Revenue Miles (VRM) per capita
- Vehicle Revenue Hours (VHM) per capita

All metrics were aggregated from the transit agency level to the MSA level and normalized by population.
Standardization followed the same robust z-score approach used for the Transit Need Index.
The final Transit Supply Index is calculated as the unweighted mean of the standardized variables:

$$ Transit Supply Index = \frac{Z_{VRM per capita} + Z_{VRH per capita}}{2}$$

### 3. Transit Need–Supply Gap

The Transit Gap metric is defined as the difference between the Transit Need Index and the Transit Supply Index:

$$ Transit Gap = Transit Need Index − Transit Supply Index $$

Positive values indicate MSAs where transit need exceeds supply,
while negative values indicate relatively higher levels of transit provision.

## VI. Key Findings

## VII. Limitations
- Census data for Urbanized Area is available, however, the data was last updated in 2020, plus the project's scope is MSAs (Need to edit more)

## VIII. Authors
Minh Kiet Tran (Charles Tran)  
Dung Tri Nguyen (Dune Nguyen)

