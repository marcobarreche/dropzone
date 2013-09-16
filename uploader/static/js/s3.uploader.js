$(function() {

var CREATE_POLICY_SERVICE = 'http://thumbr.io/get-policy-and-signature',
    GET_THUMBRIO_URL = 'http://thumbr.io/get-thumbrio',
    BUCKET_NAME = 'barreche-tb',
    BUCKET_RESOURCE_FOLDER = 'test/',
    API_KEY = '...',
    AWS_ACCESS_KEY = '...';
var BUCKET_ACTION = 'https://' + BUCKET_NAME + '.s3.amazonaws.com',
    BUCKET_URL = "https://s3.amazonaws.com/" + BUCKET_NAME + '/';
var CLASS_DETAILS_FILE = 'dz-details';

var myDropzone = new Dropzone('#uploader', {url: BUCKET_ACTION});
myDropzone.on("sending", function(file, xhr, formData) {
    uploadFile(file, xhr, formData, AWS_ACCESS_KEY);
});

myDropzone.on("success", function(file, response) {
    updateUrl(file.name, $(file.previewElement));
});

function uploadFile(file, xhr, formData, access_key) {
    $.ajax({
        url: CREATE_POLICY_SERVICE,
        async: false,
        dataType: 'json',
        success: function(policyAndSignature) {
            var policy = policyAndSignature[0];
            var signature = policyAndSignature[1];
            var key = BUCKET_RESOURCE_FOLDER + file.name;
            formData.append('key', key);
            formData.append('acl', 'public-read');
            formData.append('Content-Type', file.type);
            formData.append('AWSAccessKeyId', access_key);
            formData.append('policy', policy);
            formData.append('signature', signature);
            formData.append('file', file);
            xhr.open('POST', BUCKET_ACTION, true);
            xhr.send(formData);
        }
    });
}

function updateUrl(filename, element) {
    var queryArguments = '?url=' + BUCKET_URL + BUCKET_RESOURCE_FOLDER + filename;
    queryArguments += '&size=' + THUMBRIT.WIDTH_THUMBNAIL + 'x' + THUMBRIT.HEIGHT_THUMBNAIL + 'c';

    $.ajax({
        url: GET_THUMBRIO_URL + queryArguments,
        async: false,
        dataType: 'json',
        success: function(thumbrioUrl) {
            element.find('.' + CLASS_DETAILS_FILE + ' img').attr('src', thumbrioUrl);
        }
    });
}

});