# here we include the abstract class for all pages 

from abc import ABC
import dominate as dm
from dominate.tags import *
import os
import pandas as pd
import yaml

from __init__ import INDEX_DICT

class AbstractPage(ABC):
    '''Builder class for a given bird species.
    '''
    def __init__(self, language="EN", stop_html_init=False):
        '''Initiaize object with a given name.
        '''
        self.BIRD_DATA = pd.read_csv(INDEX_DICT[language]["PATHS_FROM_SCRIPTS"]["BIRD_INFO"], sep=";")
        
        self.lang = language

        if stop_html_init : return

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
                INDEX_DICT[self.lang]["PATHS_FROM_SCRIPTS"]["BIRD_PAGE_IMG_DIR"],
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
        with self.doc:
            self.make_lang_links()
            self.html_body()
            self.define_back()
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
        css_rawpaths = [
                os.path.join(
                INDEX_DICT[self.lang]["PATHS_FROM_SCRIPTS"]["SEQUENCES"],
                "styles.css"),
                os.path.join(
                INDEX_DICT[self.lang]["PATHS_FROM_SCRIPTS"]["CSS_DIR"],
                'two_columns.css')]
        for i, css_rawpath in enumerate(css_rawpaths):
            css_path = os.path.relpath(os.path.abspath(css_rawpath),
                    os.path.dirname(self.make_page_path()))
            link(rel=f'stylesheet', href=css_path)
        return

    def define_jscript(self):
        '''Define the style js script for the html head.
        '''
        # this can be extended. we do not use it yet.
        # script(type='text/javascript', src='script.js')
        return
    
    def make_lang_links(self):
        '''Add the links between greek and english.
        '''
        langlink = lambda lg: os.path.relpath(
                undef_path.replace(f"/{self.lang.lower()}/", f"/{lg.lower()}/"), 
                os.path.dirname(undef_path))
        undef_path = self.make_page_path()
       
        # here we load the language texts for each language
        file_basics = os.path.join(INDEX_DICT[self.lang]["PATHS_FROM_SCRIPTS"]["BIRD_TEXTS"], "basics.yml")
        text_basics = yaml.safe_load(open(file_basics, "r"))
        all_languages = [ln.lower() for ln in INDEX_DICT.keys() if len(ln)==2]
        with div(cls="language_choice", align="right"):
            p(text_basics["changelang"]["FILL_IN"])

            for i, lng in enumerate(all_languages):
                with a(href=langlink(lng)):
                    span(text_basics[lng]["FILL_IN"])
                if i < len(all_languages)-1 : span(" 🐣 ")
        return

    def save_html(self, force=False):
        '''Save html document as a file.
        '''
        file_name = self.make_page_path()
        parent_dir = os.path.dirname(file_name)
        if not os.path.exists(parent_dir) : os.makedirs(parent_dir)
        if not os.path.exists(file_name) or force:
            with open(file_name, "w") as html_file:
                html_file.write(str(self.doc))
        else:
            print(f"Html document {self.name}.html already exists.")
        return

    def get_sequence(self, bird_name=None):
        '''Load short sequence for bird.
        '''
        seq_file = os.path.join(
                INDEX_DICT[self.lang]["PATHS_FROM_SCRIPTS"]["SEQUENCES"],
                "list.html")
        seq = fetch_sequences(bird_name, seq_file)
        return seq

    def paste_svg(self, svg_file_name):
        '''Paste the code of a svg file into the html code.
        '''
        from dominate.svg import svg
        from dominate.util import raw
        #assert os.path.exists(svg_file_name), f"Image {svg_file_name} does not exist."
        with open(svg_file_name, "r") as image:
            svg_base_dir = os.path.dirname(svg_file_name)
            for line in image.readlines():
                std_line = self.standardize_path(line, svg_base_dir)
                raw(std_line)
        return

    
    def paste_svg_io(self, svg_file_name, svg_io):
        '''Paste the code of a svg file into the html code.
        '''
        from dominate.svg import svg
        from dominate.util import raw
        svg_base_dir = os.path.dirname(svg_file_name)
        for line in svg_io.readlines():
            std_line = self.standardize_path(line, svg_base_dir)
            raw(std_line)
        return


    def standardize_path(self, svg_line, svg_base_dir):
        '''Change the path link of a line within an svg image.
        '''
        import regex as re
        LINK_RE = 'href\=\"([^\"]*)\"'
        match = re.search(LINK_RE, svg_line)

        # as the internal path of the svg file could be different
        # from our html file, we reassign all links...
        if not match : return svg_line
        link = match[1]
        link_abs = os.path.abspath(os.path.join(svg_base_dir, link))
        std_path = os.path.dirname(self.make_page_path())
        link_rel = os.path.relpath(link_abs, std_path)
        return svg_line.replace(link, link_rel)

    def show_seq(self):
        '''Add the large sequence to the HMTL document.
        '''
        from dominate.util import raw
        try : seq = self.load_long_sequence()
        except FileNotFoundError : return False
        else : raw(seq)
        return True

    def load_long_sequence(self):
        '''Obtain the long nucleotide sequence of a given bird species.
        '''
        seq_file = os.path.join(
                INDEX_DICT[self.lang]["PATHS_FROM_SCRIPTS"]["SEQUENCES"],
                f"{self.name}.html")
        body = []
        body_bool = False
        with open(seq_file, "r") as html:
            for line in html.readlines():
                if line.startswith("</body>") : return "".join(body)
                if body_bool : body.append(line)
                elif line.startswith("<body>") : body_bool = True
        raise RuntimeError("Html file is not proper in its structure.")


    def define_back(self):
        '''Make a small button that returns the user to the last page.
        '''
        file_basics = os.path.join(INDEX_DICT[self.lang]["PATHS_FROM_SCRIPTS"]["BIRD_TEXTS"], "basics.yml")
        text_basics = yaml.safe_load(open(file_basics, "r"))
        with form():
            input_(
                type="button",
                value=text_basics["back"]["FILL_IN"],
                onclick="history.back()")
        return
# end AbstractPage

###############
# helpers
def get_placement_species_list(language="EN"):
    '''Return a list of bird species that are used for the placement.
    '''
    pm_dir = INDEX_DICT[language]["PATHS_FROM_SCRIPTS"]["BIRD_PLACEMENT_IMG_DIR"]
    bird_sp_list = [
            fl.replace("tree_","").replace("_question.svg", "") for fl in
            os.listdir(pm_dir) if fl.endswith("_question.svg")]
    return bird_sp_list


def fetch_sequences(bird_alias, seq_html_path):
    '''Fetch the html formatted sequence for a bird alias.
    '''
    with open(seq_html_path,"r") as sf:
        lines = sf.readlines()
        for line in lines:
            if line.startswith("<dt>"):
                short_line = line.replace("<dt>","")
                name, seq = short_line.split("</dt>")
                if name == bird_alias : return seq
    raise ValueError(f"There is no sequence available for {bird_alias}.")
