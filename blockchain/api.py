from uuid import uuid4

from flask import Flask, jsonify, request

from blockchain import Blockchain

app = Flask(__name__)
node_id = str(uuid4()).replace("-", "")
blockchain = Blockchain()


@app.route("/mine", methods=["GET"])
def mine():
    last_block = blockchain.last_block
    last_proof = last_block["proof"]
    proof = blockchain.mine(last_proof)

    blockchain.add_transaction(sender="0", recipient=node_id, amount=1)  # means this node has mined a new coin

    previous_hash = blockchain.generate_hash(last_block)
    block = blockchain.add_block(proof, previous_hash)

    response = {
        "message": "New Block Forged",
        "index": block["index"],
        "transactions": block["transactions"],
        "proof": block["proof"],
        "previous_hash": block["previous_hash"],
    }

    return jsonify(response), 200


@app.route("/transaction/new", methods=["POST"])
def transaction_new():
    values = request.get_json()

    required = ["sender", "recipient", "amount"]
    if not all(k in values for k in required):
        return "Missing values", 400

    index = blockchain.add_transaction(values["sender"], values["recipient"], values["amount"])
    response = {"message": f"Transaction will be added to Block {index}"}
    return jsonify(response), 201


@app.route("/chain", methods=["GET"])
def chain():
    response = {"chain": blockchain.chain, "length": len(blockchain.chain)}
    return jsonify(response), 200


@app.route("/nodes/register", methods=["POST"])
def register_nodes():
    nodes = request.get_json().get("nodes")

    if not nodes:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {"message": "New nodes have been added", "total_nodes": list(blockchain.nodes)}

    return jsonify(response), 201


@app.route("/nodes/resolve", methods=["GET"])
def consensus():
    replaced = blockchain.resolve_conflicts()

    msg = "Our chain was replaced" if replaced else "Our chain is authoritative"

    response = {"message": msg, "chain": blockchain.chain}

    return jsonify(response), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
