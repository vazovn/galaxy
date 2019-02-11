#!/bin/env python

def dump(obj):
   for attr in dir(obj):
       if hasattr( obj, attr ):
           # check per attribute
           #if attr == 'referer' :
               print( "obj.%s = %s" % (attr, getattr(obj, attr)))
