
# why 
Read epub in PC is pain as hell. I have tried a lot tool like `calibre` `epubreader` for better view experience. However, some of the pifalls always exist in one or another.
- Loading is slow because of the splitted file.
- No smooth scrolling.
- pdf generating is so ugly 
	
So I wonder. I have a web browser like  Chrome which is a natural epub reader. 
And we can install any plugin we want from google store.  for example, I use vim binding a lot, how do we navigate in epub with vim binding by the power of vimium plugin.

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
/usr/local/bin/epub2html "$1"
```
check `which epub2html` in your bash to make sure it's the right path.
save it, 
link the file with this app, You are good to go.



# todo 
- follow https://www.w3.org/publishing/epub3/epub-spec.html#sec-intro-epub-specs to read source.
- show/hide button does not locate in the middle of sidebar if menu too long
- repair ref link
- images and css location
