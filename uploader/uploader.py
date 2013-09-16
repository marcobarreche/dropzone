from flask import Flask, render_template, Response
import sys
import datetime
import json
import base64
import hashlib
import hmac


app = Flask(__name__)
app.config.from_object(__name__)
AWS_SECRET_KEY = '...'
BUCKET_NAME = 'barreche-tb';
BUCKET_RESOURCE_FOLDER = 'test/';


@app.route('/')
def init():
    return render_template('uploader.html')


@app.route('/get-policy-and-signature')
def get_policy_and_signature():
    """
    It returns the policy and the signature to s3.
    Returns:
        (str): It returns the list [policy, signature] in a json string. 
    """
    # The secret key is AWS_SECRET_KEY by default.
    secret_key = AWS_SECRET_KEY

    # The expiration date is one year later.
    expiration_date = datetime.datetime.now() + datetime.timedelta(days=365)
    policy_document = {
        "expiration": expiration_date.strftime('%Y-%m-%dT00:00:00Z'),
        "conditions": [
            {"bucket": BUCKET_NAME},
            ["starts-with", "$key", BUCKET_RESOURCE_FOLDER],
            {"acl": "public-read"},
            ["starts-with", "$Content-Type", ""],
            ["content-length-range", 0, 1048576]
        ]
    }
    policy = base64.b64encode(json.dumps(policy_document))
    signature = base64.b64encode(hmac.new(secret_key, policy, hashlib.sha1).digest())
    return Response(json.dumps([policy, signature]), status=200)


if __name__ == '__main__':
    ip, port = sys.argv[1].split(':')
    app.run(host=ip, port=int(port), debug=False)
