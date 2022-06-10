import csv
import mariadb

def ConnectToDB():
	infile = open("./CrawlerAPI/DBRelated/MetadataCrawlerDBConfig.csv", 'r', encoding = 'utf-8-sig')
	rows = csv.reader(infile, delimiter=',')

	config = []
	for row in rows:
		config.append(row[1])

	try:
		conn = mariadb.connect(
			user=config[1],
			password=config[2],
			host=config[0],
			port=3306,
			database=config[3]
		)
	except mariadb.Error as e:
		# print(f"Error: {e}")
		print("Connecting to DB fails")
		return None
	
	return conn

def GetTableName():
	infile = open("./CrawlerAPI/DBRelated/MetadataCrawlerDBConfig.csv", 'r', encoding = 'utf-8-sig')
	rows = csv.reader(infile, delimiter=',')
	name = ""
	for row in rows:
		name = row[1]

	return name

def CheckIsDataCrawlered(webAbbr, inputID):
	conn = ConnectToDB()
	if conn==None: # Fail to connect to DB
		return -1
	cur = conn.cursor()

	tableName = GetTableName()

	query = "SELECT `有沒有被匯入詳細資料` FROM `"+tableName+"` WHERE `來源系統縮寫`='"+webAbbr+"' AND `典藏號`='"+inputID+"'"
	cur.execute(query)
	# print(query)

	res = None
	for item in cur:
		if item[0]==b'\x01':
			res = 1
		else:
			res = 0
	
	if res==None: # No data(record) found
		print("No data(record) found")
		return -1

	return res

def GetDBFormat():
	infile = open("./CrawlerAPI/DBRelated/MetadataFormat.csv", 'r', encoding = 'utf-8-sig')
	rows = csv.reader(infile, delimiter=',')

	DBList = []
	for row in rows:
		DBList.append(row[0])
	
	return DBList

def UpdataDB(webAbbr, inputID, listIn):
	conn = ConnectToDB()
	if conn==None: # Fail to connect to DB
		return False
	cur = conn.cursor()

	tableName = GetTableName()

	DBList = GetDBFormat()
	where = " WHERE `來源系統縮寫`='"+webAbbr+"' AND `典藏號`='"+inputID+"'"
	try: 
		for i in range(len(listIn)):
			if listIn[i] == '@':
				continue

			column = "`"+DBList[i]+"`"
			target = "'"+listIn[i]+"'"
			exe = "UPDATE `"+tableName+"` SET "+column+" = "+target+where
			cur.execute(exe)
			# print(exe)
			 
	except mariadb.Error as e: # update db fails 
		# print(f"Error: {e}")
		print("Updating DB fails")
		return False

	exe = "UPDATE `"+tableName+"` SET `有沒有被匯入詳細資料` = 1"+where
	cur.execute(exe)

	conn.commit()
	return True