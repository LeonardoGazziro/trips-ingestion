DROP EXTENSION IF EXISTS postgis CASCADE;
CREATE EXTENSION postgis
WITH SCHEMA public;

-- Create table in layer operational data storage.
create table if not exists "operational".trips_log (
	trip_id SERIAL PRIMARY key,
	region VARCHAR(100),
	trip_date_time TIMESTAMP,
	trip_source VARCHAR(100),
	coord_origin geography(point),
	coord_dest geography(point)
);

ALTER TABLE operational.trips_log OWNER TO postgres;

-- Cast fields for his data type and insert in the table
insert into "operational".trips_log (
	region,
	trip_date_time,
	trip_source,
	coord_origin,
	coord_dest
)
select 
	region,
	CAST(datetime as TIMESTAMP),
	datasource,
	CAST(origin_coord as geography),
	CAST(destination_coord as geography)
from "stage".trips_log ;

-- Create view to get average trips by week
CREATE VIEW "operational".weekly_avg_trip_by_region
AS 
select 
	trips_by_week.trip_region,
	avg(trips_by_week.total_trips) 
from (
	select 
		count(1) as total_trips,
		t1.region as trip_region,
		EXTRACT(week from t1.trip_date_time) as week_number
	from "operational".trips_log t1
	group by t1.region, EXTRACT(week from t1.trip_date_time)
) trips_by_week
group by trips_by_week.trip_region;

-- Create view to get similar trips where origin and destine stay in a 2500 radius and in the same hour of day.
create view "operational".similar_trips_by_radius_and_hour
as (
	with twr as (
		select 
			distinct trip_id as id,
			region,
		   	extract(hour from trip_date_time) AS day_hour,
		    ST_buffer(coord_origin, 2500) as origin_radius,
		    ST_buffer(coord_dest, 2500) as dest_radius,
		    coord_origin,
		    coord_dest
		FROM "operational".trips_log
	)
	select 
		distinct a.id,
		a.region,
		a.day_hour,
		a.coord_origin,
		a.coord_dest
	from twr a, twr b
	where a.id <> b.id
	and ST_INTERSECTS(a.origin_radius, b.origin_radius) = true 
	and ST_INTERSECTS(a.dest_radius, b.dest_radius) = true
	and a.day_hour = b.day_hour
	group by a.id, b.id, a.region, a.day_hour, a.coord_origin, a.coord_dest
);

