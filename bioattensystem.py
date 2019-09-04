import pandas as pd
import numpy as np
import cv2
import csv
import smtplib
import random
import datetime
import face_recognition as fc
z=1
while(z):
    simage={'Imagepath':[r'C:\Users\gourav motwani\Pictures\Camera Roll\abhi1.jpg',r'C:\Users\gourav motwani\Pictures\Camera Roll\gourav1.jpg',r'C:\Users\gourav motwani\Pictures\Camera Roll\sourabh_pic.jpg']}
    df=pd.DataFrame(simage,columns=['Imagepath'])
    export_csv=df.to_csv(r'C:\Users\gourav motwani\Desktop\export_studentimage1.csv',index=None,header=True)
    #print(df)
    d=pd.read_csv(r'C:\Users\gourav motwani\Desktop\export_studentimage1.csv')
    #print(d)
    data=np.array(d)
    a=pd.DataFrame(data)
    #print(a)
    b=a[0]
    #print(b)
    f=[]
    for i in range(0,len(b)):
        #print(i)
        img2=fc.load_image_file(b[i])
        fcen2=fc.face_encodings(img2)[0]
        f.append(fcen2)
        #print(f)
        
    d1=pd.read_csv(r'C:\Users\gourav motwani\Desktop\pandasTOCSV.csv')
    #print(d1)
    data1=np.array(d1)
    c=pd.DataFrame(data1)
    #print(c)
    knowfcnm=list(c[1])
    print(knowfcnm)
    email=list(c[3])
    print(email)
    v=cv2.VideoCapture(0)
    #knowfcnm=["abhi","gourav","sourabh"]
    face_locations=[]
    face_encodings=[]
    face_names=[]
    process_this_frame=True
    presentlist=[]
    currenttime=[]
    def smtp1(em):
        sender='gouravm0908@gmail.com'
        receiver=em
        p=str(random.randint(1000,9999))
        mail=smtplib.SMTP('smtp.gmail.com',587)
        mail.ehlo()#identify computer
        mail.starttls()#transport layer security
        mail.ehlo()
        mail.login(sender,'wjsfyxvxnwidsauo')
        header='To:'+receiver+'\n'+'From:'\
               +sender+'\n'+'subject:Your OTP is \n'
        content=header+p
        mail.sendmail(sender,receiver,content)
        otp=input("enter your otp for attandance:")
        if(otp==p):
            presentlist.append("P")
            d=datetime.datetime.now()
            #d1=d.strftime("%I:%M:%S %P")
            currenttime.append(d)
        else:
            print("please enter correct otp")
        mail.close()

    while(True):
        ret,frame=v.read()
        small_frame=cv2.resize(frame,(0,0),fx=0.25,fy=0.25)
        rgb_small_frame=small_frame[:,:,::-1]
        if(process_this_frame):
            face_locations=fc.face_locations(rgb_small_frame)
            face_encodings= fc.face_encodings(rgb_small_frame,face_locations)
            face_names=[]
            for face_encoding in face_encodings:
                matches=fc.compare_faces(f,face_encoding)
                name="unknown"
                if(True in matches):
                    first_match_index=matches.index(True)
                    name=knowfcnm[first_match_index]
                face_distances=fc.face_distance(f,face_encoding)
                best_match_index=np.argmin(face_distances)
                if(matches[best_match_index]):
                    name=knowfcnm[best_match_index]
                    em=email[best_match_index]
                face_names.append(name)
        process_this_frame=not process_this_frame
        for(top,right,bottom,left),name in zip(face_locations,face_names):
            top*=4
            right*=4
            bottom*=4
            left*=4
            cv2.rectangle(frame,(left,top),(right,bottom),(0,0,255),2)
            cv2.rectangle(frame,(left,bottom-35),(right,bottom),(0,0,255),cv2.FILLED)
            font=cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame,'hello'+name,(left+6,bottom-6),font,1.0,(255,255,255),1)
            if(name in knowfcnm):
                i=knowfcnm.index(name)
                #print("name index is:",i)
                
                
            #em=email[i]
               #print("     ",em)       #cv2.putText(frame,'your otp is send mail',(left+8,bottom-8),font,1.0,(255,255,255),1)
        cv2.imshow('video',frame)
        k=cv2.waitKey(5)
        if(k==ord('q')):
            break
        #if(name in knowfcnm):
           # i=knowfcnm.index(name)
           # print(i)

    print(em)
    smtp1(em)
    print(presentlist)
    print(currenttime)
    A=pd.DataFrame({"NAME":knowfcnm[i],"P/A": presentlist,"Time": currenttime})
    with open(r"C:\Users\gourav motwani\Desktop\admin_atten.csv",'a') as csv_file:
        csv_append = csv.writer(csv_file)
        csv_append.writerow(A.loc[0][["NAME","P/A","Time"]])


    cv2.destroyAllWindows()

