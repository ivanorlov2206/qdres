var canvases = [];
const NAME_LEN = 15;


function make_random_name() {
  var s = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890";
  var len = s.length;
  var res = '';

  for (var i = 0 ; i < NAME_LEN; i++) {
    res += s.charAt(Math.floor(Math.random() * len));
  }
  return res;
}


function create_canv(w, h) {
  let canv = document.createElement("canvas");
  canv.width = w;
  canv.height = h;
  canv.id = make_random_name();
  canv.hidden = true;
  canvases.push(canv);
  document.body.appendChild(canv);
  return canv;
}

function find_contours(canv) {
  var ctx = canv.getContext('2d');
  var w = canv.width;
  var h = canv.height;

  var mnx = w, mny = h, mxx = 0, mxy = 0;

  for (var y = 0; y < h; y++) {
    for (var x = 0; x < w; x++) {
      var data = ctx.getImageData(x, y, 1, 1).data[0];
      if (data > 0) {
        if (x < mnx)
          mnx = x;
        if (x > mxx)
          mxx = x;
        if (y < mny)
          mny = y;
        if (y > mxy)
          mxy = y;
      }
    }
  }

  return [mnx, mny, mxx, mxy];
}

function crop_and_center_image(canv) {
  let w = canv.width;
  let h = canv.height;
  var nw, nh;
  var sz = 28;

  if (w > h) {
    nh = sz / w * h;
    nw = sz;
    console.log(nw, nh);
  } else {
    nw = sz / h * w;
    nh = sz;
  }

  var cnv_resized = create_canv(nw, nh);
  var imgc = cnv_resized.getContext('2d');
  imgc.drawImage(canv, 0, 0, nw, nh);

  var iy = (sz - nh) / 2;
  var ix = (sz - nw) / 2;

  var new_image = create_canv(sz, sz);
  var nc = new_image.getContext('2d');
  nc.fillStyle = "black";
  nc.fillRect(0, 0, sz, sz);
  for (var x = 0; x < sz; x++) {
    for (var y = 0; y < sz; y++) {
      if (x >= ix && x < ix + nw && y >= iy && y < iy + nh) {
        var dat = imgc.getImageData(x - ix, y - iy, 1, 1);
        if (dat.data[0] != 0)
          nc.putImageData(dat, x, y);
      }
    }
  }

  return new_image;
}

function image_to_array(canv) {
  var ctx = canv.getContext('2d');
  var arr = [];
  for (var i = 0; i < 28; i++) {
    var la = [];
    for (var j = 0; j < 28; j++) {
      var d = ctx.getImageData(j, i, 1, 1).data[0];
      if (d > 0)
        la.push(255);
      else {
        la.push(0);
      }
    }
    arr.push(la);
  }
  return arr;
}


function process_image(canv) {
  let contours = find_contours(canv);
  var cropped = create_canv(contours[2] - contours[0], contours[3] - contours[1]);
  var left = contours[0], top = contours[1], w = contours[2] - contours[0], h = contours[3] - contours[1];
  cropped.getContext('2d').drawImage(canv, left, top, w + left, h + top, 0, 0, w + left, h + top);
  var centered = crop_and_center_image(cropped);
  return image_to_array(centered);
}

function clear_canvases() {
  for (var i = 0; i < canvases.length; i++) {
    document.body.removeChild(canvases[i]);
  }
  canvases = [];
}
