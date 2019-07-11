import sublime
import sublime_plugin
import re

def process(content,pattern='todo',fn_identifier='def ',comment_identifier='#'):  #TODO read identifier from config
	function = ''	#TODO make this a stack
	#TODO add similar for class as well
	#TODO look at indentation levels to figure out when a function ends
	todos = []
	for line_id in range(len(content)):
		text = content[line_id].strip()	#removes leading and trailing whitespaces
		if text.find(fn_identifier) != -1:
			function = text[text.find(fn_identifier)+4:text.find('(')]
		l = text.lower().find(pattern)
		if l == -1:
			continue     #TODO figure out way to make this more efficient
		else:   #TODO figure out how to handle empty context, may add fuction name etc like a traceback.
			context = text[:l].strip(comment_identifier).strip() + ((' (in function {})'.format(function))*(len(function)>0))
			if len(context)==0:		#TODO maybe show the next line....
				context = ((" In function {}".format(function))*(len(function)>0))+(("General TODO")*(len(function)==0))

			comment = text[l+4:]
			todos.append('Line {}:\t{} \n {} \n'.format(str(line_id+1),context,comment))
	return todos


class TodoCommand(sublime_plugin.TextCommand): 
	def run(self, edit):   
		s = self.view.substr(sublime.Region(0,self.view.size())).split('\n')  #assign s variable the selected region
		TODOs = process(s)
		currentFolder = "/".join(self.view.file_name().split("/")[:-1])
		fileName = self.view.file_name().split("/")[-1]
		new_contents = "In file {} \n---------- \n{} \n==========".format(fileName,"".join(TODOs))
		try:
			f = open("{}/TODO.txt".format(currentFolder),"r")
			contents = f.read()
			regex = 'In file {} \n---------- \n[\s\S]*? \n=========='.format(fileName)
			if re.search(regex,contents) is None:
				write_to_file = contents + "\n" + new_contents
			else:
				write_to_file = re.sub(regex,new_contents,contents) #TODO eliminate this call
			f.close()
		except:
			write_to_file = new_contents

		with open("{}/TODO.txt".format(currentFolder),"w") as f:
			f.write(write_to_file)


#TODO have a config file to look at comment delimiters, can do it by language	
