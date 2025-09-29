# services/feature-store/feature_repo.py
from feast import Entity, Feature, FeatureView, FileSource, RepoConfig
from feast.types import Float32, String
from datetime import timedelta


# Define data source — for demo we point to local parquet created by streaming job
events_source = FileSource(
path="/data/delta/events",
event_timestamp_column="timestamp",
created_timestamp_column=None
)


user = Entity(name="user_id", value_type=String)


user_features = FeatureView(
name="user_events",
entities=["user_id"],
ttl=timedelta(days=30),
schema=[
Feature(name="score", dtype=Float32),
],
source=events_source
)
