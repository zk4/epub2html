
# why 
Read epub in PC is pain as hell. I have tried a lot tool for better view experience. No luck.
- Loading is slow because of the splitted file.
- No smooth scrolling.
- pdf generating is so ugly 
	
BUT! we have web browser which is a natural epub reader! Why dont we take advantage of it.
So, the basic idea is converting epub to a big html. Simple but effective.

![](https://github.com/zk4/epub2html/blob/master/demo.gif?raw=true)

# Tested platform 
- Mac
- Windows

# usage 
``` bash
pip install epub2html
epub2html abc.epub  

```
will open your converted epub html file in browser .


# open with double click like normal file (mac)

use automator, generate the app, create a `Run shell script` module
``` 
source ~/.bash_profile
epub2html "$1"
```
save it, 
link the file with this app, You are good to go.


# todo 
- follow https://www.w3.org/publishing/epub3/epub-spec.html#sec-intro-epub-specs to read source.
- show/hide button does not locate in the middle of sidebar if menu too long
- repair ref link
- images and css location
