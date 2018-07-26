__author__ = 'Preston Sheppard'
function uploadImage(image, accessToken)
{
    var endPoint = "https://api.imgur.com/3/image";

    var imageData = {type: 'base64',
            name: 'neon.jpg',
            title: 'test title',
            caption: 'test caption',
            image: image};

    var headers =  {'Authorization': 'Bearer ' + accessToken};

    $.ajax({
        url: endPoint,
        type: 'POST',
        data: imageData,
        header: headers,
        dataType: 'json'});
}

function shareImage(imageId, imageTitle, accessToken)
{
    var endPoint = "https://api.imgur.com/3/gallery/image/" + imageId;

    var headers = {Authorization: 'Bearer ' + accessToken};

    var postData = {title: imageTitle};

    var request = $.ajax({
        url: endPoint,
        data: postData,
        header: headers});

    request.success(function(data)
    {
        return data['data']['id'], data['data']['title']
    });
    request.error(function()
    {
        console.log(data);
    });
}

function getAccessToken(clientId, clientSecret, refreshToken)
{
    var endPoint = "https://api.imgur.com/oauth2/token";

    var data = {
        refresh_token: refreshToken,
        client_id: clientId,
        client_secret: clientSecret,
        grant_type: "refresh_token"};

    var request = $.ajax({
        url: endPoint,
        data: data});

    request.success(function(data)
    {
        return data['access_token']);
    });
    request.error(function()
    {
        console.log(data);
    });
}

fucntion getRefreshToken()
{
    var refreshToken = "a4b8f794cd436996f36ee7b038ab68c4e71909cb";
    return refreshToken;
}

var clientId = "1a73509dbf251cf";
var clientSecret = "3cc02c2a34878b0ce3cd9d81820dc514b34b0f34";
var refreshToken = getRefreshToken();
var imageId, imageTitle = uploadImage(image, accessToken);
shareImage(imageId, imageTitle, accessToken);