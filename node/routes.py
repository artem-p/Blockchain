from flask import Flask, jsonify, request
from node import app, blockchain, node_identifier


@app.route('/mine', methods=['GET'])
def mine():
    # run proof of work algorithm to get the next proof
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    
    # add new block to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    # we should receive a reward for finding the proof.
    # The sender is "0" to signify that this node has mined a new block.

    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )

    response = {
        'message': 'New Block Forged',
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }

    return jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    requeireds = ['sender', 'recipient', 'amount']

    if not all(value in values for value in requeireds):
        return 'Missing values', 400

    transaction_index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': f'Transaction will be added to Block {transaction_index}'}
    return jsonify(response), 201

    return "We'll add a new transaction"


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200