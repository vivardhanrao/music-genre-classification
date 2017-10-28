from django.shortcuts import render
from django.shortcuts import redirect

import StringIO
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import RequestContext, loader

import sqlite3
import random


from django.template.context_processors import csrf

from django.urls import reverse

batchsel = ''
sectionsel = ''

#returning to home page
def home(request):
    return render(request, 'home/home.html')

def predict(request):
    if request.method == 'POST':
        track_name = request.POST.get('track_name')
        artist_name = request.POST.get('artist_name')
        #oauth_token = request.POST.get('oauth_token')

        import requests
        import json

        url = "https://accounts.spotify.com/api/token"
        headers = {'Authorization': 'Basic NTU5MDc5YTgzZTFkNGUyNGEwNWYwZDBmYTVjZDNlY2Y6NjlmODNlYjZlYTE2NDU1OWE5NTU1MDU0NDk2ZjQ5ZjY='}
        payloads = {'grant_type':'client_credentials'}

        response = requests.post(url, data = payloads, headers = headers)

        data = json.loads(response.content)

        oauth_token = data['access_token']

        #oauth_token = 'BQATCwlbeAK3lkluleey_NI7i5glzH8054OE1UZuVTOj3Z-QHjc1IjrClZOLwFuWxgU-cR5GxeDaE6-UsUv3TSKfxNA_4BXWIAZUrR-GCX9f2GJkYk3hLHAzFpKZmgMXUFdlmFyIhg'

        if artist_name and not artist_name.isspace():
            query = track_name + ' ' + artist_name
        else:
            query = track_name
            
        url = "https://api.spotify.com/v1/search?q="+query+"&type=track&limit=10"
        auth = 'Bearer ' + oauth_token #'BQCN1FnxEZd2d50gNcXmfcpgbWlQIikTX3m-d_CBqgnfGwFl-nvUyu_Ncj8V8I0A6e3Hh1Kn21kuErNawfXKZPEl47Z3QapATuMAz4UXd3PLGtk4TY2OxbvI_zuh60vVeIZD07vE4A'
        headers = {'Accept':'application/json', 'Authorization':auth}        

        response = requests.get(url, headers = headers)
        
        print(response)
        print(response.content)

        data = json.loads(response.content)

        data2 = ''

        for track in data['tracks']['items']:
            if(artist_name != '' or artist_name != ' ' or artist_name != null):
                if(track['artists'][0]['name'] == artist_name):
                    data2 = data2 + 'Track name: ' + track['name'] + '<br>Artist: ' + track['artists'][0]['name'] + '<br>Spotify ID: ' + track['id'] + '<br><img src='+ track['album']['images'][1]['url'] +'><br>'
                    track_name = track['name']
                    artist_name = track['artists'][0]['name']
                    track_id = track['id']
                    image_url = track['album']['images'][1]['url']
                    break
                else:
                    data2 = data2 + 'Track name: ' + track['name'] + '<br>Artist: ' + track['artists'][0]['name'] + '<br>Spotify ID: ' + track['id'] + '<br><img src='+ track['album']['images'][1]['url'] +'><br>'
                    track_name = track['name']
                    artist_name = track['artists'][0]['name']
                    track_id = track['id']
                    image_url = track['album']['images'][1]['url']
                    break

        url = "https://api.spotify.com/v1/audio-features/"+track_id #?oauth_token=BQAB6v9JImeedLx23_BtFuYTeGQsUlRxafP6x3UuRI4_UsGnKo9OZTzqtdcCYqErXa2CAZ0x9EFA8bmn1aKTnHEJn_p-DXt2b_G0hBIsQ_JbE48pip5qdX2xjVf2cz4HD0A7gabwvg&oauth_signature_method=HMAC-SHA1&oauth_timestamp=1482495679&oauth_nonce=TT0guN&oauth_version=1.0&oauth_signature=ADnD3Y2c/jCs+m1pusXnvEB/

        response = requests.get(url, headers = headers)

        data = json.loads(response.content)

        features = ['danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence']

        features_track = []

        for feature in features:
            features_track.append(data[feature])

        #print(features_track)

        #Load pickled model

        import pickle

        filename = "classifier_model.sav"

        loaded_model = pickle.load(open(filename, 'rb'))

        import numpy as np

        #prediction = loaded_model.predict(np.array([[0.742, 0.476, 0, 0.508, 0.31, 0.0693, 0.929],[0.485, 0.834, 1, 0.0715, 0.0665, 0.28, 0.658],[0.536, 0.721, 0, 0.386, 0.062, 0.824, 0.388],[0.355, 0.0187, 1, 0.055, 0.991, 0.0637, 0.0641]]))
        prediction = loaded_model.predict(features_track)

        for item in prediction:
            genre = str(item)

        #html = "<html><body>"+data2+data3+"</body></html>"

        return render(request, 'home/predict.html', {'image_url':image_url,'track_name':track_name,'track_id':track_id,'artist_name':artist_name,'genre':genre})
        #return HttpResponse(html)

'''
#validating faculty credentials
def faculty1(request):
    if request.method == 'POST':
        faculty_id = request.POST.get('faculty_id')
        password1 = request.POST.get('password')
    
        #faculty login credentials
        import sqlite3

        #Database connection
        conn = sqlite3.connect('cse.db')
        c = conn.cursor()

        id=faculty_id
        password=password1
        #table name of faculty login(id and password)
        tab = "facultyLogin"

        c.execute('select * from ' +tab)
        attdata = c.fetchall()
        i = 0
        for row in attdata:
            if(row[0]==id and row[1]==password):
                i=i+1
        # directing it to the facutly page
        if(i==1):
            return render(request, 'home/faculty.html')
        else:
            return HttpResponse('Login unsuccessful')

# directing it to the student attendance page
def student1(request):
    return render(request, 'home/student.html')

# renders faculty form in home page
def homefaculty(request):
    form = NameForm()
    return render(request, 'home/homefaculty.html', {'form': form})

# renders student form in home page
def homestudent(request):
    return render(request, 'home/homestudent.html')

#rendering faculty page
def faculty(request):
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    from matplotlib.dates import DateFormatter

    percent=50

    #collecting form data
    if request.method == 'POST':
        batchsel = request.POST.get('batch')
        sectionsel = request.POST.get('section')
        optionsel = request.POST.get('option')
        subjectsel = request.POST.get('subjectsel')
        studentsel = request.POST.get('studentsel')

        batch = batchsel
        section = sectionsel
        sub = subjectsel

        #returning response according to the option selected
        if(optionsel=='overall'):
            return overall(batch,section)
        if(optionsel=='subjectwise'):
            return subjectwise(batch,section,sub)
        if(optionsel=='studentwise'):
            return studentwise(batch,section,studentsel)

#rendering image for overall attendance
def overall(a,b):
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    from matplotlib.dates import DateFormatter

    batch = a
    section = b
    
    fig = Figure()

    conn = sqlite3.connect('cse.db')
    c = conn.cursor()

    #accept from web page
    year = batch
    sec = section
    tab = 'cse'+year+sec

    #plotting data 
    roll_no = list()
    no_of_classes_attended = list()
    roll_no1 = list()
    no_of_classes_attended1 = list()

    c.execute('select * from ' +tab)
    attdata = c.fetchall()
    i = 0
    sum=0
    for row in attdata:
        if(i==0):
            for j in range(len(row)-1):
                    sum=sum+row[j+1]
            tot_classes = str(sum)
            i += 1
            sum=0
        else:
            if(i<31):
                var = row[0]
                roll_no.append(var[0:2]+'-'+var[len(var)-2:])
                for j in range(len(row)-1):
                    sum=sum+row[j+1]
                no_of_classes_attended.append(sum)
                i += 1
                sum=0
            else:
                var = row[0]
                roll_no1.append(var[0:2]+'-'+var[len(var)-2:])
                for j in range(len(row)-1):
                    sum=sum+row[j+1]
                no_of_classes_attended1.append(sum)
                i+= 1
                sum=0


    #calculate 75%
    p75=75*int(tot_classes)/100

    #calculate 65%
    p65=65*int(tot_classes)/100

    #calculate 50%
    p50=50*int(tot_classes)/100

    #create subplots
    fig= Figure()
    ax1=fig.add_subplot(211)
    ax2=fig.add_subplot(212)

    #BAR GRAPH 1
    bar_width = 0.4
    x_pos = np.arange(len(roll_no))
    ax1.bar(x_pos + bar_width, no_of_classes_attended,color='midnightblue',align='center')
    ax1.set_xticks(x_pos + bar_width)
    ax1.set_xticklabels(roll_no,rotation=30)
    ax1.set_ylabel('NUMBER OF CLASSES\n')


    #writing inside the bar
    x=0
    for i in no_of_classes_attended:
        ax1.text(x + bar_width,i-15,str(i),horizontalalignment='center',verticalalignment='center', color="white",clip_on=True)
        x=x+1;

    #BAR GRAPH 2
    bar_width = 0.4
    x_pos = np.arange(len(roll_no1))
    ax2.bar(x_pos + bar_width, no_of_classes_attended1,color='midnightblue',align='center')
    ax2.set_xticks(x_pos + bar_width)
    ax2.set_xticklabels(roll_no1,rotation=30)
    ax2.set_ylabel('NUMBER OF CLASSES\n')
    ax2.set_xlabel('\nHALLTICKET NUMBERS')

    #writing inside the bar
    x=0
    for i in no_of_classes_attended1:
        ax2.text(x + bar_width,i-15,str(i),horizontalalignment='center',verticalalignment='center', color="white",clip_on=True)
        x=x+1;
        
    #green line
    ax1.axhline(y=p75, linewidth=2, color='green')
    ax2.axhline(y=p75, linewidth=2, color='green')

    #yellow line
    ax1.axhline(y=p65, linewidth=2, color='gold')
    ax2.axhline(y=p65, linewidth=2, color='gold')

    #red line
    ax1.axhline(y=p50, linewidth=2, color='red')
    ax2.axhline(y=p50, linewidth=2, color='red')

    ax1.set_title('BAR CHART OF ATTENDANCE OF STUDENTS\n')

    #ax.grid(True)
    #fig = matplotlib.pyplot.gcf()
    fig.set_size_inches(20, 10.5, forward=True)

    canvas = FigureCanvas(fig)
    response = HttpResponse(content_type='image/png')

    canvas.print_png(response)
    canvas.print_figure('home/static/home/graphs/clstot.png')

    return response

#rendering image for a single student's attendance
def student(request):

    percent=50
    if request.method == 'POST':
        hallt = request.POST.get('hallticket')
        batch = request.POST.get('batch')
        section = request.POST.get('section')
        
        studentsel = hallt

        #Database connection
        conn = sqlite3.connect('cse.db')
        c = conn.cursor()

        #accept from web page
        roll=hallt
        year=batch
        sec=section
        
        #Calculations
        #make table name
        tab = 'cse'+year+sec

        #extract all classes for the particular student
        c.execute("select * from "+tab+" where htno='"+roll+"'")
        attdata = c.fetchall()

        #caluculate sum of all classes
        sum=0.0
        for row in attdata:
            j=1
            for i in row:
                if(j==1):
                    j=2
                    continue
                sum=sum+i
                   
        #extract total classes in all subjects
        c.execute("select * from "+tab+" where htno='total'")
        attdata = c.fetchall()

        #calculate sum of total classes held
        tsum=0.0
        for row in attdata:
            j=1
            for i in row:
                if(j==1):
                    j=2
                    continue
                tsum=tsum+i
                
        #calculate attendance percentage
        percent1=round(((sum/tsum)*100),2)

        #print percent

        #html = "<html><body><h1>%s</h1></body></html>" % str(percent)

        #Establishing the connection
        year = batch
        sec = section
        tab = 'cse'+year+sec
        name='daa'
        conn = sqlite3.connect('cse.db')
        c = conn.cursor()
        cursor = conn.execute('select * from '+tab)
        sub_name=list()
        sub_name = [description[0] for description in cursor.description]
        indexvalue = sub_name.index(name)
        sub_name.remove(name)
        sub_name.remove('htno')
        sub_name = [name] + sub_name
        roll=studentsel

        #Generating number of the classes lists
        classes =list()
        tot_class =list()
        c.execute('select * from ' +tab+ ' where htno=\''+roll+'\'')
        attdata = c.fetchall()
        for row in attdata:
            row = list(row)
            subatt = row.pop(indexvalue)
            row.pop(0)
            classes = row
            classes = [subatt] + classes
        c.execute('select * from ' +tab+ ' where htno=\'total\'')
        attdata = c.fetchall()
        for row in attdata:
            row = list(row)
            totsubatt = row.pop(indexvalue)
            row.pop(0)
            tot_class = row
            tot_class = [totsubatt] + tot_class

        #create percentage list
        percent=list()
        for i in range(0,len(tot_class)):
            p=round(((float(classes[i])/float(tot_class[i]))*100),1)
            percent.append(p)

        #create lables and explode values for pie chart
        explode=[0.1]    
        labels=list()
        for i in range(0,len(percent)): 
            labels.append(sub_name[i]+'\n('+str(percent[i])+'%)')
            if(i==0):continue
            explode.append(0)
           

        colors = ['yellowgreen', 'lightcoral','gold','lightblue','plum']        

        #pie chart
        plt.pie(percent, labels=labels, colors=colors, shadow=True, startangle=90)
                
        # Set aspect ratio to be equal so that pie is drawn as a circle.
        plt.axis('equal')
        #title
        S='COMPARISION OF CLASSES ATTENDED BY STUDENT '+roll+'\nIN ALL SUBJECTS \n\n'
        plt.title(S)
        plt.tight_layout()
        #plt.show()

        savefig('home/static/home/graphs/stutot.png', transparent="True")

        plt.cla()
        plt.clf()
        
    return render(request, 'home/student.html', {'perstu':percent1,'clsatt':sum,'totatt':tsum})

#rendering image for subjectwise attendance
def subjectwise(a,b,c):
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    from matplotlib.dates import DateFormatter

    batch = a
    section = b
    sub = c

    fig = Figure()

    conn = sqlite3.connect('cse.db')
    c = conn.cursor()

    #accept from web page
    year = batch
    sec = section
    subject = sub
    tab = 'cse'+year+sec

    #plotting data 
    roll_no = list()
    no_of_classes_attended = list()
    roll_no1 = list()
    no_of_classes_attended1 = list()

    c.execute('select htno, ' +subject+' from ' +tab)
    attdata = c.fetchall()
    i = 0
    for row in attdata:
        if(i==0):
            tot_classes = str(row[1])
            i += 1
        else:
            if(i<31):
                var = row[0]
                roll_no.append(var[0:2]+'-'+var[len(var)-2:])
                no_of_classes_attended.append(row[1])
                i += 1
            else:
                var = row[0]
                roll_no1.append(var[0:2]+'-'+var[len(var)-2:])
                no_of_classes_attended1.append(row[1])
                i+= 1
    c.close()
    conn.close()

    #calculate 75%
    p75=75*int(tot_classes)/100

    #calculate 65%
    p65=65*int(tot_classes)/100

    ax1=fig.add_subplot(211)
    ax2=fig.add_subplot(212)

    #BAR GRAPH 1
    bar_width = 0.4
    x_pos = np.arange(len(roll_no))
    ax1.bar(x_pos + bar_width, no_of_classes_attended,color='midnightblue',align='center')
    ax1.set_xticks(x_pos + bar_width)
    ax1.set_xticklabels(roll_no,rotation=30)
    ax1.set_ylabel('NUMBER OF CLASSES\n')

    #writing inside the bar
    x=0
    for i in no_of_classes_attended:
        ax1.text(x + bar_width,i-2,str(i),horizontalalignment='center',verticalalignment='center', color="white",clip_on=True)
        x=x+1;

    #BAR GRAPH 2
    bar_width = 0.4
    x_pos = np.arange(len(roll_no1))
    ax2.bar(x_pos + bar_width, no_of_classes_attended1,color='midnightblue',align='center')
    ax2.set_xticks(x_pos + bar_width)
    ax2.set_xticklabels(roll_no1,rotation=30)
    ax2.set_ylabel('NUMBER OF CLASSES\n')
    ax2.set_xlabel('\nHALLTICKET NUMBERS')

    #writing inside the bar
    x=0
    for i in no_of_classes_attended1:
        ax2.text(x + bar_width,i-2,str(i),horizontalalignment='center',verticalalignment='center', color="white",clip_on=True)
        x=x+1;

    #green line
    s=tot_classes+"\n100%"
    ax1.axhline(y=int(tot_classes), linewidth=2, color='green',label="")
    ax2.axhline(y=int(tot_classes), linewidth=2, color='green',label="")

    #yellow line
    ax1.axhline(y=p75, linewidth=2, color='gold')
    ax2.axhline(y=p75, linewidth=2, color='gold')

    #red line
    ax1.axhline(y=p65, linewidth=2, color='red')
    ax2.axhline(y=p65, linewidth=2, color='red')

    #plt.legend(('green','gold','red'), ('100%', '75%','60%'))
    roman={'13':'IV','14':'III','15':'II','16':'I'}
    ax1.set_title('ATTENDANCE OF '+roman[batch]+' CSE '+section.upper()+' IN '+subject.upper()+'\n')



    #ax.grid(True)
    #fig = matplotlib.pyplot.gcf()
    fig.set_size_inches(20, 10.5, forward=True)

    canvas = FigureCanvas(fig)
    response = HttpResponse(content_type='image/png')

    canvas.print_png(response, transparent="True")
    canvas.print_figure('home/static/home/graphs/clssub.png')

    return response
    
#rendering image for studentwise attendance
def studentwise(a,b,c):
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    from matplotlib.dates import DateFormatter

    batch = a
    section = b
    studentsel = c.upper()
    

    #Establishing the connection
    year = batch
    sec = section
    tab = 'cse'+year+sec
    name='daa'
    conn = sqlite3.connect('cse.db')
    c = conn.cursor()
    cursor = conn.execute('select * from '+tab)
    sub_name=list()
    sub_name = [description[0] for description in cursor.description]
    indexvalue = sub_name.index(name)
    sub_name.remove(name)
    sub_name.remove('htno')
    sub_name = [name] + sub_name
    roll=studentsel

    #Generating number of the classes lists
    classes =list()
    tot_class =list()
    c.execute('select * from ' +tab+ ' where htno=\''+roll+'\'')
    attdata = c.fetchall()
    for row in attdata:
        row = list(row)
        subatt = row.pop(indexvalue)
        row.pop(0)
        classes = row
        classes = [subatt] + classes
    c.execute('select * from ' +tab+ ' where htno=\'total\'')
    attdata = c.fetchall()
    for row in attdata:
        row = list(row)
        totsubatt = row.pop(indexvalue)
        row.pop(0)
        tot_class = row
        tot_class = [totsubatt] + tot_class

    #create percentage list
    percent=list()
    for i in range(0,len(tot_class)):
        p=round(((float(classes[i])/float(tot_class[i]))*100),1)
        percent.append(p)

    #create lables and explode values for pie chart
    explode=[0.1]    
    labels=list()
    for i in range(0,len(percent)): 
        labels.append(sub_name[i]+'\n('+str(percent[i])+'%)')
        if(i==0):continue
        explode.append(0)
       

    colors = ['yellowgreen', 'lightcoral','gold','lightblue','plum']    

    #pie chart
    plt.pie(percent, labels=labels, colors=colors, shadow=True, startangle=90)
            
    # Set aspect ratio to be equal so that pie is drawn as a circle.
    plt.axis('equal')
    #title
    S='COMPARISION OF CLASSES ATTENDED BY STUDENT '+roll+'\nIN ALL SUBJECTS \n\n'
    plt.title(S)
    plt.tight_layout()
    #plt.show()

    response = HttpResponse(content_type="image/jpeg")
    savefig(response)

    plt.cla()
    plt.clf()

    return response
'''
