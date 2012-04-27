#!/usr/bin/env python
from distutils.core import setup

setup(
	name			=	"vimutils",
	version			=	"0.2",
	description		=	"Vim utilities..",
	author			=	"Espen Notodden",
	author_email	=	"enotodden@gmail.com",
	url				=	"http://enotodden.net/vimutils",
	packages		=	[
							'vimutils'
						],
	scripts			=	[
							"vt",
							"ve",
							"vs",
							"vls"
						]
)


