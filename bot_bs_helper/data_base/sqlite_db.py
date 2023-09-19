import sqlite3 as sq
from create_bot import bot


########################################
def sql_start():
	base = sq.connect("qiwi_base.db")
	cur = base.cursor()
	if base:
		print('Data base connected OK!')

class Database:
	def __init__(self,db_file):
		db_file = 'qiwi_base.db'
		self.connection = sq.connect(db_file)
		self.cursor = self.connection.cursor()

	def user_exists(self,user_id):
		with self.connection:
			result = self.cursor.execute("SELECT * FROM `users` WHERE `user_id` = ?",(user_id,)).fetchall()
			return bool(len(result))

	def create_user(self,user_id,referrer_id = None):
		with self.connection:
			if referrer_id != None:
				self.cursor.execute("INSERT INTO `users`(`user_id`, `referrer_id`) VALUES (?,?)",(user_id,referrer_id,))
			else:
				 self.cursor.execute("INSERT INTO `users` (`user_id`) VALUES (?)",(user_id,))

	def add_user(self,user_id,skin = None,gender = None,hairstyle = None,name = None):
		with self.connection:
			self.cursor.execute("UPDATE `users` SET `skin` = ? WHERE `user_id` = ?",(skin,user_id,))
			self.cursor.execute("UPDATE `users` SET `gender` = ? WHERE `user_id` = ?",(gender,user_id,))
			self.cursor.execute("UPDATE `users` SET `hairstyle` = ? WHERE `user_id` = ?",(hairstyle,user_id,))
			self.cursor.execute("UPDATE `users` SET `name` = ? WHERE `user_id` = ?",(name,user_id,))			

	def about_user(self,user_id):
		with self.connection:
			result = self.cursor.execute("SELECT * FROM `users` WHERE `user_id` = ?",(user_id,)).fetchall()
			return result

	def set_user_data(self,user_id,option,new):
		with self.connection:
			return self.cursor.execute(f"UPDATE `users` SET `{option}` = ? WHERE `user_id` = ?",(new,user_id,))


	def user_money(self,user_id):
		with self.connection:
			result = self.cursor.execute("SELECT `money` FROM `users` WHERE `user_id` = ?",(user_id,)).fetchmany(1)
			return (result[0][0])

	def set_money(self,user_id,money):
		with self.connection:
			return self.cursor.execute("UPDATE `users` SET `money` = ? WHERE `user_id` = ?",(money,user_id))

	def user_gold(self,user_id):
		with self.connection:
			result = self.cursor.execute("SELECT `gold` FROM `users` WHERE `user_id` = ?",(user_id,)).fetchmany(1)
			return (result[0][0])

	def set_gold(self,user_id,gold):
		with self.connection:
			return self.cursor.execute("UPDATE `users` SET `gold` = ? WHERE `user_id` = ?",(gold,user_id))

	def set_gold_calls(self,user_id,gold):
		with self.connection:
			return self.cursor.execute("UPDATE `users` SET `gold_calls` = ? WHERE `user_id` = ?",(gold,user_id))
			
	def user_calls_gold(self,user_id):
		with self.connection:
			result = self.cursor.execute("SELECT `gold_calls` FROM `users` WHERE `user_id` = ?",(user_id,)).fetchmany(1)
			return (result[0][0])

	def user_gold_all_time(self,user_id):
		with self.connection:
			result = self.cursor.execute("SELECT `gold_all_time` FROM `users` WHERE `user_id` = ?",(user_id,)).fetchmany(1)
			return (result[0][0])

	def set_gold_all_time(self,user_id,money):
		with self.connection:
			return self.cursor.execute("UPDATE `users` SET `gold_all_time` = ? WHERE `user_id` = ?",(money,user_id))


	def add_check(self,user_id,money, bill_id):
		with self.connection:
			self.cursor.execute("INSERT INTO `check` (`user_id`,`money`,`bill_id`) VALUES (?,?,?)",(user_id, money, bill_id,))

	def get_check(self,bill_id):
			with self.connection:
				result = self.cursor.execute("SELECT * FROM `check` WHERE `bill_id` = ?",(bill_id,)).fetchmany(1)
				if not bool(len(result)):
					return False
				return result[0]

	def delete_check(self, bill_id):
			with self.connection:
				return self.cursor.execute("DELETE FROM `check` WHERE `bill_id` = ?",(bill_id,))


	def other_staf_exists(self):
			with self.connection:
				result = self.cursor.execute('SELECT * FROM `other_staf`').fetchall()
				return bool(len(result))

	def delete_staf(self, staf_name):
			with self.connection:
				return self.cursor.execute("DELETE FROM `other_staf` WHERE `name` = ?",(staf_name,))	


	async def staf_read(self):
		with self.connection:
			result = self.cursor.execute('SELECT * FROM `other_staf`').fetchall()
			return result

	def user_free_chest(self,user_id):
		with self.connection:
			result = self.cursor.execute("SELECT `when_can_open_free_chest` FROM `users` WHERE `user_id` = ?",(user_id,)).fetchmany(1)
			return (result[0][0])

	def set_free_chest(self,user_id,when_can_open_free_chest):
		with self.connection:
			return self.cursor.execute("UPDATE `users` SET `when_can_open_free_chest` = ? WHERE `user_id` = ?",(when_can_open_free_chest,user_id))	
	#bet

	def bet_exists(self,):
		with self.connection:
			result = self.cursor.execute("SELECT * FROM `JackPot`").fetchall()
			return bool(len(result))

	def all_bet(self,):
		with self.connection:
			result = self.cursor.execute("SELECT * FROM `JackPot`").fetchall()
			return result

	def add_user_bet(self,user_id):
		with self.connection:
			return self.cursor.execute("INSERT INTO `JackPot` (`user_id`) VALUES (?)",(user_id,))

	def set_gold_bet(self,user_id,gold_bet):
			with self.connection:
				return self.cursor.execute("UPDATE `JackPot` SET `gold_bet` = ? WHERE `user_id` = ?",(gold_bet,user_id))

	def user_gold_bet(self,user_id):
		with self.connection:
			result = self.cursor.execute("SELECT `gold_bet` FROM `JackPot` WHERE `user_id` = ?",(user_id,)).fetchmany(1)
			return (result[0][0])

	def set_win_chanse(self,user_id,win_chanse):
			with self.connection:
				return self.cursor.execute("UPDATE `JackPot` SET `win_chanse` = ? WHERE `user_id` = ?",(win_chanse,user_id))

	def win_chanse(self,user_id):
		with self.connection:
			result = self.cursor.execute("SELECT `win_chanse` FROM `JackPot` WHERE `user_id` = ?",(user_id,)).fetchmany(1)
			return (result[0][0])

	def user_bet_exists(self,user_id):
		with self.connection:
			result = self.cursor.execute("SELECT * FROM `JackPot` WHERE `user_id` = ?",(user_id,)).fetchall()
			return bool(len(result))

	def JackPot_time_start(self,):
		with self.connection:
			result = self.cursor.execute("SELECT `time_start` FROM `JackPot_time`").fetchmany(1)
			return (result[0][0])

	def JackPot_time_stop(self,):
		with self.connection:
			result = self.cursor.execute("SELECT `time_stop` FROM `JackPot_time`").fetchmany(1)
			return (result[0][0])	

	def JackPot_time_start_add(self,time):
		with self.connection:
			return self.cursor.execute("INSERT INTO `JackPot_time` (`time_start`) VALUES (?)",(time,))

	def JackPot_time_stop_add(self,time):
		with self.connection:
			return self.cursor.execute("UPDATE `JackPot_time` SET `time_stop` = ?",(time,))

	def JackPot_time_set(self,):
		with self.connection:
			return self.cursor.execute("DELETE FROM `JackPot_time`"),self.cursor.execute("DELETE FROM `JackPot`")

	def add_user_turn(self,user_id):
		Database.set_id_turn(self,)
		with self.connection:
			self.cursor.execute('CREATE TABLE IF NOT EXISTS turn(id INTEGER PRIMARY KEY, user_id INTEGER, gold INTEGER)')
		with self.connection:
			return self.cursor.execute("INSERT INTO `turn` (`user_id`) VALUES (?)",(user_id,))
	def set_id_turn(self,):
		with self.connection:
			result = self.cursor.execute("SELECT * FROM `turn`").fetchall()
			ok = (len(result))
		if not ok:
			with self.connection:
				return self.cursor.execute("DROP TABLE turn")

	def set_user_turn(self,user_id,gold):
			with self.connection:
				return self.cursor.execute("UPDATE `turn` SET `gold` = ? WHERE `user_id` = ?",(gold,user_id))

	def user_turn_data(self,user_id):
		with self.connection:
			result = self.cursor.execute("SELECT * FROM `turn` WHERE `user_id` = ?",(user_id,)).fetchall()
			return result[0]

	def delete_user_turn(self, bill_id):
			with self.connection:
				return self.cursor.execute("DELETE FROM `turn` WHERE `id` = ?",(bill_id,))

	def user_turn_exists(self,user_id):
		with self.connection:
			result = self.cursor.execute("SELECT * FROM `turn` WHERE `user_id` = ?",(user_id,)).fetchall()
			return bool(len(result))

	def support_exists(self,user_id):
		with self.connection:
			result = self.cursor.execute("SELECT * FROM `support` WHERE `user_id` = ?",(user_id,)).fetchall()
			return bool(len(result))

	def add_support(self,user_id):
		with self.connection:
			return self.cursor.execute("INSERT INTO `support` (`user_id`) VALUES (?)",(user_id,))

	def delete_support(self, bill_id):
			with self.connection:
				return self.cursor.execute("DELETE FROM `support` WHERE `user_id` = ?",(bill_id,))

	def count_referals(self,user_id):
		with self.connection:
			return self.cursor.execute("SELECT COUNT (`id`) as count FROM `users` WHERE `referrer_id`=?",(user_id,)).fetchone()[0]

	def user_referrer(self,user_id):
		with self.connection:
			result = self.cursor.execute("SELECT `referrer_id` FROM `users` WHERE `user_id` = ?",(user_id,)).fetchmany(1)
			return (result[0][0])

	def user_top_week_exists(self,user_id):
		with self.connection:
			result = self.cursor.execute("SELECT * FROM `top_week` WHERE `user_id` = ?",(user_id,)).fetchall()
			return bool(len(result))

	def user_top_month_exists(self,user_id):
		with self.connection:
			result = self.cursor.execute("SELECT * FROM `top_month` WHERE `user_id` = ?",(user_id,)).fetchall()
			return bool(len(result))

	def add_top_week(self,user_id):
		with self.connection:
			return self.cursor.execute("INSERT INTO `top_week` (`user_id`) VALUES (?)",(user_id,))

	def add_top_month(self,user_id):
		with self.connection:
			return self.cursor.execute("INSERT INTO `top_month` (`user_id`) VALUES (?)",(user_id,))

	def set_gold_top_week(self,user_id,gold):
		with self.connection:
			return self.cursor.execute("UPDATE `top_week` SET `gold` = ? WHERE `user_id` = ?",(gold,user_id,))

	def set_gold_top_month(self,user_id,gold):
		with self.connection:
			return self.cursor.execute("UPDATE `top_month` SET `gold` = ? WHERE `user_id` = ?",(gold,user_id,))

	def user_gold_top_week(self,user_id):
		with self.connection:
			result = self.cursor.execute("SELECT `gold` FROM `top_week` WHERE `user_id` = ?",(user_id,)).fetchmany(1)
			return (result[0][0])

	def user_gold_top_month(self,user_id):
		with self.connection:
			result = self.cursor.execute("SELECT `gold` FROM `top_month` WHERE `user_id` = ?",(user_id,)).fetchmany(1)
			return (result[0][0])

	def set_top_week(self,):
			with self.connection:
				return self.cursor.execute("DELETE FROM `top_week`")

	def set_top_month(self,):
			with self.connection:
				return self.cursor.execute("DELETE FROM `top_month`")
	
	def show_top_week(self,):
		with self.connection:
			result = self.cursor.execute("SELECT * FROM `top_week` ORDER BY `gold` DESC").fetchall()
			return result

	def show_top_month(self,):
		with self.connection:
			result = self.cursor.execute("SELECT * FROM `top_month` ORDER BY `gold` DESC").fetchall()
			return result

	def all_promo(self,):
		with self.connection:
			result = self.cursor.execute("SELECT * FROM `promo`").fetchall()
			return result

	def add_key(self,user_id,):
		with self.connection:
			return self.cursor.execute("INSERT INTO `promo` (`key`) VALUES (?)",(user_id,))

	def del_key(self, bill_id):
			with self.connection:
				return self.cursor.execute("DELETE FROM `promo` WHERE `key` = ?",(bill_id,))

	def time_week(self,week):
		with self.connection:
			result = self.cursor.execute("SELECT `week` FROM `time_top_set` WHERE `id` = ?",(week,)).fetchmany(1)
			return (result[0][0])

	def time_month(self,month):
		with self.connection:
			result = self.cursor.execute("SELECT `month` FROM `time_top_set` WHERE `id` = ?",(month,)).fetchmany(1)
			return (result[0][0])

	def set_month(self,user_id,gold):
		with self.connection:
			return self.cursor.execute("UPDATE `time_top_set` SET `month` = ? WHERE `id` = ?",(gold,user_id,))

	def set_week(self,user_id,gold):
		with self.connection:
			return self.cursor.execute("UPDATE `time_top_set` SET `week` = ? WHERE `id` = ?",(gold,user_id,))

	def wardrobe_exists(self,user_id):
		with self.connection:
			result = self.cursor.execute("SELECT * FROM `users_wardrobes` WHERE `user_id` = ?",(user_id,)).fetchall()
			return bool(len(result))

	def create_wardrobe(self,user_id):
		with self.connection:
			self.cursor.execute("INSERT INTO `users_wardrobes` (`user_id`) VALUES (?)",(user_id,))

	def set_user_wardrobe(self,user_id,option,new):
		with self.connection:
			return self.cursor.execute(f"UPDATE `users_wardrobes` SET `{option}` = ? WHERE `user_id` = ?",(new,user_id,))

	def about_user_wardrobe(self,user_id):
		with self.connection:
			result = self.cursor.execute("SELECT * FROM `users_wardrobes` WHERE `user_id` = ?",(user_id,)).fetchall()
			return result
	
	def items_dir_to_name(self,direct):
		with self.connection:
			result = self.cursor.execute("SELECT `name` FROM `items_base` WHERE `dir` = ?",(direct,)).fetchmany(1)
			#print('----------------------------------')
			#print(result)
			return (result[0][0])

	def items_dir_to_name2(self,direct):
			with self.connection:
				result = self.cursor.execute("SELECT `name` FROM `items_base` WHERE `dir` = ?",(direct,)).fetchmany(1)
				print('----------------------------------')
				print(result)
				return (result[0][0])

	def items_name_to_info(self,name):
		with self.connection:
			result = self.cursor.execute("SELECT * FROM `items_base` WHERE `name` = ?",(name,)).fetchall()[0]
			return {'dir':result[1],'name':result[2],'price':result[3],'category' : result[4],'description':result[5]}

	def items_base_data(self,category):
		with self.connection:
			result = self.cursor.execute("SELECT * FROM `items_base` WHERE `category` = ? ORDER BY `price` ASC",(category,)).fetchall() 
			return result

	def bussiness_data(self,bussuness_name = None):
		with self.connection:
			if bussuness_name != None:
				result = (self.cursor.execute("SELECT * FROM `business_data` WHERE `bussuness_name` = ?",(bussuness_name,)).fetchall())[0]
				result = {'bussuness_name':result[1],'income':result[2],'net_income':result[3],'storage':result[4],'picture_dir':result[6],'price':result[7]}
			else:
				result = (self.cursor.execute("SELECT * FROM `business_data` ORDER BY `id` ASC").fetchall())
			return result

	def business_processes (self,user_id):
		with self.connection:
			result = (self.cursor.execute("SELECT * FROM `business_processes` WHERE `user_id` = ?",(user_id,)).fetchall())[0]
			result = {'on_account':result[2],'busines_name':result[3],'start_time':result[4],'storage_empty_time':result[5],'storage':result[6]}
			return result

	def create_business_p(self,user_id):
		with self.connection:
			return self.cursor.execute("INSERT INTO `business_processes` (`user_id`) VALUES (?)",(user_id,))		
	
	def set_business_p_data(self,user_id,option,new):
		with self.connection:
			return self.cursor.execute(f"UPDATE `business_processes` SET `{option}` = ? WHERE `user_id` = ?",(new,user_id,))

	def create_trade(self,from_id = None,to_id = None,trade_item = None,trade_price = None,type_price = None,random_id = None):
		with self.connection:
			self.cursor.execute("INSERT INTO `trades`(`from_id`, `to_id`,`trade_item`,`trade_price`,`type_price`,`random_id`) VALUES (?,?,?,?,?,?)",(from_id,to_id,trade_item,trade_price,type_price,random_id))	
	
	def del_trade(self, random_id):
		with self.connection:
			return self.cursor.execute("DELETE FROM `trades` WHERE `random_id` = ?",(random_id,))

	def trade_data(self,random_id):
		with self.connection:
			result = self.cursor.execute("SELECT * FROM `trades` WHERE `random_id` = ?",(random_id,)).fetchall()[0]
			result_d = {'id':result[0],'from_id':result[1],'to_id':result[2],'trade_item':result[3],'trade_price':result[4],'type_price':result[5],'random_id':result[6],}
			return result_d

	def answer_item_trade(self,random_id,type_price):
		with self.connection:
			return self.cursor.execute("UPDATE `trades` SET `type_price` = ? WHERE `random_id` = ?",(type_price,random_id))




