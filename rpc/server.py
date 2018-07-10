import tushare as ts
from waitress import serve
from werkzeug.wrappers import Request, Response
from jsonrpc import JSONRPCResponseManager, dispatcher


@dispatcher.add_method
def get_k_data(code, start="2016-01-01", end="2018-07-01", ktype='D', autype='qfq', index=False):
    data = ts.get_k_data(code, start, end, ktype, autype, index)
    del data['code']
    return data.to_json(orient="records")


@Request.application
def application(request):

    response = JSONRPCResponseManager.handle(
        request.data, dispatcher)
    return Response(response.json, mimetype='application/json')


if __name__ == '__main__':
    serve(application, listen='*:4000')
