# Purpose
Light novel cave is a website that hosts web novels. This program is made to help with downloading novel chapters.

# Helpful Info
 ### URL Format  
 `https://www.lightnovelcave.com/novel/<novel_name>/<chapter>`


It seems like the way that the novel name and the chapters in the URL are referenced changes every now and then and sometimes have random numbers.
In order to to get the correct URL, we will focus on just using a starting full url, then grabbing the URL for the next chapter while parsing that page.

###  Next page tag:
```
<a rel="next" class="button nextchap " href="/novel/shadow-slave-1365/chapter-1717" title="Chapter 1717: Rustle.">
<span>Next</span>
<i class="icon-right-open"></i>
</a>
```

### Chapter text
Is all in a single **div** tag with the id of `chapter-container`. Each paragraph is contained in a **p** tag.
```
<div id="chapter-container" class="chapter-content font_default" itemprop="description" style="">
<p>Because he wanted to.</p>
<p>For once, Sunny's heart wasn't full of fear and despair. Instead, it was filled with defiant indignation. He was tired of bending under the pressure of the world, furtively clutching to the tiniest glimmers of hope, always afraid, always willing to do anything, abandon anything, just to survive for another day. It wasn't enough anymore.</p>
 ...
</div>  
```