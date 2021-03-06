from flask import Flask, jsonify, abort, request, send_from_directory
from Utils.TransactionOrganizer import Transactions, DBhandler, TransactionManager
from flask_cors import CORS
from flasgger import Swagger 
import os

app = Flask(__name__)
Swagger(app)
CORS(app)

#! API
@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

@app.errorhandler(500)
def internal_server_error(e="Internal server error"):
    return jsonify(error=str(e)), 500

@app.route('/<path:path>', methods=['GET'])
def static_proxy(path):
    return send_from_directory(os.environ.get('DIST_PATH'), path)

@app.route("/")
def hello_world():
    """
    serve website
    """
    return send_from_directory(os.environ.get('DIST_PATH'), 'index.html')


@app.route("/health")
def healthCheck():
    return "<h2>I am online</h2>"

#! Transactions API
#* Helper functions
def getTransactions(year: int, month: int) -> Transactions:
    try: 
        return TransactionManager.getTransactions(year, month)
    except Exception as e:
        abort(404, "Data for this month does not exist")

def handleRequest(year: int, month: int, dataType: str):
    if month < 1 or month > 12:
        abort(404, "Month values must be between 1 and 12") 

    try:
        transactions = getTransactions(year, month)
    except Exception as e:
        print(e)
        abort(500, "Internal error getting transactions for month")

    if not transactions: 
        abort(500, "Internal error getting translactions for month")
    
    if dataType == "ALL":
        data = {
            "incoming": transactions.incoming,
            "outgoing": transactions.outgoing
        }
    elif dataType == "outgoing": data = transactions.outgoing
    elif dataType == "incoming": data = transactions.incoming
    elif dataType == "outgoing_cat": data = transactions.outgoing_cat
    else: abort(500)

    return jsonify(status="OK", data=data)

#* Routes
@app.route("/api/v1/transactions/<int:year>/<int:month>")
def transactions(year, month):
    """
    Get incoming and outgoing transactios for selected month
    ---
    tags:
        - transactions
        - incoming
        - outgoing
    parameters:
        - name: month
          in: path
          required: true
          type: integer 
    responses:
        200:
            description: transactions for selected month have been returned successfully
        404:
            description: A wrong month has been selected (month values must be between 1 and 12) or data for this month does not exist
        500:
            description: Internal sevver error retreiving transactions
    """
    return handleRequest(year, month, "ALL")

#@app.route("/api/v1/transactions/<int:month>/incoming")
@app.route("/api/v1/transactions/<int:year>/<int:month>/incoming")
def transactions_incoming(year, month):
    """
    Get incoming transactions
    ---
    tags:
        - transactions
        - incoming
    parameters:
        - name: month
          in: path
          required: true
          type: integer 
    responses:
        200:
            description: incoming transactions for selected month have been returned successfully
        404:
            description: A wrong month has been selected (month values must be between 1 and 12) or data for this month does not exist
        500:
            description: Internal sevver error retreiving transactions
    """
    return handleRequest(year, month, "incoming")

@app.route("/api/v1/transactions/<int:year>/<int:month>/outgoing")
def transactions_outgoing(year, month):
    """
    Get outgoing transactions
    ---
    tags:
        - transactions
        - outgoing
    parameters:
        - name: month
          in: path
          required: true
          type: integer 
    responses:
        200:
            description: outgoing transactions for selected month have been returned successfully
        404:
            description: A wrong month has been selected (month values must be between 1 and 12) or data for this month does not exist
        500:
            description: Internal sevver error retreiving transactions
    """
    return handleRequest(year, month, "outgoing")

@app.route("/api/v1/transactions/<int:year>/<int:month>/outgoing/categorized")
def transactions_outgoing_categorized(year, month):
    """
    Get categorized outgoing transactions
    ---
    tags:
        - transactions
        - incoming
        - categorized
    parameters:
        - name: month
          in: path
          required: true
          type: integer 
    responses:
        200:
            description: outgoing transactions grouped together by categories
        404:
            description: A wrong month has been selected (month values must be between 1 and 12) or data for this month does not exist
        500:
            description: Internal sevver error retreiving transactions
    """
    return handleRequest(year, month, "outgoing_cat")

#! categories API
#* Helper functions
def handleDBreq(data, operation):
    response = {}
    for key, val in data.items():
        try:
            if type(val) == list:
                for item in val:
                    if item == "other":
                        continue
                    operation(key, item)
            else:
                if not val == "other":
                    operation(key, val)
            response[key] = "OK"
        except Exception:
            response[key] = "NOK"
    return jsonify(status="OK", data=response)

#* Routes
@app.route("/api/v1/categories", methods=['GET'])
def get_categories():
    """
    get category names along with their regex values
    ---
    tags:
        - categories
    responses:
        200:
            description: json body of categories
        500:
            description: Internal sevver error
    """
    categories = DBhandler.getCategories()
    return jsonify(status="OK", data=categories)

@app.route("/api/v1/categories", methods=['POST'])
def add_category_item():
    """
    add a new item to a category
    ---
    tags:
        - categories
    responses:
        200:
            description: item aded successfully
        404:
            description: no data in body request
        500:
            description: Internal sevver error
    """
    data = request.json
    if not data:
        abort(404, "No data in request body")
    return handleDBreq(data, DBhandler.addToCategory)

@app.route("/api/v1/categories", methods=['PUT'])
def change_item_category():
    """
    move item from one category to another
    ---
    tags:
        - categories
    responses:
        200:
            description: item moved to a different category successfully
        404:
            description: no data in body request
        500:
            description: Interval server error 
    """
    data = request.json
    #FIXME: these should not be 404!
    # ^ suck my left nut, past me. I'm not fixing shit!
    if not data:
        abort(404, "No data in request body")
    #return handleDBreq(data, DBhandler.addToCategory)
    if not data.get("currentCategory"):
        abort(404, "currentCategory field not in data")

    if not data.get("newCategory"):
        abort(404, "newCategory field not in data")

    if not data.get("name"):
        abort(404, "name field not in data")

    delPayload = {
        data.get("currentCategory"): data.get("name")
    }

    addPayload = {
        data.get("newCategory"): data.get("name")
    }

    with DBhandler._db.client.start_session() as session:

        try:
            if not data.get("currentCategory") == "other":
                removal = handleDBreq(delPayload, DBhandler.delFromCategory)

            if not data.get("newCategory") == "other":
                addition = handleDBreq(addPayload, DBhandler.addToCategory)

        except Exception:
            if 'removal' in locals():
                handleDBreq(delPayload, DBhandler.addToCategory)
            if 'addition' in locals():
                handleDBreq(addPayload, DBhandler.delFromCategory)

    return jsonify(status="OK", data=data)

@app.route("/api/v1/categories", methods=['DELETE'])
def remove_category_item():
    """
    remove item from category
    ---
    tags:
        - categories
    responses:
        200:
            description: item successfully deleted from category
        404:
            description: no data in body request
        500:
            description: Internal sevver error
    """
    data = request.json
    if not data:
        abort(404, "No data in request body")
    return handleDBreq(data, DBhandler.delFromCategory)

@app.route("/api/v1/categories/<catName>/delete", methods=['DELETE'])
def remove_category(catName):
    """
    remove category
    ---
    tags:
        - categories
    parameters:
        - name: category
          in: path
          required: true
          type: string
    responses:
        204:
            descrption: category successfully deleted
        404:
            description: category does not exist
        500:
            description: Internal sevver error
    """
    result = DBhandler.dropCategory(catName)
    if not result.get("ok"):
        if result.get("errmsg") == 'ns not found':
            abort(404, "Category does not exist")
        else:
            abort(500)
    return '', 204


@app.route("/api/v1/categories/names")
def get_category_names():
    """
    retreive category names, without items
    ---
    tags:
        - categories
    responses:
        200:
            description: get category names
        404:
            description: category does not exist
        500:
            description: Internal sevver error
    """
    categories = DBhandler.getCategoryNames()
    return jsonify(status="OK", data=categories)

if __name__ == "__main__":
    app.run(host="localhost", port=8000)