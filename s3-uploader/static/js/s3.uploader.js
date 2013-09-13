/*
    user            ACCESS key              SECRET KEY
    marcobarreche   AKIAIC72F3VVTJSB27GA    CmGntNl/x2kV/qisZJU4OnAb6qBCASNl2kn6Q/5h
    user_upload     AKIAJLHD6SHE45DVDL4Q    m8ZUN2MFW78hgpWY3LttwUzuvO7/VhaKCfIHmAtk
*/


$(function() {
    // Constants
    var _AWS_ACCESS_KEY = 'AKIAJLHD6SHE45DVDL4Q';
    var _AWS_SECRET_KEY = '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';

    var BUCKET_NAME = 'barreche-tb';
    var BUCKET_RESOURCE_FOLDER = 'test/';
    var BUCKET_ACTION = 'https://' + BUCKET_NAME + '.s3.amazonaws.com';
    var BUCKET_URL = "https://s3.amazonaws.com/" + BUCKET_NAME + '/';
    var THUMBRIT = {
        'BASE_URL': 'http://api.thumbr.io/',
        'API_KEY': 'D-lvXHFIHpY',
        'SECRET_KEY': '7yZYotUT8b3qnu9Rc.CE',
        'WIDTH_THUMBNAIL': 100,
        'HEIGHT_THUMBNAIL': 100,
    };
    var CLASS_DETAILS_FILE = 'dz-details';

    
    var myDropzone = new Dropzone('#uploader', {url: BUCKET_ACTION});
    myDropzone.on("sending", function(file, xhr, formData) {
        uploadFile(file, xhr, formData, _AWS_ACCESS_KEY, _AWS_SECRET_KEY);
    });
    myDropzone.on("success", function(file, response) {
        updateUrl(file.name, $(file.previewElement));
    });

    function uploadFile(file, xhr, formData, access_key, secret_key) {
        var policyAndSignature = createPoliceText(secret_key);
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

    function createPoliceText(secret) {
        var POLICY_JSON = {
            "expiration": "2015-01-01T00:00:00Z",
            "conditions": [
                {"bucket": "barreche-tb"},
                ["starts-with", "$key", BUCKET_RESOURCE_FOLDER],
                {"acl": "public-read"},
                ["starts-with", "$Content-Type", ""],
                ["content-length-range", 0, 1048576]
            ]
        };
        var policyBase64 = Base64.encode(JSON.stringify(POLICY_JSON));
        var signature = b64_hmac_sha1(secret, policyBase64) + '=';
        return [policyBase64, signature];
    }

    function updateUrl(filename, element) {
        var url = BUCKET_URL + BUCKET_RESOURCE_FOLDER + filename;
        var thumbritUrl = thumbrit(url, THUMBRIT.WIDTH_THUMBNAIL, THUMBRIT.HEIGHT_THUMBNAIL,
                                   '', false, [], filename);
        element.find('.' + CLASS_DETAILS_FILE + ' img').attr('src', thumbritUrl);
    }

    function thumbrit(url, width, height, crop, download, effects, seoname) {
        var encodedUrl = encodeURIComponent(url.replace('http://', '')).replace(/%2F/g, '/'),
            sizeAndOptions = width + 'x' + height + crop,
            i;
        if (download)
            sizeAndOptions += '-d';
        for (i = 0; i < effects.length; i++)
            if (effects[i])
                sizeAndOptions += '-e' + effects[i];
        var urlToSecure = THUMBRIT.BASE_URL + THUMBRIT.API_KEY + '/' + encodedUrl + '/' + sizeAndOptions + '/' + seoname;
        var hmac = Crypto.HMAC(Crypto.MD5, urlToSecure, THUMBRIT.SECRET_KEY);
        return THUMBRIT.BASE_URL + hmac + '/' + THUMBRIT.API_KEY + '/' + encodedUrl + '/' + sizeAndOptions + '/' + seoname;
    }
});