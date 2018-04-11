#!/usr/bin/python3
# -*- coding: utf8 -*-

import logging


KAP_logger = logging.getLogger(__name__)


if __name__ == '__main__':
    import json

    from kafka import KafkaProducer
    from kafka.errors import KafkaError

    import util

    util.enable_default_log()

    logging.getLogger().setLevel(logging.WARNING)

    producer = KafkaProducer(
        bootstrap_servers=['127.0.0.1:9092'],
        value_serializer=lambda m: json.dumps(m).encode('utf8'))

    def on_send_success(record_metadata):
        # print('%'*20)
        # print(repr(record_metadata))
        KAP_logger.warning(
            "<<< %s:%d:%d"
            % (record_metadata.topic, record_metadata.partition,
                record_metadata.offset))

    def on_send_error(excp):
        KAP_logger.error('I am an errback', exc_info=excp)
        # handle exception

    try:
        for x in range(0, 4):
            # produce asynchronously with callbacks
            producer.send(
                'my-topic',
                {'key-%s' % str(x): 'value-%s' % str(x)},
                key=b'my-key')\
                .add_callback(on_send_success).add_errback(on_send_error)

        # block until all async messages are sent
        producer.flush()

        producer.close()
    except KafkaError:
        # Decide what to do if produce request failed...
        KAP_logger.exception()
        pass
