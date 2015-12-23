pichook
=============
  
<small>selwyn-lloyd mcpherson <<a href='mailto:selwyn.mcpherson@gmail.com'>selwynlloyd.mcpherson@gmail.com</a>></small>

## Aim
A stream of data may include URIs to data like images or documents. **pichook** is a demonstration of the machinations required to obtain those resources, and showcases just a few domain-specific idiosyncrasies involved in downloading them.

The second goal is to suggest how one might extract metadata embedded the resource itself. This can then be used for more interesting analyses, potentially identiying more precisely the source of the link and the tendancies of a given stream in general.

## Implementation
Any arbitrary stream can be used. Here, I monitor IRC logs as generated by Textual, a Mac client. Setting up an IRC bot is a great way to spend time accomplishing little.

    One day the cat got into the dairy and twenty of
    them were at work moving all the milk out; no one
    thought of moving the cat.
    
    - C.S. Lewis' The Voyage of the Dawn Treader
The basic idea is: use what you have, even if it isn't pretty. It's fair to use Textual's internal logging feature, which outputs text files and folders based on the channel and date. Managing those files isn't really our main concern here.

I'm using several channels and several dates, but as **pichook** needs simply one stream, there is some easy bash scripting to collect all the logs and present them. <font color='#FF88AA'>We use the **tailer** package to at the moment.</font>

## Sources
The resources from the channels I picked generally fell under one of just a few domains, so it is not too expensive to spend time working them out. The default is to simply request the URI, which should retrieve a bytestring equivalent to the image, or fail, which should be noted. **pichook** can recognize a few of the domains I noticed frequently (that analysis is elsewhere but can be integrated). Many of these domains require some request manipulation to retrieve the actual resource. In theory, we would like to have a standard library of such interfacs, expecting protocols will remain the same.

## Localization and Identification
Depending on the source of the documents, meta-data can be gleaned from the pure byte representation.

In this scenario, I am gathering images, so I am interested in EXIF data. This is extremely useful when available, though often, at the point of acquisition, EXIF data may have been altered from its original form, or, more likely, scrapped alltogether. 

That being said, each EXIF data point can be used to correlate various elements, including location.

<font color='#FF88AA'>A helper script can perform whois queries to determine location but that is currently not in scope.</font>