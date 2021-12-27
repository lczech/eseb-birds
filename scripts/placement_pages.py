# here we include the core class that designs the 
# html pages for the phylogenetic placement of a
# bird species

import dominate as dm
from dominate.tags import *
import os
import pandas as pd

from abstract_page import AbstractPage
from __init__ import INDEX_DICT

class PlacementPage(AbstractPage):
    '''Builder class for placement page of a given bird species.
    '''
    def __init__(self, bird_name, language="EN"):
        '''Initiaize object with a given name.
        '''
        self.name = bird_name
        super().__init__(language=language)
        self.get_data()
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
        return bird_name in get_placement_species_list(language=self.lang)


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
        if not hasattr(self, "data"):
            self.get_data()
        title = f"Phylogenetic placement for a newly discovered bird."
        return title
    

    def make_page_path(self):
        '''Build name of path for html page.
        '''
        file_name = os.path.join(
                INDEX_DICT[self.lang]["PATHS_FROM_SCRIPTS"]["PLACEMENT_HTML_DIR"],
                f"{self.name}_placement.html")
        return os.path.abspath(file_name)

    def make_img_path(self, bird_name):
        '''Build name of path for a bird image.
        '''
        assert self.check_name(bird_name), f"{bird_name} is not in list."

        file_name = os.path.join(
                INDEX_DICT[self.lang]["PATHS_FROM_SCRIPTS"]["BIRD_PAGE_IMG_DIR"],
                f"{bird_name}.png")
        # return os.path.abspath(file_name)
        return os.path.relpath(file_name, os.path.dirname(self.make_page_path()))


    def make_tree_img_path(self, bird_name):
        '''Build name of path for a bird image.
        '''
        assert self.check_name(bird_name), f"{bird_name} is not in list."

        file_name = os.path.join(
                INDEX_DICT[self.lang]["PATHS_FROM_SCRIPTS"]["BIRD_PLACEMENT_IMG_DIR"],
                f"tree_{bird_name}.svg")
        # return os.path.abspath(file_name)
        return os.path.relpath(file_name, os.path.dirname(self.make_page_path()))

    def make_img_link(self, bird_name):
        '''Build a link to error or success page.
        '''
        if self.name == bird_name: 
            file_link = os.path.join(
                    INDEX_DICT[self.lang]["PATHS_FROM_SCRIPTS"]["PLACEMENT_HTML_DIR"],
                    f"{self.name}_success.html")
        else:
            file_link = os.path.join(
                    INDEX_DICT[self.lang]["PATHS_FROM_SCRIPTS"]["START_AND_ERROR_HTML_DIR"],
                    "error_page.html")
        return os.path.relpath(file_link, os.path.dirname(self.make_page_path()))

    # HTML functions
    def html_body(self):
        '''Build the body of the html document.
        '''
        self.define_header()
        with div(cls="row"):
            self.column1()
            self.column2()
        return


    def define_stylesheet(self):
        '''Define the style sheet for the html head.
        '''
        super().define_stylesheet()
        # define path
        css_rawpath = os.path.join(
                INDEX_DICT[self.lang]["PATHS_FROM_SCRIPTS"]["CSS_DIR"],
                'two_columns.css')
        css_path = os.path.relpath(os.path.abspath(css_rawpath),
                os.path.dirname(self.make_page_path()))
        # set stylesheet for two columns
        link(rel='stylesheet', href=css_path)
        return


    def define_header(self):
        '''Put together the name information about the bird species as header.
        '''
        # make a large title with name as species
        page_title = f"Phylogenetic placement"
        # make subtitle of latin name in italics
        page_subtitle = "Which bird could be placed here on the tree?"
        
        with div():
            attr(id="header")
            h1(page_title)
            h2(em(page_subtitle))
        return

    def plot_with_info(self, image_path, bird_name=None, tree=False, count=None):
        '''Add image to html document and annotate it with background info.
        '''
        from dominate.util import raw
        if not tree: 
            data = self.BIRD_DATA[self.BIRD_DATA["CODE"]==bird_name].squeeze()
            # get license information
            license_info = data["license notice for plain text "]
            # get license link
            license_link = data["license notice HTML (https://lizenzhinweisgenerator.de/)"]
            # content of image is habitus
            img_content = "habitus"
        else:
            # we use this as image alternativ text
            license_info = "Phylogenetic tree for placement."
            # this is the image caption
            license_link = "Our wet lab sent us this data after sequencing of the bird."
            # it is a tree
            img_content = "tree"
        with div():
            # sometimes we have multiple images
            if count is not None : attr_id = f"image{count}"
            else : attr_id = "image"
            attr(id=attr_id)
            with figure():
                attr(id=img_content)
                img(src=image_path,
                        alt=license_info)
                if isinstance(license_link, str):
                    figcaption(raw(license_link))
                else:  # for missing data
                    figcaption("Missing.")
        return

    def column1(self):
        '''Make the first column, which includes the tree image.
        '''
        with div(cls="column"):
            tree_path = self.make_tree_img_path(self.name)
            self.plot_with_info(tree_path, tree=True)
        return


    def column2(self):
        '''Make the second column, which includes the images of birds to place.
        '''
        with div(cls="column"):
            p("Which bird could it be that fits into the tree?")
            for i, bird_name in enumerate(get_placement_species_list(language=self.lang)):
                img_path = self.make_img_path(bird_name)
                img_link = self.make_img_link(bird_name)
                with a(href=img_link):
                    self.plot_with_info(img_path, bird_name=bird_name, count=i+1)
        return
# end PlacementPage

# helper
def get_placement_species_list(language="EN"):
    '''Return a list of bird species that are used for the placement.
    '''
    pm_dir = INDEX_DICT[language]["PATHS_FROM_SCRIPTS"]["BIRD_PLACEMENT_IMG_DIR"]
    bird_sp_list = [
            fl.replace("tree_","").replace(".svg", "") for fl in 
            os.listdir(pm_dir) if fl.startswith("tree_")]
    return bird_sp_list

###############
def main():
    for lang in ["EN", "GR"]:
        bird_names = get_placement_species_list(language=lang)
        for bird_name in bird_names:
            pp = PlacementPage(bird_name, language=lang)
            pp.build_html()
            pp.save_html(force=True)
    return

if __name__ == "__main__":
    main()

