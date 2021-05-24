# -*- coding: utf-8 -*-


import tkinter as tk
from tkinter import *
from tkinter import Message, Text
import cv2, os
from email.message import EmailMessage
import shutil
import csv
import numpy as np
import PIL
import socket
from PIL import Image, ImageTk
import pandas as pd
import datetime
import re
from tkmacosx import Button
import time
import smtplib, ssl
import tkinter.ttk as ttk
import tkinter.font as font


ts = time.time()
date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
day, month, year = date.split("-")

mont = {'01': 'January',
        '02': 'February',
        '03': 'March',
        '04': 'April',
        '05': 'May',
        '06': 'June',
        '07': 'July',
        '08': 'August',
        '09': 'September',
        '10': 'October',
        '11': 'November',
        '12': 'December'
        }


def tick():
    time_string = time.strftime('%H:%M:%S')
    clock.config(text=time_string)
    clock.after(200, tick)


window = tk.Tk()
window.geometry("1280x720")
window.resizable(True, False)
window.title("Attendance System")
window.configure(background='slate grey')

frame1 = tk.Frame(window, bg="#EBEBEB")
frame1.place(relx=0.11, rely=0.17, relwidth=0.39, relheight=0.80)

frame2 = tk.Frame(window, bg="#EBEBEB")
frame2.place(relx=0.51, rely=0.17, relwidth=0.38, relheight=0.80)

message3 = tk.Label(window, text="Face Recognition Based Attendance System", fg="white", bg="#5271FF", width=50,
                    height=1, font=('Montserrat', 29, ' bold '), justify=CENTER).pack(anchor='center')
# message3.place(x=10, y=10)

frame3 = tk.Frame(window, bg="#c4c6ce")
frame3.place(relx=0.52, rely=0.09, relwidth=0.09, relheight=0.07)

frame4 = tk.Frame(window, bg="#c4c6ce")
frame4.place(relx=0.36, rely=0.09, relwidth=0.16, relheight=0.07)

datef = tk.Label(frame4, text=day + "-" + mont[month] + "-" + year + "  |  ", fg="orange", bg="#262523", width=55,
                 height=1, font=('Montserrat', 22, ' bold '))
datef.pack(fill='both', expand=1)

clock = tk.Label(frame3, fg="orange", bg="#262523", width=55, height=1, font=('Montserrat', 22, ' bold '))
clock.pack(fill='both', expand=1)
tick()

head2 = tk.Label(frame2, text="For New Registrations", fg="black",
                 bg="#EBEBEB", font=('Montserrat', 20, ' bold '), justify = CENTER).pack(anchor='center')
# head2.grid(row=0, column=0)

head1 = tk.Label(frame1, text="For Already Registered", fg="black",
                 bg="#EBEBEB", font=('Montserrat', 20, ' bold '), justify = CENTER).pack(anchor='center')
# head1.place(x=0, y=0)

lbl = tk.Label(frame2, text="Enter ID", width=10, height=1, fg="black",bg="#EBEBEB", font=('Montserrat', 17, ' bold '), justify=LEFT)
lbl.place(x=0, y=55)

txt = tk.Entry(frame2, width=25, fg="black", font=('Montserrat', 15, ' bold '))
txt.place(x=30, y=88)

lbl2 = tk.Label(frame2, text="Enter Name", width=10, height=1, fg="black",bg="#EBEBEB", font=('Montserrat', 17, ' bold '), justify=LEFT)
lbl2.place(x=15, y=140)

txt2 = tk.Entry(frame2, width=25, fg="black", font=('Montserrat', 15, ' bold '))
txt2.place(x=30, y=173)

message = tk.Label(frame2, text="Steps\n1)Take Images\n2)Train Images", bg="white smoke", fg="black", width=30, height=3,
                   activebackground="yellow", font=('Montserrat', 15, ' italic '))
message.place(x=75, y=230)

message = tk.Label(frame2, text="", bg="#5271FF", fg="red", width=25, height=1, activebackground="yellow",
                   font=('Montserrat', 16, ' bold '))
message.place(x=75, y=500)

message2 = tk.Label(frame1, text="Attendance Record", width=60, fg="black", bg="white", height=5,
                    font=('times', 17, ' italic '))
message2.place(x=0, y=200)


def clear():
    txt.delete(0, 'end')
    res = ""
    message.configure(text=res)


def clear2():
    txt2.delete(0, 'end')
    res = ""
    message.configure(text=res)


#
# def clear3():
#     txt2.delete(0, 'end')
#     res = ""
#     message.configure(text=res)


def is_number(roll_num):
    try:
        val = int(roll_num)
    except ValueError:
        return False

    return True


def is_name(name):
    if not all(x.isalpha or x == "" for x in name):
        return False
    else:
        return True


# def is_mail(email):
#     regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
#
#     if re.search(regex, email):
#         return True
#     else:
#         return False
#
# def send_mail(receiver, name, id,time):
#     port = 465
#     sender_email = "visophi.notification@gmail.com"
#     sender_pass = "visophi@123"
#     body = """\
#     Subject: VisoPhi Attendance Marked
#     Dear {}, you have been marked present. Please find the details below- \n
#     ID: {} \nTime: {}""".format(name, id, time)
#     context = ssl.create_default_context()
#
#     with smtplib.SMTP_SSL("smtp@gmail.com", port, context = context) as server:
#         server.login(sender_email,sender_pass)
#         server.sendmail(sender_email,receiver,body)


def TakeImages():
    Id = (txt.get())
    name = (txt2.get())
    # email = (txt3.get())

    if is_number(Id) and is_name(name):
        cam = cv2.VideoCapture(0)
        harcascadePath = "/Users/adityatomar/PycharmProjects/SPM_Project/haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(harcascadePath)
        sample_num = 0
        while (True):
            ret, img = cam.read()  # if frame is read correctly ret is True
            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # convert colour space
            faces = detector.detectMultiScale(gray_img, 1.2, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)  # incrementing sample number
                sample_num = sample_num + 1
                cv2.imwrite(
                    "/Users/adityatomar/PycharmProjects/SPM_Project/TrainingImage/TrainingImage" + name + "." + Id + '.' + str(
                        sample_num) + ".jpg",
                    gray_img[y:y + h, x:x + w])  ## saving the captured face in the dataset folder TrainingImage
                cv2.imshow('frame', img)  # display the frame
            # wait for 100 miliseconds
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            # break if the sample number is more than 60
            elif sample_num > 60:
                break

        cam.release()
        cv2.destroyAllWindows()
        res = "Images Saved for ID : " + Id + " Name : " + name
        row = [Id, name]
        with open('/Users/adityatomar/PycharmProjects/SPM_Project/StudentDetails/StudentDetails.csv',
                  'a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
        message.configure(text=res)
    else:
        if not is_number(Id):
            res = "Enter Numeric Id"
            message.configure(text=res)
        if not is_name(name):
            res = "Enter Alphabetical Name"
            message.configure(text=res)
        # if is_mail(email):
        #     res = "Enter Valid Email"
        #     message.configure(text=res)


def TrainImages():
    recognizer = cv2.face.LBPHFaceRecognizer_create()  # recognizer = cv2.face.LBPHFaceRecognizer_create()#$cv2.createLBPHFaceRecognizer()
    harcascadePath = "/Users/adityatomar/PycharmProjects/SPM_Project/haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(harcascadePath)
    faces, Id = getImagesAndLabels("/Users/adityatomar/PycharmProjects/SPM_Project/TrainingImage")
    recognizer.train(faces, np.array(Id))
    recognizer.save("/Users/adityatomar/PycharmProjects/SPM_Project/TrainingImageLabel/Trainner.yml")
    res = "Image Trained"  # +",".join(str(f) for f in Id)
    message.configure(text=res)


def getImagesAndLabels(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    # print(imagePaths)

    # create empty face list
    faces = []
    # create empty ID list
    Ids = []
    # now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        # loading the image and converting it to gray scale
        pilImage = Image.open(imagePath).convert('L')
        # Now we are converting the PIL image into numpy array
        imageNp = np.array(pilImage, 'uint8', dtype=object)
        # getting the Id from the image
        Id = int(os.path.split(imagePath)[-1].split(".")[1])
        # extract the face from the training image sample
        faces.append(imageNp)
        Ids.append(Id)
    return faces, Ids


def TrackImages():
    recognizer = cv2.face.LBPHFaceRecognizer_create()  # cv2.createLBPHFaceRecognizer()
    recognizer.read(
        "/Users/adityatomar/PycharmProjects/SPM_Project/TrainingImageLabel/Trainner.yml")
    harcascadePath = "/Users/adityatomar/PycharmProjects/SPM_Project/haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath)
    df = pd.read_csv(
        "/Users/adityatomar/PycharmProjects/SPM_Project/StudentDetails/StudentDetails.csv")
    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names = ['Id', 'Name', 'Date', 'Time']
    attendance = pd.DataFrame(columns=col_names)
    while True:
        ret, im = cam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)
        tt = ""

        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (225, 0, 0), 2)
            Id, conf = recognizer.predict(gray[y:y + h, x:x + w])
            if (conf < 50):
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                aa = df.loc[df['Id'] == Id]['Name'].values
                tt = str(Id) + "-" + aa
                attendance.loc[len(attendance)] = [Id, aa, date, timeStamp]

            else:
                Id = 'Unknown'
                tt = str(Id)
                noOfFile = len(os.listdir(
                    "/Users/adityatomar/PycharmProjects/SPM_Project/ImagesUnknown")) + 1
                cv2.imwrite(
                    "/Users/adityatomar/PycharmProjects/SPM_Project/ImagesUnknown/Image" + str(
                        noOfFile) + ".jpg", im[y:y + h, x:x + w])

            cv2.putText(im, str(Id), (x, y + h), font, 2, (255, 255, 255), 2)
        attendance = attendance.drop_duplicates(subset=['Id'], keep='first')
        cv2.imshow('Attendance', im)
        if (cv2.waitKey(1) == ord('q')):
            break

    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
    Hour, Minute, Second = timeStamp.split(":")
    fileName = "/Users/adityatomar/PycharmProjects/SPM_Project/Attendance/Attendance_" + date + "_" + Hour + "-" + Minute + "-" + Second + ".csv"
    attendance.to_csv(fileName, index=False)
    cam.release()
    cv2.destroyAllWindows()
    # print(attendance)
    res = attendance
    message2.configure(text=res)



clearButton = tk.Button(frame2, text="Clear", command=clear, fg='black', bg="#5271FF", width=11,
                        activebackground="white", font=('Montserrat', 11, ' bold '))
clearButton.place(x=335, y=86)
clearButton2 = tk.Button(frame2, text="Clear", command=clear2, fg="black", bg="#5271FF", width=11,
                         activebackground="white", font=('Montserrat', 11, ' bold '))
clearButton2.place(x=335, y=172)

takeImg = tk.Button(frame2, text="TAKE IMAGES", command=TakeImages, fg="black", bg="#5271FF", width=25, height=1,
                    activebackground="grey", font=('Montserrat', 20))
takeImg.place(x=30, y=320)

trainImg = tk.Button(frame2, text="TRAIN IMAGES", command=TrainImages, fg="black", bg="#5271FF", width=25, height=1,
                     activebackground="#5271FF", font=('Montserrat', 20))
trainImg.place(x=30, y=400)

trackImg = tk.Button(frame1, text="TAKE ATTENDANCE", command=TrackImages, fg="black", bg="#5271FF", width=20, height=1,
                     activebackground="#5271FF", font=('Montserrat', 20), justify = CENTER)
trackImg.place(x=120, y=50)

quitWindow = tk.Button(frame1, text="Quit", command=window.destroy, fg="black", bg="red", width=35, height=1,
                       activebackground="white", font=('Montserrat', 15))
quitWindow.place(x=30, y=450)

window.mainloop()
