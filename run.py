import boto3
import os
import dotenv
from botocore.exceptions import ClientError
from flask import Flask, render_template, request

app = Flask(__name__)

# def get_user_policies(iam_username):
#     # Replace 'your_access_key' and 'your_secret_key' with your AWS access key and secret key
#     aws_access_key = 'AKIAUSW6SE2F2VSFRCN6'
#     aws_secret_key = 'cpXUgKeUAUZXHn9/3olhaE4iSbVfJUFmNspj3Kz3'
dotenv.load_dotenv()

def get_user_policies(iam_username):
    aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')

    if aws_access_key is None or aws_secret_key is None:
        return ["Error: AWS credentials not provided in environment variables."]

    try:
        # Create an IAM client with the specified AWS region
        client = boto3.client('iam', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)

        # Get the user's policy list
        response = client.list_attached_user_policies(UserName=iam_username)

        # Extract attached policy names
        attached_policies = []
        if 'AttachedPolicies' in response:
            attached_policies = [policy['PolicyName'] for policy in response['AttachedPolicies']]
        return attached_policies
    except ClientError as e:
        return [str(e)]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        iam_username = request.form['username']
#        aws_region = request.form['region']
        attached_policies = get_user_policies(iam_username)
        return render_template('index.html', iam_username=iam_username, policies=attached_policies)
    return render_template('index.html', iam_username='', policies=[])

if __name__ == '__main__':
    app.run(debug=True)