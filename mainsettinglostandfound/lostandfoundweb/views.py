from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.sessions.models import Session
from lostandfoundweb.models import Newuser
from lostandfoundweb.forms import NewuserForm
from lostandfoundweb.models import Storefound
from lostandfoundweb.forms import StorefoundForm
from lostandfoundweb.models import Storelost
from lostandfoundweb.forms import StorelostForm
from lostandfoundweb.models import Storeclaim
from lostandfoundweb.forms import StoreclaimForm
from lostandfoundweb.models import Storematching
from lostandfoundweb.models import Storereturn
import re 
from django.utils.safestring import mark_safe
import json
from django.core.mail import send_mail
from random import randint

#if request.session['logivalue]==True then access page otherwise login first
#sessions and ddu email id validation 

# Create your views here.
def home(request):
    return render(request,"home.html")

def webmainpage(request):
    #try:
    #    if request.session['loginvalue']==True:
    return render(request,"webmainpage.html")
    #except:
    #    return render(request,"home.html")

def login(request):
    return render(request,"login.html")

def signup(request):
    return render(request,"signup.html")

def verifyotp(request):
    otpr = request.POST['otp']
    print(otpr)
    print(request.session['genotp'])
    print(type(otpr))
    print(type(request.session['genotp']))
    #----------------------------if wrong then delete this users data remaining-----------------
    if otpr == str(request.session['genotp']):
        return render(request,"webmainpage.html")
    else:
        delthis=Newuser.objects.get(userid=request.session['sessionuserid'])
        delthis.delete()
        return render(request,"home.html")

def newuser(request):
    #Here we are entering values into the database
    
    if request.method=="POST":
        # userid = request.POST['userid']
        # name = request.POST['name']
        # phoneno = request.POST['phoneno']
        email = request.POST['email']
        print(email[0:10])
        #dduhandlematch='^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        dduhandlematch = '^[a-z0-9]+[\._]?[a-z0-9]+[@]ddu.ac.in$'
        if(re.search(dduhandlematch,email) and email[0:10]==request.POST['userid']):
            # password = request.POST['password']
            form = NewuserForm(request.POST)
            if form.is_valid():
                try:
                    form.save()
                    request.session['loginvalue'] = True
                    request.session['sessionusername'] = request.POST['name']
                    request.session['sessionuserid']=request.POST['userid']
                    #return render(request,"webmainpage.html")
                    listofadd=[]
                    
                    listofadd.append(email)
                    
                    genotp=randint(10000,100000)
                    request.session['genotp']=genotp
                    print(genotp)
                    #Enable to send mail
                    message="This is auto generated mail.Your otp is {otp}.".format(otp=genotp)
                    subject="OTP"
                    send_mail(subject,message,"maradiyakhilan@gmail.com",listofadd,fail_silently=False)
                    return render(request,"getotp.html")
                except:
                    pass
            
        else:
            return render(request,"signup.html")
        
    else:
        form = NewuserForm()

    return render(request,"signup.html",{'form':form})

def checklogin(request):
    #Here we are verifying id & pass
    userid = request.POST['userid']
    password = request.POST['password'] 

    users=Newuser.objects.all()
    flag=0
    for x in users:
        if x.userid==userid:
            if x.password==password:
                request.session['sessionusername'] = x.name
                request.session['sessionuserid']=x.userid
                print(request.session['sessionusername'])
                flag=1
    if flag==1:
        request.session['loginvalue'] = True
        print("flag is 1 so"+str(request.session['loginvalue']))
        return render(request,"webmainpage.html")
    
    return render(request,"login.html")
    
def lostform(request):
    #if request.session.has_key('loginvalue'): then lostform 
    return render(request,"lostform.html")    
    #return render(request,"login.html")

def foundform(request):
    #If response is not post then we return form else we have to store value
    #less secure access apps is active on google account
    if request.method=="POST":
        selectitem1=request.POST['selectitem']
        color1=request.POST['color']
        brand1=request.POST['brand']
        place1=request.POST['place']
        date1=request.POST['date']
        description1=request.POST['description']
        handovername1=request.POST['handovername']
        branchname1=request.POST['branchname']
        print(selectitem1)
        print(color1)
        print(brand1)
        print(place1)
        print(date1)
        print(description1)
        print("Handover :"+handovername1)
        print(branchname1)
        form=StorefoundForm(request.POST,request.FILES)
        
        if form.is_valid():
            #form.save()
            #NOT Enable to send mail
            """listofadd=[]
            alluser=Newuser.objects.filter()
            for x in alluser:
                listofadd.append(x.email) 
            
            #Add the name from request.session to message
            message="This is auto generated mail.The {item} is found of {name}.If anyone have lost then please contact {name1}".format(item=request.POST['selectitem'],name=request.session['sessionusername'],name1=request.session['sessionusername'])
            subject="Regarding lost item"
            send_mail(subject,message,"maradiyakhilan@gmail.com",listofadd,fail_silently=False)"""

            
            print("valid")

            if handovername1=="":
                print("No handover")
                #Set handovername as founder name if self is selected
                handovername1=request.session['sessionusername']
                
                #Set branchname as user ids 
                usr=Newuser.objects.get(userid=request.session['sessionuserid'])
                print(usr.email)
                branchname1=usr.email
                branchname1=branchname1[2:4]
                branchname1=branchname1.upper()
                print(branchname1 +" if self is selected")
                
            
            #Storefound.objects.create(selectitem=selectitem1,color=color1,brand=brand1,place=place1,date=date1,img=request.FILES['img'],description=description1,useridforeignfound=Newuser.objects.get(userid=request.session['sessionuserid']),foundername=request.session['sessionusername'])
            #Storefound.objects.create(selectitem=selectitem1,color=color1,brand=brand1,place=place1,date=date1,img=request.FILES['img'],description=description1,useridforeignfound=Newuser.objects.get(userid=request.session['sessionuserid']),foundername=request.session['sessionusername'],handovername=handovername1)
            Storefound.objects.create(selectitem=selectitem1,color=color1,brand=brand1,place=place1,date=date1,img=request.FILES['img'],description=description1,useridforeignfound=Newuser.objects.get(userid=request.session['sessionuserid']),foundername=request.session['sessionusername'],handovername=handovername1,branchname=branchname1)
            #less secure access apps is active on google account
            
            lost=Storelost.objects.all()
            flag=0
            #Matching with lost items if found then add to matching database
            for x in lost:
                #print(x.selectitem)
                #print(x.date)
                #print(request.POST['date'])
                print(x.useridforeign.userid)
                print(Newuser.objects.get(userid=x.useridforeign.userid).userid)
                if x.selectitem==request.POST['selectitem'] and x.place==request.POST['place'] and str(x.date)==request.POST['date']: #and Newuser.objects.get(userid=x.useridforeign.userid).userid!=request.session['sessionuserid']:
                    print("Entered in this")
                    id=Storefound.objects.filter(useridforeignfound=request.session['sessionuserid']).last().id
                    #print(id)
                    Storematching.objects.create(name=x.selectitem,place=x.place,date=x.date,founditemid=Storefound.objects.get(id=id),lostitemid=Storelost.objects.get(id=x.id))


            return render(request,"thanksforfound.html")
        else:
            print("Not valid")
            return render(request,"foundform.html")
    else:
        return render(request,"foundform.html")

def showlost(request):
    #stl=Storelost.objects.all
    stl=Storelost.objects.values('selectitem','color', 'brand', 'place' ,'date','description','ownername','reward','recievedstatus','lostbranchname')
    #print(stl)
    return render(request,"showlost.html",{'stl':stl})

def showfound(request):
    #print(request.session['loginvalue'])
    #return render(request,"showfound.html",{'stf':stf})
    try:
        if request.session['loginvalue']==True:
            stf=Storefound.objects.all
            print("Logged in")
            return render(request,"showfound.html",{'stf':stf})
    except:
        print("Not logged in")
        return render(request,"home.html")

def storelost(request):
    #Here we are storing lost items
    #less secure access apps is active on google account
    selectitem1=request.POST['selectitem']
    color1=request.POST['color']
    brand1=request.POST['brand']
    place1=request.POST['place']
    date1=request.POST['date']
    description1=request.POST['description']
    reward1=request.POST['reward']
    lostbranch1=request.POST['branchname']
    
    print(selectitem1)
    print(color1)
    print(brand1)
    print(place1)
    print(date1)
    print(description1)
    print(reward1)
    print(lostbranch1)
    if reward1=='':
        reward1=0
    
    if place1=="Library":
        print("Lib")
        lostbranch1="Library"
    elif place1=="CF":
        print("CF")
        lostbranch1="CF"
    elif place1=="Canteen":
        print("Canteen")
        lostbranch1="Canteen"
    elif place1=="Campus":
        print("Campus")
        lostbranch1="Campus"
    
    print("Lost branch is "+lostbranch1)
        

    #Storelost.objects.create(selectitem=selectitem1,color=color1,brand=brand1,place=place1,date=date1,description=description1,useridforeign=request.session['sessionuserid'],ownername=request.session['sessionusername'])
    form=StorelostForm(request.POST)
    #useridforeign=Newuser.objects.get(userid=request.session['sessionuserid'])
    #print(useridforeign.values)
    #ownername=request.session['sessionusername']
    if form.is_valid():
        #form.save()
        print("hello")
        print(request.session['sessionuserid'])
        print(request.session['sessionusername'])
        #Storelost.objects.create(selectitem=selectitem1,color=color1,brand=brand1,place=place1,date=date1,description=description1,useridforeign=Newuser.objects.get(userid=request.session['sessionuserid']),ownername=request.session['sessionusername'])
        #Storelost.objects.create(selectitem=selectitem1,color=color1,brand=brand1,place=place1,date=date1,description=description1,reward=reward1,useridforeign=Newuser.objects.get(userid=request.session['sessionuserid']),ownername=request.session['sessionusername'])
        Storelost.objects.create(selectitem=selectitem1,color=color1,brand=brand1,place=place1,date=date1,description=description1,reward=reward1,useridforeign=Newuser.objects.get(userid=request.session['sessionuserid']),ownername=request.session['sessionusername'],lostbranchname=lostbranch1)
        #NOT Enable to send mail
        """listofadd=[]
        alluser=Newuser.objects.filter()
        for x in alluser:
            listofadd.append(x.email) 
        
        #Add the name from request.session to message
        message="This is auto generated mail.The {item} is lost of {name}.If anyone have founded then please contact {name1}".format(item=request.POST['selectitem'],name=request.session['sessionusername'],name1=request.session['sessionusername'])
        subject="Regarding lost item"
        send_mail(subject,message,"maradiyakhilan@gmail.com",listofadd,fail_silently=False)"""

        #Store if matching Item found

        found=Storefound.objects.all()
        
        for x in found:
            print(x.selectitem)
            print(x.date)
            print(request.POST['date'])
            
            if x.selectitem==request.POST['selectitem'] and x.place==request.POST['place'] and str(x.date)==request.POST['date']:# and Newuser.objects.get(userid=x.useridforeignfound.userid).userid!=request.session['sessionuserid']:
                #print(Newuser.objects.filter(userid=request.session['sessionuserid']))
                #print(x.useridforeignfound.id)
                print(Newuser.objects.get(userid=x.useridforeignfound.userid).userid)
                print(request.session['sessionuserid'])
                               
                id=Storelost.objects.filter(useridforeign=request.session['sessionuserid']).last().id
                print(id)
                Storematching.objects.create(name=x.selectitem,place=x.place,date=x.date,founditemid=Storefound.objects.get(id=x.id),lostitemid=Storelost.objects.get(id=id))
        
        
        return render(request,"thanksforlost.html")
    else:
        print(form.errors)
        return render(request,"lostform.html")
    
def logout(request):
    del request.session['loginvalue']
    return render(request,"home.html")

def profile(request):
    users=Newuser.objects.all()
    sendthisuser=Newuser()
    userid=request.session['sessionuserid']
    for x in users:
        if x.userid==userid:
            print(x.name)
            sendthisuser.userid=request.session['sessionuserid']
            sendthisuser.name=x.name
            sendthisuser.password=x.password
            sendthisuser.email=x.email
            sendthisuser.userid=x.userid
            sendthisuser.phoneno=x.phoneno
    
    stf1=Storefound.objects.all()
    #stf1.filter(useridforeignfound__icontains=request.session['sessionuserid'])
    stf1=Storefound.objects.filter(useridforeignfound=request.session['sessionuserid'])

    stl1=Storelost.objects.all()
    #stl1.filter(useridforeign__icontains=request.session['sessionuserid'])
    stl1=Storelost.objects.filter(useridforeign=request.session['sessionuserid'])

    return render(request,"profilepage.html",{'sendthisuser':sendthisuser,'stf':stf1,'stl':stl1})

def searchlost(request):
    stl1=Storelost.objects.all()
    if request.method=='POST':
        searchlostitem=request.POST['searchlostitem']
        if searchlostitem=="":
            stl1=Storelost.objects.all()
            return render(request,"showlost.html",{'stl':stl1})
        else:        
            #print(searchlostitem)
            stl1=Storelost.objects.all()
            stl1.filter(selectitem__icontains=searchlostitem)
            stl1=Storelost.objects.filter(selectitem=searchlostitem)
            return render(request,"showlost.html",{'stl':stl1})
    else:
        return render(request,"showlost.html",{'stl':stl1})

def searchfound(request):
    stf1=Storefound.objects.all()
    if request.method=='POST':
        searchfounditem=request.POST['searchfounditem']
        if searchfounditem=="":
            stf=Storefound.objects.all()
            return render(request,"showfound.html",{'stf':stf})
        else:
            stf1=Storefound.objects.all()
            stf1.filter(selectitem__icontains=searchfounditem)
            stf1=Storefound.objects.filter(selectitem=searchfounditem)
            return render(request,"showfound.html",{'stf':stf1})
    else:
        return render(request,"showfound.html",{'stf':stf1})

def update(request):
    """print(request.POST['name'],request.POST['email'],request.POST['phoneno'])
    updateuser=Newuser.objects.all()
    updateuser.filter(userid__icontains=request.session['sessionuserid'])
    updateuser=Newuser.objects.get(userid=request.session['sessionuserid'])
    print(updateuser,request.session['sessionuserid'])
    print(updateuser.userid," ",updateuser.name)
    form=NewuserForm(request.POST,instance=updateuser)
    if form.is_valid():
        print("success")
        form.save()
    else:
        
        print(form.errors)
        print("not valid")
    """
    print(request.POST['password'])
    print(request.POST['newpassword'])
    print(request.POST['renewpassword'])

    if request.POST['password']=='':
        print("pass is null")

    if request.method=="POST":
        #Newuser.objects.filter(userid=request.session['sessionuserid']).update(name=request.POST['name'])
        #Newuser.objects.filter(userid=request.session['sessionuserid']).update(email=request.POST['email'])
        #Newuser.objects.filter(userid=request.session['sessionuserid']).update(phoneno=request.POST['phoneno'])
        
        usr=Newuser.objects.get(userid=request.session['sessionuserid'])
        msg=""
        if request.POST['phoneno']!=usr.phoneno:
            Newuser.objects.filter(userid=request.session['sessionuserid']).update(phoneno=request.POST['phoneno'])
            msg+="Phone no updated successfully "
            
        if request.POST['password']!='':
            if usr.password==request.POST['password']:
                if request.POST['newpassword']==request.POST['renewpassword']:
                    Newuser.objects.filter(userid=request.session['sessionuserid']).update(password=request.POST['newpassword'])
                    msg+="Password updated successfully"
                else:
                    msg+="New Entered password must match with reentered entered password"
            else:
                msg+="Password is not correct"
        #Storelost.objects.filter(useridforeign=request.session['sessionuserid']).update(ownername=request.POST['name'])
        #Storefound.objects.filter(useridforeignfound=request.session['sessionuserid']).update(foundername=request.POST['name'])

        sendthisuser=Newuser.objects.get(userid=request.session['sessionuserid'])
        

        stf1=Storefound.objects.all()
        #stf1.filter(useridforeignfound__icontains=request.session['sessionuserid'])
        stf1=Storefound.objects.filter(useridforeignfound=request.session['sessionuserid'])

        stl1=Storelost.objects.all()
        #stl1.filter(useridforeign__icontains=request.session['sessionuserid'])
        stl1=Storelost.objects.filter(useridforeign=request.session['sessionuserid'])

        return render(request,"profilepage.html",{'sendthisuser':sendthisuser,'msg':msg,'stf':stf1,'stl':stl1})

        #return render(request,"profilepage.html",{'sendthisuser':sendthisuser,'msg':msg})
    else:
        return render(request,"webmainpage.html")

# def storefound(request):
#     #Here we are storing found items
#     selectitem=request.POST['selectitem']
#     color=request.POST['color']
#     brand=request.POST['brand']
#     place=request.POST['place']
#     date=request.POST['date']
#     description=request.POST['description']
#     img=request.POST['img']
#     print(selectitem)
#     print(color)
#     print(brand)
#     print(place)
#     print(date)
#     print(description)
#     print(img)
#     return render(request,"showfound.html")

#On the profile page delete lost item uploaded by user
def deletelost(request,id):
    print(Storelost.objects.get(id=id))
    delthis=Storelost.objects.get(id=id)
    delthis.delete()
    users=Newuser.objects.all()
    sendthisuser=Newuser()
    userid=request.session['sessionuserid']
    for x in users:
        if x.userid==userid:
            print(x.name)
            sendthisuser.userid=request.session['sessionuserid']
            sendthisuser.name=x.name
            sendthisuser.password=x.password
            sendthisuser.email=x.email
            sendthisuser.userid=x.userid
            sendthisuser.phoneno=x.phoneno
    
    stf1=Storefound.objects.all()
    #stf1.filter(useridforeignfound__icontains=request.session['sessionuserid'])
    stf1=Storefound.objects.filter(useridforeignfound=request.session['sessionuserid'])

    stl1=Storelost.objects.all()
    #stl1.filter(useridforeign__icontains=request.session['sessionuserid'])
    stl1=Storelost.objects.filter(useridforeign=request.session['sessionuserid'])

    return render(request,"profilepage.html",{'sendthisuser':sendthisuser,'stf':stf1,'stl':stl1})

#On the profile page delete selected found item uploaded by user
def deletefound(request,id):
    print(Storefound.objects.get(id=id))
    
    delthis=Storefound.objects.get(id=id)
    delthis.delete()

    users=Newuser.objects.all()
    sendthisuser=Newuser()
    userid=request.session['sessionuserid']
    for x in users:
        if x.userid==userid:
            print(x.name)
            sendthisuser.userid=request.session['sessionuserid']
            sendthisuser.name=x.name
            sendthisuser.password=x.password
            sendthisuser.email=x.email
            sendthisuser.userid=x.userid
            sendthisuser.phoneno=x.phoneno
    
    stf1=Storefound.objects.all()
    #stf1.filter(useridforeignfound__icontains=request.session['sessionuserid'])
    stf1=Storefound.objects.filter(useridforeignfound=request.session['sessionuserid'])

    stl1=Storelost.objects.all()
    #stl1.filter(useridforeign__icontains=request.session['sessionuserid'])
    stl1=Storelost.objects.filter(useridforeign=request.session['sessionuserid'])

    return render(request,"profilepage.html",{'sendthisuser':sendthisuser,'stf':stf1,'stl':stl1})

def showlostreward(request):
    stl=Storelost.objects.all()
    stl=Storelost.objects.exclude(reward=0)
    return render(request,"showlost.html",{'stl':stl})

def claim(request):
    return render(request,"claimform.html")

def searchclaim(request):
    stf=Storefound.objects.all()
    stf=Storefound.objects.filter(selectitem=request.POST['selectitem'])
    stf=stf.filter(place=request.POST['place'])
    stf=stf.filter(date=request.POST['date'])
    request.session['sessionclaimdetailsemail']=request.POST['claimdetailsemail']
    return render(request,"searchclaim.html",{'stf':stf})

def storeclaim(request,foundid):
    #Send mail and store into claim database and button enable for returnedstatus
    
    listofadd=[]
    stf=Storefound.objects.get(id=foundid)
    
    
    usr=Newuser.objects.get(userid=stf.useridforeignfound.userid)
    print(usr.email)
    listofadd.append(usr.email)
    
    if 'sessionclaimdetailsemail' not in request.session:
        message="This is auto generated mail.{name} is claiming for {item}.Please contact through chat support or any other way .Please verify this user from your side and if valid then after giving item in your profile page press Returned button and enter {id}.".format(name=request.session['sessionusername'],item=stf.selectitem,id=request.session['sessionuserid'])    
    else:
        message="This is auto generated mail.{name} is claiming for {item}.Please contact through chat support or any other way .Please verify this user from your side and if valid then after giving item in your profile page press Returned button and enter {id}.Information from user :{information}".format(name=request.session['sessionusername'],item=stf.selectitem,id=request.session['sessionuserid'],information=request.session['sessionclaimdetailsemail'])    
    #Enable to send mail
    #Add the name from request.session to message
    #message="This is auto generated mail.{name} is claiming for {item}.Please contact through chat support or any other way .Please verify this user from your side and if valid then after giving item in your profile page press Returned button and enter {id}.Information from user :{information}".format(name=request.session['sessionusername'],item=stf.selectitem,id=request.session['sessionuserid'],information=request.session['sessionclaimdetailsemail'])
    subject="Regarding Claiming of item"
    send_mail(subject,message,"maradiyakhilan@gmail.com",listofadd,fail_silently=False)
    
    print(foundid)
    stf=Storefound.objects.get(id=foundid)
    #Enable returned button
    Storefound.objects.filter(id=foundid).update(returnedstatus=1)
    #place,date,itemname,foundername,claimername,claimerid,founditemid,givenstatus
    print(stf.selectitem)
    print(stf.place)
    print(stf.date)

    Storeclaim.objects.create(name=stf.selectitem,place=stf.place,date=stf.date,foundername=stf.foundername,claimername=request.session['sessionusername'],claimerid=Newuser.objects.get(userid=request.session['sessionuserid']),founditemid=Storefound.objects.get(id=foundid))
    return render(request,'thanksforclaim.html')

def showclaim(request):
    stclaim=Storeclaim.objects.all()
    return render(request,"showclaim.html",{'stclaim':stclaim})

def returned(request,foundid):
    
    request.session['founditemid']=foundid
    return render(request,"getclaimerid.html")
        
def returned1(request):
    #Make givenstatus(claim_db) is 1 and returnedstatus as 2(found_db)
    # if request.method=="POST":
    #     Storeclaim.objects.filter(founditemid=foundid).update(givenstatus=1)
        
    #     stclaim=Storeclaim.objects.all()
    #     return render(request,"showclaim.html",{'stclaim':stclaim})
    
        #Storefound.objects.filter(id=foundid).update(returnedstatus=2)
    try:
        Storefound.objects.filter(id=request.session['founditemid']).update(returnedstatus=2)

        Storeclaim.objects.filter(claimerid=Newuser.objects.get(userid=request.POST['claimerid']),founditemid=Storefound.objects.get(id=request.session['founditemid'])).update(givenstatus=1)
        stclaim=Storeclaim.objects.all()
        return render(request,"showclaim.html",{'stclaim':stclaim})
    except:
        m="Please enter correct ID that you recieved in mail."
        return render(request,"getclaimerid.html",{"msg":m})

def showmatching(request):
    sm=Storematching.objects.all()
    sl=Storelost()
    sf=Storefound()
    names=[]
    places=[]
    dates=[]
    rewards=[]
    ownernames=[]
    foundernames=[]
    buttons=[]
    founditemids=[]
    lostitemids=[]
    for x in sm:
        #print(type(x.lostitemid.useridforeign.userid))
        if request.session["sessionuserid"]==x.founditemid.useridforeignfound.userid or request.session["sessionuserid"]==x.lostitemid.useridforeign.userid:
            if request.session["sessionuserid"]==x.founditemid.useridforeignfound.userid:
                buttons.append(0)
            else:
                buttons.append(1)
            #print(x.lostitemid.id)
            #print(type(x.date))
            dates.append(str(x.date))
            names.append(x.name)
            places.append(x.place)
            s=Storelost.objects.get(id=x.lostitemid.id)
            
            lostitemids.append(x.lostitemid.id)
            #print(type(s.reward))
            #print(s.reward)
            rewards.append(s.reward)
            #print(s.ownername)
            ownernames.append(s.ownername)
            f=Storefound.objects.get(id=x.founditemid.id)
            
            founditemids.append(x.founditemid.id)
            #print(f.foundername)
            foundernames.append(f.foundername)
    #print(names)
    newlist=zip(names,places,dates,ownernames,rewards,foundernames,buttons,founditemids,lostitemids)
    return render(request,"showmatching.html",{"newlist":newlist})


def rtnform(request):
    return render(request,"returnform.html")

def searchreturn(request):
    stl=Storelost.objects.all()
    stl=Storelost.objects.filter(selectitem=request.POST['selectitem'])
    stl=stl.filter(place=request.POST['place'])
    stl=stl.filter(date=request.POST['date'])
    request.session['sessionreturndetailsemail']= request.POST['returndetailsemail']
    print(request.POST['returndetailsemail'])
    return render(request,"searchreturn.html",{'stl':stl})
    
def storereturn(request,lostid):
    #Send mail and store into return database and button enable for Recievedstatus
    
    listofadd=[]
    stl=Storelost.objects.get(id=lostid)
    
    
    usr=Newuser.objects.get(userid=stl.useridforeign.userid)
    print(usr.email)
    listofadd.append(usr.email)
    #print(request.session['sessionreturndetailsemail'])
    
    if 'sessionreturndetailsemail' not in request.session:
        message="This is auto generated mail.{name} is founded your {item}.Please contact through chat support or any other way.Please enter ID of this user after recieving item.ID is {id}.".format(name=request.session['sessionusername'],item=stl.selectitem,id=request.session['sessionuserid'])
    else:
        message="This is auto generated mail.{name} is founded your {item}.Please contact through chat support or any other way.Please enter ID of this user after recieving item.ID is {id}. Information from user:{information}".format(name=request.session['sessionusername'],item=stl.selectitem,id=request.session['sessionuserid'],information=request.session['sessionreturndetailsemail'])
    #Enable to send mail
    #Add the name from request.session to message
    #message="This is auto generated mail.{name} is founded your {item}.Please contact through chat support or any other way.Please enter ID of this user after recieving item.ID is {id}. Information from user:{information}".format(name=request.session['sessionusername'],item=stl.selectitem,id=request.session['sessionuserid'],information=request.session['sessionreturndetailsemail'])
    subject="Regarding item founded"
    send_mail(subject,message,"maradiyakhilan@gmail.com",listofadd,fail_silently=False)
    
    print(lostid)
    stl=Storelost.objects.get(id=lostid)
    #Enable recieved button
    Storelost.objects.filter(id=lostid).update(recievedstatus=1)
    #place,date,itemname,foundername,claimername,claimerid,founditemid,givenstatus
    print(stl.selectitem)
    print(stl.place)
    print(stl.date)

    Storereturn.objects.create(name=stl.selectitem,place=stl.place,date=stl.date,ownername=stl.ownername,foundername=request.session['sessionusername'],founderid=Newuser.objects.get(userid=request.session['sessionuserid']),lostitemid=Storelost.objects.get(id=lostid))
    return render(request,'thanksforclaim.html')


def showreturn(request):
    stre=Storereturn.objects.all()
    return render(request,"showreturn.html",{"stre":stre})

def recieved(request,lostid):
    
    request.session['lostitemid']=lostid
    return render(request,"getfounderid.html")

def recieved1(request):
    try:
        Storelost.objects.filter(id=request.session['lostitemid']).update(recievedstatus=2)

        Storereturn.objects.filter(founderid=Newuser.objects.get(userid=request.POST['founderid']),lostitemid=Storelost.objects.get(id=request.session['lostitemid'])).update(givenstatus=1)
        stre=Storereturn.objects.all()
        return render(request,"showreturn.html",{"stre":stre})
        
    except:
        m="Please enter correct ID that you recieved in mail."
        return render(request,"getfounderid.html",{"msg":m})


def room(request, room_name='a'):
    #request.session['sessionuserid']=request.POST['id']
    #request.session['sessionusernme']=request.POST['username']
    print(request.session['sessionuserid'])
    print(request.session['sessionusername'])
    return render(request, 'chat/room.html', {
        'room_name': 'a',
        'username': mark_safe(json.dumps(request.session['sessionusername'])),
        'idofuser': mark_safe(json.dumps(request.session['sessionuserid'])),
    })

