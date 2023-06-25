import requests
import speedtest
import socket
import psutil
import os
from time import sleep
from dotenv import load_dotenv



load_dotenv()



class main:
	def __init__(self):
		self.server_name = socket.gethostname()

	def connection_status(self):
		try:
			socket.gethostbyaddr('www.yandex.ru')
			return True
		except socket.gaierror:
			return False

	def now_ip(self):
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect(("8.8.8.8", 80))
		return s.getsockname()[0]

	def get_open_ports(self):
		open_ports = []

		for port in range(1, 1000):
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.settimeout(1)

			try:
				result = sock.connect_ex(('localhost', port))
				if result == 0:
					open_ports.append((port, "TCP"))
				sock.close()
			except:
				pass
			try:
				udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
				udp_sock.settimeout(1)
				udp_sock.bind(('localhost', port))
				open_ports.append((port, "UDP"))
				udp_sock.close()
			except:
				pass
		
		return ' '.join([f"{ipp[0]}/{ipp[1]}" for ipp in open_ports])

	def system_info(self):
		cpu_usage = psutil.cpu_percent(interval=1)
		available_memory = psutil.virtual_memory().available / (1024*1024)
		disk_usage = psutil.disk_usage(os.getcwd()).free / (1024*1024*1024)

		st = speedtest.Speedtest()
		download_speed = st.download() / (1024*1024)
		upload_speed = st.upload() / (1024*1024)

		data = ["CPU Usage: {}%".format(cpu_usage), "Available Memory: {:.2f} MB".format(available_memory), "Free Disk Space: {:.2f} GB".format(disk_usage), "Download Speed: {:.2f} Mbps".format(download_speed), "Upload Speed: {:.2f}Mbps".format(upload_speed)]

		return ''.join([f"{i}\n" for i in data])

class Telegram:
	def __init__(self):
		self.user_id = os.getenv("USER_ID")
		self.token = os.getenv("TOKEN")
	
	def send_message(self, message: str):
		send_request = requests.get(f'https://api.telegram.org/bot{self.token}/sendMessage?chat_id={self.user_id}&text={message}')

if __name__ == "__main__":
	tg = Telegram()
	
	tg.send_message(f'Сервер {main().server_name} успешно запущен!\nЛокальный IP: {main().now_ip()}\nВнешний IP: {requests.get("http://ifconfig.me/ip").text}\nОткрытые порты: {main().get_open_ports()}\n\n{main().system_info()}')
	print("Sending IP sucess!")

	global ip
	ip = main().now_ip()

	while True:
		sleep(60)
		if main().connection_status():
			if ip == main().now_ip():
				print("IP not changed!")
			else:
				tg.send_message(f'IP сервера {main().server_name} изменился!\nЛокальный IP: {main().now_ip()}\nВнешний IP: {requests.get("http://ifconfig.me/ip").text}')
				ip = main().now_ip()
		else:
			print("No Enternet Connection!")
