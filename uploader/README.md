s3 uploader
==========

### Configurate our amazon s3 bucket
1. We have to go to our amazon s3 bucket.
2. Then we must click on "PERMISSIONS" and then in "EDIT CORS CONFIGURATION" and edit the next below:

<pre>
	<code>
 &lt;?xml version="1.0" encoding="UTF-8"?&gt;
 &lt;CORSConfiguration xmlns="http://s3.amazonaws.com/doc/2006-03-01/"&gt;
     &lt;CORSRule&gt;
         &lt;AllowedOrigin&gt;*&lt;/AllowedOrigin&gt;
         &lt;AllowedMethod&gt;GET&lt;/AllowedMethod&gt;
         &lt;AllowedMethod&gt;POST&lt;/AllowedMethod&gt;
         &lt;MaxAgeSeconds&gt;3000&lt;/MaxAgeSeconds&gt;
         &lt;AllowedHeader&gt;*&lt;/AllowedHeader&gt;
     &lt;/CORSRule&gt;
 &lt;/CORSConfiguration&gt;
	</code>
</pre>

3. Now we have to select (or create) a folder in our bucket where all resources will be uploaded by our users.
   Once we have choosen the folder, we click on "ACTIONS" and then in "MAKE PUBLIC".
   Now, everybody is able to access to the contents of the folder.

4. Now we need to create a user with several grants: List all files of the bucket and access
   to the properties of each one, create a user, delete a user and generate a policy to a user.
   To do this we must go click on "SECURITY CREDENTIALS", and later in "Users".
   We click on "CREATE NEW USER". We give it a name and link it the next policy:

<pre>
	<code>
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "s3:*"
      ],
      "Sid": "Stmt1379078059000",
      "Resource": [
        "arn:aws:s3:::bucket-name/*"
      ],
      "Effect": "Allow"
    }
  ]
}
	</code>
</pre>


Dropbox uploader
==========
### Configurate our DROPBOX FOLDER
1. First you have to create an app. To do this, go to https://www.dropbox.com/developers/apps. Click on "CREATE APP".
2. Select: DROPBOX API APP -> FILES AND DATASTORES -> NO -> ALL THE TYPES. Write a name and press on CREATE APP.
3. In Oauth Redirect URIs, add this url: https://thumbr.io/create/dropbox/access_token.
4. Write app key and app secret in https://thumbr.io/profile/dropbox.



The JAVASCRIPT API
=====================

### 1. Constructor:
UploaderThumbrio :: UploaderThumbrio(options)
    options is a dictionary with these options:
        1. url: (str) Optional. It is the URL of our uploader.
                                Default value: https://{{ bucket_name }}.s3.amazonaws.com
        2. dropzoneClass: (str) Optional. It is the class of the uploader. Default value: '.dropzone'
        3. maxFileSize: (int) Optional. It is the maximum size of a file expressed in MB. Default value: 10
        4. acceptedFiles: (str) Optional. The accepted files to upload. Example: images/* if you only want
                                          to upload images. Default value: null.
        5. maxFiles: (int) Optional. It is the maximum number of files you can upload. Default value: null.
        6. addRemoveLinks: (bool) Optional. True if you want a button in the thumbnail to remove it. Default
                                            value: true.


### 2. Methods:
void  setApiKey(apiKey):
    Set the api key of the user and upload the values of the variable 'serviceOptions'.
    Arguments:
        apiKey (str): The api key of thumbrio of the user.


void storeRemote(fileOptions, serviceOptions):
    Set the fileOptions and serviceOptions variable and upload the value of 'policy' and 'signature'.
    
    Arguments:    
        fileOptions (Dict<str, T>) The restrictions of the file. The keys are these:
            1. public (str): Optional. We specify if the file will be public or private  (default: public-read).
                             The possible values are listed in
                             http://docs.aws.amazon.com/AmazonS3/latest/dev/ACLOverview.html#SampleAcl.
            2. contentType (str | List<str>): Optional. We specify the contentType of the files (default: null).
            3. maxSize (int): Optional. Optional. Maximum size of the uploaded file in bytes (default: 10MB).
            4. minSize (int): Optional. We specify the minimum number of bytes the file can get (default: 0).
            5. onSuccessUpload (function()): Optional. The function well be called when we were success
                                                       uploading a file (default null).
            6. onErrorUpload (function()): Optional. The function will be called when we get an error
                                                     uploading a file (default null).
        serviceOptions (Dict<str, str>) The settings of the repository s3. The keys are these:
            1. signature (str): The signature to upload a file
            2. policy (str): The policy to upload a file.
            3. service (str): The type of service. The possible values are: 'S3' or 'DROPBOX'. (default: S3).
            4. expirationDate (str): (Only in dropbox) The date must have this format: YYYY-MM-DD<T>HH:MM:SS<Z>.
                    For example: 2013-01-22T23:50:40Z. This date must be the same that the date specified in policy.
                    (default: current date plus one hour).
            5. bucketName (str): Optional. (Only in s3) The bucket name. This parameter is only important when we are using the service S3.
            6. path (str): Optional. The path of the user. It must start and end by '/'.
                           For example: '/one/two/', or '/'.
            7. publicKey (str): Optional. The public key it is the awsAccessKey of s3 or the appAccessKey of dropbox.
           
    (*) Note1: if you call to the function 'setApiKey' with a correct apiKey, the options "path", "publicKey", and
               "bucketName" will take the values you specify in your thumbrio settings.
    (*) Note2: If you are using dropbox, the parameters "public" and "bucketName" will be pointless. If you want upload your
                files in a public place, the "path" must start by /public/.
    (*) Note3: If you are using s3, "expirationDate" will be pointless.
  

void deleteFile(filename, authorization, date) 
    Delete a file from bucket
    Arguments:
        filename (str): It is the name of the filename.
        authorization (str): It is a string that authorizes someone to commit the action. The method
                             generateAuthorization creates this authorization.
        date (Date): This is the date you use to create the string 'authorization'.


URLS API
=====================
### 1. http://thumbr.io/get/service_settings
Get the public key, the resource path and the bucket name of a user.

METHOD:
    GET

Data:
    api_key: api of thumbrit.
    service: s3 or dropbox.

Returns:
    A list: [public_key, resource_path, bucket_name]

=================================================================
### 2. http://thumbr.io/get/thumbrio_thumbnail_url
Get the url of the thumbnail of a file which is uploaded in s3 or dropbox.

METHOD:
    GET

Data:
    api_key: api of thumbrit.
    filename: the absolute path to the filename.
    width: the width of the thumbnail.
    height: the height of the thumbnail.
    service: s3 or dropbox.

Returns:
    The url of the thumbnail

=================================================================    
### 3. http://thumbr.io/upload/dropbox/file
Upload a file to dropbox

METHOD:
    POST

Data:
    api_key: api key of thumbrit.
    key: absolute path of the file.
    file: The file.
    file_options: json of file_options
    service_options: json of service_options

=================================================================
### 4. http://thumbr.io/delete/dropbox/file
Delete a file to dropbox

METHOD:
    POST

Data:
    api_key: api key of thumbrit.
    remote_filename: absolute path of the file.
    expiration_date: expiration date.
    authorization: authorization.


### Instructions to use our uploader

1. We have to install the uploader app.
  $ ./install.sh

2. Execute the uploader app
  $ python uploader.py IP:PORT

