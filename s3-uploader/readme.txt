1. Ir a la página donde está nuestro bucket "barreche-tb"
2. Hacemos click en "PERMISSIONS" y luego en "EDIT CORS CONFIGURATION y escribimos lo siguiente:

<?xml version="1.0" encoding="UTF-8"?>
<CORSConfiguration xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
    <CORSRule>
        <AllowedOrigin>*</AllowedOrigin>
        <AllowedMethod>GET</AllowedMethod>
        <AllowedMethod>POST</AllowedMethod>
        <MaxAgeSeconds>3000</MaxAgeSeconds>
        <AllowedHeader>*</AllowedHeader>
    </CORSRule>
</CORSConfiguration>

(*) Nota: En allowedOrigin tenemos que poner el dominio del origen que está permitido.
Tambien hay que especificar los métodos permitidos. En nuestro caso get y post.

3. Vamos a la carpeta donde se almacenará todo el contenido que vamos a subir. Pichamos en acciones
y clicamos en "MAKE PUBLIC". Ahora todo el mundo podrá acceder al contenido que aquí se guarda.

4. Ahora debemos ir a nuestro "SECURITY CREDENTIALS". Hacemos click en "GROUPS"
- Pinchamos en create new group le damos un nombre y le agregamos la siguiente politica:

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
        "arn:aws:s3:::barreche-tb/test/*"
      ],
      "Effect": "Allow"
    }
  ]
}

(*) Nota: Lo que estamos haciendo es que todos los usuarios de dicho grupo pueden añadir contenido
sobre s3. Y que el recurso al que tiene acceso es la carpeta "test" ("barreche-tb/test/*")

5. Ahora nos creamos un usuario, le damos un nombre y le asociamos el grupo que hemos creado.

