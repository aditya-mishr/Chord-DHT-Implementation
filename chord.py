import numpy as np
import hashlib
import random
import matplotlib.pyplot as plt

class Node:
	def __init__(self,new_id):
		self.id = new_id
		self.succ = None
		self.pred = None
		self.finger =[]
		self.key = {}



class DHT:
	def __init__(self,m):
		self.m = m
		self.start_node = None
		self.dht = []
		self.no_of_hopes=[]
		self.no_of_search_query = 0

	def join(self,new_id):
		new_node = Node(new_id)

		if self.start_node == None:
			new_node.pred = new_node
			for i in range(self.m):
				new_node.finger.append({})
				new_node.finger[i]["node"] = new_node
				new_node.finger[i]["start"] = (new_id+(2**i))%(2**self.m)
			self.start_node = new_node
		
		else:
			for i in range(self.m):
				new_node.finger.append({})
				new_node.finger[i]["start"] = (new_id+(2**i))%(2**self.m)
			
			self.init_finger_table(new_node)
			
			self.update_others(new_node)
			
		self.dht.append(new_node)


	def add_key(self,k):
		succ =  self.find_successor(k,mode=False)
		succ.key[k] = "aditya"


	def print_dht(self):
		for i in range(len(self.dht)):
			print(str(i)+"th node in dht-->")
			print(self.dht[i].id)
			print(self.dht[i].finger[0]["node"].id)
			print(self.dht[i].pred.id)
			print(self.dht[i].key)

	def find_successor(self,new_node_id, mode = False):
		n,path = self.find_predecessor(new_node_id)
		if mode==False:
			return n.finger[0]["node"]
		else:
			path.append(n.finger[0]["node"].id)
			return path

	
	def find_predecessor(self,new_node_id):
		node = self.start_node
		path = [node.id]
		while not self.belongs_to(new_node_id,node.id,node.finger[0]["node"].id,2):
			node = self.closest_preceding_finger(node,new_node_id)
			path.append(node.id)
		return node,path

	
	def closest_preceding_finger(self,node,new_node_id):
		for i in range(self.m-1,-1,-1):
			if self.belongs_to(node.finger[i]["node"].id,node.id,new_node_id,1):
				return node.finger[i]["node"]
		return node
	

	def belongs_to(self,x,a,b,type):
		if(a < b):
			if type == 1:
				# ()
				return a + 1 <= x <= b - 1
			elif type == 2:
				# (]
				return a + 1 <= x <= b
			elif type == 3:
				# [)
				return a <= x <= b - 1
			else:
				# []
				return a <= x <= b
		elif a == b:
			if type == 1:
				# ()
				return not (a == x)
			elif type == 2:
				# (]
				return True
			elif type == 3:
				# [)
				return True
			else:
				# []
				return True

		else:
			if type == 1:
				# ()
				return not (b <= x <= a)
			elif type == 2:
				# (]
				return not (b < x <= a)
			elif type == 3:
				# [)
				return not (b <= x < a)
			else:
				# []
				return not (b < x < a)


	def init_finger_table(self,new_node):
		new_node.finger[0]["node"] = self.find_successor(new_node.finger[0]["start"])
		new_node.pred = new_node.finger[0]["node"].pred
		new_node.finger[0]["node"].pred = new_node
		new_node.pred.finger[0]["node"] = new_node
		for i in range(0,self.m-1):
			if  self.belongs_to(new_node.finger[i+1]["start"],new_node.id,new_node.finger[i]["node"].id,3):
				new_node.finger[i+1]["node"] = new_node.finger[i]["node"]
			else:
				new_node.finger[i+1]["node"] = self.find_successor(new_node.finger[i+1]["start"])


	def update_others(self,new_node):
		for i in range(self.m):
			ide = (new_node.id-(2**(i)))%(2**self.m)
			p,path = self.find_predecessor(ide)
			if p.id!=new_node.id:
				self.update_finger_table(p,new_node,i)

	
	def update_finger_table(self,n,s,i):
		if self.belongs_to(s.id,n.id,n.finger[i]["node"].id,3):
			n.finger[i]["node"] = s
			p = n.pred
			if p.id!=s.id:
				self.update_finger_table(p,s,i)


	def lookup(self,key):
		path_list = self.find_successor(key,mode=True)
		self.no_of_hopes.append(len(path_list))
		self.no_of_search_query = self.no_of_search_query + 1
		return path_list


	def delete(self,node):
		node.pred.finger[0]["node"] = self.find_successor(node.finger[0]["start"])
		node.finger[0]["node"].pred = node.pred
		for i in range(self.m):
			ide = (node.id - (2**i))%(2**self.m)
			node_pre,path = self.find_predecessor(ide)
			self.update_finger_table_delete(node_pre,node,i)
		self.dht.remove(node)
		node_succ = node.pred.finger[0]["node"]
		node_succ.key.update(node.key)
		if node==self.start_node:
			self.start_node = node.finger[0]["node"]
		del node


	def update_finger_table_delete(self,node_pre,node,i):
		if node_pre.finger[i]["node"].id == node.id:
			node_pre.finger[i]["node"] = node.finger[0]["node"]
			node_pre = node_pre.pred
			self.update_finger_table_delete(node_pre,node,i)



def SHA1(ip):
	ip = ip.split(".")
	ip = "".join(ip)
	hash_ip =  hashlib.sha1(ip.encode()).hexdigest()
	return hash_ip



def generate_random_ip():
	ip = []
	for i in range(4):
		ip.append(random.randint(0,255))
	ip = list(map(str,ip))
	ip = ".".join(ip)
	return ip

def compress(node_id,k):
	node_id = bin(node_id).replace("0b","")
	compress_node_id = ""
	for i in range(k):
		compress_node_id = compress_node_id + node_id[random.randint(0,len(node_id)-1)]
	return int(compress_node_id,2)

def generate_random_node(k):
	ip = generate_random_ip()
	node_id = SHA1(ip)
	node_id = int(node_id,16)
	node_id = compress(node_id,k)
	return node_id

def rmse_box_plot(nodes):
	
	graph=["100","500","1000"]
	box = plt.boxplot(nodes,patch_artist=True,labels=graph)

	colors = ['green', 'red','orange']
	for patch, color in zip(box['boxes'], colors):
		patch.set_facecolor(color)
	plt.xlabel("No of nodes")
	plt.ylabel("Path length")
	plt.show()


if __name__ == '__main__':

	k = 160
	N=[100,500,1000]
	nodes=[]
	for n in N:
		no_key = 10000
		no_lookups = 100000
		no_delete_node = n//2

		dht = DHT(k)
		for i in range(n):
			node_id = generate_random_node(k)
			dht.join(node_id)
		print("......",n," nodes added.........")

		for i in range(no_key):
			key = random.randint(0,(2**k)-1)
			dht.add_key(key)
		print("......",no_key," keys added........")

		for i in range(no_lookups):
			key = random.randint(0,(2**k)-1)
			print("Lookup for:",key)
			print(dht.lookup(key))
		print("......",no_lookups," performed.......")
		
		for i in range(no_delete_node):
			dht.delete(dht.dht[random.randint(0,len(dht.dht)-1)])
		dht.print_dht()
		
		print("avg no of hops:",sum(dht.no_of_hopes)/dht.no_of_search_query)
		
		nodes.append(dht.no_of_hopes)

	rmse_box_plot(nodes)
	# plt.figure(figsize=(7,5))
	# plt.hist(dht.no_of_hopes,edgecolor = "black")
	# plt.xlabel("Path Length")
	# plt.ylabel("No of Lookups")
	# plt.savefig("11.svg")
	# plt.show()


	# for i in range(no_lookups):
	# 	key = random.randint(0,(2**k)-1)
	# 	dht.lookup(key)
	# print("......",no_lookups," performed.......")
	# print("avg no of hops:",sum(dht.no_of_hopes)/dht.no_of_search_query)
	
	# plt.figure(figsize=(7,5))
	# plt.hist(dht.no_of_hopes,edgecolor = "black")
	# plt.xlabel("Path Length")
	# plt.ylabel("No of Lookups")
	# plt.savefig("21.svg")
	# plt.show()

	# del dht
	