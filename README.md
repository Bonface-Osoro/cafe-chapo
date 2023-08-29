# Capacitated Facility Location of Electric Charging Points (cafe-chapo)
Over the next century we are expected to experience an increase in the frequency and severity of climate-related hazards, including coastal flooding, riverine flooding, and tropical storms. Dealing with extreme events is considerably easy for the affluent, who have the resources to vacate to a safer location and replace damaged property. In contrast, those living on the poverty line (US$ 2 per day) often must shelter in place and may have their entire livelihood disrupted from storm damage. 

1.	What portion of the global poverty-line population is unconnected (to 2G, 3G, 4G and 5G) and where are they?

Methodology
==============
The method (see `Figure 1`) will utilize 47 million OpenCelliD data points to inform 2G, 3G, 4G and 5G coverage. Income estimates for low and middle income countries will be utilized for poverty estimation at the 1 km2 level (Chi et al., 2022). Additionally, multiple hazard models will be utilized, for flooding from the World Resource Institute Aqueduct platform, and for tropical cyclones from recently developed maximum wind speed estimates. Hazard impacts will be compared for a historical scenario (1980) and compared to a worst-case (RCP8.5) representing no emissions abatement, for different event probabilities. 

## Method Box

#### Figure 1 Proposed Method.
<p align="center">
  <img src="/docs/method.png" />
</p>

The results are based on the data for historical baseline from 1980 and the Representative Concentration Pathway 8.5 (rising carbon emissions) (RCP8.5) scenarios obtained from the World Resource Institute [1]. 

## Required Data
[1]	“Open Spatial Demographic Data and Research,” WorldPop. https://www.worldpop.org/ (accessed May 08, 2023).

[2]	GADM, “Global Administrative Areas Boundaries.” https://gadm.org/download_world.html (accessed Sep. 14, 2022).

[3] Country metadafile. Contained in `/data/countries.csv`
