# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ducktape.utils.util import wait_until

from kafkatest.tests.verifiable_consumer_test import VerifiableConsumerTest

class PluggableConsumerTest(VerifiableConsumerTest):
    """ Verify that the pluggable client framework works. """

    TOPIC = "test_topic"
    NUM_PARTITIONS = 1

    def __init__(self, test_context):
        super(PluggableConsumerTest, self).__init__(test_context, num_consumers=1, num_producers=0,
                                num_zk=1, num_brokers=1, topics={
                                self.TOPIC : { 'partitions': self.NUM_PARTITIONS, 'replication-factor': 1 },
        })

    def test_start_stop(self):
        """
        Test that a pluggable VerifiableConsumer module load works
        """
        consumer = self.setup_consumer(self.TOPIC)

        for num_started, node in enumerate(consumer.nodes, 1):
            consumer.start_node(node)

        self.logger.debug("Waiting for %d nodes to start" % len(consumer.nodes))
        wait_until(lambda: len(consumer.alive_nodes()) == len(consumer.nodes),
                   timeout_sec=60,
                   err_msg="Timed out waiting for consumers to start")
        self.logger.debug("Started: %s" % str(consumer.alive_nodes()))
        consumer.stop_all()

        self.logger.debug("Waiting for %d nodes to stop" % len(consumer.nodes))
        wait_until(lambda: len(consumer.dead_nodes()) == len(consumer.nodes),
                   timeout_sec=self.session_timeout_sec+5,
                   err_msg="Timed out waiting for consumers to shutdown")
