import sublime
import sublime_plugin
import re
import json

config_path = 'TODO_config.json'
def process(content,pattern='todo',done_pattern='DONE',fn_identifier='def ',comment_identifier='#'):  #TODO read identifier from config
	function = ''   #TODO make this a stack
	#TODO add similar for class as well
	#TODO look at indentation levels to figure out when a function ends
	todos = []
	view = content
	content = content.split('\n')
	for line_id in range(len(content)):
		text = content[line_id].strip() #removes leading and trailing whitespaces
		if text.find(fn_identifier) != -1:
			function = text[text.find(fn_identifier)+4:text.find('(')]
		l = text.lower().find(pattern)

		if l == -1:
			continue     #TODO figure out way to make this more efficient
		else:   #TODO figure out how to handle empty context, may add fuction name etc like a traceback.
			context = text[:l].strip(comment_identifier).strip() + ((' (in function {})'.format(function))*(len(function)>0))
			if len(context)==0:     #TODO maybe show the next line....
				context = ((" In function {}".format(function))*(len(function)>0))+(("General TODO")*(len(function)==0))

			comment = text[l+4:]
			if comment.find(done_pattern) != -1:  #TODO somehow change the original file to delete the comment
				view.replace(text,context)
				continue
			todos.append('Line {}:{} \n {} \n\n'.format(str(line_id+1),context,comment))
	return todos,view


class TodoCommand(sublime_plugin.TextCommand): 
	def run(self, edit):   
		#config = json.load(open(config_path,'r'))
		s = self.view.substr(sublime.Region(0,self.view.size()))  
		TODOs,new_text = process(s)
		print(self.view.file_name())
		currentFolder = "/".join(self.view.file_name().split("/")[:-1])
		fileName = self.view.file_name().split("/")[-1]
		new_contents = "In file {} \n---------- \n{} \n==========".format(fileName,"".join(TODOs))
		try:
			f = open("{}/{}".format(currentFolder,"TODO.txt"),"r")
			contents = f.read()
			regex = 'In file {} \n---------- \n[\s\S]*? \n=========='.format(fileName)
			if re.search(regex,contents) is None:
				write_to_file = contents + "\n" + new_contents
			else:
				write_to_file = re.sub(regex,new_contents,contents) #TODO eliminate this call -- DONE
			f.close()
		except FileNotFoundError:
			write_to_file = new_contents

		with open("{}/{}".format(currentFolder,"TODO.txt"),"w") as f:
			f.write(write_to_file)
		self.view.replace(edit,sublime.Region(0,self.view.size()),new_text)
#TODO have a config file to look at comment delimiters, can do it by language   
