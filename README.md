# CitizenSensor

Mapping and Citizen Sensor project

Contents of 'data' directory
============================

**Lucas_data.zip**

This contains the allocated land cover and land use labels for all photos in the Eurostat LUCAS survey. 

**Places_scene_attributes.csv**

This file allocates a usefulness to each of the semantic attributes in terms of identifying land cover, according to the following rule.
- u = Useful
- m = may be useful
- n = not useful

The file also records the Level 1 LUCAS landcovers with which that tag could be associated. Where multiple landcover associations are possible, these are separated by '&' characters.

a:	ARTIFICIAL LAND -	Areas characterized by an artificial and often impervious cover of constructions and pavement.

b:	CROPLAND -	Areas where crops are planted and cultivated.

c:	WOODLAND -	Areas covered by trees with a canopy of at least 10% (of the extended window). Also woody hedges belong to this class.
NB: Height of trees at maturity and width of woody features have to be assessed.

d:	SHRUBLAND -	Areas dominated (more than 10% of the surface) by shrubs and low woody plants capable of growing to a height of <5m at maturity.  It may include sparsely occurring trees within a maximum limit of 10% canopy. 


e:	GRASSLAND -	Land predominantly covered by communities of grassland, grass-like plants and forbs. It may include sparsely occurring trees within a limit of a canopy of <10% and shrubs within a total limit of cover (including trees) of 20%.

f:	BARE LAND AND LICHENS -	Areas with no dominant vegetation cover on at least 90% of the area or areas covered by lichens.

g:	WATER AREAS	 -Inland or coastal areas without vegetation and covered by water and flooded surfaces or likely to be so over a large part of the year.  
Temporarily submerged islands and sandbanks are to be assigned in F classes.

h:	WETLANDS -	Wetlands are areas that fall between land and water. These are areas that are wet for long enough periods that the plants and animals living in or near them are adapted to, and often dependent on, wet conditions for at least part of their life cycle. 




**Places_semantic_attributes.csv**

This file allocates a usefulness to each of the semantic attributes, and records the Level 1 LUCAS lndcovers with which that tag could be associated, as above. Almost all semantic attributes have potential usefulness, but a large proportion of them simply inform us that a photograph was tken indoors. For this reason, this file contains an additional column, 'why_useful' which allocates attributes to classes as follows:

- bi = built environment, indoors

- b = built environment, may be indoors or outdoors

- n = natural environment

- hf = human feature (e.g., a bridge, railway line, fountain, windmill...) May be placed in a natural landcscape

- hl = human landuse (e.g., agriculture, gardens, golf course). Landscape may be vegetated but human influence is expected to affect a substantial area of the scene.
