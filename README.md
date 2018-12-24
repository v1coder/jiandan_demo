# 煎蛋妹子图爬虫 demo



![](http://wx1.sinaimg.cn/mw600/82e98952ly1fygoarfjxqj20uo1hc7ci.jpg)

为了不增加网站的负担，这里只做一个demo，输出一页的图片地址
<br>

------

### 具体方法：

- 找到图片代码位置

打开 Chrome 浏览器开发者工具（Mac 下快捷键 option+command+I），点击开发者工具左上角的箭头，再将点击网页中的图片，就能定位到图片代码的位置

![](https://blog-pic-1253208066.file.myqcloud.com/2018-12-24-144607.png)

<br>

- 网页源码中找信息

Chrome 浏览器打开网页源码（Mac 下快捷键 option+command+U），在本该出现图片地址的位置是以下代码

```html
<p><img src="//img.jandan.net/img/blank.gif" onload="jandan_load_img(this)" /><span class="img-hash">Ly93eDEuc2luYWltZy5jbi9tdzYwMC84MmU5ODk1Mmx5MWZ5Z29hcmZqeHFqMjB1bzFoYzdjaS5qcGc=</span></p>
```

这里有两个关键信息：

`jandan_load_img(this)` 函数和`"img-hash">` 后面的值

<br>

- 解码网址

先从 `jandan_load_img(this)` 入手

开发者模式下全局搜索（Windows快捷键 ctrl+shift+f，Mac 快捷键 option+command+F），搜函数名`jandan_load_img` ，找到对应的的 js 文件，再点击花括号

![](https://blog-pic-1253208066.file.myqcloud.com/2018-12-24-151152.png)

<br>

就可以看到 js 文件的代码，在里面搜索（快捷键 command+F）函数名`jandan_load_img`

```javascript
function jandan_load_img(b) {
    var d = $(b);
    var f = d.next("span.img-hash");
    var e = f.text();
    f.remove();
    var c = jdQFXcEeWzpGANTZyHb1G0w0ggDlCZ5ILV(e, "qOzLfOL8mfbbsawjoQQPkWwkakHnOGze");
    var a = $('<a href="' + c.replace(/(\/\/\w+\.sinaimg\.cn\/)(\w+)(\/.+\.(gif|jpg|jpeg))/, "$1large$3") + '" target="_blank" class="view_img_link">[查看原图]</a>');
    d.before(a);
    d.before("<br>");
    d.removeAttr("onload");
    d.attr("src", location.protocol + c.replace(/(\/\/\w+\.sinaimg\.cn\/)(\w+)(\/.+\.gif)/, "$1thumb180$3"));
    if (/\.gif$/.test(c)) {
        d.attr("org_src", location.protocol + c);
        b.onload = function() {
            add_img_loading_mask(this, load_sina_gif)
        }
    }
}
```

大概意思是说取到 `class='img-hash'` 的 span 标签中的值, 通过 `jdQFXcEeWzpGANTZyHb1G0w0ggDlCZ5ILV` 这个函数处理之后, 然后再拼接成图片的地址。

<br>

 我们再查找` jdQFXcEeWzpGANTZyHb1G0w0ggDlCZ5ILV` 这个函数

```javascript
var jdQFXcEeWzpGANTZyHb1G0w0ggDlCZ5ILV = function(o, y, g) {
    var d = o;
    var l = "DECODE";
    var y = y ? y : "";
    var g = g ? g : 0;
    var h = 4;
    y = md5(y);
    var x = md5(y.substr(0, 16));
    var v = md5(y.substr(16, 16));
    if (h) {
        if (l == "DECODE") {
            var b = md5(microtime());
            var e = b.length - h;
            var u = b.substr(e, h)
        }
    } else {
        var u = ""
    }
    var t = x + md5(x + u);
    var n;
    if (l == "DECODE") {
        g = g ? g + time() : 0;
        tmpstr = g.toString();
        if (tmpstr.length >= 10) {
            o = tmpstr.substr(0, 10) + md5(o + v).substr(0, 16) + o
        } else {
            var f = 10 - tmpstr.length;
            for (var q = 0; q < f; q++) {
                tmpstr = "0" + tmpstr
            }
            o = tmpstr + md5(o + v).substr(0, 16) + o
        }
        n = o
    }
    var k = new Array(256);
    for (var q = 0; q < 256; q++) {
        k[q] = q
    }
    var r = new Array();
    for (var q = 0; q < 256; q++) {
        r[q] = t.charCodeAt(q % t.length)
    }
    for (var p = q = 0; q < 256; q++) {
        p = (p + k[q] + r[q]) % 256;
        tmp = k[q];
        k[q] = k[p];
        k[p] = tmp
    }
    var m = "";
    n = n.split("");
    for (var w = p = q = 0; q < n.length; q++) {
        w = (w + 1) % 256;
        p = (p + k[w]) % 256;
        tmp = k[w];
        k[w] = k[p];
        k[p] = tmp;
        m += chr(ord(n[q]) ^ (k[(k[w] + k[p]) % 256]))
    }
    if (l == "DECODE") {
        m = base64_encode(m);
        var c = new RegExp("=","g");
        m = m.replace(c, "");
        m = u + m;
        m = base64_decode(d)
    }
    return m
};
```

大概意思是对图片网址进行了 base64 编码，所以我们尝试对源码中的`"img-hash">` 后面的值进行 base64 解码。

解码方式：

```python
import base64
b = 'Ly93eDEuc2luYWltZy5jbi9tdzYwMC84MmU5ODk1Mmx5MWZ5Z29hcmZqeHFqMjB1bzFoYzdjaS5qcGc='
base64.b64decode(b)
# 输出
b'//wx1.sinaimg.cn/mw600/82e98952ly1fygoarfjxqj20uo1hc7ci.jpg'
```

<br>

- 最后

把 bytes 对象转换成 str ，再把网址拼接完整就可以了。

```python
url = str(url_bytes, encoding='utf-8')
complete_url = 'http:' + url
```

