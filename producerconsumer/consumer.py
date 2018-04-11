#!/usr/bin/python3
# -*- coding: utf8 -*-

import logging


KAC_logger = logging.getLogger(__name__)


if __name__ == '__main__':
    import json

    from kafka import KafkaConsumer
    from kafka.errors import KafkaError

    import util

    util.enable_default_log()

    logging.getLogger().setLevel(logging.WARNING)

    # To consume latest messages and auto-commit offsets
    consumer = KafkaConsumer(
        'my-topic',
        group_id='my-group',
        bootstrap_servers=['127.0.0.1:9092'],
        consumer_timeout_ms=1000,
        value_deserializer=lambda m: json.loads(m.decode('utf8')))

    try:
        for message in consumer:
            # message value and key are raw bytes -- decode if necessary!
            # e.g., for unicode: `message.value.decode('utf-8')`
            KAC_logger.warning(
                ">>> %s:%d:%d: key=%s value=%s"
                % (message.topic, message.partition,
                    message.offset, message.key,
                    message.value))

        consumer.close()
    except KafkaError:
        # Decide what to do if produce request failed...
        KAC_logger.exception()
        pass
