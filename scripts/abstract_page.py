# here we include the abstract class for all pages 

import dominate as dm
from dominate.tags import *
import os
import pandas as pd

from __init__ import INDEX_DICT

class AbstractPage:
    '''Builder class for a given bird species.
    '''
    BIRD_DATA = pd.read_csv(INDEX_DICT["PATHS_FROM_SCRIPTS"]["BIRD_INFO"])
    
    def __init__(self):
        '''Initiaize object with a given name.
        '''
        # initiate html page
        self.initiate_html()
        return
    
    # helpers
    def make_title(self):
        '''Build a title for the HTML.
        '''
        title = None
        return title
    

    def make_img_path(self):
        '''Build name of path for bird image.
        '''
        file_name = os.path.join(
                INDEX_DICT["PATHS_FROM_SCRIPTS"]["BIRD_PAGE_IMG_DIR"],
                f"{self.name}.png")
        return os.path.relpath(file_name, os.path.dirname(self.make_page_path()))

# HTML functions
    def initiate_html(self):
        '''Initiate the dominate document.
        '''
        self.doc = dm.document(title=self.make_title())
        return

    def build_html(self):
        '''Build html document with head and body.
        '''
        self.html_head()
        self.html_body()
        return


    def html_head(self):
        '''Build the head of the html document.
        '''
        with self.doc.head:
            self.define_meta()
            self.define_stylesheet()
            self.define_jscript()
        return
    

    def html_body(self):
        '''Build the body of the html document.
        '''
        return

    def define_meta(self):
        '''Define meta information of html document for head.
        '''
        # we use english and UTF-8
        meta(charset="UTF-8")
        meta(lang="en")
        return

    def define_stylesheet(self):
        '''Define the style sheet for the html head.
        '''
        # this can be extended. we do not use it yet.
        # link(rel='stylesheet', href='style.css')
        return

    def define_jscript(self):
        '''Define the style js script for the html head.
        '''
        # this can be extended. we do not use it yet.
        # script(type='text/javascript', src='script.js')
        return
    
    def save_html(self, force=False):
        '''Save html document as a file.
        '''
        file_name = self.make_page_path()
        if not os.path.exists(file_name) or force:
            with open(file_name, "w") as html_file:
                html_file.write(str(self.doc))
        else:
            print(f"Html document {self.name}.html already exists.")
        return
# end AbstractPage

###############