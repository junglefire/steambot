# -*- coding: utf-8 -*- 
#!/usr/bin/env python
import string

"""
https://store.steampowered.com/search/results/?query&start=200&count=50&dynamic_data=&sort_by=_ASC&snr=1_7_7_230_7&infinite=1

https://store.steampowered.com/search/results/?query&start=900&count=50&dynamic_data=&sort_by=_ASC&snr=1_7_7_230_7&infinite=1
"""

# url template 
LIST_OF_ALL_GAMES = "https://store.steampowered.com/search/results/?query&start=$PAGE_START&count=$PAGE_STEP&dynamic_data=&sort_by=_ASC&snr=1_7_7_230_7&infinite=1"

tpl_list_of_all_games = string.Template(LIST_OF_ALL_GAMES)

