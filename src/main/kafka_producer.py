import json
from kafka import KafkaProducer
import environ

env = environ.Env()
env.read_env()

producer = KafkaProducer(
    bootstrap_servers=[env('BOOTSTRAP_SERVERS')], # localhost:9092
    value_serializer=lambda v: json.dumps(v,default=str).encode('utf-8') # converting python dict into json
)

def publish_listing_created(listing):

    event = {
        'event': 'LISTING_CREATED',
        "listing_id": str(listing.id),
        "model": listing.model, 
        "brand": listing.brand,
    }

    producer.send('listing-event', value=event)
    producer.flush()  # Ensure the message is sent before proceeding
