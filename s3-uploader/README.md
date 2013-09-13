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
         &lt;AllowedOrigin&bt*&lt;/AllowedOrigin&gt;
         &lt;AllowedMethod&btGET&lt;/AllowedMethod&gt;
         &lt;AllowedMethod&btPOST&lt;/AllowedMethod&gt;
         &lt;MaxAgeSeconds&bt3000&lt;/MaxAgeSeconds&gt;
         &lt;AllowedHeader&bt*&lt;/AllowedHeader&gt;
     &lt;/CORSRule&gt;
 &lt;/CORSConfiguration&gt;
	</code>
</pre>

3. Now we have to select or create a folder where all resources will be uploaded by our users.
   Once we have choosen the folder, click on "ACTIONS" and then in "MAKE PUBLIC".
   Now, everybody is able to access to the contents of the folder.

4. Now we need to create a user with several grants to access to our bucket, upload a image, eliminate it,
   list all the contents of a folder, etc. To do this we must go click on "SECURITY CREDENTIALS", and later in "GROUPS". We click on "CREATE NEW GROUP". We give it a name and link it the next policy:

<pre>
	<code>
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "s3:CreateBucket",
        "s3:GetObject",
        "s3:ListAllMyBuckets",
        "s3:ListBucket",
        "s3:PutBucketPolicy",
        "s3:PutObject"
      ],
      "Sid": "Stmt1379078059000",
      "Resource": [
        "arn:aws:s3:::$&l;bucket-name&gt;/&l;folder-path&g;/*"
      ],
      "Effect": "Allow"
    }
  ]
}
	</code>
</pre>

(*) Note: The users in this group can do all the actions listed in "ACTION" on the Resource:
  arn:aws:s3:::$&l;bucket-name&gt;/&l;folder-path&g;/*

5. Now, we create a user, name it and associate it to the previous group.



### Instructions to use our uploader
1. We have to install the uploader app.
  $ ./install.sh

2. Execute the uploader app
  $ python uploader.py <IP>:<PORT>

