# why 
Read epub in PC is pain as hell. I try a lot tool for better view experience. No luck.
- Loading is slow because of the splitted file.
- No smooth scrolling.
- pdf generating is so ugly 
	
BUT! we have chrome! rendering HTML is super fast. Why dont we take advantage of it.
So, the basic idea it convert epub to a static html. That's it.


# usage 
``` bash
pip install epub2html
epub2html abc.epub  ./
```


# todo 
- some chapter hash jump does not work because it's only a html file. try to recreate id in content file 
- show/hide button does not locate in the middle of sideb if menu too long
- generate decent pdf 
