class Error(Exception):
	"""Base class for other exceptions"""
	pass
	
class NoSGM(Error):
	"""Raised when the input file is not SGML"""
	pass
	
class breakedCollection(Error):
	"""Raised when the input data does not correspond declaration"""
	pass