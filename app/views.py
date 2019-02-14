# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import docker
import commands
client = docker.from_env()
# Create your views here.

def index(request):
	containers = client.containers.list(all=True)
	return render(request, 'default/index.html', {"containers": containers, "client": client})
# -------------------------------------- Volume Works --------------------------------------#

def volumes(request):
	c = docker.APIClient()
	volumes = c.volumes()
	volumes = volumes['Volumes']
	return render(request, 'default/volumes.html', {"apiclient": c, "volumes": volumes, "client": client})

def volume_add(request):
	if request.method == "POST":
		custom_command = request.POST.get("custom_command", None)
		if custom_command:
			result = commands.getoutput(custom_command)
			return render(request, 'default/volume_create.html', {"client": client, "result": result, "code": 200})
		else:
			name = request.POST.get("name", None)
			label = request.POST.get("label", None)
			driver = request.POST.get("driver", None)
			options = request.POST.get("options", None)
			command = "docker volume create --name {} --label {} --driver {}".format(name, label, driver)
			if options:
				command += "--opt " + str(options)
			result = commands.getoutput(command)
			return render(request, 'default/volume_create.html', {"client": client, "result": result, "code": 200})


	return render(request, 'default/volume_create.html', {"client": client})

def volume_delete(request, vol_name):
	if vol_name:
		volumes = client.volumes.list()
		volume = client.volumes.get(vol_name)
		result = ""
		try:
			result = volume.remove()
		except Exception as e:
			if "has active endpoints" in str(e):
				return error(request, str(e), "3")
			else:
				return error(request, str(e), "0")
		c = docker.APIClient()
		volumes = c.volumes()
		volumes = volumes['Volumes']				
		return render(request, 'default/volumes.html', {"volumes": volumes, "client": client, "vol_name": vol_name, "code": 200})

# -------------------------------------- Network Works --------------------------------------#
def networks(request):
	networks = client.networks.list()
	return render(request, 'default/networks.html', {"networks": networks, "client": client})

def network_add(request):
	if request.method == "POST":
		command = request.POST.get("command", None)
		if command:
			result = commands.getoutput(command)
			return render(request, 'default/network_create.html', {"client": client, "result": result, "code": 200})

	return render(request, 'default/network_create.html', {"client": client})

def network_delete(request, n_id):
	if n_id:
		networks = client.networks.list()
		network = client.networks.get(n_id)
		name = network.name
		result = ""
		try:
			result = network.remove()
		except Exception as e:
			if "has active endpoints" in str(e):
				return error(request, str(e), "3")
		return render(request, 'default/networks.html', {"networks": networks, "client": client, "code": 200, "net_name": name})

def network_detail(request, n_id):

	networks = client.networks.list()
	if n_id:
		network = client.networks.get(n_id)
		attributes = zip(network.attrs,network.attrs.values())

	return render(request, 'default/network_detail.html', {"network": network, "attributes": attributes, "client": client})

# -------------------------------------- Container Works --------------------------------------#

def containers(request):
	containers = client.containers.list(all=True)
	return render(request, 'default/containers.html', {"containers": containers, "client": client})

def container_detail(request, c_id):

	containers = client.containers.list(all=True)
	if c_id:
		container = client.containers.get(c_id)

	if request.method == "POST" and container:
		action = request.POST.get("action", None)
		if action:
			try:
				if action == "stop":
					result = container.stop()
				elif action == "pause":
					result = container.pause()
				elif action == "kill":
					result = container.kill()
				elif action == "restart":
					result = container.restart()
				elif action == "unpause":
					result = container.unpause()
			except Exception as e:
				return render(request, 'default/containers.html', {"containers": containers, "client": client, "code": 200, "result": str(e)})	

	return render(request, 'default/container_detail.html', {"container": container, "client": client})

def container_add(request):
	# container = client.containers.get(c_id)
	if request.method == "POST":
		command = request.POST.get("command", None)
		if command:
			result = commands.getoutput(command)
			return render(request, 'default/container_create.html', {"client": client, "result": result, "code": 200})

	return render(request, 'default/container_create.html', {"client": client})
"""
def container_detail(request, c_id):

	containers = client.containers.list(all=True)
	if c_id:
		container = client.containers.get(c_id)

	if request.method == "POST" and container:
		action = request.POST.get("action", None)
		if action:
			if action == "stop":
				result = container.stop()
			elif action == "pause":
				result = container.pause()
			elif action == "kill":
				result = container.kill()
			elif action == "restart":
				result = container.restart()
			elif action == "unpause":
				result = container.unpause()				

			return HttpResponseRedirect("/containers")

	return render(request, 'default/container_detail.html', {"container": container, "client": client})	"""

def container_delete(request, c_id):
	if c_id:
		containers = client.containers.list(all=True)
		container = client.containers.get(c_id)
		name = container.name
		result = container.remove()
		return render(request, 'default/containers.html', {"containers": containers, "client": client, "code": 200, "con_name": name})	

def container_start(request, c_id):
	if c_id:
		containers = client.containers.list(all=True)
		container = client.containers.get(c_id)
		try:
			if str(container.status) == "paused":
				result = container.unpause()
			else:
				result = container.start()
		except Exception as e:
			return render(request, 'default/containers.html', {"containers": containers, "client": client, "code": 500, "result": str(e)})	

		return HttpResponseRedirect("/containers")

def container_logs(request, c_id):
	pass

# -------------------------------------- Instruction Works --------------------------------------#

def instruction(request):
	if request.method == "POST":
		command = request.POST.get("command", None)
		if command and command.find("docker") == 0:
			result = commands.getoutput(command)
			return render(request, 'default/instruction.html', {"client": client, "result": result})
		else:
			result = "Wrong Command"
			return render(request, 'default/instruction.html', {"client": client, "result": result})


	return render(request, 'default/instruction.html', {"client": client})

# -------------------------------------- Docker Info --------------------------------------#

def info(request):
	return render(request, 'default/info.html', {"client": client})

def error(request, message="", code="4"):
	return render(request, 'default/error_page.html', {"message": message, "code": code})