/**
 * Decoders for zig.js sensor's streams (rgb, depth)
 */

// http://stackoverflow.com/questions/9543248/access-kinect-rgb-image-data-from-zigjs
var bufferWidth = 160;
var bufferHeight = 120;

/**
 * Decodes the sensor's image stream (rgb)
 * @param zigPlugin
 * @returns {HTMLElement} canvas containing the decoded image
 */
function imageToCanvas(zigPlugin) {
    return toCanvas(zigPlugin.imageMap, function(data, srcData, length) {
        for (var i = 0; i < length; i++) {
            data[i * 4] = srcData[i * 3 + 2];
            data[i * 4 + 1] = srcData[i * 3 + 1];
            data[i * 4 + 2] = srcData[i * 3 + 0];
            data[i * 4 + 3] = 255; // no alpha
        }
    });
}

/**
 * Decode the sensors's depth stream
 * @param zigPlugin
 * @returns {HTMLElement} canvas containing the decoded image
 */
function depthToCanvas(zigPlugin) {
    return toCanvas(zigPlugin.depthMap, function(data, srcData, length) {
        for (var i = 0; i < length; i++) {
            data[i * 4] = srcData[i * 2 + 0];
            data[i * 4 + 1] = srcData[i * 2 + 1];
            data[i * 4 + 2] = 255;
            data[i * 4 + 3] = 255;
        }
    });
}


function toCanvas(stream, decodeFunction) {
    var buffer = document.createElement('canvas');
    buffer.width = bufferWidth;
    buffer.height = bufferHeight;

    var ctx = buffer.getContext("2d");
    var pix = ctx.createImageData(buffer.width, buffer.height);
    var data = pix.data;
    var srcData = Base64.decode(stream);
    decodeFunction(data, srcData, buffer.width * buffer.height)
    ctx.putImageData(pix, 0, 0);
    return buffer;
}