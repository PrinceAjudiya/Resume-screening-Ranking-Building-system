import os
from flask import Flask, flash, request, redirect, render_template,url_for
from constants import file_constants as cnst
from processing import resume_matcher
from utils import file_utils
import PyPDF2
import textract
import re
import string
import pandas as pd
import matplotlib.pyplot as plt
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import os

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','docx'])
app = Flask(__name__)
UPLOAD_FOLDER = 'static/UPLOAD_FOLDER'

app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def upload_form():
    return render_template('index.html')

@app.route('/resume_loader.html')
def about():

    #print("yyyyyy--------------------------------")
    #upload_form()
    #print("hello how are yoy-----------------------------------")
    return render_template('resume_loader.html')
@app.route('/index.html')
def home():
    return render_template('index.html')

@app.route('/failure')
def failure():
   return 'No files were selected'

@app.route('/success/<name>')
def success(name):
   return 'Files %s has been selected' %name


@app.route('/predict', methods=['POST', 'GET'])
def chart():
    print("chaartttttttttttttttttttt---------------------------")
    if request.method == 'POST':
        file = request.files['image']
        filename = file.filename
        file_path = os.path.join('static', filename)
        file.save(file_path)
        rsrcmgr = PDFResourceManager()
        retstr = StringIO()
        codec = 'utf-8'
        laparams = LAParams()
        device = TextConverter(rsrcmgr, retstr, laparams=laparams)
        var1 = 'D:\\Sem-7\\SGP\\Resume Ranking\\static\\' + filename
        fp = open(var1, 'rb')
        print(var1)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        text = ''
        for page in PDFPage.get_pages(fp, check_extractable=True):
            interpreter.process_page(page)

        text = retstr.getvalue()
        # Convert all strings to lowercase
        text = text.lower()
        # Remove numbers
        text = re.sub(r'\d+', '', text)
        # Remove punctuation
        text = text.translate(str.maketrans('', '', string.punctuation))
        # Create dictionary with industrial and system engineering key terms by area
        terms = {'programing': ['c', 'c++', 'java', 'python', 'php', 'html',
                                'css', 'javascript', 'go', 'r', 'c#', 'ruby on rails', 'swift', 'vba', 'angular',
                                'data structure & algorithm', 'stack', 'queue', 'tree',
                                'graph', 'linked list', 'hash map', 'sql', 'mysql'],

                 'Data Science': ['python', 'r', 'pandas', 'numpy', 'scipy', 'scikit-learn',
                                  'matplotlib', 'machine learning', 'deep learning', 'natural language processing',
                                  'data analytics', 'data visualizations', 'tabeleau', 'matlab', 'data science',
                                  'java script', 'jquery', 'sql', 'ms excel', 'microsoft excel', 'iot', ],

                 'HR': ['communication skills', 'administrative expert', 'hrm knowledge and expertise', 'Proactivity',
                        'advising', 'coaching', 'recruitment and selection', 'selection',
                        'hris knowledge', 'intercultural sensitivity', 'analytically driven and oriented',
                        'hr reporting skills', 'teamwork', 'ms word', 'ms excel',
                        'powerpoint', 'mba', 'management'],

                 'Advocate': ['ms office', 'english', 'reading', 'writting', 'speaking', 'hindi',
                              'law', 'llb', 'high court', 'supreme court', 'judge', 'criminal law', 'law of torts'
                                                                                                    'the law of contract',
                              'land law', 'property law', 'qquity and trusts'
                                                          'constitutional and administrative law', 'eu law'],

                 'Arts': ['communications', 'operating system', 'bussiness', 'critical thinking',
                          'interpersonal skills',
                          'self-confidence', 'detail-oriented', 'problem-solving', 'communication',
                          'time management', 'ability to take criticism', 'philosophy', 'fine arts', 'psychology'
                                                                                                     'fashion study'],

                 'Web Designing': ['html', 'css', 'javascript', 'php', 'bootstrap', 'angularjs',
                                   'reactjs', 'jquery', 'nodejs', 'python', 'visual studio', 'wordpress',
                                   'react', 'ajax', 'mysql', 'sql', '.net', 'laravel', 'codeigniter', 'yii', 'cakephp',
                                   'c#', 'photoshop'],

                 'Mechanical Engineer': ['machine', 'autocad', 'engineer graphic', 'microsoft office', 'solidwork',
                                         'ansys',
                                         'finite element analysis', 'project management', 'project planning', 'matlab',
                                         'vehicle dynamics',
                                         'optimum tire', 'dynamics', 'physics', 'thermodynamics',
                                         'engineering mechanics',
                                         'solid mechanics', 'fluid mechanics ', 'machine design', 'ic engines'],

                 'Sales': ['communication', 'sales', 'marketing', 'sales and marketing', 'customer sales', 'planning',
                           'strategy', 'client relationship', 'collaboration', 'active listening',
                           'verbal communication',
                           'time management', 'strategic thinking'],

                 'Civil Engineer': ['autocad', 'physics', 'mathematics', 'civil 3D', 'on-site construction',
                                    'reinforced concrete',
                                    'steel design', 'design', 'soil testing', 'analysis reports',
                                    'test building materials', 'construction engineering',
                                    'bridge engineering', 'enviroment engineering'],

                 'Java Developer': ['java', 'springboot', 'spring', 'hibernate', 'java server faces',
                                    'google web toolkit',
                                    'j2ee', 'springmvc', 'jdbc', 'jsf', 'core java',
                                    'servlet', 'vaadin', 'struts', 'blade', 'play',
                                    'grails', 'drop wizard'],

                 'Business Analyst': ['powerbi', 'data', 'tableau', 'analytical skills', 'problem-solving skills',
                                      'requriment gathering',
                                      'ms excel', 'writting report', 'data visualization', 'database', 'blueprint',
                                      'sas', 'spss', 'stata', 'data mining', 'database design',
                                      'process modeling', 'r', 'python'],

                 'Electrical Engineer': ['circuit', 'programmable logic controllers', 'automation', 'physics',
                                         'electronic troubleshooting',
                                         'test engineering', 'transformers', 'c', 'dc machine', 'c++',
                                         'vhdl', 'power engineer', 'hdl', 'raspberry pi'],

                 'Python Developer': ['python', 'flask', 'django', 'web2py', 'pandas', 'numpy',
                                      'machine learning', 'deep learning', 'sckit learn', 'scipy', 'matplotlib',
                                      'sas', 'spss', 'stata', 'data mining', 'database design',
                                      'cubicweb', 'pylon', 'cherrypy'],

                 'DevOps Engineer': ['aws', 'cloud', 'azure', 'gcp', 'ci/cd', 'networking', 'git', 'bitbucket',
                                     'automation', 'sql', 'jenkies'],

                 'Network Security Engineer': ['cisco', 'linux', 'ubntu', 'networking', 'ec-council',
                                               'fundamentaal of networking',
                                               'cryptography', 'internet protocol', 'network security', 'security'],

                 'Database': ['sql', 'mysql', 'firebase', 'mongodb', 'mariadb', 'nosql', 'oracle', 'db2',
                              'database management system', 'sql server'
                                                            'ibm', 'rdms'],

                 'Software Engineer': ['agile', 'waterfall model', 'sdlc model', 'project manager', 'quality assurance',
                                       'scrum master'
                                       'jira', 'selenium', 'testing'],

                 'Blockchain': ['bitcoin', 'block', 'mining', 'blockchain architecture', 'hashcash', 'cryptography',
                                'mist', 'truffle', 'parity'],

                 'Testing': ['selenium', 'quality assurance', 'testing', 'manual testing', 'automation testing',
                             'risk analysis',
                             'white box testing', 'black box testing', 'unit testing', 'ui testing', 'api testing',
                             'frontend testing',
                             'backend testing'],

                 'Content Writer': ['eassy', 'seo', 'fluency of writting', 'knowledge of domain']

                 }
        # Initializie score counters for each area
        programing = 0
        Data_Science = 0
        HR = 0
        Advocate = 0
        Arts = 0
        Web_Designing = 0
        Mechanical_Engineer = 0
        Sales = 0
        Civil_Engineer = 0
        Java_Developer = 0
        Business_Analyst = 0
        Electrical_Engineer = 0
        Python_Developer = 0
        DevOps_Engineer = 0
        Network_Security_Engineer = 0
        Database = 0
        Software_Engineer = 0
        Blockchain = 0
        Testing = 0
        Content_Writer = 0

        # Create an empty list where the scores will be stored
        scores = []
        # Obtain the scores for each area
        for area in terms.keys():

            if area == 'programing':
                for word in terms[area]:
                    if word in text:
                        programing += 1
                scores.append(programing)
                print("Hello")

            elif area == 'Data Science':
                for word in terms[area]:
                    if word in text:
                        Data_Science += 1
                scores.append(Data_Science)

            elif area == 'HR':
                for word in terms[area]:
                    if word in text:
                        HR += 1
                scores.append(HR)

            elif area == 'Advocate':
                for word in terms[area]:
                    if word in text:
                        Advocate += 1
                scores.append(Advocate)

            elif area == 'Arts':
                for word in terms[area]:
                    if word in text:
                        Arts += 1
                scores.append(Arts)

            elif area == 'Web Designing':
                for word in terms[area]:
                    if word in text:
                        Web_Designing += 1
                scores.append(Web_Designing)

            elif area == 'Mechanical Engineer':
                for word in terms[area]:
                    if word in text:
                        Mechanical_Engineer += 1
                scores.append(Mechanical_Engineer)

            elif area == 'Sales':
                for word in terms[area]:
                    if word in text:
                        Sales += 1
                scores.append(Sales)

            elif area == 'Civil Engineer':
                for word in terms[area]:
                    if word in text:
                        Civil_Engineer += 1
                scores.append(Civil_Engineer)

            elif area == 'Java Developer':
                for word in terms[area]:
                    if word in text:
                        Java_Developer += 1
                scores.append(Java_Developer)

            elif area == 'Business Analyst':
                for word in terms[area]:
                    if word in text:
                        Business_Analyst += 1
                scores.append(Business_Analyst)

            elif area == 'Electrical Engineer':
                for word in terms[area]:
                    if word in text:
                        Electrical_Engineer += 1
                scores.append(Electrical_Engineer)

            elif area == 'Python Developer':
                for word in terms[area]:
                    if word in text:
                        Python_Developer += 1
                scores.append(Python_Developer)

            elif area == 'DevOps Engineer':
                for word in terms[area]:
                    if word in text:
                        DevOps_Engineer += 1
                scores.append(DevOps_Engineer)

            elif area == 'Network Security Engineer':
                for word in terms[area]:
                    if word in text:
                        Network_Security_Engineer += 1
                scores.append(Network_Security_Engineer)

            elif area == 'Database':
                for word in terms[area]:
                    if word in text:
                        Database += 1
                scores.append(Database)

            elif area == 'Software_Engineer':
                for word in terms[area]:
                    if word in text:
                        Software_Engineer += 1
                scores.append(Software_Engineer)

            elif area == 'Blockchain':
                for word in terms[area]:
                    if word in text:
                        Blockchain += 1
                scores.append(Blockchain)

            elif area == 'Testing':
                for word in terms[area]:
                    if word in text:
                        Testing += 1
                scores.append(Testing)

            else:
                for word in terms[area]:
                    if word in text:
                        Content_Writer += 1
                scores.append(Content_Writer)
        # Create a data frame with the scores summary
        summary = pd.DataFrame(scores, index=terms.keys(), columns=['score']).sort_values(by='score', ascending=False)
        summary2 = summary[summary['score'] >= 1]

        pie = plt.figure(figsize=(15, 15))
        plt.pie(summary2['score'], labels=summary2.index, autopct='%1.0f%%', shadow=True, startangle=90,
                counterclock=True,radius = 0.5)
        plt.title('Pie Chart\n\n\n')
        plt.axis('equal')
        #plt.show()

        # Save pie chart as a .png file
        pie.savefig('D:\\Sem-7\\SGP\\Resume Ranking\\static\\'+ filename +'.png')
        #output = 'D:\\Sem-7\\SGP\\Pie-chart_Flask\\static\\resume_screening_results.png'
        #l = os.path.join('D:\\Sem-7\\SGP\\Pie-chart_Flask\\static\\', 'resume_screening_results.png')
        #print("---------------------------------------------------------------", l)
        #filename1 = 'D:\\Sem-7\\SGP\\Resume Ranking\\static\\UPLOAD_FOLDER\\resume_screening_results.png'
        filename=filename +'.png'
        # print("---------------------------------------------------------------",full_filename)
        return render_template('index.html', filename=filename)



@app.route('/display/<filename>')
def display_image(filename):
    print("displayyyyyyyyyyyyyyyyyyyyyyyy------------------------")
    print('display_image filename: ' + filename)
    return redirect(url_for('static', filename=filename), code=301)



@app.route('/resume_loader.html', methods=['POST', 'GET'])
def check_for_file():
    print("hello functionnnnnnnnnnnnnnnnnnnnnnnnnn-------------------------------")
    if request.method == 'POST':
        # check if the post request has the file part
        if 'reqFile' not in request.files:
           flash('Requirements document can not be empty')
           return redirect(request.url)

        if 'resume_files' not in request.files:

           flash('Select at least one resume File to proceed further')
           return redirect(request.url)
        file = request.files['reqFile']

        if file.filename == '':
           flash('Requirement document has not been selected')
           return redirect(request.url)


        resume_files = request.files.getlist("resume_files")
        print("Resume Files--------",type(resume_files))
        print(resume_files)

        if len(resume_files) == 0:
            flash('Select atleast one resume file to proceed further')
            return redirect(request.url)

        if ((file and allowed_file(file.filename)) and (len(resume_files) > 0)):
           #filename = secure_filename(file.filename)
           abs_paths = []
           filename = file.filename
           req_document = cnst.UPLOAD_FOLDER+'\\'+filename
           file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

           for resumefile in resume_files:
               filename = resumefile.filename
               #abs_paths.append(cnst.UPLOAD_FOLDER + '\\' + filename)
               abs_paths.append('D:\\Sem-7\\SGP\\Resume Ranking\\static\\UPLOAD_FOLDER' + '\\' + filename)
               resumefile.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))


           result = resume_matcher.process_files(req_document,abs_paths)

           # for file_path in abs_paths:
           #     file_utils.delete_file(file_path)

           return render_template("resume_results.html", result=result)

        else:
           flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
           return redirect(request.url)

if __name__ == "__main__":
    app.run(debug = True)
