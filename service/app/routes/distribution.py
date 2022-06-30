from flask import jsonify, make_response, g
from app.flask_app import app


@app.get('/distributions/<type>')
def get_distribution(type: str):
    if type == 'node':
        result = g.profile.get_node_distribution()
        return make_response(jsonify(result), 200)
    if type == 'relation':
        result = g.profile.get_relation_distribution()
        return make_response(jsonify(result), 200)

@app.get('/granularity_distributions/<nodetype>')
def get_node_granularity_distributions(nodetype: str):
    result = g.profile.get_node_granularity_distributions(nodetype)
    return make_response(jsonify(result), 200)