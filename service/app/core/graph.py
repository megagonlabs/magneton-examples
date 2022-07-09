import uuid, traceback, json
import pandas as pd
from .database import Database


class Graph:

    def __init__(self, uri, username, password):
        try:
            neo4j_user = username
            neo4j_pwd = password
            self.neo4j_conn = Database(uri, neo4j_user, neo4j_pwd)
        except Exception:
            raise Exception('Failed to connect to database.')

    def stop(self):
        self.neo4j_conn.close()

    def get_node_attributes(self, node, row=None, column_index=None):
        if "attributes" not in node.keys():
            attributes = {}
            for p in node['properties']:
                attributes[p['name']] = row[column_index[p['column_id']]]
            return attributes
        return node["attributes"]

# get existing node

    def get_node(self, attributes, label):
        try:
            node = self.neo4j_conn.get_nodes_by_label_attributes(
                attributes, label, True)
            return node
        except Exception as exception:
            print('Error getting node {}'.format(attributes))
            print('Exceptaion details: {}'.format(exception))
            traceback.print_exc()

    def get_stat_by_node_label(self):
        exclude_labels = []
        results = self.neo4j_conn.get_node_types()
        nodeTypeCount = {}
        for result in results:
            nodeType = result['nodeType'][0]
            if nodeType not in exclude_labels:
                nodeTypeCount[nodeType] = self.neo4j_conn.count_nodes_by_type(
                    nodeType)
        return nodeTypeCount

    def get_stat_by_node_granularity(self, nodeType=None):
        nodeGranularityCount = {}
        node_property = 'type'
        values = ['class', 'instance']

        for value in values:
            if nodeType != 'all':
                nodeGranularityCount[
                    value] = self.neo4j_conn.get_count_by_type_attribute_value(
                        nodeType, node_property, value)
            else:
                nodeGranularityCount[
                    value] = self.neo4j_conn.get_count_by_type_attribute_value(
                            None, node_property, value)
        return nodeGranularityCount

    def get_children_stat_by_node_type(self, nodeType=None):
        if nodeType == 'all':
            return self.get_stat_by_node_label()

        source_label = nodeType
        source_filter = 'type'
        source_filter_value = 'class'

        dest_label = nodeType
        dest_filter = 'type'
        dest_filter_value = 'instance'

        relation = 'specialization'

        return_node_type = 'source'
        count_node_type = 'dest'

        results = self.neo4j_conn.get_nodes_by_relation_and_type(
            source_label, source_filter, source_filter_value, dest_label,
            dest_filter, dest_filter_value, relation, return_node_type,
            count_node_type)

        compiled_results = {}

        key = 'src' if return_node_type == 'source' else 'dest'

        for result in results:
            compiled_results[result[key]['title']] = result['node_count'] + 1
        return dict(sorted(compiled_results.items(), key=lambda item: item[1]))

    def relation_count(self):
        results = self.neo4j_conn.get_per_relation_count()

        relation_dist = {}

        for result in results:
            relation_dist[result['relation']] = result['count']
        return dict(sorted(relation_dist.items(), key=lambda item: item[1]))

    def get_node_degree_distributions(self, nodeType):
        results_in = self.neo4j_conn.get_node_degree_distribution(nodeType, 'in')
        results_out = self.neo4j_conn.get_node_degree_distribution(nodeType, 'out')
        relation_dist = {}

        temp_dict = {}
        for result in results_in:
            temp_dict[result['relation']] = result['count']

        in_ls = sorted(temp_dict.items(), key=lambda item: item[1])

        temp_dict = {}
        for result in results_out:
            temp_dict[result['relation']] = result['count']

        out_ls = sorted(temp_dict.items(), key=lambda item: item[1])

        for k,v in in_ls:
            relation_dist[k] = {'count':v, 'type':'in'}
        for k,v in out_ls:
            relation_dist[k] = {'count':v, 'type':'out'}
        return relation_dist

    def is_skippable(self, res, exclude_labels, include_labels):
        label_a = res['key']
        if include_labels is not None and label_a not in include_labels:
            return True
        if label_a in exclude_labels:
            return True
        if res['value']["type"] == 'relationship':
            return True
        return False

    def get_graph_edge_list(self,
                            include_labels=None):
        query = ('call apoc.meta.schema() ' + 'YIELD value ' +
                 'UNWIND keys(value) AS key ' +
                 'RETURN key, value[key] AS value')
        results = self.neo4j_conn.run_query_kh(query)
        relation_dict = {}
        result_list = json.loads(results)
        exclude_labels = []
        
        for res in result_list:
            if self.is_skippable(res, exclude_labels, include_labels):
                continue
            label_a = res['key']
            relationships = res['value']['relationships']
            for relation, properties in relationships.items():
                direction = properties['direction']
                labels = properties['labels']
                for label_b in labels:
                    if label_b in exclude_labels:
                        continue
                    if include_labels and label_b not in include_labels:
                        continue
                    if 'out' in direction:
                        key = (label_a, label_b, relation)
                        if key not in relation_dict:
                            relation_dict[key] = 1
                    else:
                        key = (label_b, label_a, relation)
                        if key not in relation_dict:
                            relation_dict[key] = 1
        edge_list = []
        for key, value in relation_dict.items():
            source, target, _type = key
            weight = value
            edge_list.append({
                "source": source,
                "target": target,
                "weight": value,
                "label": _type
            })
        return edge_list

    def get_node_neighborhood_schema(self, node_label, 
        node_property, node_property_value):
        query = ('MATCH (n:' + node_label + '{' + node_property + ':"' + 
                  node_property_value + '"})' +
                 'CALL apoc.path.spanningTree(n, {' +
                 'relationshipFilter: "< | >",' +
                 'minLevel: 1,' +
                 'maxLevel: 1 })' +
                 'YIELD path' + 
                 'RETURN path')
        results = self.neo4j_conn.run_query_kh(query)
        relation_dict = {}
        result_list = json.loads(results)

        edge_list = []
        for res in result_list:
            source = res['path']['start'][node_property]
            target = res['path']['end'][node_property]
            relationship_name = res['path']['segments'][0]['relationship']['type']
            edge_list.append({
                "source": source,
                "target": target,
                "weight": 1,
                "label": relationship_name
            })
        return edge_list

    def get_relation_neighborhood_schema(self, node_label, node_property, 
        node_property_value, relationship_name, direction):
        if direction == 'in':
            relation_param = "<" + relationship_name
        else:
            relation_param = relationship_name + ">"

        query = ('MATCH (n:' + node_label + '{' + node_property + ':"' + 
                  node_property_value + '"})' +
                 'CALL apoc.neighbors.athop(n, "' + relation_param + '", 1)' +
                 'YIELD node ' +
                 'RETURN node')
        results = self.neo4j_conn.run_query_kh(query)
        relation_dict = {}
        result_list = json.loads(results)

        edge_list = []
        for res in result_list:
            source = node_property_value
            target = res['node'][node_property]
            edge_list.append({
                "source": source,
                "target": target,
                "weight": 1,
                "label": relationship_name
            })
        return edge_list