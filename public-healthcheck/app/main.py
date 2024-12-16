from flask import Flask, jsonify
from kubernetes import client, config

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def cluster_health():
    try:
        # Load in-cluster or kubeconfig settings
        config.load_incluster_config()  # When running inside the cluster
        v1 = client.CoreV1Api()

        # Query health of nodes
        nodes = v1.list_node()
        health_status = {"nodes": []}
        for node in nodes.items:
            health_status["nodes"].append({
                "name": node.metadata.name,
                "status": node.status.conditions[-1].type
            })
        return jsonify({"status": "healthy", "details": health_status}), 200
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

