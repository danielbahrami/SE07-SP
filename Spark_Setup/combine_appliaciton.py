from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType
from pyspark.sql.functions import *

if __name__ == "__main__":
    spark = SparkSession.builder.appName("SWITRS_COORDINATES_COMBINATION").getOrCreate()

    streaming_SWITRS_COLLISION = (
        spark.readStream.format("kafka")
        .option("kafka.bootstrap.servers", "strimzi-kafka-bootstrap.kafka:9092")
        .option("subscribe", "SWITRS_COLLISIONS")
        .option("startingOffsets", "earliest")
        .load()
    )

    streaming_COORDINATES = (
        spark.readStream.format("kafka")
        .option("kafka.bootstrap.servers", "strimzi-kafka-bootstrap.kafka:9092")
        .option("subscribe", "COORDINATES")
        .option("startingOffsets", "earliest")
        .load()
    )

    collisionStringDF = streaming_SWITRS_COLLISION.selectExpr("CAST(value AS STRING)")
    coordinateStringDF = streaming_COORDINATES.selectExpr("CAST(value AS STRING)")

    schemaCollision = StructType([ \
        StructField("case_id",StringType()), \
        StructField("jurisdiction",StringType()), \
        StructField("officer_id",StringType()), \
        StructField("reporting_district",StringType()), \
        StructField("chp_shift",StringType()), \
        StructField("population",StringType()), \
        StructField("county_city_location",StringType()), \
        StructField("county_location",StringType()), \
        StructField("special_condition",StringType()), \
        StructField("beat_type",StringType()), \
        StructField("chp_beat_type",StringType()), \
        StructField("city_division_lapd",StringType()), \
        StructField("chp_beat_class",StringType()), \
        StructField("beat_number",StringType()), \
        StructField("primary_road",StringType()), \
        StructField("secondary_road",StringType()), \
        StructField("distance",IntegerType()), \
        StructField("direction",StringType()), \
        StructField("intersection",IntegerType()), \
        StructField("weather_1",StringType()), \
        StructField("weather_2",StringType()), \
        StructField("state_highway_indicator",IntegerType()), \
        StructField("caltrans_county",StringType()), \
        StructField("caltrans_district",IntegerType()), \
        StructField("state_route",IntegerType()), \
        StructField("route_suffix",StringType()), \
        StructField("postmile_prefix",StringType()), \
        StructField("postmile",DoubleType()), \
        StructField("location_type",StringType()), \
        StructField("ramp_intersection",StringType()), \
        StructField("side_of_highway",StringType()), \
        StructField("tow_away",IntegerType()), \
        StructField("collision_severity",StringType()), \
        StructField("killed_victims",IntegerType()), \
        StructField("injured_victims",IntegerType()), \
        StructField("party_count",IntegerType()), \
        StructField("primary_collision_factor",StringType()), \
        StructField("pcf_violation_code",StringType()), \
        StructField("pcf_violation_category",StringType()), \
        StructField("pcf_violation",IntegerType()), \
        StructField("pcf_violation_subsection",StringType()), \
        StructField("hit_and_run",StringType()), \
        StructField("type_of_collision",StringType()), \
        StructField("motor_vehicle_involved_with",StringType()), \
        StructField("pedestrian_action",StringType()), \
        StructField("road_surface",StringType()), \
        StructField("road_condition_1",StringType()), \
        StructField("road_condition_2",StringType()), \
        StructField("lighting",StringType()), \
        StructField("control_device",StringType()), \
        StructField("chp_road_type",StringType()), \
        StructField("pedestrian_collision",IntegerType()), \
        StructField("bicycle_collision",IntegerType()), \
        StructField("motorcycle_collision",IntegerType()), \
        StructField("truck_collision",IntegerType()), \
        StructField("not_private_property",IntegerType()), \
        StructField("alcohol_involved",IntegerType()), \
        StructField("statewide_vehicle_type_at_fault",StringType()), \
        StructField("chp_vehicle_type_at_fault",StringType()), \
        StructField("severe_injury_count",IntegerType()), \
        StructField("other_visible_injury_count",IntegerType()), \
        StructField("complaint_of_pain_injury_count",IntegerType()), \
        StructField("pedestrian_killed_count",IntegerType()), \
        StructField("pedestrian_injured_count",IntegerType()), \
        StructField("bicyclist_killed_count",IntegerType()), \
        StructField("bicyclist_injured_count",IntegerType()), \
        StructField("motorcyclist_killed_count",IntegerType()), \
        StructField("motorcyclist_injured_count",IntegerType()), \
        StructField("primary_ramp",StringType()), \
        StructField("secondary_ramp",StringType()), \
        StructField("collision_date",StringType()), \
        StructField("collision_time",StringType()), \
        StructField("process_date",StringType()), \
    ])
    
    schemaCoordiantes = StructType([ \
        StructField("case_id",StringType()), \
        StructField("latitude",DoubleType()), \
        StructField("longitude",DoubleType()), \
    ])

    collisionJson_df = collisionStringDF.withColumn("value", from_json(col("value").cast("string"), schemaCollision)).selectExpr("value.*")
    coordinatesJson_df = coordinateStringDF.withColumn("value", from_json(col("value").cast("string"), schemaCoordiantes)).selectExpr("value.*")

    collisionJson_df.createOrReplaceTempView("collisions")
    coordinatesJson_df.createOrReplaceTempView("coordinates")
    combinedJson_df = spark.sql("SELECT * FROM coordinates INNER JOIN collisions ON coordinates.case_id = collisions.case_id")

    finalDF = combinedJson_df.select(col("collisions.case_id"), to_json(struct("*"), options={"ignoreNullFields":False})).toDF("key", "value")

    finalDF.selectExpr("key","value").writeStream.format("kafka").option("kafka.bootstrap.servers", "strimzi-kafka-bootstrap.kafka:9092").option("topic", "COMBINED_SWITRS_COLLISIONS").option("checkpointLocation", "checkpoint").start().awaitTermination()

    spark.stop()