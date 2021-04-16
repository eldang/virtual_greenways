CREATE INDEX bike_geom_idx ON bike USING GIST(geom);
CREATE INDEX planned_geom_idx ON bike_planned USING GIST(geom);
CREATE INDEX streets_geom_idx ON streets USING GIST(geom);

DROP TABLE IF EXISTS bike_agg;
CREATE TABLE bike_agg AS
	SELECT
		street_nam AS street_name,
		CASE
			WHEN existing_f IN ('Neighborhood Greenway', 'Multi-use Trail', 'In Street, Major Separation') THEN 'AAA'
			WHEN existing_f = 'In Street, Major Separation' THEN 'Intermediate'
			WHEN existing_f = 'In Street, Minor Separation' THEN 'Difficult'
			ELSE 'Unclassified'
		END AS difficulty,
		status,
		network,
		existing_f AS existing_facility,
		planned_fa AS planned_facility,
		ST_Union(geom) AS geom
	FROM public.bike
	GROUP BY street_nam, status, network, existing_f, planned_fa;

CREATE INDEX bike_agg_geom_idx ON bike_agg USING GIST(geom);


DROP TABLE IF EXISTS bike_planned_agg;
CREATE TABLE bike_planned_agg AS
	SELECT
		street_nam AS street_name,
		CASE
			WHEN planned_fa IN ('Neighborhood Greenway', 'Multi-use Trail', 'In Street, Major Separation') THEN 'AAA'
			WHEN planned_fa = 'In Street, Major Separation' THEN 'Intermediate'
			WHEN planned_fa = 'In Street, Minor Separation' THEN 'Difficult'
			ELSE 'Unclassified'
		END AS difficulty,
		status,
		network,
		existing_f AS existing_facility,
		planned_fa AS planned_facility,
		ST_Union(geom) AS geom
	FROM public.bike_planned
	GROUP BY street_nam, status, network, existing_f, planned_fa;

CREATE INDEX bike_planned_agg_geom_idx ON bike_planned_agg USING GIST(geom);
