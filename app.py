from flask import Flask, jsonify, abort, request
from TransactionOrganizer import Transactions, DBhandler, TransactionManager

app = Flask(__name__)

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
#@app.route("/api/v1/transactions/<int:month>")
TRANSPATH = "/".join([APIPREFIX, TRANSPREFIX])
@app.route("/".join(TRANSPATH, "<int:month>"))
def getTransactions(month):
    if month < 1 or month > 12:
        abort(404, "Month values must be between 1 and 12") 
    try:
        transactions = TransactionManager.getTransactions(month - 1)
    except Exception:
        abort(404)
    if not transactions:
        abort(500) 
    return jsonify(status="OK", incoming=transactions.incoming, outgoing=transactions.outgoing)

#@app.route("/api/v1/transactions/<int:month>/incoming")
@app.route("/".join([TRANSPATH, "<int:month>", "incoming"]))
def getIncoming(month):
    if month < 1 or month > 12:
        abort(404, "Month values must be between 1 and 12") 
    transactions = TransactionManager.getTransactions(month - 1)
    if not transactions:
        abort(500) 
    return jsonify(status="OK", outgoing=transactions.incoming)

@app.route("/".join([TRANSPATH, "<int:month>", "outgoing"]))
def getOutgoing(month):
    if month < 1 or month > 12:
        abort(404, "Month values must be between 1 and 12") 
    transactions = TransactionManager.getTransactions(month - 1)
    if not transactions:
        abort(500) 
    return jsonify(status="OK", outgoing=transactions.outgoing)

@app.route("/".join([TRANSPATH, "<int:month>", "outgoing", "categorized"]))
def getCat(month):
    if month < 1 or month > 12:
        abort(404, "Month values must be between 1 and 12") 
    transactions = TransactionManager.getTransactions(month - 1)
    if not transactions:
        abort(500) 
    return jsonify(status="OK", data=transactions.outgoing_cat)


#! categories API
CATPATH = "/".join([APIPATH, CATPREFIX])

def DBinteracter(data, operation):
    catNames = DBhandler.getCategoryNames()
    response = {}
    for key, val in data.items():
        if key in catNames:
            if type(val) == list:
                for item in val:
                    operation(key, item)
            else:
                    operation(key, val)
            response[key] = "OK"
        else:
            response[key] = "NOK"
    return jsonify(status="OK", res=response)

@app.route(CATPATH, methods=['GET'])
def get_categories():
    categories = DBhandler.getCategories()
    return jsonify(status="OK", categories=categories)

@app.route(CATPATH, methods=['POST'])
def add_category_item():
    data = request.json
    if not data:
        abort(404, "No data in request body")
    return DBinteracter(data, DBhandler.addToCategory)

@app.route(CATPATH, methods=['DELETE'])
def remove_category_item():
    data = request.json
    if not data:
        abort(404, "No data in request body")
    return DBinteracter(data, DBhandler.delFromCategory)

@app.route("/".join([CATPATH, "names"]))
def get_category_names():
    categories = DBhandler.getCategoryNames()
    return jsonify(status="OK", names=categories)

if __name__ == "__main__":
    app.run("localhost", 5000)