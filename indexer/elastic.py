"""
Elastic Search App Mixin
"""

# from indexer.workers.importer

import argparse
import os
import sys
from logging import getLogger
from typing import Any, List, Optional
from urllib.parse import urlparse

from elastic_transport import NodeConfig, ObjectApiResponse
from elasticsearch import Elasticsearch

from indexer.app import ArgsProtocol

logger = getLogger(__name__)


class ElasticMixin:
    """
    mixin class for Apps that use Elastic Search API
    """

    def define_options(self: ArgsProtocol, ap: argparse.ArgumentParser) -> None:
        super().define_options(ap)

        ap.add_argument(
            "--elasticsearch-hosts",
            dest="elasticsearch_hosts",
            default=os.environ.get("ELASTICSEARCH_HOSTS") or "",
            help="comma separated list of ES server URLs",
        )

    def elasticsearch_client(self: ArgsProtocol) -> Elasticsearch:
        assert self.args
        hosts = self.args.elasticsearch_hosts
        if not hosts:
            logger.fatal("need --elasticsearch-hosts or ELASTICSEARCH_HOSTS")
            sys.exit(1)

        # Connects immediately, performs failover and retries
        return Elasticsearch(hosts.split(","))


class ElasticSnapshotMixin(ElasticMixin):
    def define_options(self: ArgsProtocol, ap: argparse.ArgumentParser) -> None:
        super().define_options(ap)

        ap.add_argument(
            "--elasticsearch-snapshot-repo",
            dest="elasticsearch_snapshot_repo",
            default=os.environ.get("ELASTICSEARCH_SNAPSHOT_REPO") or "",
            help="ES snapshot repository name",
        )

    def get_elasticsearch_snapshot(self: ArgsProtocol) -> Any:
        assert self.args
        if not self.args.elasticsearch_snapshot_repo:
            logger.fatal(
                "need --elasticsearch-snapshot-repo or ELASTICSEARCH_SNAPSHOT_REPO"
            )
            sys.exit(1)
        return self.args.elasticsearch_snapshot_repo
