from flask import Flask, jsonify, abort, request
from Utils.TransactionOrganizer import Transactions, DBhandler, TransactionManager
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

APIPREFIX = "/api"
VERSION = "v1"
TRANSPREFIX = "transactions"
CATPREFIX = "categories"

APIPATH = "/".join([APIPREFIX, VERSION])

#! API
@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

@app.errorhandler(500)
def internal_server_error(e="Internal server error"):
    return jsonify(error=str(e)), 500

@app.route("/")
def hello_world():
    return f"<p>Hello world {TransactionManager.logRequest()}</p>"

@app.route("/api/v1")
def status_kek():
    return f"<p>Hello api {TransactionManager.logRequest()}</p>"

#! Transactions API
#* Helper functions
def getTransactions(month: int):
    try: 
        return TransactionManager.getTransactions(month - 1)
    except Exception as e:
        #print(e)
        abort(404, "Data for this month does not exist")

def handleRequest(month: int, dataType: str):
    if month < 1 or month > 12:
        abort(404, "Month values must be between 1 and 12") 

    transactions = getTransactions(month)

    if not transactions: 
        abort(500)
    
    if dataType == "ALL":
        data = {
            "incoming": transactions.incoming,
            "outgoing": transactions.outgoing
        }
    elif dataType == "outgoing": data = transactions.outgoing
    elif dataType == "incoming": data = transactions.incoming
    elif dataType == "outgoing_cat": data = transactions.outgoing_cat
    #else: raise ValueError("Incorrect data type")
    else: abort(500)

    return jsonify(status="OK", data=data)

#* Routes
@app.route("/api/v1/transactions/<int:month>")
def transactions(month):
    return handleRequest(month, "ALL")

#@app.route("/api/v1/transactions/<int:month>/incoming")
@app.route("/api/v1/transactions/<int:month>/incoming")
def transactions_incoming(month):
    return handleRequest(month, "incoming")

@app.route("/api/v1/transactions/<int:month>/outgoing")
def transactions_outgoing(month):
    return handleRequest(month, "outgoing")

@app.route("/api/v1/transactions/<int:month>/outgoing/categorized")
def transactions_outgoing_categorized(month):
    return handleRequest(month, "outgoing_cat")

#! categories API
#* Helper functions
def handleDBreq(data, operation):
    catNames = DBhandler.getCategoryNames()
    response = {}
    for key, val in data.items():
        try:
            if type(val) == list:
                for item in val:
                    operation(key, item)
            else:
                    operation(key, val)
            response[key] = "OK"
        except Exception:
            response[key] = "NOK"
    return jsonify(status="OK", res=response)

#* Routes
@app.route("/api/v1/categories", methods=['GET'])
def get_categories():
    categories = DBhandler.getCategories()
    return jsonify(status="OK", categories=categories)

@app.route("/api/v1/categories", methods=['POST'])
def add_category_item():
    data = request.json
    if not data:
        abort(404, "No data in request body")
    return handleDBreq(data, DBhandler.addToCategory)

@app.route("/api/v1/categories", methods=['DELETE'])
def remove_category_item():
    data = request.json
    if not data:
        abort(404, "No data in request body")
    return handleDBreq(data, DBhandler.delFromCategory)

@app.route("/api/v1/categories/<catName>/delete", methods=['DELETE'])
def remove_category(catName):
    result = DBhandler.dropCategory(catName)
    #FIXME: DBhandler.dropCategory() always returns None regardless of whether or not the collection was deleted.
    return jsonify(status="OK")


@app.route("/api/v1/categories/names")
def get_category_names():
    categories = DBhandler.getCategoryNames()
    return jsonify(status="OK", names=categories)

if __name__ == "__main__":
    app.run("localhost", 5000)
