from flask import *
import sendgrid 

sg = sendgrid.SendGridClient('username' ,'password') ##edit this with sendgrid credentials
class course(object):
	def __init__(self, demand , email ):
		self.demand = demand 
		self.email = ''

app = Flask(__name__) 
table = {} 
def update(key): 
	if key in table:
		table[key].demand = table[key].demand + 1
		return str(table[key].demand) 
	else:
		table[key] = course(1,'')
		return "1" 

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/counter', methods=['POST'])
def test(): 
	print 'here'
	print request.form
	key = str(request.form['deptNum'])+str(request.form['course'])+str(request.form['section'])
	print 'there'
	temp = update(key) 
	return temp 
	
@app.route('/<int:demand>')
def home(demand):
	# render stuff
	if demand >= 20:
		section = demand % 20
		message = sendgrid.Mail()
		message.add_to('David <ada80@scarletmail.rutgers.edu>')
		message.set_subject('New Sections Needed')
		message.set_html('Hello, we are writing to inform you that there are currently '+str(demand)+' students waiting for a course in your department.')
		message.set_text('Hello, we are writing to inform you that there are currently '+str(demand)+' students waiting for a course in your department.')
		message.set_from('SPN <spn@rutgers.edu>')
		sg.send(message)
	return jsonify({"demand":demand})

##thanks to vivek for implementation. he helped, but not enough for him to be a contributor lol
app.run(debug=True) 
app = Flask(__name__, static_url_path='')
