from flask import request
from flask import Flask
import urllib.request as req
import json
import pymysql
from flask import render_template
from flask import session
from flask import redirect
import requests


app=Flask(__name__, static_folder = "public", static_url_path = "/")
app.secret_key = "helloFlaskeefdsfsdfsdfwefwec"
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True

db = pymysql.connect(host = "localhost", user = "root", password = "Lqsym233!", database = "website")
cursor = db.cursor()
x = {"number":0}
# Pages
@app.route("/")
def index():
	return render_template("index.html")
@app.route("/attraction/<id>")
def attraction(id):
	session["data"] = id
	return render_template("attraction.html", name = session["data"])
@app.route("/booking")
def booking():
	if "name" in session:
		return render_template("booking.html", name = session["name"])
	else:
		return redirect("/")
@app.route("/thankyou")
def thankyou():
	data = request.args.get("number")
	return render_template("thankyou.html", name = data)
@app.route("/api/attractions")
def attractions():
	alldata = []
	end = 12
	page = int(request.args.get("page"))
	nextpage = page + 1
	page = (page*12) + 1

	if page >=313:
		nextpage = None
		end = 7
	if page > 324:
		return json.dumps({
				"error":True,
				"message":"資料錯誤"
			},ensure_ascii = False)
	keyword = request.args.get("keyword")

	if keyword == None:
		try:
			for j in range(page, (page + end)):
				imgages = []
				url = """SELECT * FROM img WHERE no = '%s'"""%(j)
				cursor.execute(url)
				results = cursor.fetchall()
				for k in results:
					img = [k[2]]
					imgages += img
				da = """SELECT * FROM data WHERE id ='%s'"""%(j)
				cursor.execute(da)
				result = cursor.fetchall()
				for i in result:
					ide = i[0]
					name = i[1]
					category = i[2]
					description = i[3]
					address = i[4]
					transport = i[5]
					mrt = i[6]
					latitude = i[7]
					longitude = i[8]
					data  = [{
							"id":ide,
							"name":name,
							"category":category,
							"description":description,
							"address":address,
							"transport":transport,
							"mrt":mrt,
							"latitude":latitude,
							"longitude":longitude,
							"images":imgages
						}]
					alldata += data
			return json.dumps({
				"nextPage":nextpage,
				"data":alldata
			},ensure_ascii = False)
		except:
			return json.dumps({
				"error":True,
				"message":"資料錯誤"
			},ensure_ascii = False)

	else:
		try:
			count = -1
			keyword = "%" + keyword + "%"
			da = """SELECT * FROM data WHERE name LIKE '%s'"""%(keyword)
			cursor.execute(da)
			result = cursor.fetchall()
			for i in result:
				count += 1
				ide = i[0]
				name = i[1]
				category = i[2]
				description = i[3]
				address = i[4]
				transport = i[5]
				mrt = i[6]
				latitude = i[7]
				longitude = i[8]
				imgages = []
				url = """SELECT * FROM img WHERE no = '%s'"""%(ide)
				cursor.execute(url)
				res = cursor.fetchall()
				for j in res:
					img = [j[2]]
					imgages += img
				data  = [{
						"id":ide,
						"name":name,
						"category":category,
						"description":description,
						"address":address,
						"transport":transport,
						"mrt":mrt,
						"latitude":latitude,
						"longitude":longitude,
						"images":imgages
					}]
				alldata += data
			if count  <= (page + 10):
				nextpage = None
			if count < (page - 1):
				return json.dumps({
					"error":True,
					"message":"資料錯誤"
				},ensure_ascii = False)
			else:
				return json.dumps({
					"nextPage":nextpage,
					"data":alldata[(page - 1):(page + 11)]
				},ensure_ascii = False)
		except:
			return json.dumps({
					"error":True,
					"message":"資料錯誤"
				},ensure_ascii = False)
@app.route("/api/attraction/<number>")
def attractions2 (number):
	x = []
	try:
		url = """SELECT * FROM img WHERE NO = '%s'"""%(number)
		cursor.execute(url)
		results = cursor.fetchall()
		for k in results:
			imgages = [k[2]]
			x = x + imgages
		sql = """SELECT * FROM data WHERE id = '%s'"""%(number)
		cursor.execute(sql)
		result = cursor.fetchall()
		for i in result:
			ide = i[0]
			name = i[1]
			category = i[2]
			description = i[3]
			address = i[4]
			transport = i[5]
			mrt = i[6]
			latitude = i[7]
			longitude = i[8]
			data  = {
					"id":ide,
					"name":name,
					"category":category,
					"description":description,
					"address":address,
					"transport":transport,
					"mrt":mrt,
					"latitude":latitude,
					"longitude":longitude,
					"images":x
				}
		return json.dumps({
					"data":data
				},ensure_ascii = False)
	except:
		return json.dumps({
			"error":True,
			"message":"資料錯誤"
		},ensure_ascii = False)
@app.route ("/api/user", methods = ["POST"])
def apiuserpost():
	try:
		data = request.get_json()
		if data["name"]  == "" or data["email"]  == "" or data["password"] == "" :
			return json.dumps({
				"error":True,
				"message":"資料不全,註冊失敗!"
			}, ensure_ascii = False)
		email = data["email"]
		mailsql = """SELECT * FROM user WHERE email = '%s'"""%(email)
		cursor.execute(mailsql)
		result = cursor.fetchall()
		if len(result) == 0:
			emailsql = """INSERT INTO user (name, email, password) VALUES ('%s', '%s', '%s')"""%(data["name"], data["email"], data["password"])
			cursor.execute(emailsql)
			db.commit()
			return json.dumps({
				"ok":True
			})
		else:
			return json.dumps({
				"error":True,
				"message":"該電子信箱已註冊!"
			}, ensure_ascii = False)
	except:
		return json.dumps({
			"error":True,
			"message":"註冊失敗"
		}, ensure_ascii = False)
@app.route("/api/user", methods = ["PATCH"])
def apiuserpatch():
	try:
		data = request.get_json()
		sql = """SELECT * FROM user WHERE email = '%s'"""%(data["email"])
		cursor.execute(sql)
		result = cursor.fetchall()
		if len(result) == 0:
			return json.dumps({
				"error":True,
				"message":"信箱或密碼錯誤"
			},ensure_ascii = False)
		else:
			for i in result:
				if i[3] == data["password"] :
					session["id"] = i[0]
					session["name"] = i[1]
					session["email"] = data["email"]
					return json.dumps({
						"ok":True
					})
				else:
					return json.dumps({
						"error":True,
						"message":"信箱或密碼錯誤"
					},ensure_ascii = False)
	except:
		return json.dumps({
			"error":True,
			"message":"信箱或密碼錯誤"
		},ensure_ascii = False)
@app.route("/api/user", methods = ["GET"])
def apiuserget():
	if "email" in session:
		return json.dumps({
			"data":{
				"id":session["id"],
				"name":session["name"],
				"email":session["email"]
			}
		},ensure_ascii = False)
	else:
		return json.dumps({
			"data":None
		})
@app.route("/api/user", methods = ["DELETE"])
def apiuserdelete():
	try:
		session.pop("id")
		session.pop("name")
		session.pop("email")
		if "time" in session:
			session.pop("date")
			session.pop("time")
			session.pop("price")
			session.pop("registername")
			session.pop("address")
			session.pop("image")
			session.pop("attractionId")
		return json.dumps({
			"ok":True
		})
	except:
		return json.dumps({
			"ok":False
		})
@app.route("/api/booking", methods =["GET"])
def apibookingget():
	try:
		if "email" in session:
			if "attractionId" in session:
				url = "http://13.231.74.51:3000//api/attraction/" + session["attractionId"]
				with req.urlopen(url) as response:
					data = json.load(response)
				session["registername"] = data["data"]["name"]
				session["address"] = data["data"]["address"]
				session["images"] = data["data"]["images"]
				return json.dumps({
					"data":{
						"attraction":{
							"id":session["attractionId"],
							"name":session["registername"],
							"address":session["address"],
							"image":session["images"]
						},
						"date":session["date"],
						"time":session["time"],
						"price":session["price"]
					}
				},ensure_ascii = False)
			else:
				return json.dumps({
					"data":None,
					"message":"目前沒有任何待預定的行程"
				},ensure_ascii = False)
		else:
			return json.dumps({
				"error":True,
				"message":"Nothing"
			})
	except:
		return json.dumps({
				"error":True,
				"message":"程式出現錯誤,未取得資料"
			})
	
@app.route("/api/booking", methods = ["POST"])
def apibookingpost():
	try:
		data = request.get_json()
		session["attractionId"] = data["attractionId"]
		session["date"] = data["date"]
		session["time"] = data["time"]
		session["price"] = data["price"]
		return json.dumps({
			"ok":True
		})
	except:
		return json.dumps({
			"error":True,
			"message":"系統錯誤"
		})
@app.route("/api/booking", methods = ["DELETE"])
def apibookingdelete():
	try:
		session.pop("date")
		session.pop("time")
		session.pop("price")
		session.pop("registername")
		session.pop("address")
		session.pop("images")
		session.pop("attractionId")
		return json.dumps({
			"ok":True
		})
	except:
		return json.dumps({
			"error":True,
			"message":"系統出錯"
		})

@app.route("/api/order/<ordernumber>")
def apiorderget(ordernumber):
	if "email" in session:
		if session[ordernumber] == None:
			return json.dumps({
				"data":None
			})
		else:
			return json.dumps(
				session[ordernumber]
			,ensure_ascii = False)
	else:
		return json.dumps({
				"data":"未登入系統"
			},ensure_ascii = False)
@app.route("/api/order", methods = ["POST"])
def apiorderpost():
	# try:
	#確認登入狀況,以email來驗證
	if "email" not in session:
		return json.dumps({
			"error": True,
			"message": "未登入會員,請正常連線"
		},ensure_ascii = False)
	#抓到前端送來的資料,並存放到session裡面
	data = request.get_json()
	x["number"] += 1 ; session["ordernumber"] = str(202100000 + x["number"])
	session["thisid"] = data["order"]["trip"]["attraction"]["id"]; session["registername"] =  data["order"]["trip"]["attraction"]["name"]; session["address"] =  data["order"]["trip"]["attraction"]["address"]; session["image"] =  data["order"]["trip"]["attraction"]["image"]
	session["price"] = data["order"]["price"]; session["date"] = data["order"]["trip"]["date"]; session["time"] = data["order"]["trip"]["time"]
	session["contactname"] = data["order"]["contact"]["name"]; session["contactemail"] = data["order"]["contact"]["email"]; session["contactphone"] = data["order"]["contact"]["phone"]
	session[session["ordernumber"]] = {
		"data": {
			"number": session["ordernumber"],
			"price": session["price"],
			"trip": {
			"attraction": {
				"id": session["thisid"],
				"name": session["registername"],
				"address": session["address"],
				"image": session["image"]
			},
			"date": session["date"],
			"time": session["time"]
			},
			"contact": {
			"name": session["contactname"],
			"email": session["contactemail"],
			"phone": session["contactphone"]
			},
			"status": 1
		}
	}

	userinfo = """INSERT INTO thisorder (ordernumber, id, name, address, image, price, date, time, contactname, contactemail, contactphone, paystate) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '未付款')"""%(session["ordernumber"], session["thisid"], session["name"], session["address"], session["image"], session["price"], session["date"], session["time"], session["contactname"], session["contactemail"], session["contactphone"])
	cursor.execute(userinfo)
	db.commit()
	
	myjson = {
		"prime": data["prime"],
		"partner_key": "partner_XzCtS627kYMVlz6jeQThQZC1VxqZznceaJn571qu1ADvNsMC88utdRv0",
		"merchant_id": "sosqoo78902000_TAISHIN",
		"details":"TapPay Test",
		"amount": data["order"]["price"],
		"cardholder": {
			"phone_number": data["order"]["contact"]["phone"],
			"name": data["order"]["contact"]["name"],
			"email": data["order"]["contact"]["email"],
		},
	}
	url = "https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime"
	payresult = requests.post(url, json = myjson, headers = {"Content-Type":"application/json","x-api-key":"partner_XzCtS627kYMVlz6jeQThQZC1VxqZznceaJn571qu1ADvNsMC88utdRv0"}, timeout = 30000)
	status = payresult.json()
	if (status["status"] == 0):
		paystate = """UPDATE thisorder SET paystate = '已付款' WHERE ordernumber = '%s'"""%(session["ordernumber"])
		cursor.execute(paystate)
		db.commit()
		return json.dumps({
			"data": {
				"number": session["ordernumber"],
				"payment": {
				"status": 0,
				"message": "付款成功"
				}
			}
		}, ensure_ascii = False)
	else:
		return json.dumps({
			"error": True,
			"message": "付款失敗,錯誤原因:" + status["msg"] + "訂單編號:" + str(session["ordernumber"])
		},ensure_ascii = False)
	# except:
	# 	return json.dumps({
	# 			"error": True,
	# 			"message": "後端程序錯誤"
	# 		},ensure_ascii = False)
app.run(host = "0.0.0.0", port=3000)