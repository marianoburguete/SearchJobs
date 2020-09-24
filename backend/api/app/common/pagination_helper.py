from flask import make_response, jsonify

def makePagResponse(pagination, schema):
    items =  schema.dump(pagination.items, many=True)
    result = {
        'results': items,
        'currentPage': pagination.page,
        'totalPages': pagination.pages,
        'per_page': pagination.per_page,
        'totalResults': pagination.total,
        'previousPage': pagination.prev_num,
        'nextPage': pagination.next_num
    }
    return make_response(jsonify(result), 200)