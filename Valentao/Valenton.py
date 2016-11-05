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
OK = "OK"
LIDER = "LIDER"
CURRENT_VALENTON = 0
#==============Functions======================#

#Class that initialize the node
class Node:
	node_port = 0
	node_id = -1
	nodePorts = [5000, 5001, 5002, 5003,5004]
	time = 0
	coordenator = -1
	

	def __init__(self, node_id):
		self.node_id = node_id
		self.node_port = self.nodePorts[node_id] #Self eh o this no java
		self.time = randint(0,100) #cada node recebe um tempo aleatorio

	def rinit(self):
		global CURRENT_VALENTON

		try:
			sock.bind(('localhost', nodePorts[self.node_id]))
		except Exception:
			pass

		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

		raw_input("") # press enter to send a request - ELEICAO

		if self.node_id >= CURRENT_VALENTON:
			CURRENT_VALENTON = self.node_id
			print "CURRENT VALENTAUM", CURRENT_VALENTON

		if self.node_id == 4:
			message_ziped = pickle.dumps(COORDENADOR)
			self.coordenator = 4
		else:
			message_ziped = pickle.dumps(ELEICAO)

		for i in range (len(self.nodePorts)):
			if i > self.node_id and self.node_id != 4: # evita que envie pra si mesmo
				self.sock.sendto(message_ziped, ('localhost', self.nodePorts[i])) #enviara para todos os processos
			if self.node_id == 4 and i < self.node_id == 4:
				self.sock.sendto(message_ziped, ('localhost', self.nodePorts[i])) #enviara para todos os processos


	def findIdCoord(PORT):
		if PORT == 5000:
			return 0;
		elif PORT == 5001:
			return 1;
		elif PORT == 5002:
			return 2;
		elif PORT == 5003:
			return 3;
		elif PORT == 5004:
			return 4;

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
						#SE O PROCESSO RECEBER UMA ELEICAO DEVE ENVIAR UM OK PARA QUEM ENVIOU PARA ELE
						#TOMA O PODER
						message_ziped = pickle.dumps(OK) # ENVIA O OK PRA QUEM ENVIOU A ELEICAO - UNICAST
						print "SENDING OK TO --> [IP: ", ADDRESS,"]","[PORT:", PORT,"]"
						sock.sendto(message_ziped, ('localhost', PORT))

						#TENHO QUE MANDAR UMA ELEICAO PARA TODOS OS NODES ACIMA DE MIM
						message_ziped = pickle.dumps(LIDER)
						for i in range (len(self.nodePorts)):
							if i > self.node_id:
								sock.sendto(message_ziped, ('localhost', self.nodePorts[i]))

					if message == LIDER:
						if self.node_id == CURRENT_VALENTON:
							print "DEI O GOLPE E GANHEI A ELICAO!!!"
							self.coordenator = self.node_id #SIGNIFICA QUE EU SOU O VALENTAO

						#COMO SOU O VALENTAUM VOU NOTIFICAR A TODOS QUE GANHEI A ELICAO
						message_ziped = pickle.dumps(COORDENADOR)
						for i in range (len(self.nodePorts)):
							if i < self.node_id:
								sock.sendto(message_ziped, ('localhost', self.nodePorts[i]))

					elif message == COORDENADOR:
						nProc = findIdCoord(PORT)
						self.coordenator = nProc #atualiza o coordenador[valentaum] do processo
						print "MY COORDENATOR NOW IS: ", str(self.coordenator)
					elif message == OK: 
						print "OK - RECEIVED"


if __name__ == '__main__':
	# Sao 5 processos , numerados de 0:4
	#specificy which specific process[Node]
	node_id = int(sys.argv[1])

	node = Node(node_id)

	print "Node: ", node_id
	print "Node coordenator: ", node.coordenator
	print "Node port: ", node.node_port

	start_new_thread(node.receiver,())

	node = Node(node_id)

	start_new_thread(node.rinit,())

	while True:
		time.sleep(10)
		print "LISTENING...\n"
