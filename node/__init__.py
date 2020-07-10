# instantiate the node
from flask import Flask
from uuid import uuid4
from blockchain import Blockchain

app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()

from node import routes