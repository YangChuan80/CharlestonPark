import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import tkinter.font as tkf
import sqlite3
import datetime

DB_file = 'Samples_DB.sqlite'
conn = sqlite3.connect(DB_file)
cur = conn.cursor()

sqlstr = '''SELECT *
FROM Samples JOIN Patients ON Samples.patient_id = Patients.id_in_patients
ORDER BY Samples.id_in_samples
'''
spreadsheet = cur.execute(sqlstr)

combination = []
for row in spreadsheet:
    combination.append(row)

cur.execute('SELECT * FROM Samples')
headers_samples = [item[0] for item in cur.description]

cur.execute('SELECT * FROM Patients')
headers_patients = [item[0] for item in cur.description]

headers = headers_samples + headers_patients

## Helper functions
#### Table related

def OnDoubleClick(event):
    global idglb
    try:
        item = table.selection()[0]
        value = table.item(item, 'values')    
        iden = value[0]
        ExtractID(iden)     
        idglb = iden
        
    except:
        pass

def sortby(tree, col, descending):
    """sort tree contents when a column header is clicked on"""
    # grab values to sort
    data = [(tree.set(child, col), child) for child in tree.get_children('')]
    # if the data to be sorted is numeric change to float
    #data =  change_numeric(data)
    # now sort the data in place
    data.sort(reverse=descending)
    for ix, item in enumerate(data):
        tree.move(item[1], '', ix)
    # switch the heading so it will sort in the opposite direction
    tree.heading(col, command=lambda col=col: sortby(tree, col, int(not descending)))

#### Function related

def refreshDB():
    global conn, cur, desc, headers, combination
    conn.close()
    conn = sqlite3.connect(DB_file)
    cur = conn.cursor()

    cur.execute('SELECT * FROM Samples')
    headers_samples = [item[0] for item in cur.description]

    cur.execute('SELECT * FROM Patients')
    headers_patients = [item[0] for item in cur.description]
    
    headers = headers_samples + headers_patients
    
    sqlstr = '''SELECT * FROM Samples JOIN Patients 
    ON Samples.patient_id = Patients.id_in_patients
    ORDER BY Samples.id_in_samples
    '''
    spreadsheet = cur.execute(sqlstr)

    combination = []
    for row in spreadsheet:
        combination.append(row)

def ExtractID(iden): 
    sqlstr = '''SELECT * FROM Samples 
    JOIN Patients ON Samples.patient_id = Patients.id_in_patients 
    WHERE Samples.id_in_samples = ?    
    '''
    cur.execute(sqlstr, (iden,))
    rowSelected = cur.fetchone()
    
    item = {}    
    for i in range(len(rowSelected)):
        item[headers[i]] = rowSelected[i]
    display_in_text(item)

def display_in_table(combination):
    for row in combination:
        table.insert("", "end", "", values=row)
    num = str(len(combination))
    text_num.delete('1.0', tk.END)
    text_num.insert('1.0', num)

def display_in_text(item):
    
    # //// Samples ///////////////////////////////
    
    text_id_in_samples.delete('1.0', tk.END)
    text_id_in_samples.insert('1.0', item['id_in_samples'])
    
    text_RackNumber.delete('1.0', tk.END)
    text_RackNumber.insert('1.0', item['RackNumber'])  
    
    text_SampleType.delete('1.0', tk.END)
    text_SampleType.insert('1.0', item['SampleType'])
    
    text_SampleID.delete('1.0', tk.END)
    text_SampleID.insert('1.0', item['SampleID'])
    
    text_SampleStatus.delete('1.0', tk.END)
    text_SampleStatus.insert('1.0', item['SampleStatus'])
    
    text_PatientName_in_samples.delete('1.0', tk.END)
    text_PatientName_in_samples.insert('1.0', item['PatientName_in_samples'])
    
    text_Samples_patient_id.delete('1.0', tk.END)
    text_Samples_patient_id.insert('1.0', item['patient_id'])
    
    # //// Patients ///////////////////////////////
    
    text_id_in_patients.delete('1.0', tk.END)
    text_id_in_patients.insert('1.0', item['id_in_patients'])
    
    text_PatientName_in_patients.delete('1.0', tk.END)
    text_PatientName_in_patients.insert('1.0', item['PatientName_in_patients'])
    
    text_InPatientID.delete('1.0', tk.END)
    text_InPatientID.insert('1.0', item['InPatientID'])
    
    text_CitizenID.delete('1.0', tk.END)
    text_CitizenID.insert('1.0', item['CitizenID'])
    
    text_BirthDate.delete('1.0', tk.END)
    text_BirthDate.insert('1.0', item['BirthDate'])  
    
    text_Gender.delete('1.0', tk.END)
    text_Gender.insert('1.0', item['Gender'])   
    
    text_PatientName_CN.delete('1.0', tk.END)
    text_PatientName_CN.insert('1.0', item['PatientName_CN'])
        
    text_ProbandName.delete('1.0', tk.END)
    text_ProbandName.insert('1.0', item['ProbandName'])
    
    text_proband_id.delete('1.0', tk.END)
    text_proband_id.insert('1.0', item['proband_id'])
    
    text_RelationshipOfProband.delete('1.0', tk.END)
    text_RelationshipOfProband.insert('1.0', item['RelationshipOfProband'])
    
    text_Telephone.delete('1.0', tk.END)
    text_Telephone.insert('1.0', item['Telephone'])
    
    text_Comments.delete('1.0', tk.END)
    text_Comments.insert('1.0', item['Comments'])
    
    text_Diagnosis1.delete('1.0', tk.END)
    text_Diagnosis1.insert('1.0', item['Diagnosis1'])
    
    text_Diagnosis2.delete('1.0', tk.END)
    text_Diagnosis2.insert('1.0', item['Diagnosis2'])
    
    text_Diagnosis3.delete('1.0', tk.END)
    text_Diagnosis3.insert('1.0', item['Diagnosis3'])
    
    text_Diagnosis4.delete('1.0', tk.END)
    text_Diagnosis4.insert('1.0', item['Diagnosis4'])
    
    text_Diagnosis5.delete('1.0', tk.END)
    text_Diagnosis5.insert('1.0', item['Diagnosis5'])  

def clear():
    for i in table.get_children():
        table.delete(i)

def browse():
    clear()
    refreshDB()
    display_in_table(combination)

def samples():    
    cur.execute('SELECT * FROM Samples')
    headers_samples = [item[0] for item in cur.description]
        
    sqlstr = 'SELECT * FROM Samples ORDER BY id_in_samples'
    spreadsheet = cur.execute(sqlstr)
    combination = []        
    for row in spreadsheet:
        combination.append(row)
    
    def OnDoubleClick_Samples(event):
        global idglb
        try:
            item = table.selection()[0]
            value = table.item(item, 'values')    
            iden = value[0]
            ExtractID(iden)     
            idglb = iden

        except:
            pass
        
    def ExtractID(iden): 
        sqlstr = 'SELECT * FROM Samples WHERE id_in_samples = ?'
        cur.execute(sqlstr, (iden,))
        rowSelected = cur.fetchone()

        item = {}    
        for i in range(len(rowSelected)):
            item[headers[i]] = rowSelected[i]
        display_in_text(item)
        
    def display_in_table(combination):
        for row in combination:
            table.insert("", "end", "", values=row)
        
    def display_in_text(item):  
        text_id_in_samples.delete('1.0', tk.END)
        text_id_in_samples.insert('1.0', item['id_in_samples'])

        text_RackNumber.delete('1.0', tk.END)
        text_RackNumber.insert('1.0', item['RackNumber'])  

        text_SampleType.delete('1.0', tk.END)
        text_SampleType.insert('1.0', item['SampleType'])

        text_SampleID.delete('1.0', tk.END)
        text_SampleID.insert('1.0', item['SampleID'])

        text_SampleStatus.delete('1.0', tk.END)
        text_SampleStatus.insert('1.0', item['SampleStatus'])

        text_PatientName_in_samples.delete('1.0', tk.END)
        text_PatientName_in_samples.insert('1.0', item['PatientName_in_samples'])

        text_Samples_patient_id.delete('1.0', tk.END)
        text_Samples_patient_id.insert('1.0', item['patient_id'])
        
    def update_samples():
        try:        
            text_id_in_samples_gotten = text_id_in_samples.get('1.0', tk.END).rstrip()        
            RackNumber_gotten = text_RackNumber.get('1.0', tk.END).rstrip()
            SampleID_gotten = text_SampleID.get('1.0', tk.END).rstrip()
            SampleType_gotten = text_SampleType.get('1.0', tk.END).rstrip()
            SampleStatus_gotten = text_SampleStatus.get('1.0', tk.END).rstrip()
            PatientName_in_samples_gotten = text_PatientName_in_samples.get('1.0', tk.END).rstrip()
            Samples_patient_id_gotten = text_Samples_patient_id.get('1.0', tk.END).rstrip()       

            Question_mark = '(' + '?, ' * 6 + '?)'

            cur.execute('DELETE FROM Samples WHERE id_in_samples = ?', (text_id_in_samples_gotten,))        
            conn.commit()

            Update_values = (text_id_in_samples_gotten, 
                             RackNumber_gotten, 
                             SampleID_gotten, 
                             SampleType_gotten, 
                             SampleStatus_gotten, 
                             PatientName_in_samples_gotten,
                             Samples_patient_id_gotten)

            Update_Fields = '''(
            id_in_samples, 
            RackNumber, 
            SampleID, 
            SampleType, 
            SampleStatus, 
            PatientName_in_samples, 
            patient_id)
            '''

            #cur.execute('INSERT INTO BloodSamples (SampleID, PatientName, SampleType) VALUES (?, ?, ?)', 
            #('201706181718000444', 'PatientName, 'Serum'))

            cur.execute('INSERT INTO Samples '+ Update_Fields + ' VALUES ' + Question_mark, 
                        Update_values)
            conn.commit()  

            #messagebox.showinfo("Updated", "Sample information successfully updated!") 
            
            # //////////////////// Refresh the Table ///////////////////////////////////////////////////
            # Clear the table
            for i in table.get_children():
                table.delete(i)

            # Refresh the whole database
            refreshDB()

            # Refresh variable combination

            sqlstr = 'SELECT * FROM Samples ORDER BY id_in_samples'
            spreadsheet = cur.execute(sqlstr)
            combination = []        
            for row in spreadsheet:
                combination.append(row)
                
            # Display the table
            display_in_table(combination)

        except:
            pass
    
    def delete_sample():
        id_in_samples_gotten = text_id_in_samples.get('1.0', tk.END).rstrip()
    
        if id_in_samples_gotten == '':
            messagebox.showinfo("Empty", "There's no sample to delete. Please make sure.")

        else:           
            result = messagebox.askquestion('Delete', 'Are you sure to delete this sample?', 
                                            icon='warning')

            if result == 'yes':
                cur.execute('DELETE FROM Samples WHERE id_in_samples = ?', (id_in_samples_gotten,))        
                conn.commit()            
                messagebox.showinfo("Deleted", "Sample has been deleted!")
                
                # //////////////////// Refresh the Table ///////////////////////////////////////////////////
                # Clear the table
                for i in table.get_children():
                    table.delete(i)
                
                # Refresh the whole database
                refreshDB()
                
                # Refresh variable combination
                
                sqlstr = 'SELECT * FROM Samples ORDER BY id_in_samples'
                spreadsheet = cur.execute(sqlstr)
                combination = []        
                for row in spreadsheet:
                    combination.append(row)
                    
                # Display the table        
                display_in_table(combination)

    
    # /////// Main Flow ////////////////////////////

    root_samples = tk.Tk()    
    
    w = 1200 # width for the Tk root
    h = 730 # height for the Tk root

    # get screen width and height
    ws = root_samples.winfo_screenwidth() # width of the screen
    hs = root_samples.winfo_screenheight() # height of the screen

    # calculate x and y coordinates for the Tk root window
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)

    # set the dimensions of the screen 
    # and where it is placed
    root_samples.geometry('%dx%d+%d+%d' % (w, h, x, y))   
    root_samples.title('Samples')  
    
    # /////// Multicolumn Listbox /////////////////////////
    table = ttk.Treeview(root_samples, height="20", columns=headers_samples, selectmode="extended")
    table.pack(padx=10, pady=20, ipadx=1200, ipady=200)

    '''
    ['id_in_samples', 'RackNumber', 'SampleID', 'SampleType', 'SampleStatus', 
    'PatientName_in_samples', 'patient_id'] 
    '''

    i = 1
    header_width = [30, 50, 100, 50, 30, 
                    30, 30]

    for header in headers_samples:
        table.heading('#'+str(i), text=header.title(), anchor=tk.W, 
                      command=lambda c=header: sortby(table, c, 0))
        table.column('#'+str(i), stretch=tk.NO, minwidth=0, 
                     width=tkf.Font().measure(header.title())+header_width[i-1])
        i+=1    
    table.column('#0', stretch=tk.NO, minwidth=0, width=0)

    table.bind("<Double-1>", OnDoubleClick_Samples)
    #///////////////////////////////////////////////////////////////////////////////////////////

    # Scrollbar////////////////////////////////////////////////////////////////////////////////////////
    vsb = ttk.Scrollbar(table, orient = "vertical",  command = table.yview)
    hsb = ttk.Scrollbar(table, orient = "horizontal", command = table.xview)
    ## Link scrollbars activation to top-level object
    table.configure(yscrollcommand = vsb.set, xscrollcommand = hsb.set)
    ## Link scrollbar also to every columns
    map(lambda col: col.configure(yscrollcommand = vsb.set, xscrollcommand = hsb.set), table)
    vsb.pack(side = tk.RIGHT, fill = tk.Y)
    hsb.pack(side = tk.BOTTOM, fill = tk.X)
    
    # ///////////////Samples///////////////

    y_origin = 540
    gain = 50
    i = 0
    
    # ///////////// Raised Label Block ////////////////////////////////////////////////

    label_Patients=tk.Label(root_samples,width=165, height=9 , relief='raised', borderwidth=1)
    label_Patients.place(x=10,y=y_origin+i*gain-40)
    
    # ///////////// Routine Edits////////////////

    text_id_in_samples = tk.Text(root_samples, width=10, height=1, font=('tahoma', 8), wrap='none')
    text_id_in_samples.place(x=820, y=y_origin+i*gain)
    label_id_in_samples = tk.Label(root_samples, text='id_samples:', font=('tahoma', 8))
    label_id_in_samples.place(x=820,y=y_origin+i*gain-25)

    text_RackNumber = tk.Text(root_samples, width=20, height=1, font=('tahoma', 8), wrap='none')
    text_RackNumber.place(x=40, y=y_origin+i*gain)
    label_RackNumber = tk.Label(root_samples, text='Rack Number:', font=('tahoma', 8))
    label_RackNumber.place(x=40,y=y_origin+i*gain-25)

    text_SampleID = tk.Text(root_samples, width=26, height=1, font=('tahoma', 8), wrap='none')
    text_SampleID.place(x=240, y=y_origin+i*gain)
    label_SampleID = tk.Label(root_samples, text='Sample ID:', font=('tahoma', 8))
    label_SampleID.place(x=240,y=y_origin+i*gain-25)

    text_SampleType = tk.Text(root_samples, width=20, height=1, font=('tahoma', 8), wrap='none')
    text_SampleType.place(x=440, y=y_origin+i*gain)
    label_SampleType = tk.Label(root_samples, text='Sample Type:', font=('tahoma', 8))
    label_SampleType.place(x=440,y=y_origin+i*gain-25)

    text_SampleStatus = tk.Text(root_samples, width=20, height=1, font=('tahoma', 8), wrap='none')
    text_SampleStatus.place(x=640, y=y_origin+i*gain)
    label_SampleStatus = tk.Label(root_samples, text='Sample Status:', font=('tahoma', 8))
    label_SampleStatus.place(x=640,y=y_origin+i*gain-25)
    
    i = 1

    text_PatientName_in_samples = tk.Text(root_samples, width=20, height=1, font=('tahoma', 8), wrap='none')
    text_PatientName_in_samples.place(x=40, y=y_origin+i*gain)
    label_PatientName_in_samples = tk.Label(root_samples, text='Patient Name:', font=('tahoma', 8))
    label_PatientName_in_samples.place(x=40,y=y_origin+i*gain-25)

    text_Samples_patient_id = tk.Text(root_samples, width=20, height=1, font=('tahoma', 8), wrap='none')
    text_Samples_patient_id.place(x=240, y=y_origin+i*gain)
    label_patient_id = tk.Label(root_samples, text='Patient ID:', font=('tahoma', 8))
    label_patient_id.place(x=240,y=y_origin+i*gain-25)  
    
    # ////// Buttons //////////////////////////
    
    button_update_sample = ttk.Button(root_samples, text='Update', width=15, command=update_samples)
    button_update_sample.place(x=640, y=590)
    
    button_delete_sample = ttk.Button(root_samples, text='Delete', width=15, command=delete_sample)
    button_delete_sample.place(x=800, y=590)
    
    button_exit = ttk.Button(root_samples, text='Exit', width=15, command=root_samples.destroy)
    button_exit.place(x=800, y=670)
    
    # ///// Browse Automatically /////////////////////
    
    display_in_table(combination)
    
    root_samples.mainloop()

def patients():
    cur.execute('SELECT * FROM Patients')
    headers_patients = [item[0] for item in cur.description]
        
    sqlstr = 'SELECT * FROM Patients ORDER BY id_in_patients'
    spreadsheet = cur.execute(sqlstr)
    combination = []        
    for row in spreadsheet:
        combination.append(row)
    
    def OnDoubleClick_Patients(event):
        global idglb
        try:
            item = table.selection()[0]
            value = table.item(item, 'values')    
            iden = value[0]
            ExtractID(iden)     
            idglb = iden

        except:
            pass
        
    def ExtractID(iden): 
        sqlstr = 'SELECT * FROM Patients WHERE id_in_patients = ?'
        cur.execute(sqlstr, (iden,))
        rowSelected = cur.fetchone()

        item = {}    
        for i in range(len(rowSelected)):
            item[headers_patients[i]] = rowSelected[i]
        display_in_text(item)
        
    def display_in_table(combination):
        for row in combination:
            table.insert("", "end", "", values=row)     
        
    def display_in_text(item): 
        text_id_in_patients.delete('1.0', tk.END)
        text_id_in_patients.insert('1.0', item['id_in_patients'])

        text_PatientName_in_patients.delete('1.0', tk.END)
        text_PatientName_in_patients.insert('1.0', item['PatientName_in_patients'])

        text_InPatientID.delete('1.0', tk.END)
        text_InPatientID.insert('1.0', item['InPatientID'])

        text_CitizenID.delete('1.0', tk.END)
        text_CitizenID.insert('1.0', item['CitizenID'])

        text_BirthDate.delete('1.0', tk.END)
        text_BirthDate.insert('1.0', item['BirthDate'])  

        text_Gender.delete('1.0', tk.END)
        text_Gender.insert('1.0', item['Gender'])   

        text_PatientName_CN.delete('1.0', tk.END)
        text_PatientName_CN.insert('1.0', item['PatientName_CN'])

        text_ProbandName.delete('1.0', tk.END)
        text_ProbandName.insert('1.0', item['ProbandName'])

        text_proband_id.delete('1.0', tk.END)
        text_proband_id.insert('1.0', item['proband_id'])

        text_RelationshipOfProband.delete('1.0', tk.END)
        text_RelationshipOfProband.insert('1.0', item['RelationshipOfProband'])

        text_Telephone.delete('1.0', tk.END)
        text_Telephone.insert('1.0', item['Telephone'])

        text_Comments.delete('1.0', tk.END)
        text_Comments.insert('1.0', item['Comments'])

        text_Diagnosis1.delete('1.0', tk.END)
        text_Diagnosis1.insert('1.0', item['Diagnosis1'])

        text_Diagnosis2.delete('1.0', tk.END)
        text_Diagnosis2.insert('1.0', item['Diagnosis2'])

        text_Diagnosis3.delete('1.0', tk.END)
        text_Diagnosis3.insert('1.0', item['Diagnosis3'])

        text_Diagnosis4.delete('1.0', tk.END)
        text_Diagnosis4.insert('1.0', item['Diagnosis4'])

        text_Diagnosis5.delete('1.0', tk.END)
        text_Diagnosis5.insert('1.0', item['Diagnosis5'])
        
    def update_patients():
            try:
                id_in_patients_gotten = text_id_in_patients.get('1.0', tk.END).rstrip()
                PatientName_in_patients_gotten = text_PatientName_in_patients.get('1.0', tk.END).rstrip()
                PatientName_CN_gotten = text_PatientName_CN.get('1.0', tk.END).rstrip()                
                Gender_gotten = text_Gender.get('1.0', tk.END).rstrip()

                ProbandName_gotten = text_ProbandName.get('1.0', tk.END).rstrip()
                proband_id =  text_proband_id.get('1.0', tk.END).rstrip()
                RelationshipOfProband_gotten = text_RelationshipOfProband.get('1.0', tk.END).rstrip()

                InPatientID_gotten = text_InPatientID.get('1.0', tk.END).rstrip()
                CitizenID_gotten = text_CitizenID.get('1.0', tk.END).rstrip()
                BirthDate_gotten = text_BirthDate.get('1.0', tk.END).rstrip() 

                Diagnosis1_gotten = text_Diagnosis1.get('1.0', tk.END).rstrip()
                Diagnosis2_gotten = text_Diagnosis2.get('1.0', tk.END).rstrip()
                Diagnosis3_gotten = text_Diagnosis3.get('1.0', tk.END).rstrip()
                Diagnosis4_gotten = text_Diagnosis4.get('1.0', tk.END).rstrip()
                Diagnosis5_gotten = text_Diagnosis5.get('1.0', tk.END).rstrip()

                Telephone_gotten = text_Telephone.get('1.0', tk.END).rstrip()
                Comments_gotten = text_Comments.get('1.0', tk.END).rstrip()

                Question_mark = '(' + '?, ' * 16 + '?)'

                cur.execute('DELETE FROM Patients WHERE id_in_patients = ?', (id_in_patients_gotten,))        
                conn.commit()

                Update_values = (id_in_patients_gotten,                          
                                 PatientName_in_patients_gotten,
                                 PatientName_CN_gotten, 
                                 Gender_gotten, 

                                 InPatientID_gotten, 
                                 CitizenID_gotten,                         
                                 BirthDate_gotten, 

                                 ProbandName_gotten, 
                                 proband_id, 
                                 RelationshipOfProband_gotten,                            

                                 Diagnosis1_gotten,
                                 Diagnosis2_gotten,
                                 Diagnosis3_gotten,
                                 Diagnosis4_gotten,
                                 Diagnosis5_gotten, 

                                 Telephone_gotten, 
                                 Comments_gotten)

                Update_Fields = '''(id_in_patients, PatientName_in_patients, PatientName_CN, Gender,

                InPatientID, CitizenID, BirthDate, 

                ProbandName, proband_id, RelationshipOfProband, 

                Diagnosis1, Diagnosis2, Diagnosis3, Diagnosis4, Diagnosis5, 
                Telephone, Comments)
                '''

                #cur.execute('INSERT INTO BloodSamples (SampleID, PatientName, SampleType) VALUES (?, ?, ?)', 
                #('201706181718000444', 'PatientName, 'Serum'))

                cur.execute('INSERT INTO Patients '+ Update_Fields + ' VALUES ' + Question_mark, 
                            Update_values)
                conn.commit()  

                #messagebox.showinfo("Updated", "Patient's information successfully updated!")
                
                # //////////////////// Refresh the Table ///////////////////////////////////////////
                # Clear the table
                for i in table.get_children():
                    table.delete(i)
                
                # Refresh the whole database
                refreshDB()
                
                # Refresh variable combination
                
                sqlstr = 'SELECT * FROM Patients ORDER BY id_in_patients'
                spreadsheet = cur.execute(sqlstr)
                combination = []        
                for row in spreadsheet:
                    combination.append(row)
                
                # Display the table
                display_in_table(combination)
                
            except:
                pass
    
    def delete_patient():
        id_in_patients_gotten = text_id_in_patients.get('1.0', tk.END).rstrip()
    
        if id_in_patients_gotten == '':
            messagebox.showinfo("Empty", "There's no patient's information to delete. Please make sure.")

        else:           
            result = messagebox.askquestion('Delete', 'Are you sure to delete this patient?', 
                                            icon='warning')

            if result == 'yes':
                cur.execute('DELETE FROM Patients WHERE id_in_patients = ?', (id_in_patients_gotten,))        
                conn.commit()            
                messagebox.showinfo("Deleted", "The patient's information has been deleted!")
                
                # //////////////////// Refresh the Table ///////////////////////////////////////////
                # Clear the table
                for i in table.get_children():
                    table.delete(i)
                
                # Refresh the whole database
                refreshDB()
                
                # Refresh variable combination
                
                sqlstr = 'SELECT * FROM Patients ORDER BY id_in_patients'
                spreadsheet = cur.execute(sqlstr)
                combination = []        
                for row in spreadsheet:
                    combination.append(row)
                
                # Display the table        
                display_in_table(combination)

    # //////////////////////////////////////////////////////
    # /////// Main Flow ////////////////////////////

    root_patients = tk.Tk()    
    
    w = 1200 # width for the Tk root
    h = 840 # height for the Tk root

    # get screen width and height
    ws = root_patients.winfo_screenwidth() # width of the screen
    hs = root_patients.winfo_screenheight() # height of the screen

    # calculate x and y coordinates for the Tk root window
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)

    # set the dimensions of the screen 
    # and where it is placed
    root_patients.geometry('%dx%d+%d+%d' % (w, h, x, y))   
    root_patients.title('Patients')  
    
    # /////// Multicolumn Listbox /////////////////////////
    table = ttk.Treeview(root_patients, height="20", columns=headers_patients, selectmode="extended")
    table.pack(padx=10, pady=20, ipadx=1200, ipady=140)

    '''
    ['id_in_patients', 'PatientName_in_patients', 'PatientName_CN', 'ProbandName', 'proband_id', 
'RelationshipOfProband',  'InPatientID', 'CitizenID', 'BirthDate', 'Gender', 
'Diagnosis1', 'Diagnosis2', 'Diagnosis3', 'Diagnosis4', 'Diagnosis5', 'Telephone', 'Comments'] 
'''

    i = 1
    header_width = [-30, -50, -20, 30, -30,
                    50, 70, 80, 50, 40,
                    90, 90, 90, 90, 90, 60, 50]

    for header in headers_patients:
        table.heading('#'+str(i), text=header.title(), anchor=tk.W, 
                      command=lambda c=header: sortby(table, c, 0))
        table.column('#'+str(i), stretch=tk.NO, minwidth=0, 
                     width=tkf.Font().measure(header.title())+header_width[i-1])
        i+=1    
    table.column('#0', stretch=tk.NO, minwidth=0, width=0)

    table.bind("<Double-1>", OnDoubleClick_Patients)
    #///////////////////////////////////////////////////////////////////////////////////////////

    # Scrollbar////////////////////////////////////////////////////////////////////////////////////////
    vsb = ttk.Scrollbar(table, orient = "vertical",  command = table.yview)
    hsb = ttk.Scrollbar(table, orient = "horizontal", command = table.xview)
    ## Link scrollbars activation to top-level object
    table.configure(yscrollcommand = vsb.set, xscrollcommand = hsb.set)
    ## Link scrollbar also to every columns
    map(lambda col: col.configure(yscrollcommand = vsb.set, xscrollcommand = hsb.set), table)
    vsb.pack(side = tk.RIGHT, fill = tk.Y)
    hsb.pack(side = tk.BOTTOM, fill = tk.X)   
    
    # ///////////////Patients///////////////

    y_origin = 420
    gain = 50
    i = 0
    
     # ///////////// Raised Label Block ////////////////////////////////////////////////

    label_Patients=tk.Label(root_patients,width=165, height=26 , relief='raised', borderwidth=1)
    label_Patients.place(x=10,y=y_origin+i*gain-40)
    
    # ///////////// Routine Edits////////////////      

    text_id_in_patients = tk.Text(root_patients, width=10, height=1, font=('tahoma', 9), wrap='none')
    text_id_in_patients.place(x=640, y=y_origin+i*gain)
    label_id_in_patients = tk.Label(root_patients, text='id_patients:', font=('tahoma', 8))
    label_id_in_patients.place(x=640,y=y_origin+i*gain-25)

    text_PatientName_CN = tk.Text(root_patients, width=20, height=1, font=('tahoma', 9), wrap='none')
    text_PatientName_CN.place(x=40, y=y_origin+i*gain)
    label_PatientName_CN = tk.Label(root_patients, text='Patient\'s Chinese Name:', font=('tahoma', 8))
    label_PatientName_CN.place(x=40,y=y_origin+i*gain-25)

    text_PatientName_in_patients = tk.Text(root_patients, width=20, height=1, font=('tahoma', 8), wrap='none')
    text_PatientName_in_patients.place(x=240, y=y_origin+i*gain)
    label_PatientName_in_patients = tk.Label(root_patients, text='Patient\' Name:', font=('tahoma', 8))
    label_PatientName_in_patients.place(x=240,y=y_origin+i*gain-25)
    
    i = 1

    text_Gender = tk.Text(root_patients, width=20, height=1, font=('tahoma', 8), wrap='none')
    text_Gender.place(x=40, y=y_origin+i*gain)
    label_Gender = tk.Label(root_patients, text='Gender:', font=('tahoma', 8))
    label_Gender.place(x=40,y=y_origin+i*gain-25)

    text_ProbandName = tk.Text(root_patients, width=20, height=1, font=('tahoma', 8), wrap='none')
    text_ProbandName.place(x=240, y=y_origin+i*gain)
    label_ProbandName = tk.Label(root_patients, text='Proband Name:', font=('tahoma', 8))
    label_ProbandName.place(x=240,y=y_origin+i*gain-25)

    text_proband_id = tk.Text(root_patients, width=20, height=1, font=('tahoma', 8), wrap='none')
    text_proband_id.place(x=440, y=y_origin+i*gain)
    label_proband_id = tk.Label(root_patients, text='Proband ID:', font=('tahoma', 8))
    label_proband_id.place(x=440,y=y_origin+i*gain-25)

    text_RelationshipOfProband = tk.Text(root_patients, width=40, height=1, font=('tahoma', 8), wrap='none')
    text_RelationshipOfProband.place(x=640, y=y_origin+i*gain)
    label_RelationshipOfProband = tk.Label(root_patients, text='Relationship of Proband:', font=('tahoma', 8))
    label_RelationshipOfProband.place(x=640,y=y_origin+i*gain-25)

    i = 2

    text_InPatientID = tk.Text(root_patients, width=20, height=1, font=('tahoma', 8), wrap='none')
    text_InPatientID.place(x=40, y=y_origin+i*gain)
    label_InPatientID = tk.Label(root_patients, text='In-Patient ID:', font=('tahoma', 8))
    label_InPatientID.place(x=40,y=y_origin+i*gain-25)

    text_CitizenID = tk.Text(root_patients, width=25, height=1, font=('tahoma', 8), wrap='none')
    text_CitizenID.place(x=240, y=y_origin+i*gain)
    label_CitizenID = tk.Label(root_patients, text='Citizen ID:', font=('tahoma', 8))
    label_CitizenID.place(x=240,y=y_origin+i*gain-25)


    text_BirthDate = tk.Text(root_patients, width=20, height=1, font=('tahoma', 8), wrap='none')
    text_BirthDate.place(x=440, y=y_origin+i*gain)
    label_BirthDate = tk.Label(root_patients, text='Birth Date:', font=('tahoma', 8))
    label_BirthDate.place(x=440,y=y_origin+i*gain-25)

    i = 3

    text_Diagnosis1 = tk.Text(root_patients, width=40, height=1, font=('tahoma', 8), wrap='none')
    text_Diagnosis1.place(x=40, y=y_origin+i*gain)
    label_Diagnosis1 = tk.Label(root_patients, text='Diagnosis 1:', font=('tahoma', 8))
    label_Diagnosis1.place(x=40,y=y_origin+i*gain-25)

    text_Diagnosis2 = tk.Text(root_patients, width=40, height=1, font=('tahoma', 8), wrap='none')
    text_Diagnosis2.place(x=340, y=y_origin+i*gain)
    label_Diagnosis2 = tk.Label(root_patients, text='Diagnosis 2:', font=('tahoma', 8))
    label_Diagnosis2.place(x=340,y=y_origin+i*gain-25)

    text_Diagnosis3 = tk.Text(root_patients, width=40, height=1, font=('tahoma', 8), wrap='none')
    text_Diagnosis3.place(x=640, y=y_origin+i*gain)
    label_Diagnosis3 = tk.Label(root_patients, text='Diagnosis 3:', font=('tahoma', 8))
    label_Diagnosis3.place(x=640,y=y_origin+i*gain-25)
    
    i = 4

    text_Diagnosis4 = tk.Text(root_patients, width=40, height=1, font=('tahoma', 8), wrap='none')
    text_Diagnosis4.place(x=40, y=y_origin+i*gain)
    label_Diagnosis4 = tk.Label(root_patients, text='Diagnosis 4:', font=('tahoma', 8))
    label_Diagnosis4.place(x=40,y=y_origin+i*gain-25)

    text_Diagnosis5 = tk.Text(root_patients, width=40, height=1, font=('tahoma', 8), wrap='none')
    text_Diagnosis5.place(x=340, y=y_origin+i*gain)
    label_Diagnosis5 = tk.Label(root_patients, text='Diagnosis 5:', font=('tahoma', 8))
    label_Diagnosis5.place(x=340,y=y_origin+i*gain-25)

    i = 5

    text_Telephone = tk.Text(root_patients, width=40, height=1, font=('tahoma', 8), wrap='none')
    text_Telephone.place(x=40, y=y_origin+i*gain)
    label_Telephone = tk.Label(root_patients, text='Telephone:', font=('tahoma', 8))
    label_Telephone.place(x=40,y=y_origin+i*gain-25)
    
    i = 6

    text_Comments = tk.Text(root_patients, width=140, height=1, font=('tahoma', 8), wrap='none')
    text_Comments.place(x=40, y=y_origin+i*gain)
    label_Comments = tk.Label(root_patients, text='Comments:', font=('tahoma', 8))
    label_Comments.place(x=40,y=y_origin+i*gain-25)
    
    # ////// Buttons //////////////////////////
    
    button_update_sample = ttk.Button(root_patients, text='Update', width=15, command=update_patients)
    button_update_sample.place(x=640, y=670)
    
    button_delete_sample = ttk.Button(root_patients, text='Delete', width=15, command=delete_patient)
    button_delete_sample.place(x=800, y=670)
    
    button_exit = ttk.Button(root_patients, text='Exit', width=15, command=root_patients.destroy)
    button_exit.place(x=800, y=790)
    
    # ///// Browse Automatically /////////////////////
    
    display_in_table(combination)
    
    root_patients.mainloop()

def update_samples():
    try:        
        text_id_in_samples_gotten = text_id_in_samples.get('1.0', tk.END).rstrip()        
        RackNumber_gotten = text_RackNumber.get('1.0', tk.END).rstrip()
        SampleID_gotten = text_SampleID.get('1.0', tk.END).rstrip()
        SampleType_gotten = text_SampleType.get('1.0', tk.END).rstrip()
        SampleStatus_gotten = text_SampleStatus.get('1.0', tk.END).rstrip()
        PatientName_in_samples_gotten = text_PatientName_in_samples.get('1.0', tk.END).rstrip()
        Samples_patient_id_gotten = text_Samples_patient_id.get('1.0', tk.END).rstrip()       
        
        Question_mark = '(' + '?, ' * 6 + '?)'
        
        cur.execute('DELETE FROM Samples WHERE id_in_samples = ?', (text_id_in_samples_gotten,))        
        conn.commit()
               
        Update_values = (text_id_in_samples_gotten, 
                         RackNumber_gotten, 
                         SampleID_gotten, 
                         SampleType_gotten, 
                         SampleStatus_gotten, 
                         PatientName_in_samples_gotten,
                         Samples_patient_id_gotten)
        
        Update_Fields = '''(
        id_in_samples, 
        RackNumber, 
        SampleID, 
        SampleType, 
        SampleStatus, 
        PatientName_in_samples, 
        patient_id)
        '''
        
        #cur.execute('INSERT INTO BloodSamples (SampleID, PatientName, SampleType) VALUES (?, ?, ?)', 
        #('201706181718000444', 'PatientName, 'Serum'))
        
        cur.execute('INSERT INTO Samples '+ Update_Fields + ' VALUES ' + Question_mark, 
                    Update_values)
        conn.commit()  
        
        messagebox.showinfo("Updated", "Sample information successfully updated!")
        clear()
        refreshDB()
        display_in_table(combination)
        
    except:
        pass

def update_patients():
    try:
        id_in_patients_gotten = text_id_in_patients.get('1.0', tk.END).rstrip()
        PatientName_in_patients_gotten = text_PatientName_in_patients.get('1.0', tk.END).rstrip()
        PatientName_CN_gotten = text_PatientName_CN.get('1.0', tk.END).rstrip()                
        Gender_gotten = text_Gender.get('1.0', tk.END).rstrip()
        
        ProbandName_gotten = text_ProbandName.get('1.0', tk.END).rstrip()
        proband_id =  text_proband_id.get('1.0', tk.END).rstrip()
        RelationshipOfProband_gotten = text_RelationshipOfProband.get('1.0', tk.END).rstrip()
        
        InPatientID_gotten = text_InPatientID.get('1.0', tk.END).rstrip()
        CitizenID_gotten = text_CitizenID.get('1.0', tk.END).rstrip()
        BirthDate_gotten = text_BirthDate.get('1.0', tk.END).rstrip() 
        
        Diagnosis1_gotten = text_Diagnosis1.get('1.0', tk.END).rstrip()
        Diagnosis2_gotten = text_Diagnosis2.get('1.0', tk.END).rstrip()
        Diagnosis3_gotten = text_Diagnosis3.get('1.0', tk.END).rstrip()
        Diagnosis4_gotten = text_Diagnosis4.get('1.0', tk.END).rstrip()
        Diagnosis5_gotten = text_Diagnosis5.get('1.0', tk.END).rstrip()
        
        Telephone_gotten = text_Telephone.get('1.0', tk.END).rstrip()
        Comments_gotten = text_Comments.get('1.0', tk.END).rstrip()
        
        Question_mark = '(' + '?, ' * 16 + '?)'
        
        cur.execute('DELETE FROM Patients WHERE id_in_patients = ?', (id_in_patients_gotten,))        
        conn.commit()
               
        Update_values = (id_in_patients_gotten,                          
                         PatientName_in_patients_gotten,
                         PatientName_CN_gotten, 
                         Gender_gotten, 
                         
                         InPatientID_gotten, 
                         CitizenID_gotten,                         
                         BirthDate_gotten, 
                         
                         ProbandName_gotten, 
                         proband_id, 
                         RelationshipOfProband_gotten,                            
                         
                         Diagnosis1_gotten,
                         Diagnosis2_gotten,
                         Diagnosis3_gotten,
                         Diagnosis4_gotten,
                         Diagnosis5_gotten, 
                         
                         Telephone_gotten, 
                         Comments_gotten)
        
        Update_Fields = '''(id_in_patients, PatientName_in_patients, PatientName_CN, Gender,
        
        InPatientID, CitizenID, BirthDate, 
        
        ProbandName, proband_id, RelationshipOfProband, 
        
        Diagnosis1, Diagnosis2, Diagnosis3, Diagnosis4, Diagnosis5, 
        Telephone, Comments)
        '''
        
        #cur.execute('INSERT INTO BloodSamples (SampleID, PatientName, SampleType) VALUES (?, ?, ?)', 
        #('201706181718000444', 'PatientName, 'Serum'))
        
        cur.execute('INSERT INTO Patients '+ Update_Fields + ' VALUES ' + Question_mark, 
                    Update_values)
        conn.commit()  
        
        messagebox.showinfo("Updated", "Patient's information successfully updated!")
        clear()
        refreshDB()
        display_in_table(combination)
        
    except:
        pass

def new_sample():
    root_new_sample = tk.Tk()
    
    w = 1080 # width for the Tk root
    h = 320 # height for the Tk root

    # get screen width and height
    ws = root_new_sample.winfo_screenwidth() # width of the screen
    hs = root_new_sample.winfo_screenheight() # height of the screen

    # calculate x and y coordinates for the Tk root window
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)

    # set the dimensions of the screen 
    # and where it is placed
    root_new_sample.geometry('%dx%d+%d+%d' % (w, h, x, y))   
    root_new_sample.title('New Sample')
    
    time_text = str(datetime.datetime.now())
    id = ''
    for t in time_text:
        if t!=' 'and t!= '-' and t != ':' and t != '.':
            id += t
    
    def create():
        try:
            RackNumber_gotten = text_RackNumber.get('1.0', tk.END).rstrip()
            SampleID_gotten = text_SampleID.get('1.0', tk.END).rstrip()
            SampleType_gotten = text_SampleType.get('1.0', tk.END).rstrip()
            SampleStatus_gotten = text_SampleStatus.get('1.0', tk.END).rstrip()
            PatientName_in_samples_gotten = text_PatientName_in_samples.get('1.0', tk.END).rstrip()
            Samples_patient_id_gotten = text_Samples_patient_id.get('1.0', tk.END).rstrip()       

            Question_mark = '(' + '?, ' * 5 + '?)'   
            
            # Should rule out the primary key!!!!!!

            Update_values = (RackNumber_gotten, 
                             SampleID_gotten, 
                             SampleType_gotten, 
                             SampleStatus_gotten, 
                             PatientName_in_samples_gotten,
                             Samples_patient_id_gotten)

            Update_Fields = '''(
            RackNumber, 
            SampleID, 
            SampleType, 
            SampleStatus, 
            PatientName_in_samples, 
            patient_id)
            '''
            #cur.execute('INSERT INTO BloodSamples (SampleID, PatientName, SampleType) VALUES (?, ?, ?)', 
            #('201706181718000444', 'PatientName, 'Serum'))

            cur.execute('INSERT INTO Samples '+ Update_Fields + ' VALUES ' + Question_mark, 
                        Update_values)
            conn.commit()

            messagebox.showinfo("Created", "Sample information successfully created!") 
                        
            clear()
            refreshDB()
            display_in_table(combination)
            root_new_sample.destroy()
            
        except:
            pass  

    # ///////////////// Main Stream /////////////////////////////////
    
    y_origin = 100
    gain = 55
    i = 0
    
     # ///////////// Raised Label Block ////////////////////////////////////////////////

    label_new_patient=tk.Label(root_new_sample, width=150, height=10 , relief='raised', borderwidth=1)
    label_new_patient.place(x=10,y=y_origin+i*gain-40)
    
    # ///////////// Routine Edits////////////////

    text_RackNumber = tk.Text(root_new_sample, width=20, height=1, font=('tahoma', 8), wrap='none')
    text_RackNumber.place(x=40, y=y_origin+i*gain)
    label_RackNumber = tk.Label(root_new_sample, text='Rack Number:', font=('tahoma', 8))
    label_RackNumber.place(x=40,y=y_origin+i*gain-25)

    text_SampleID = tk.Text(root_new_sample, width=26, height=1, font=('tahoma', 8), wrap='none')
    text_SampleID.place(x=240, y=y_origin+i*gain)
    label_SampleID = tk.Label(root_new_sample, text='Sample ID:', font=('tahoma', 8))
    label_SampleID.place(x=240,y=y_origin+i*gain-25)
    
    text_SampleID.delete('1.0', tk.END)
    text_SampleID.insert('1.0', id)  

    text_SampleType = tk.Text(root_new_sample, width=20, height=1, font=('tahoma', 8), wrap='none')
    text_SampleType.place(x=440, y=y_origin+i*gain)
    label_SampleType = tk.Label(root_new_sample, text='Sample Type:', font=('tahoma', 8))
    label_SampleType.place(x=440,y=y_origin+i*gain-25)

    text_SampleStatus = tk.Text(root_new_sample, width=20, height=1, font=('tahoma', 8), wrap='none')
    text_SampleStatus.place(x=640, y=y_origin+i*gain)
    label_SampleStatus = tk.Label(root_new_sample, text='Sample Status:', font=('tahoma', 8))
    label_SampleStatus.place(x=640,y=y_origin+i*gain-25)
    
    i = 1

    text_PatientName_in_samples = tk.Text(root_new_sample, width=20, height=1, font=('tahoma', 8), wrap='none')
    text_PatientName_in_samples.place(x=40, y=y_origin+i*gain)
    label_PatientName_in_samples = tk.Label(root_new_sample, text='Patient Name:', font=('tahoma', 8))
    label_PatientName_in_samples.place(x=40,y=y_origin+i*gain-25)

    text_Samples_patient_id = tk.Text(root_new_sample, width=20, height=1, font=('tahoma', 8), wrap='none')
    text_Samples_patient_id.place(x=240, y=y_origin+i*gain)
    label_patient_id = tk.Label(root_new_sample, text='Patient ID:', font=('tahoma', 8))
    label_patient_id.place(x=240,y=y_origin+i*gain-25)  
    
    # ////// Buttons //////////////////////////
    
    i = 3 
    
    button_add=ttk.Button(root_new_sample, text='Create', width=15, command=create)
    button_add.place(x=300, y=y_origin+i*gain)

    button_cancel=ttk.Button(root_new_sample, text='Cancel', width=15, command=root_new_sample.destroy)
    button_cancel.place(x=650, y=y_origin+i*gain)      
    
    root_new_sample.mainloop()
    
    #t = datetime.datetime.now()
    #ts = str(datetime.datetime.now())

    #datetime.datetime.strptime(ts, '%Y%m%d%I%M%S%f')

def new_patient():
    root_new_patient = tk.Tk()
    
    w = 980 # width for the Tk root
    h = 540 # height for the Tk root

    # get screen width and height
    ws = root_new_patient.winfo_screenwidth() # width of the screen
    hs = root_new_patient.winfo_screenheight() # height of the screen

    # calculate x and y coordinates for the Tk root window
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)

    # set the dimensions of the screen 
    # and where it is placed
    root_new_patient.geometry('%dx%d+%d+%d' % (w, h, x, y))   
    root_new_patient.title('New Patient')
    
    time_text = str(datetime.datetime.now())
    id = ''
    for t in time_text:
        if t!=' 'and t!= '-' and t != ':' and t != '.':
            id += t
    
    def create():
        #try:            
            PatientName_in_patients_gotten = text_PatientName_in_patients.get('1.0', tk.END).rstrip()
            PatientName_CN_gotten = text_PatientName_CN.get('1.0', tk.END).rstrip()                
            Gender_gotten = text_Gender.get('1.0', tk.END).rstrip()

            ProbandName_gotten = text_ProbandName.get('1.0', tk.END).rstrip()
            proband_id =  text_proband_id.get('1.0', tk.END).rstrip()
            RelationshipOfProband_gotten = text_RelationshipOfProband.get('1.0', tk.END).rstrip()

            InPatientID_gotten = text_InPatientID.get('1.0', tk.END).rstrip()
            CitizenID_gotten = text_CitizenID.get('1.0', tk.END).rstrip()
            BirthDate_gotten = text_BirthDate.get('1.0', tk.END).rstrip() 

            Diagnosis1_gotten = text_Diagnosis1.get('1.0', tk.END).rstrip()
            Diagnosis2_gotten = text_Diagnosis2.get('1.0', tk.END).rstrip()
            Diagnosis3_gotten = text_Diagnosis3.get('1.0', tk.END).rstrip()
            Diagnosis4_gotten = text_Diagnosis4.get('1.0', tk.END).rstrip()
            Diagnosis5_gotten = text_Diagnosis5.get('1.0', tk.END).rstrip()

            Telephone_gotten = text_Telephone.get('1.0', tk.END).rstrip()
            Comments_gotten = text_Comments.get('1.0', tk.END).rstrip()

            Question_mark = '(' + '?, ' * 15 + '?)'

            Update_values = (PatientName_in_patients_gotten,
                             PatientName_CN_gotten, 
                             Gender_gotten, 

                             InPatientID_gotten, 
                             CitizenID_gotten,                         
                             BirthDate_gotten, 

                             ProbandName_gotten, 
                             proband_id, 
                             RelationshipOfProband_gotten,                            

                             Diagnosis1_gotten,
                             Diagnosis2_gotten,
                             Diagnosis3_gotten,
                             Diagnosis4_gotten,
                             Diagnosis5_gotten, 

                             Telephone_gotten, 
                             Comments_gotten)

            Update_Fields = '''(PatientName_in_patients, PatientName_CN, Gender,

            InPatientID, CitizenID, BirthDate, 

            ProbandName, proband_id, RelationshipOfProband, 

            Diagnosis1, Diagnosis2, Diagnosis3, Diagnosis4, Diagnosis5, 
            Telephone, Comments)
            '''

            #cur.execute('INSERT INTO BloodSamples (SampleID, PatientName, SampleType) VALUES (?, ?, ?)', 
            #('201706181718000444', 'PatientName, 'Serum'))

            cur.execute('INSERT INTO Patients '+ Update_Fields + ' VALUES ' + Question_mark, 
                        Update_values)
            conn.commit()  

            messagebox.showinfo("Created", "Patient's information successfully created!")
            
            clear()
            refreshDB()
            display_in_table(combination)
            root_new_patient.destroy()
                
        #except:
            #pass

    # ///////// Main Stream ////////////////////////
    
    y_origin = 80
    gain = 50
    i = 0
    
     # ///////////// Raised Label Block ////////////////////////////////////////////////

    label_Patients=tk.Label(root_new_patient,width=135, height=23 , relief='raised', borderwidth=1)
    label_Patients.place(x=10,y=y_origin+i*gain-40)
    
    # ///////////// Routine Edits////////////////          

    text_PatientName_CN = tk.Text(root_new_patient, width=20, height=1, font=('tahoma', 9), wrap='none')
    text_PatientName_CN.place(x=40, y=y_origin+i*gain)
    label_PatientName_CN = tk.Label(root_new_patient, text='Patient\'s Chinese Name:', font=('tahoma', 8))
    label_PatientName_CN.place(x=40,y=y_origin+i*gain-25)

    text_PatientName_in_patients = tk.Text(root_new_patient, width=20, height=1, font=('tahoma', 8), wrap='none')
    text_PatientName_in_patients.place(x=240, y=y_origin+i*gain)
    label_PatientName_in_patients = tk.Label(root_new_patient, text='Patient\' Name:', font=('tahoma', 8))
    label_PatientName_in_patients.place(x=240,y=y_origin+i*gain-25)
    
    i = 1

    text_Gender = tk.Text(root_new_patient, width=20, height=1, font=('tahoma', 8), wrap='none')
    text_Gender.place(x=40, y=y_origin+i*gain)
    label_Gender = tk.Label(root_new_patient, text='Gender:', font=('tahoma', 8))
    label_Gender.place(x=40,y=y_origin+i*gain-25)

    text_ProbandName = tk.Text(root_new_patient, width=20, height=1, font=('tahoma', 8), wrap='none')
    text_ProbandName.place(x=240, y=y_origin+i*gain)
    label_ProbandName = tk.Label(root_new_patient, text='Proband Name:', font=('tahoma', 8))
    label_ProbandName.place(x=240,y=y_origin+i*gain-25)

    text_proband_id = tk.Text(root_new_patient, width=20, height=1, font=('tahoma', 8), wrap='none')
    text_proband_id.place(x=440, y=y_origin+i*gain)
    label_proband_id = tk.Label(root_new_patient, text='Proband ID:', font=('tahoma', 8))
    label_proband_id.place(x=440,y=y_origin+i*gain-25)

    text_RelationshipOfProband = tk.Text(root_new_patient, width=40, height=1, font=('tahoma', 8), wrap='none')
    text_RelationshipOfProband.place(x=640, y=y_origin+i*gain)
    label_RelationshipOfProband = tk.Label(root_new_patient, text='Relationship of Proband:', font=('tahoma', 8))
    label_RelationshipOfProband.place(x=640,y=y_origin+i*gain-25)

    i = 2

    text_InPatientID = tk.Text(root_new_patient, width=20, height=1, font=('tahoma', 8), wrap='none')
    text_InPatientID.place(x=40, y=y_origin+i*gain)
    label_InPatientID = tk.Label(root_new_patient, text='In-Patient ID:', font=('tahoma', 8))
    label_InPatientID.place(x=40,y=y_origin+i*gain-25)

    text_CitizenID = tk.Text(root_new_patient, width=25, height=1, font=('tahoma', 8), wrap='none')
    text_CitizenID.place(x=240, y=y_origin+i*gain)
    label_CitizenID = tk.Label(root_new_patient, text='Citizen ID:', font=('tahoma', 8))
    label_CitizenID.place(x=240,y=y_origin+i*gain-25)


    text_BirthDate = tk.Text(root_new_patient, width=20, height=1, font=('tahoma', 8), wrap='none')
    text_BirthDate.place(x=440, y=y_origin+i*gain)
    label_BirthDate = tk.Label(root_new_patient, text='Birth Date:', font=('tahoma', 8))
    label_BirthDate.place(x=440,y=y_origin+i*gain-25)

    i = 3

    text_Diagnosis1 = tk.Text(root_new_patient, width=40, height=1, font=('tahoma', 8), wrap='none')
    text_Diagnosis1.place(x=40, y=y_origin+i*gain)
    label_Diagnosis1 = tk.Label(root_new_patient, text='Diagnosis 1:', font=('tahoma', 8))
    label_Diagnosis1.place(x=40,y=y_origin+i*gain-25)

    text_Diagnosis2 = tk.Text(root_new_patient, width=40, height=1, font=('tahoma', 8), wrap='none')
    text_Diagnosis2.place(x=340, y=y_origin+i*gain)
    label_Diagnosis2 = tk.Label(root_new_patient, text='Diagnosis 2:', font=('tahoma', 8))
    label_Diagnosis2.place(x=340,y=y_origin+i*gain-25)

    text_Diagnosis3 = tk.Text(root_new_patient, width=40, height=1, font=('tahoma', 8), wrap='none')
    text_Diagnosis3.place(x=640, y=y_origin+i*gain)
    label_Diagnosis3 = tk.Label(root_new_patient, text='Diagnosis 3:', font=('tahoma', 8))
    label_Diagnosis3.place(x=640,y=y_origin+i*gain-25)
    
    i = 4

    text_Diagnosis4 = tk.Text(root_new_patient, width=40, height=1, font=('tahoma', 8), wrap='none')
    text_Diagnosis4.place(x=40, y=y_origin+i*gain)
    label_Diagnosis4 = tk.Label(root_new_patient, text='Diagnosis 4:', font=('tahoma', 8))
    label_Diagnosis4.place(x=40,y=y_origin+i*gain-25)

    text_Diagnosis5 = tk.Text(root_new_patient, width=40, height=1, font=('tahoma', 8), wrap='none')
    text_Diagnosis5.place(x=340, y=y_origin+i*gain)
    label_Diagnosis5 = tk.Label(root_new_patient, text='Diagnosis 5:', font=('tahoma', 8))
    label_Diagnosis5.place(x=340,y=y_origin+i*gain-25)

    i = 5

    text_Telephone = tk.Text(root_new_patient, width=40, height=1, font=('tahoma', 8), wrap='none')
    text_Telephone.place(x=40, y=y_origin+i*gain)
    label_Telephone = tk.Label(root_new_patient, text='Telephone:', font=('tahoma', 8))
    label_Telephone.place(x=40,y=y_origin+i*gain-25)
    
    i = 6

    text_Comments = tk.Text(root_new_patient, width=140, height=1, font=('tahoma', 8), wrap='none')
    text_Comments.place(x=40, y=y_origin+i*gain)
    label_Comments = tk.Label(root_new_patient, text='Comments:', font=('tahoma', 8))
    label_Comments.place(x=40,y=y_origin+i*gain-25)
    
    i = 8 
    
    button_add=ttk.Button(root_new_patient, text='Create', width=15, command=create)
    button_add.place(x=250, y=y_origin+i*gain)

    button_cancel=ttk.Button(root_new_patient, text='Cancel', width=15, command=root_new_patient.destroy)
    button_cancel.place(x=600, y=y_origin+i*gain)      
    
    root_new_patient.mainloop()
    
    #t = datetime.datetime.now()
    #ts = str(datetime.datetime.now())

    #datetime.datetime.strptime(ts, '%Y%m%d%I%M%S%f')

def delete_sample():
    id_in_samples_gotten = text_id_in_samples.get('1.0', tk.END).rstrip()
    
    if id_in_samples_gotten == '':
        messagebox.showinfo("Empty", "There's no sample to delete. Please make sure.")
        
    else:           
        result = messagebox.askquestion('Delete', 'Are you sure to delete this sample?', icon='warning')

        if result == 'yes':
            cur.execute('DELETE FROM Samples WHERE id_in_samples = ?', (id_in_samples_gotten,))        
            conn.commit()            
            messagebox.showinfo("Deleted", "Sample has been deleted!")
            
            clear()
            refreshDB()
            display_in_table(combination)

def delete_patient():
    id_in_patients_gotten = text_id_in_patients.get('1.0', tk.END).rstrip()
    
    if id_in_patients_gotten == '':
        messagebox.showinfo("Empty", "There's no patient information to delete. Please make sure.")
        
    else:           
        result = messagebox.askquestion('Delete', 
                                        'Are you sure to delete this patient\'s information?', 
                                        icon='warning')

        if result == 'yes':
            cur.execute('DELETE FROM Patients WHERE id_in_patients = ?', 
                        (id_in_patients_gotten,))        
            conn.commit()            
            messagebox.showinfo("Deleted", "The Patient's information has been deleted!")
            
            clear()
            refreshDB()
            display_in_table(combination)

def patientNameSearch():
    gotten = text_PatientName_Search.get('1.0', tk.END).rstrip()
    
    cur.execute('SELECT * FROM BloodSamples WHERE PatientName = ?', (gotten,))
    items = cur.fetchall()
    
    clear()
    display_in_table(items)    

## Main Flow

root = tk.Tk()
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
#root.attributes('-fullscreen', True)
root.title('CharlestonPark')
root.iconbitmap('CharlestonParkIcon.ico')

### Multicolumn Listbox

# Multicolumn Listbox/////////////////////////////////////////////////////////////////////////////
table = ttk.Treeview(root, height="20", columns=headers, selectmode="extended")
table.pack(padx=10, pady=20, ipadx=1200, ipady=200)

'''
['id_in_samples', 'RackNumber', 'SampleID', 'SampleType', 'SampleStatus', 'PatientName_in_samples', 
'patient_id', 
'id_in_patients', 'PatientName_in_patients', 'PatientName_CN', 'ProbandName', 'proband_id', 
'RelationshipOfProband',  'InPatientID', 'CitizenID', 'BirthDate', 'Gender', 
'Diagnosis1', 'Diagnosis2', 'Diagnosis3', 'Diagnosis4', 'Diagnosis5', 'Telephone', 'Comments'] 
'''
i = 1
header_width = [-60, 20, 100, 40, 20, -50, 
                -30, 
                -30, -50, -20, 30, -30, 
                50, 70, 80, 50, 40, 
                90, 90, 90, 90, 90, 60, 50]

for header in headers:
    table.heading('#'+str(i), text=header.title(), anchor=tk.W, command=lambda c=header: sortby(table, c, 0))
    table.column('#'+str(i), stretch=tk.NO, minwidth=0, width=tkf.Font().measure(header.title())+header_width[i-1])
    i+=1    
table.column('#0', stretch=tk.NO, minwidth=0, width=0)

table.bind("<Double-1>", OnDoubleClick)
#///////////////////////////////////////////////////////////////////////////////////////////

# Scrollbar////////////////////////////////////////////////////////////////////////////////////////
vsb = ttk.Scrollbar(table, orient = "vertical",  command = table.yview)
hsb = ttk.Scrollbar(table, orient = "horizontal", command = table.xview)
## Link scrollbars activation to top-level object
table.configure(yscrollcommand = vsb.set, xscrollcommand = hsb.set)
## Link scrollbar also to every columns
map(lambda col: col.configure(yscrollcommand = vsb.set, xscrollcommand = hsb.set), table)
vsb.pack(side = tk.RIGHT, fill = tk.Y)
hsb.pack(side = tk.BOTTOM, fill = tk.X) 

### Other Controls

# ///////Text Edit/////////////////////////

y_origin = 580
gain = 50
i = 0

# ///////////// Raised Label Block ////////////////////////////////////////////////

label_Patients=tk.Label(root,width=230, height=5 , relief='raised', borderwidth=1)
label_Patients.place(x=10,y=540)

label_Samples=tk.Label(root,width=230, height=15 , relief='raised', borderwidth=1)
label_Samples.place(x=10,y=638)

# ///////////// Routine Edits////////////////
# ///////////////Samples///////////////

text_id_in_samples = tk.Text(root, width=10, height=1, font=('tahoma', 8), wrap='none')
text_id_in_samples.place(x=1220, y=y_origin+i*gain)
label_id_in_samples = tk.Label(root, text='id_samples:', font=('tahoma', 8))
label_id_in_samples.place(x=1220,y=y_origin+i*gain-25)

text_RackNumber = tk.Text(root, width=20, height=1, font=('tahoma', 8), wrap='none')
text_RackNumber.place(x=40, y=y_origin+i*gain)
label_RackNumber = tk.Label(root, text='Rack Number:', font=('tahoma', 8))
label_RackNumber.place(x=40,y=y_origin+i*gain-25)

text_SampleID = tk.Text(root, width=26, height=1, font=('tahoma', 8), wrap='none')
text_SampleID.place(x=240, y=y_origin+i*gain)
label_SampleID = tk.Label(root, text='Sample ID:', font=('tahoma', 8))
label_SampleID.place(x=240,y=y_origin+i*gain-25)

text_SampleType = tk.Text(root, width=20, height=1, font=('tahoma', 8), wrap='none')
text_SampleType.place(x=440, y=y_origin+i*gain)
label_SampleType = tk.Label(root, text='Sample Type:', font=('tahoma', 8))
label_SampleType.place(x=440,y=y_origin+i*gain-25)

text_SampleStatus = tk.Text(root, width=20, height=1, font=('tahoma', 8), wrap='none')
text_SampleStatus.place(x=640, y=y_origin+i*gain)
label_SampleStatus = tk.Label(root, text='Sample Status:', font=('tahoma', 8))
label_SampleStatus.place(x=640,y=y_origin+i*gain-25)

text_PatientName_in_samples = tk.Text(root, width=20, height=1, font=('tahoma', 8), wrap='none')
text_PatientName_in_samples.place(x=840, y=y_origin+i*gain)
label_PatientName_in_samples = tk.Label(root, text='Patient Name:', font=('tahoma', 8))
label_PatientName_in_samples.place(x=840,y=y_origin+i*gain-25)

text_Samples_patient_id = tk.Text(root, width=20, height=1, font=('tahoma', 8), wrap='none')
text_Samples_patient_id.place(x=1040, y=y_origin+i*gain)
label_patient_id = tk.Label(root, text='Patient ID:', font=('tahoma', 8))
label_patient_id.place(x=1040,y=y_origin+i*gain-25)

i = 2

# ///////////////Patients///////////////

text_id_in_patients = tk.Text(root, width=10, height=1, font=('tahoma', 9), wrap='none')
text_id_in_patients.place(x=1340, y=y_origin+i*gain)
label_id_in_patients = tk.Label(root, text='id_patients:', font=('tahoma', 8))
label_id_in_patients.place(x=1340,y=y_origin+i*gain-25)

text_PatientName_CN = tk.Text(root, width=20, height=1, font=('tahoma', 9), wrap='none')
text_PatientName_CN.place(x=40, y=y_origin+i*gain)
label_PatientName_CN = tk.Label(root, text='Patient\'s Chinese Name:', font=('tahoma', 8))
label_PatientName_CN.place(x=40,y=y_origin+i*gain-25)

text_PatientName_in_patients = tk.Text(root, width=20, height=1, font=('tahoma', 8), wrap='none')
text_PatientName_in_patients.place(x=240, y=y_origin+i*gain)
label_PatientName_in_patients = tk.Label(root, text='Patient\' Name:', font=('tahoma', 8))
label_PatientName_in_patients.place(x=240,y=y_origin+i*gain-25)

text_Gender = tk.Text(root, width=20, height=1, font=('tahoma', 8), wrap='none')
text_Gender.place(x=440, y=y_origin+i*gain)
label_Gender = tk.Label(root, text='Gender:', font=('tahoma', 8))
label_Gender.place(x=440,y=y_origin+i*gain-25)

text_ProbandName = tk.Text(root, width=20, height=1, font=('tahoma', 8), wrap='none')
text_ProbandName.place(x=640, y=y_origin+i*gain)
label_ProbandName = tk.Label(root, text='Proband Name:', font=('tahoma', 8))
label_ProbandName.place(x=640,y=y_origin+i*gain-25)

text_proband_id = tk.Text(root, width=20, height=1, font=('tahoma', 8), wrap='none')
text_proband_id.place(x=840, y=y_origin+i*gain)
label_proband_id = tk.Label(root, text='Proband ID:', font=('tahoma', 8))
label_proband_id.place(x=840,y=y_origin+i*gain-25)

text_RelationshipOfProband = tk.Text(root, width=40, height=1, font=('tahoma', 8), wrap='none')
text_RelationshipOfProband.place(x=1040, y=y_origin+i*gain)
label_RelationshipOfProband = tk.Label(root, text='Relationship of Proband:', font=('tahoma', 8))
label_RelationshipOfProband.place(x=1040,y=y_origin+i*gain-25)

i = 3

text_InPatientID = tk.Text(root, width=20, height=1, font=('tahoma', 8), wrap='none')
text_InPatientID.place(x=40, y=y_origin+i*gain)
label_InPatientID = tk.Label(root, text='In-Patient ID:', font=('tahoma', 8))
label_InPatientID.place(x=40,y=y_origin+i*gain-25)

text_CitizenID = tk.Text(root, width=25, height=1, font=('tahoma', 8), wrap='none')
text_CitizenID.place(x=240, y=y_origin+i*gain)
label_CitizenID = tk.Label(root, text='Citizen ID:', font=('tahoma', 8))
label_CitizenID.place(x=240,y=y_origin+i*gain-25)

text_BirthDate = tk.Text(root, width=20, height=1, font=('tahoma', 8), wrap='none')
text_BirthDate.place(x=440, y=y_origin+i*gain)
label_BirthDate = tk.Label(root, text='Birth Date:', font=('tahoma', 8))
label_BirthDate.place(x=440,y=y_origin+i*gain-25)

i = 4

text_Diagnosis1 = tk.Text(root, width=40, height=1, font=('tahoma', 8), wrap='none')
text_Diagnosis1.place(x=40, y=y_origin+i*gain)
label_Diagnosis1 = tk.Label(root, text='Diagnosis 1:', font=('tahoma', 8))
label_Diagnosis1.place(x=40,y=y_origin+i*gain-25)

text_Diagnosis2 = tk.Text(root, width=40, height=1, font=('tahoma', 8), wrap='none')
text_Diagnosis2.place(x=340, y=y_origin+i*gain)
label_Diagnosis2 = tk.Label(root, text='Diagnosis 2:', font=('tahoma', 8))
label_Diagnosis2.place(x=340,y=y_origin+i*gain-25)

text_Diagnosis3 = tk.Text(root, width=40, height=1, font=('tahoma', 8), wrap='none')
text_Diagnosis3.place(x=640, y=y_origin+i*gain)
label_Diagnosis3 = tk.Label(root, text='Diagnosis 3:', font=('tahoma', 8))
label_Diagnosis3.place(x=640,y=y_origin+i*gain-25)

text_Diagnosis4 = tk.Text(root, width=40, height=1, font=('tahoma', 8), wrap='none')
text_Diagnosis4.place(x=940, y=y_origin+i*gain)
label_Diagnosis4 = tk.Label(root, text='Diagnosis 4:', font=('tahoma', 8))
label_Diagnosis4.place(x=940,y=y_origin+i*gain-25)

text_Diagnosis5 = tk.Text(root, width=40, height=1, font=('tahoma', 8), wrap='none')
text_Diagnosis5.place(x=1240, y=y_origin+i*gain)
label_Diagnosis5 = tk.Label(root, text='Diagnosis 5:', font=('tahoma', 8))
label_Diagnosis5.place(x=1240,y=y_origin+i*gain-25)

i = 5

text_Telephone = tk.Text(root, width=40, height=1, font=('tahoma', 8), wrap='none')
text_Telephone.place(x=40, y=y_origin+i*gain)
label_Telephone = tk.Label(root, text='Telephone:', font=('tahoma', 8))
label_Telephone.place(x=40,y=y_origin+i*gain-25)

text_Comments = tk.Text(root, width=140, height=1, font=('tahoma', 8), wrap='none')
text_Comments.place(x=340, y=y_origin+i*gain)
label_Comments = tk.Label(root, text='Comments:', font=('tahoma', 8))
label_Comments.place(x=340,y=y_origin+i*gain-25)

# /////Buttons//////////////////////
button_browse=ttk.Button(root, text='Samples...', width=15, command=samples)
button_browse.place(x=1210, y=500)

button_browse=ttk.Button(root, text='Patients...', width=15, command=patients)
button_browse.place(x=1345, y=500)

button_browse=ttk.Button(root, text='Browse', width=15, command=browse)
button_browse.place(x=1480, y=500)

# ////////////// Record Num/////////////////

text_num = tk.Text(root, width=8, height=1, font=('tahoma', 8), wrap='none')
text_num.place(x=1050, y=500)

# ////////////// Function Button //////////

button_update_sample = ttk.Button(root, text='Update', width=15, command=update_samples)
button_update_sample.place(x=1345, y=580)

button_delete_sample = ttk.Button(root, text='Delete', width=15, command=delete_sample)
button_delete_sample.place(x=1480, y=580)

button_update_patient = ttk.Button(root, text='Update', width=15, command=update_patients)
button_update_patient.place(x=1230, y=825)

button_delete_patient = ttk.Button(root, text='Delete', width=15, command=delete_patient)
button_delete_patient.place(x=1355, y=825)

button_exit = ttk.Button(root, text='Exit', width=15, command=root.destroy)
button_exit.place(x=1480, y=825)

button_new_sample = ttk.Button(root, text='New Sample...', width=20, command=new_sample)
button_new_sample.place(x=30, y=500)

button_new_patient = ttk.Button(root, text='New Patient...', width=20, command=new_patient)
button_new_patient.place(x=200, y=500)

# ///// Search Edit Box//////////

text_PatientName_Search = tk.Text(root, width=20, height=1, font=('tahoma', 9), wrap='none')
text_PatientName_Search.place(x=440, y=510)
label_PatientName_Search = tk.Label(root, text='Patient\'s Name:', font=('tahoma', 8))
label_PatientName_Search.place(x=440,y=485)

button_PatientName_Search=ttk.Button(root, text='Search', width=15, command=patientNameSearch)
button_PatientName_Search.place(x=620, y=500)

root.mainloop()

conn.close()

#t = datetime.datetime.now()
#ts = str(datetime.datetime.now())

#datetime.datetime.strptime(ts, '%Y%m%d%I%M%S%f')