import sys
import glob
import os

github = "https://github.com/"
user = "bpRsh"
project = "/2019_shear_analysis_after_dmstack"
path = "/blob/master/Jan_2020/a01_jan8/"
nbview = "https://nbviewer.jupyter.org/github/"

notebooks = sorted([ nb for nb in glob.glob('*.ipynb')])

# note: do not name it  README, this may harm some day,
# rename nb_links later to README.md
with open('nb_links.md','w') as fo:
    # first write the header
    line = "|  Notebook | Rendered   | Description  |  Author |"
    fo.write(line + '\n')

    line = "|---|---|---|---|"
    fo.write(line + '\n')

    # then loop over all the notebooks
    for notebook in notebooks:
        gh_link = github + user + project + path + notebook
        nb_link = nbview + user + project + path + notebook

        line = """| {notebook}  | [ipynb]({gh_link}), [rendered]({nb_link})  |   | [Bhishan Poudel](https://bhishanpdl.github.io/)  |""".format(notebook=notebook,nb_link=nb_link,gh_link=gh_link)
        fo.write(line + '\n')

# if we do not have any readme, then make it.
if not os.path.isfile('README.md'):
    os.rename('nb_links.md', 'README.md')