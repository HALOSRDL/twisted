
import os
from twisted.internet import app 
from twisted.web.woven import page
from twisted.web import server, static, microdom, domhelpers

rootDirectory = os.path.expanduser("~/Pictures")

class DirectoryListing(page.Page):

    templateFile = "directory-listing3.xhtml"

    def initialize(self, *args, **kwargs):
        self.directory = kwargs['directory']

    def wmfactory_title(self, request):
      return self.directory

    def wmfactory_directory(self, request):
      files = os.listdir(self.directory)
      for i in xrange(len(files)):
          if os.path.isdir(os.path.join(self.directory,files[i])):
              files[i] = files[i] + '/'
      return files

    def getDynamicChild(self, name, request):
      path = os.path.join(self.directory,name)
      if os.path.exists(path):
          if os.path.isdir(path):
              return DirectoryListing(directory=path)
          else:
              return ImageDisplay(image=path)

    def wvupdate_thumbnail(self, request, node, data):
        size = request.args.get('thumbnailSize',('200',))[0]
        a = microdom.lmx(node)
        a['href'] = data
        if os.path.isdir(os.path.join(self.directory,data)):
            a.text(data)
        else:
            a.add('img', src=(data+'/preview'),width=size,height=size)

    def wvupdate_adjuster(self, request, widget, data):
        size = request.args.get('thumbnailSize',('200',))[0]
        domhelpers.locateNodes(widget.node.childNodes, 
                               'value', size)[0].setAttribute('selected', '1')
       
        
        
class ImageDisplay(page.Page):

    templateFile="image-display.xhtml"

    def initialize(self, *args, **kwargs):
        self.image = kwargs['image']

    def wmfactory_image(self, request):
        return self.image

    def wchild_preview(self, request):
        return static.File(self.image)
        
site = server.Site(DirectoryListing(directory=rootDirectory))
application = app.Application("ImagePool") 
application.listenTCP(8088, site)

if __name__ == '__main__': 
    import sys               
    from twisted.python import log 
    log.startLogging(sys.stdout, 0) 
    application.run() 
