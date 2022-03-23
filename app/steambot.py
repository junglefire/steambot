# -*- coding: utf-8 -*- 
#!/usr/bin/env python
import logging as log
import bs4 as bs
import requests
import click
import json
import time
import os

import _config as cfg
import _store

# main function
# ex: py app/steambot.py --debug <subcommand>
#     The `debug` parameter must be before the subcommand name
@click.group()
@click.option('--debug', type=bool, required=False, is_flag=True, help='print debug log information')
def main(debug):
	if debug:
		log.basicConfig(
			format='[%(asctime)s][%(levelname)s] %(message)s', 
			level=log.DEBUG, 
			# filename='logs/robot.log',
			# filemode='w'
		)
	else:
		log.basicConfig(format='[%(asctime)s][%(levelname)s] %(message)s', level=log.INFO)

# get information from steam
@main.command()
@click.option('-f', '--dbf', type=str, required=True, default="db/raw.dbf", help='database data file')
@click.option('--start', type=int, required=True, default=0, help='page from')
@click.option('--step', type=int, required=True, default=50, help='page step')
@click.option('--truncate', type=bool, is_flag=False, default=False, help='page step')
def getlist(dbf, start, step, truncate):
	log.info("get list of all games...")
	db = _store.create_database(dbf, truncate)
	# get last page number
	last_pageno = _store.get_last_pageno(db)
	print(last_pageno)
	if start <= last_pageno:
		start = last_pageno+step
	# download list of games
	url = cfg.tpl_list_of_all_games.substitute(PAGE_START=start, PAGE_STEP=step)
	log.info("download page: {}".format(url))
	ret = requests.get(url)
	if ret.status_code != 200:
		log.error("download failed, err: {}".format(ret.reason))
		os._exit()
	hm = json.loads(ret.text)
	_store.insert_record(db, _store.SQL_INSERT_INTO_RAW_LIST, (start, hm["results_html"]))
	start += step
	if hm["total_count"] <= start:
		log.info("get list of games done!")
		os._exit(0)
	for idx in range(start, hm["total_count"], step):
		url = cfg.tpl_list_of_all_games.substitute(PAGE_START=idx, PAGE_STEP=step)
		log.info("download page: {}".format(url))
		ret = requests.get(url)
		if ret.status_code != 200:
			log.error("download failed, err: {}".format(ret.reason))
			os._exit()
		hm = json.loads(ret.text)
		_store.insert_record(db, _store.SQL_INSERT_INTO_RAW_LIST, (idx, hm["results_html"]))
		time.sleep(3)
	# parse the page of `list of games`
	cursor = db.cursor()
	rows = cursor.execute(_store.SQL_QUERY_RAW_LIST)
	db.close()

# get game information
@main.command()
@click.option('-f', '--dbf', type=str, required=True, default="db/raw.dbf", help='database data file')
def getinfo(dbf):
	log.info("get list of all games...")
	db = _store.create_database(dbf, truncate=False)
	cursor = db.cursor()
	rows = cursor.execute(_store.SQL_QUERY_RAW_LIST)
	for row in rows:
		soup = bs.BeautifulSoup(row[0], 'html.parser')
		list_of_games = soup.find_all('a', class_="search_result_row ds_collapse_flag")
		for game in list_of_games:
			appid = game.get("data-ds-appid")
			name = game.find('span', class_="title").text
			price = game.find('div', class_="col search_price_discount_combined responsive_secondrow").get("data-price-final")
			date = game.find('div', class_="col search_released responsive_secondrow").text
			log.info("appid: {}, name: {}, price: {}, release data: {}".format(appid, name, price, date))
			_store.insert_record(db, _store.SQL_INSERT_INTO_GAME_LIST, (appid, name, price, date))
	db.close()

# get game information by appid
@main.command()
@click.option('-f', '--dbf', type=str, required=True, default="db/raw.dbf", help='database data file')
@click.option('-i', '--appid', type=int, required=True, help='steam appid')
def getgame(dbf, appid):
	log.info("get game `{}` info ...".format(appid))
	ret = requests.get("https://store.steampowered.com/app/1245620/")
	if ret.status_code != 200:
		log.error("download failed, err: {}".format(ret.reason))
		os._exit()
	print(ret.text)


if __name__ == '__main__':
	main()