# Capacitated Facility Location Model for Electric Vehicle Service Centers (cafe-visit)
According to the International Energy Agency, the electric car sales in 2022 exceeded 10 million indicating that it has tripled in the last three years. This number is expected to grow especially at the backdrop of policies and efforts to decarbonize road transportation sector. However, the switch to electric vehicles will require extensive supporting infrastructure such as servicing centers and charging points for countries that are yet to adopt them. Although the electric vehicles are not made out of a completely new technology, servicing them will require new set of skills that may be lacking among conventional mechanics and technicians in developing world. Therefore, it is important for the distributors and sellers of EV to setup regional service centers for repairs, training and retraining of the car technicians and even sale of spare parts. Setting such a center requires initial capital investment as well as ensuring that it is located in an optimal position where it serves the needs of the nearby car owners. To this end, this work seeks to develop a model for determining the optimal number and location of EV service centers in Sub-Saharan Africa (SSA). The model will account for the cost of reaching the service center as well as the fixed construction cost. A hypothetical cost of taxes, electricity, rent and maintenance will be included as fixed costs. The number of potential car owners will be obtained from population satellite raster layers and calculated as a percentage of the total population. Therefore, the paper will determine the number and location of service centers that meet the customers demand while reducing the access and fixed costs. 

Methodology
==============
The method (see `Figure 1`) ..... 

## Method Box

#### Figure 1 Proposed Optimization Method.
<p align="center">
  <img src="/docs/method.png" />
</p>

Results
==============
`Figure 2` shows the potential annual customer care EV service requests by country sub-regions for Kenya, Mozambique, Cameroon and Ghana.

#### Figure 2 Projected Customer Demand Across four Sub-Saharan Africa Countries.
<p align="center">
  <img src="/docs/Combined_SSA_sites_maps.png" />
</p>

`Figure 3` shows the optimized EV service center locations by country sub-regions for Kenya, Mozambique, Cameroon and Ghana.

#### Figure 3 Optimized EV Service Center Locations for four Sub-Saharan Africa Countries.
<p align="center">
  <img src="/docs/Combined_optimized_maps.png" />
</p>

## Required Data
[1]	“Open Spatial Demographic Data and Research,” WorldPop. https://www.worldpop.org/ (accessed May 08, 2023).

[2]	GADM, “Global Administrative Areas Boundaries.” https://gadm.org/download_world.html (accessed Sep. 14, 2022).

[3] Country metadafile. Contained in `/data/countries.csv`
