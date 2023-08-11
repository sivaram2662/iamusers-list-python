from flask import Flask, render_template, request
import boto3

app = Flask(__name__,template_folder='templates' )

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        aws_username = request.form.get('aws_username')
        # Use Boto3 to get the permissions associated with the provided AWS username
        permissions = get_aws_user_permissions(aws_username)
        return render_template('index.html', permissions=permissions)
    return render_template('index.html')

def get_aws_user_permissions(username):
    # Use Boto3 to interact with AWS and retrieve user permissions
    # You need to implement this function based on your requirements
    pass

if __name__ == '__main__':
    app.run(debug=True)
