# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2022 Geo Secretariat.
#
# geo-comments is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Comment service config."""


class MetricsBuilder:
    """Base class to represent a metrics builder.

    A Metrics Builder is an entity who enable users to generate
    metrics. Also, users can, via configuration, modify the properties
    of the generated metrics (e.g., Precision).
    """

    def __init__(self, search, **kwargs):
        """Initializer."""
        self._search = search

    def generate(self):
        """Generate the metrics."""
        pass


class RecordFeedbackMetrics(MetricsBuilder):
    """Record feedback metrics.

    Generate metrics from the feedback topics available in a record.

    ToDo:
        Check if Invenio already have solutions for this kind of operation.
    """

    @property
    def metric(self):
        """Metric definition query."""
        return dict(
            aggs={
                "topics": {
                    "nested": {"path": "topics"},
                    "aggs": {
                        "topics_term": {
                            "terms": {"field": "topics.name"},
                            "aggs": {
                                "topics_values": {"stats": {"field": "topics.rating"}}
                            },
                        }
                    },
                }
            }
        )

    def __init__(self, search, precision=3, **kwargs):
        """Initializer."""
        super(RecordFeedbackMetrics, self).__init__(search, **kwargs)

        self._precision = precision

    def generate(self):
        """Generate the metrics."""
        # Configuring the search client.
        _search = self._search.update_from_dict(self.metric)

        # Performing the search
        metrics_result = _search.execute()

        # Configuring the metrics results in a standard format.
        metrics = []

        if metrics_result.aggregations.topics.doc_count > 0:
            metric_buckets = metrics_result.aggregations.topics.topics_term.buckets

            for metric_bucket in metric_buckets:
                metric_topic_values = metric_bucket["topics_values"]
                metric_topic_values_dict = {}

                # updating the precision of the metrics
                for metric_value_key in ["min", "max", "avg", "sum", "count"]:
                    metric_value = metric_topic_values[metric_value_key]
                    metric_value = round(metric_value, self._precision)

                    metric_topic_values_dict[metric_value_key] = metric_value

                metrics.append(
                    dict(name=metric_bucket["key"], stats=metric_topic_values_dict)
                )

        return dict(topics=metrics)
