# here we include the class that designs the 
# html pages for successful placements of
# each bird species

import dominate as dm
from dominate.tags import *
import os
import pandas as pd

from __init__ import INDEX_DICT

class RightPlacementPage:
    '''Builder class for a given bird species.
    '''
    BIRD_DATA = pd.read_csv(INDEX_DICT["PATHS_FROM_SCRIPTS"]["BIRD_INFO"])
    
    def __init__(self, bird_name):
        '''Initiaize object with a given name.
        '''
        assert self.check_placementname(bird_name), (
                f"{bird_name} is not in list of phylogenetic placement.")
 
        self.name = bird_name
        self.get_data()

        # initiate html page
        self.initiate_html()
        return
    
    # helpers
    def check_name(self, bird_name):
        '''Check if bird name is in list.
        '''
        return self.BIRD_DATA["CODE"].str.match(bird_name).any()

    def check_placementname(self, bird_name):
        '''Check if bird name occurs in the list of birds that should be
        phylogenetically placed.
        '''
        return bird_name in get_placement_species_list()

    def get_data(self):
        '''Select the data of the bird name from the whole `BIRD_DATA`.
        '''
        self.data = self.BIRD_DATA[self.BIRD_DATA["CODE"]==self.name].squeeze()
        return


    def make_title(self):
        '''Build a title for the HTML.
        '''
        # this can be edited.
        # so far, we simply take the latin name.
        title = self.data.loc["Latin"]
        return title
    
    def make_page_path(self):
        '''Build name of path for html page.
        '''
        file_name = os.path.join(
                INDEX_DICT["PATHS_FROM_SCRIPTS"]["PLACEMENT_HTML_DIR"],
                f"{self.name}_success.html")
        return os.path.abspath(file_name)


    def make_img_path(self):
        '''Build name of path for bird image.
        '''
        file_name = os.path.join(
                INDEX_DICT["PATHS_FROM_SCRIPTS"]["BIRD_PAGE_IMG_DIR"],
                f"{self.name}.png")
        # return os.path.abspath(file_name)
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
        with self.doc:
            self.define_header()
            self.plot_with_info()


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
    
    def define_header(self):
        '''Put together the name information about the bird species as header.
        '''
        # make a large title with name as species
        page_title = f"Successfully placed: {self.data.loc['Name']}"
        # make subtitle of latin name in italics
        page_subtitle = ("You are a great researcher. Your dry "
            "lab team approved that this bird fits into the "
            "phylogenetic placement")
        
        with div():
            attr(id="header")
            h1(page_title)
            h2(em(page_subtitle))
            self.define_infopagelink()
        return

    def plot_with_info(self):
        '''Add image to html document and annotate it with background info.
        '''
        from dominate.util import raw
        
        # get image location
        image_file = self.make_img_path()
        # image_file = self.data["Photolink"]
        # get license information
        license_info = self.data["license notice for plain text "]
        # get license link
        license_link = self.data["license notice HTML (https://lizenzhinweisgenerator.de/)"]
        with div():
            attr(id="image")
            with figure():
                attr(id="habitus")
                img(src=image_file,
                        alt=license_info)
                if isinstance(license_link, str):
                    figcaption(raw(license_link))
                else:  # for missing data
                    figcaption("Missing.")
        return

    def define_infopagelink(self):
        '''Make a small button that brings the user to the info page.
        '''
        from bird_pages import BirdPage
        bp = BirdPage(self.name)
        bp_path = bp.make_page_path()
        with form():
            input_(
                    type="button",
                    value="Learn more about this bird...",
                    onclick=f"window.location.href='{bp_path}'")
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
# end BirdPage


# helpers
def get_placement_species_list():
    '''Return a list of bird species that are used for the placement.
    '''
    pm_dir = INDEX_DICT["PATHS_FROM_SCRIPTS"]["BIRD_PLACEMENT_IMG_DIR"]
    bird_sp_list = [
            fl.replace("tree_","").replace(".svg", "") for fl in 
            os.listdir(pm_dir) if fl.startswith("tree_")]
    return bird_sp_list


###############
def main():
    bird_names = get_placement_species_list()
    for bird_name in bird_names:
        bird_name = bird_name.strip()
        rp = RightPlacementPage(bird_name)
        rp.build_html()
        rp.save_html(force=True)
    return

if __name__ == "__main__":
    main()
