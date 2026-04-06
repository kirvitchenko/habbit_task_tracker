CREATE TABLE kafka_task_events (
    event_type String,
    task_id UInt64,
    value String,
    timestamp DateTime
) ENGINE = Kafka
SETTINGS kafka_broker_list = 'kafka:9092',
         kafka_topic_list = 'task.events',
         kafka_group_name = 'clickhouse_task_consumer',
         kafka_format = 'JSONEachRow';

CREATE TABLE task_events (
    event_type String,
    task_id UInt64,
    value String,
    timestamp DateTime
) ENGINE = MergeTree()
ORDER BY (timestamp, task_id);

CREATE MATERIALIZED VIEW kafka_task_events_mv TO task_events AS
SELECT event_type, task_id, value, timestamp
FROM kafka_task_events;

CREATE TABLE kafka_category_events (
    event_type String,
    category_id UInt64,
    value String,
    timestamp DateTime
) ENGINE = Kafka
SETTINGS kafka_broker_list = 'kafka:9092',
         kafka_topic_list = 'category.events',
         kafka_group_name = 'clickhouse_category_consumer',
         kafka_format = 'JSONEachRow';

CREATE TABLE category_events (
    event_type String,
    category_id UInt64,
    value String,
    timestamp DateTime
) ENGINE = MergeTree()
ORDER BY (timestamp, category_id);

CREATE MATERIALIZED VIEW kafka_category_events_mv TO category_events AS
SELECT event_type, category_id, value, timestamp
FROM kafka_category_events;