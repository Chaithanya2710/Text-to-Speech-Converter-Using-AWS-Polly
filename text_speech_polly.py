#GUI for T2S converter
import tkinter as tk #Module which provides and crteates gui interface
import boto3#python sdk for aws and it is used to access and connect aws account andservices
import os
import sys
from tempfile import gettempdir
from contextlib import closing


#Create window called root
root=tk.Tk()
root.geometry("400x240")#window size
root.title("T2S-Con Amazon Polly")#window title
textExample=tk.Text(root,height=10)#created text area
textExample.pack()#packing text example to the window


def getText():#name of function and we are going to fetch the text written in the text area
    aws_mag_con=boto3.session.Session(profile_name='demo_user')#first step is to go to amazon management console , creating a session(management console)
    client=aws_mag_con.client(service_name='polly',region_name='us-east-1')#open amazon polly in dashboard
    result=textExample.get("1.0","end")#read from 1st point to end and store in result
    print(result)

    
    response=client.synthesize_speech(Text=result,Engine='neural',OutputFormat='mp3',VoiceId='Joey')#input the result to polly, because to store in result
    print(response)

    if "AudioStream" in response:
        with closing(response['AudioStream']) as stream:
            output= os.path.join(gettempdir(),"speech.mp3")
            try:
                with open(output,"wb") as file:
                    file.write(stream.read())
            except IOError as error:
                print(error)
                sys.exit(-1)
    else:
        print("Could not find the stream!")
        sys.exit(-1)
    if sys.platform=="win32":
        os.startfile(output)

btnRead=tk.Button(root,height=1,width=10,text="Read",command=getText)#button creation in root window that actually converts text to speech
btnRead.pack()#packing button to the vendor

root.mainloop()#keep window open until we close it

#This part is for creating GUI to read text(1)