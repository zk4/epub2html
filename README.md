Fastest epub reader.
# Why 
Reading epub in PC is pain as hell. I have tried a lot tool like `calibre` `epubreader`,`Mac books`, `MarginNote` for quick and good view experience. However, some of the pifalls always exist in one or another.
- Loading is super slow for big epub because of splitted files.
- No smooth scrolling. 
	
I think most of the epub reader focus too much on the layout, instead of contents.
So I wonder. I have a web browser like Chrome which is a natural epub reader, and it's fast enough.
The basic idea is converting epub to a big html. Simple but effective.

![](https://github.com/zk4/epub2html/blob/master/demo.gif?raw=true)

# Tested platform 
- Mac
- Windows

# Usage 
``` bash
pip install epub2html
epub2html abc.epub  

```
will open your converted epub html file in browser .


# Open with double click like normal file (mac)

use automator, generate the app, create a `Run shell script` module
``` 
source ~/.bash_profile
/usr/local/bin/epub2html "$1"
```
check `which epub2html` in your bash to make sure it's the right path.
save it, 
link the file with this app, You are good to go.


# Dev

``` python
python3 -m venv --clear .p3env
source .p3env/bin/activate
pip install -r requirements.txt
```


# Last
I won't follow the [standard](https://www.w3.org/publishing/epub3/epub-spec.html#sec-intro-epub-specs) to parse epub, since it's way too complicated. If some epub is not openable.Please make a PR ,or,sobmit the epub to the issues, I would fix it as soon as I can.
