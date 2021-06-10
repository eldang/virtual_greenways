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


DROP TABLE IF EXISTS streets_agg;
CREATE TABLE streets_agg AS
	SELECT
		ord_stname AS street_name,
		l_city AS city,
		ST_Union(geom) AS geom
	FROM public.streets
	GROUP BY ord_stname, l_city;

CREATE INDEX streets_agg_geom_idx ON streets_agg USING GIST(geom);



CREATE OR REPLACE VIEW bike_aaa_kml AS
	SELECT
		'<Placemark>' ||
		CASE WHEN street_name IS NOT NULL THEN
			'<name>' || street_name || '</name>'
		ELSE '' END ||
		'<styleUrl>#AAA</styleUrl>' ||
		'<ExtendedData><SchemaData schemaUrl="#bike_friendliness">' ||
		CASE WHEN street_name IS NOT NULL THEN
			'<SimpleData name="street_name">' || street_name || '</SimpleData>'
		ELSE '' END ||
		CASE WHEN difficulty IS NOT NULL THEN
			'<SimpleData name="difficulty">' || difficulty || '</SimpleData>'
		ELSE '' END ||
		CASE WHEN status IS NOT NULL THEN
			'<SimpleData name="status">' || status || '</SimpleData>'
		ELSE '' END ||
		CASE WHEN network IS NOT NULL THEN
			'<SimpleData name="network">' || network || '</SimpleData>'
		ELSE '' END ||
		CASE WHEN existing_facility IS NOT NULL THEN
			'<SimpleData name="existing_facility">' || existing_facility || '</SimpleData>'
		ELSE '' END ||
		CASE WHEN planned_facility IS NOT NULL THEN
			'<SimpleData name="planned_facility">' || planned_facility || '</SimpleData>'
		ELSE '' END ||
		'</SchemaData></ExtendedData>' ||
		ST_AsKml(geom) ||
		'</Placemark>'
	FROM bike_agg
	WHERE difficulty = 'AAA';

CREATE OR REPLACE VIEW bike_intermediate_kml AS
	SELECT
		'<Placemark>' ||
		CASE WHEN street_name IS NOT NULL THEN
			'<name>' || street_name || '</name>'
		ELSE '' END ||
		'<styleUrl>#Intermediate</styleUrl>' ||
		'<ExtendedData><SchemaData schemaUrl="#bike_friendliness">' ||
		CASE WHEN street_name IS NOT NULL THEN
			'<SimpleData name="street_name">' || street_name || '</SimpleData>'
		ELSE '' END ||
		CASE WHEN difficulty IS NOT NULL THEN
			'<SimpleData name="difficulty">' || difficulty || '</SimpleData>'
		ELSE '' END ||
		CASE WHEN status IS NOT NULL THEN
			'<SimpleData name="status">' || status || '</SimpleData>'
		ELSE '' END ||
		CASE WHEN network IS NOT NULL THEN
			'<SimpleData name="network">' || network || '</SimpleData>'
		ELSE '' END ||
		CASE WHEN existing_facility IS NOT NULL THEN
			'<SimpleData name="existing_facility">' || existing_facility || '</SimpleData>'
		ELSE '' END ||
		CASE WHEN planned_facility IS NOT NULL THEN
			'<SimpleData name="planned_facility">' || planned_facility || '</SimpleData>'
		ELSE '' END ||
		'</SchemaData></ExtendedData>' ||
		ST_AsKml(geom) ||
		'</Placemark>'
	FROM bike_agg
	WHERE difficulty = 'Intermediate';

CREATE OR REPLACE VIEW bike_difficult_kml AS
	SELECT
		'<Placemark>' ||
		CASE WHEN street_name IS NOT NULL THEN
			'<name>' || street_name || '</name>'
		ELSE '' END ||
		'<styleUrl>#Difficult</styleUrl>' ||
		'<ExtendedData><SchemaData schemaUrl="#bike_friendliness">' ||
		CASE WHEN street_name IS NOT NULL THEN
			'<SimpleData name="street_name">' || street_name || '</SimpleData>'
		ELSE '' END ||
		CASE WHEN difficulty IS NOT NULL THEN
			'<SimpleData name="difficulty">' || difficulty || '</SimpleData>'
		ELSE '' END ||
		CASE WHEN status IS NOT NULL THEN
			'<SimpleData name="status">' || status || '</SimpleData>'
		ELSE '' END ||
		CASE WHEN network IS NOT NULL THEN
			'<SimpleData name="network">' || network || '</SimpleData>'
		ELSE '' END ||
		CASE WHEN existing_facility IS NOT NULL THEN
			'<SimpleData name="existing_facility">' || existing_facility || '</SimpleData>'
		ELSE '' END ||
		CASE WHEN planned_facility IS NOT NULL THEN
			'<SimpleData name="planned_facility">' || planned_facility || '</SimpleData>'
		ELSE '' END ||
		'</SchemaData></ExtendedData>' ||
		ST_AsKml(geom) ||
		'</Placemark>'
	FROM bike_agg
	WHERE difficulty = 'Difficult';

CREATE OR REPLACE VIEW bike_unclassified_kml AS
	SELECT
		'<Placemark>' ||
		CASE WHEN street_name IS NOT NULL THEN
			'<name>' || street_name || '</name>'
		ELSE '' END ||
		'<styleUrl>#Unclassified</styleUrl>' ||
		'<ExtendedData><SchemaData schemaUrl="#bike_friendliness">' ||
		CASE WHEN street_name IS NOT NULL THEN
			'<SimpleData name="street_name">' || street_name || '</SimpleData>'
		ELSE '' END ||
		CASE WHEN difficulty IS NOT NULL THEN
			'<SimpleData name="difficulty">' || difficulty || '</SimpleData>'
		ELSE '' END ||
		CASE WHEN status IS NOT NULL THEN
			'<SimpleData name="status">' || status || '</SimpleData>'
		ELSE '' END ||
		CASE WHEN network IS NOT NULL THEN
			'<SimpleData name="network">' || network || '</SimpleData>'
		ELSE '' END ||
		CASE WHEN existing_facility IS NOT NULL THEN
			'<SimpleData name="existing_facility">' || existing_facility || '</SimpleData>'
		ELSE '' END ||
		CASE WHEN planned_facility IS NOT NULL THEN
			'<SimpleData name="planned_facility">' || planned_facility || '</SimpleData>'
		ELSE '' END ||
		'</SchemaData></ExtendedData>' ||
		ST_AsKml(geom) ||
		'</Placemark>'
	FROM bike_agg
	WHERE difficulty = 'Unclassified' OR difficulty IS NULL;

CREATE OR REPLACE VIEW bike_kml AS
	SELECT
		'<?xml version="1.0" encoding="utf-8" ?>' ||
		'<kml xmlns="http://www.opengis.net/kml/2.2">' ||
		'<Document id="root_doc">' ||
		'<Schema name="bike_friendliness" id="bike_friendliness">' ||
		'<SimpleField name="street_name" type="string"></SimpleField>' ||
		'<SimpleField name="difficulty" type="string"></SimpleField>' ||
		'<SimpleField name="status" type="string"></SimpleField>' ||
		'<SimpleField name="network" type="string"></SimpleField>' ||
		'<SimpleField name="existing_facility" type="string"></SimpleField>' ||
		'<SimpleField name="planned_facility" type="string"></SimpleField>' ||
		'</Schema>' ||
    '<Style id="AAA">' ||
    '<LineStyle><width>5</width><color>FF65b24e</color></LineStyle>' ||
    '</Style>' ||
    '<Style id="Intermediate">' ||
    '<LineStyle><width>3</width><color>FFc78952</color></LineStyle>' ||
    '</Style>' ||
    '<Style id="Difficult">' ||
    '<LineStyle><width>3</width><color>FF0c05dc</color></LineStyle>' ||
    '</Style>' ||
    '<Style id="Unclassified">' ||
    '<LineStyle><width>4</width><color>FF777777</color></LineStyle>' ||
    '</Style>' ||
    '<Folder><name>AAA</name>'
  UNION ALL
  	SELECT * FROM bike_aaa_kml
  UNION ALL
		SELECT '</Folder><Folder><name>Intermediate</name>'
  UNION ALL
  	SELECT * FROM bike_intermediate_kml
  UNION ALL
		SELECT '</Folder><Folder><name>Difficult</name>'
  UNION ALL
  	SELECT * FROM bike_difficult_kml
  UNION ALL
		SELECT '</Folder><Folder><name>Unclassified</name>'
  UNION ALL
  	SELECT * FROM bike_unclassified_kml
  UNION ALL
		SELECT '</Folder></Document></kml>';

SELECT * FROM bike_kml;
