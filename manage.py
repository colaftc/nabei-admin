import os
from app import create_app
from flask import request,jsonify,Response
from flask_script import Manager

app=create_app(os.getenv('FLASK_CONFIG') or 'debug')

@app.errorhandler(404)
def page_not_found(e):
    if request.accept_mimetypes.accept_json and \
       not request.accept_mimetypes.accept_html:

        app.logger.warn('an json client accept and 404')
        response=jsonify({'error':'object not found'})
        response.status_code=404
        return response

    else:
        app.logger.warn('an html client accept and 404')
        return "<html><body><h1>Sorry , Object Not Found</h1></body></html>",404

#@app.before_request()
#def app_before_request():
    #pass

@app.route('/testing_running')
def testing_running():
    if not app.config['TESTING']:
        return jsonify({'error':'not in testing'}),500
    else:
        return Response('TESTING...'),201


if __name__ == '__main__':
    app.run()
