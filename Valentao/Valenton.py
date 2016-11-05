# coding = utf-8

# Name: Gabriel Stankevix Soares	511340
# Name: Luis Agusto Franca Barbosa	511374
# 
# Projet: Valentao
#
# Federal University of Sao Carlos - UFSCar
# Campus: Sorocaba
# Teacher: Fabio Verdi
#

#TOPICOS IMPORTANTES
# 1 - Faca o cenario funcionar para 5 processos
# 2 - crie diferentes situacoes para testar e provar o funcionamento do algoritmo
# 3 - Defina um tempo de espera (timeout) pela resposta de convocacao de eleicao
# 4 - Use este tempo para definir se o processo que disparou a eleicao deve se tornar lider

#Coisas do livro
# 1 - Em geral, algoritmos de eleicao tentam localizar o processo que tenha o numero de processo mais 
#	  alto e designa-lo como coordenador

# Implementacao
#	Um processo, P, convoca uma eleicao:
#		1 . P envia uma mensagem ELEICAO a todos os processos de numero mais altos
#		2 . Se nenhum responder, P vence a eleicao e se torna o coordenador
#		3 . Se um dos processos de numero mais alto responder, ele toma om poder e 
#			o trabalho de P esta concluido
#		4 . A qualquer momento, um processo pode receber uma mensagem ELEICAO de seus
#			seus colegas de numero mais baixos
#			4 . 1  Se a chegar uma, o recepetor envia uma mensagem OK de volta ao remetente para indicar
#					que esta vivo e tomara o poder.
#
#		5 . Se um processo inativo voltar, faz uma eleicao. Caso tenha o maior numero, ganha a eleicao
#
#
#=================Importing Modules============#
import socket
import random
import pickle
import time
from thread import *
from threading import Thread
from threading import Lock
import sys
import traceback
from collections import *
import os
from random import *


#==============Global Variables================#

TIMEOUT = 10
ELEICAO = "ELEICAO"
COORDENADOR = "COORDENADOR"
#==============Functions======================#

#Class that initialize the node
class Node:
	node_port = 0
	node_id = -1
	nodePorts = [5000, 5001, 5002, 5003,5004]
	time = 0

	def __init__(self, node_id):
		self.node_id = node_id
		self.node_port = self.nodePorts[node_id] #Self eh o this no java
		self.time = randint(0,100) #cada node recebe um tempo aleatorio

	def rinit(self):
		try:
			sock.bind(('localhost', nodePorts[self.node_id]))
		except Exception:
			pass

		raw_input("") # press enter to send a request

		if self.node_id == 4:
			message_ziped = pickle.dumps(COORDENADOR)
		else:
			message_ziped = pickle.dumps(ELEICAO)

		for i in range (len(self.nodePorts)):
			if i > self.node_id and self.node_id != 4: # evita que envie pra si mesmo
				self.sock.sendto(message_ziped, ('localhost', self.nodePorts[i])) #enviara para todos os processos
			if self.node_id == 4 and i < self.node_id == 4:
				self.sock.sendto(message_ziped, ('localhost', self.nodePorts[i])) #enviara para todos os processos

#The listener, waiting to get the message
def receiver(self):
		sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP

		try:
	   		sock.bind(('localhost', self.node_port))
	   	except Exception:
			pass

		while True:
	   		try:
	   			message_ziped, (ADDRESS, PORT) = sock.recvfrom(1024)
	   			message = pickle.loads(message_ziped)
	   		except Exception:
				time.sleep(10)
				print "\nWaiting message"
				pass
			else:
				if(message == ELEICAO):
					#SE ELE FOR O MAIOR DEVE ENVIAR UM OK PARA TODOS MENORES
					#TOMA O PODER
					#COMO SABER QUE ELE EH O MAIOR NUMERO ATUAL?

				elif message == COORDENADOR:
					#Caso valentao tenha acordado


if __name__ == '__main__':
	# Sao 5 processos , numerados de 0:4
	#specificy which specific process[Node]
	node_id = int(sys.argv[1])

	node = Node(node_id)

	print "My port", node.node_port

	start_new_thread(node.receiver,())

	node = Node(node_id)

	start_new_thread(node.rinit,())

	while True:
		time.sleep(10)
		print "LISTENING...\n"
