import tkinter as tk
from tkinter import messagebox  # import this to fix messagebox error
import RSA
import Common_Mode_Attack
import Low_Encryption_Exponent_Attack
import Low_Private_Exponent_Attack


window = tk.Tk()
window.title('Welcome to RSA Encryption and decryption system ')
window.geometry('450x300')

# welcome image
canvas = tk.Canvas(window, height=300, width=500)
image_file = tk.PhotoImage(file='welcome.gif')
image = canvas.create_image(0, 0, anchor='nw', image=image_file)
canvas.pack(side='top')

tk.Label(window, text='Do you need to encrypt or decrypt?').place(x=100, y=180)

entext = 0
d = 0
N = 0

def Encrypt():
    def Encrypt_GUI():
        global entext, d, N, p, q
        e, d, N, p, q =RSA.get_key()
        Text_public_key.insert(1.0, '('+str(N)+','+str(e)+')')

        '''加密过程'''
        global entext
        entext = RSA.RSA_Encrypt(message.get(), N, e)
        Text_encryption_result.insert(1.0, entext)  # RSA通过公钥（N, e)进行加密
        tk.messagebox.showinfo('Encryption result', 'The Encryption result is as follows：' + str(entext))

    window_encrypt = tk.Toplevel(window)
    window_encrypt.geometry('800x500')
    window_encrypt.title('Encryption system')

    message = tk.StringVar()
    message.set('   Please enter the Message ')
    tk.Label(window_encrypt, text='Message : ').place(x=120, y=100)
    entry_message = tk.Entry(window_encrypt, highlightcolor='red', textvariable=message)
    entry_message.place(x=240, y=100, width=200)

    tk.Label(window_encrypt, text='Public key: ').place(x=120, y=145)
    Text_public_key = tk.Text(window_encrypt, width=120, height=30, font=('楷书', 10), bg="OldLace")
    Text_public_key.place(x=240, y=145, height=100, width=500)

    tk.Label(window_encrypt, text='Encryption result: ').place(x=120, y=275)
    Text_encryption_result = tk.Text(window_encrypt, width=120, height=30, font=('楷书', 10), bg="LightCyan")
    Text_encryption_result.place(x=240, y=275, height=100, width=500)

    btn_Encrypt = tk.Button(window_encrypt, text='Encrypt', command=Encrypt_GUI)
    btn_Encrypt.place(x=240, y=400)






def Decrypt():

    def Decrypt_GUI():
        decrypted, run_time = RSA.RSA_Decrypt(entext, N, d)
        Text_Decryption_result.insert(1.0, decrypted)
        runtime.set(str(run_time))
        tk.messagebox.showinfo('Decryption result', 'The result Decryption is as follows：'+str(decrypted)+'\nRuntime: '+str(run_time))

    window_decrypt = tk.Toplevel(window)
    window_decrypt.geometry('800x600')
    window_decrypt.title('Decryption system')

    # ciphertext = tk.StringVar()
    # ciphertext.set('   Please enter the ciphertext ')t
    tk.Label(window_decrypt, text='Ciphertext: ').place(x=120, y=120)
    Text_ciphertext = tk.Text(window_decrypt, width=120, height=30, font=('楷书', 10), bg="Ivory",)
    Text_ciphertext.place(x=240, y=80, height=100, width=500)
    Text_ciphertext.insert(1.0, entext)

    # Secret_key = tk.StringVar()
    tk.Label(window_decrypt, text='Secret key: ').place(x=120, y=240)
    Text_Secret_key = tk.Text(window_decrypt, width=120, height=30, font=('楷书', 10), bg="WhiteSmoke")
    Text_Secret_key.place(x=240, y=200, height=100, width=500)
    Text_Secret_key.insert(1.0, d)
    # Decryption_result = tk.StringVar()
    tk.Label(window_decrypt, text='Decryption result: ').place(x=120, y=360)
    Text_Decryption_result = tk.Text(window_decrypt, width=120, height=30, font=('楷书', 10), bg="Azure")
    Text_Decryption_result.place(x=240, y=320, height=100, width=500)

    runtime = tk.StringVar()
    tk.Label(window_decrypt, text='Run_time : ').place(x=120, y=430)
    entry_run_time = tk.Entry(window_decrypt, highlightcolor='red', textvariable=runtime)
    entry_run_time.place(x=240, y=430, width=200)

    btn_Decrypt = tk.Button(window_decrypt, text='Decrypt', command=Decrypt_GUI)
    btn_Decrypt.place(x=240, y=470)



#解密算法改进
def CRT():
    def CRT_GUI():
        crt_decrypted, crt_run_time = RSA.RSA_CRT(entext, p, q, d)
        Text_crt_Decryption_result.insert(1.0, crt_decrypted)
        crt_runtime.set(str(crt_run_time))
        tk.messagebox.showinfo('Decryption result', 'The result Decryption is as follows：'+str(crt_decrypted)+'\nRuntime: '+str(crt_run_time))

    window_crt_decrypt = tk.Toplevel(window)
    window_crt_decrypt.geometry('800x600')
    window_crt_decrypt.title('Decryption system:CRT')

    # ciphertext = tk.StringVar()
    # ciphertext.set('   Please enter the ciphertext ')t
    tk.Label(window_crt_decrypt, text='Ciphertext: ').place(x=120, y=120)
    Text_crt_ciphertext = tk.Text(window_crt_decrypt, width=120, height=30, font=('楷书', 10), bg="Ivory",)
    Text_crt_ciphertext.place(x=240, y=80, height=100, width=500)
    Text_crt_ciphertext.insert(1.0, entext)

    # Secret_key = tk.StringVar()
    tk.Label(window_crt_decrypt, text='Secret key: ').place(x=120, y=240)
    Text_crt_Secret_key = tk.Text(window_crt_decrypt, width=120, height=30, font=('楷书', 10), bg="WhiteSmoke")
    Text_crt_Secret_key.place(x=240, y=200, height=100, width=500)
    Text_crt_Secret_key.insert(1.0, d)
    # Decryption_result = tk.StringVar()
    tk.Label(window_crt_decrypt, text='Decryption result: ').place(x=120, y=360)
    Text_crt_Decryption_result = tk.Text(window_crt_decrypt, width=120, height=30, font=('楷书', 10), bg="Azure")
    Text_crt_Decryption_result.place(x=240, y=320, height=100, width=500)

    crt_runtime = tk.StringVar()
    tk.Label(window_crt_decrypt, text='CRT_Run_time : ').place(x=120, y=430)
    entry_crt_run_time = tk.Entry(window_crt_decrypt, highlightcolor='red', textvariable=crt_runtime)
    entry_crt_run_time.place(x=240, y=430, width=200)

    btn_crt_Decrypt = tk.Button(window_crt_decrypt, text='CRT_Decrypt', command=CRT_GUI)
    btn_crt_Decrypt.place(x=240, y=470)

def Common_Mode_attack():
    def Attack():
        e1, e2, s1, s2, Attack_mess, N = Common_Mode_Attack.Common_Mode_Attack(Message.get())
        # print(s1)
        e1_text.insert(1.0, e1)
        e2_text.insert(1.0, e2)
        s1_text.insert(1.0, s1)
        s2_text.insert(1.0, s2)
        attack_text.insert(1.0, Attack_mess)
        Text_N.insert(1.0, N)


    window_Mode_attack = tk.Toplevel(window)
    window_Mode_attack.geometry('800x600')
    window_Mode_attack.title('Common_Mode_attack')

    Message = tk.StringVar()
    Message.set('     Please enter the Message ')
    tk.Label(window_Mode_attack, text='Message : ').place(x=150, y=80)
    entry_message = tk.Entry(window_Mode_attack, highlightcolor='red', textvariable=Message)
    entry_message.place(x=240, y=80, width=200)

    tk.Label(window_Mode_attack, text='N: ').place(x=150, y=130)
    Text_N = tk.Text(window_Mode_attack, width=120, height=30, font=('楷书', 10), bg="WhiteSmoke")
    Text_N.place(x=240, y=130, height=100, width=400)


    tk.Label(window_Mode_attack, text='e1 : ').place(x=150, y=250)
    e1_text = tk.Text(window_Mode_attack, width=120, height=30, font=('楷书', 10), bg="LightGrey", )
    e1_text.place(x=240, y=250, height=40, width=400)


    tk.Label(window_Mode_attack, text='e2 : ').place(x=150, y=310)
    e2_text = tk.Text(window_Mode_attack, width=120, height=30, font=('楷书', 10), bg="Honeydew", )
    e2_text.place(x=240, y=310, height=40, width=400)



    tk.Label(window_Mode_attack, text='s1 : ').place(x=150, y=370)
    s1_text = tk.Text(window_Mode_attack, width=120, height=30, font=('楷书', 10), bg="LightCyan", )
    s1_text.place(x=240, y=370, height=40, width=400)

    tk.Label(window_Mode_attack, text='s2 : ').place(x=150, y=430)
    s2_text = tk.Text(window_Mode_attack, width=120, height=30, font=('楷书', 10), bg="OldLace", )
    s2_text.place(x=240, y=430, height=40, width=400)

    tk.Label(window_Mode_attack, text='Attack_text : ').place(x=150, y=490)
    attack_text = tk.Text(window_Mode_attack, width=120, height=30, font=('楷书', 10), bg="Tan", )
    attack_text.place(x=240, y=490, height=40, width=400)

    btn_Mode_attack = tk.Button(window_Mode_attack, text='Attack', command=Attack)     
    btn_Mode_attack.place(x=240, y=550)

def Low_Encryption_Exponent_attack():
    def Attack():
        n1, n2, n3, C1, C2, C3, M = Low_Encryption_Exponent_Attack.Low_Exponent_Attack(msg.get())
        n1_text.insert(1.0, n1)
        n2_text.insert(1.0, n2)
        n3_text.insert(1.0, n3)
        C1_text.insert(1.0, C1)
        C2_text.insert(1.0, C2)
        C3_text.insert(1.0, C3)
        M_text.insert(1.0, M)

    window_Low_Encryption_Exponent_attack = tk.Toplevel(window)
    window_Low_Encryption_Exponent_attack.geometry('800x600')
    window_Low_Encryption_Exponent_attack.title('Low_Encryption_Exponent_attack')

    msg = tk.StringVar()
    msg.set('     Please enter the Message ')
    tk.Label(window_Low_Encryption_Exponent_attack, text='Message : ').place(x=150, y=80)
    entry_msg = tk.Entry(window_Low_Encryption_Exponent_attack, highlightcolor='red', textvariable=msg)
    entry_msg.place(x=240, y=80, width=200)

    tk.Label(window_Low_Encryption_Exponent_attack, text='n1: ').place(x=150, y=130)
    n1_text = tk.Text(window_Low_Encryption_Exponent_attack, width=120, height=30, font=('楷书', 10), bg="WhiteSmoke")
    n1_text.place(x=240, y=130, height=20, width=400)


    tk.Label(window_Low_Encryption_Exponent_attack, text='n2 : ').place(x=150, y=170)
    n2_text = tk.Text(window_Low_Encryption_Exponent_attack, width=120, height=30, font=('楷书', 10), bg="WhiteSmoke", )
    n2_text.place(x=240, y=170, height=20, width=400)


    tk.Label(window_Low_Encryption_Exponent_attack, text='n3 : ').place(x=150, y=210)
    n3_text = tk.Text(window_Low_Encryption_Exponent_attack, width=120, height=30, font=('楷书', 10), bg="WhiteSmoke", )
    n3_text.place(x=240, y=210, height=20, width=400)

    tk.Label(window_Low_Encryption_Exponent_attack, text='C1 : ').place(x=150, y=250)
    C1_text = tk.Text(window_Low_Encryption_Exponent_attack, width=120, height=30, font=('楷书', 10), bg="LightCyan", )
    C1_text.place(x=240, y=250, height=20, width=400)

    tk.Label(window_Low_Encryption_Exponent_attack, text='C2 : ').place(x=150, y=290)
    C2_text = tk.Text(window_Low_Encryption_Exponent_attack, width=120, height=30, font=('楷书', 10), bg="LightCyan", )
    C2_text.place(x=240, y=290, height=20, width=400)

    tk.Label(window_Low_Encryption_Exponent_attack, text='C3 : ').place(x=150, y=330)
    C3_text = tk.Text(window_Low_Encryption_Exponent_attack, width=120, height=30, font=('楷书', 10), bg="LightCyan", )
    C3_text.place(x=240, y=330, height=20, width=400)

    tk.Label(window_Low_Encryption_Exponent_attack, text='Attack Process : ').place(x=350, y=370)
    tk.Label(window_Low_Encryption_Exponent_attack, text='C1=M³(mod n1) ').place(x=350, y=390)
    tk.Label(window_Low_Encryption_Exponent_attack, text='C2=M³(mod n2) ').place(x=350, y=410)
    tk.Label(window_Low_Encryption_Exponent_attack, text='C3=M³(mod n3) ').place(x=350, y=430)
    tk.Label(window_Low_Encryption_Exponent_attack, text='Figure out the M ').place(x=350, y=450)

    tk.Label(window_Low_Encryption_Exponent_attack, text='M : ').place(x=150, y=490)
    M_text = tk.Text(window_Low_Encryption_Exponent_attack, width=120, height=30, font=('楷书', 10), bg="Tan", )
    M_text.place(x=240, y=490, height=40, width=400)

    btn_Low_Encryption_Exponent_attack = tk.Button(window_Low_Encryption_Exponent_attack, text='Attack', command=Attack)     
    btn_Low_Encryption_Exponent_attack.place(x=240, y=550)

def Low_private_exponent():
    def Attack():
        e, N, d = Low_Private_Exponent_Attack.generateKeys()    #生成公钥和私钥
        entext = Low_Private_Exponent_Attack.RSA_Encrypt(msg.get(), N, e)   #加密
        d1 = Low_Private_Exponent_Attack.hack_RSA(e, N, entext)   #攻击得到私钥d1
        m = Low_Private_Exponent_Attack.RSA_Decrypt(entext, N, d)    #通过d1得到明文
        d_text.insert(1.0, d)
        d1_text.insert(1.0, d1)
        m_text.insert(1.0, m)


    window_Low_Private_Exponent_Attack = tk.Toplevel(window)
    window_Low_Private_Exponent_Attack.geometry('800x600')
    window_Low_Private_Exponent_Attack.title('Low_Private_Exponent_Attack')

    msg = tk.StringVar()
    msg.set('     Please enter the Message ')
    tk.Label(window_Low_Private_Exponent_Attack, text='Message : ').place(x=150, y=80)
    entry_msg = tk.Entry(window_Low_Private_Exponent_Attack, highlightcolor='red', textvariable=msg)
    entry_msg.place(x=240, y=80, width=200)

    tk.Label(window_Low_Private_Exponent_Attack, text='The secret key‘d’ we choose: ').place(x=330, y=130)
    d_text = tk.Text(window_Low_Private_Exponent_Attack, width=120, height=30, font=('楷书', 10), bg="WhiteSmoke")
    d_text.place(x=240, y=160, height=100, width=400)

    tk.Label(window_Low_Private_Exponent_Attack, text='The secret key‘d1’ we get by attacking: ').place(x=330, y=280)
    d1_text = tk.Text(window_Low_Private_Exponent_Attack, width=120, height=30, font=('楷书', 10), bg="WhiteSmoke")
    d1_text.place(x=240, y=310, height=100, width=400)

    tk.Label(window_Low_Private_Exponent_Attack, text='The message‘M’ we get by using ‘d1’: ').place(x=330, y=430)
    m_text = tk.Text(window_Low_Private_Exponent_Attack, width=120, height=30, font=('楷书', 10), bg="WhiteSmoke")
    m_text.place(x=240, y=450, height=100, width=400)

    btn_Low_Private_Exponent_Attack = tk.Button(window_Low_Private_Exponent_Attack, text='Attack', command=Attack)     
    btn_Low_Private_Exponent_Attack.place(x=240, y=560)

# Encrypt  and Decrypt button
btn_encrypt = tk.Button(window, text='encrypt', command=Encrypt)
btn_encrypt.place(x=130, y=220)
btn_decrypt = tk.Button(window, text='decrypt', command=Decrypt)
btn_decrypt.place(x=210, y=220)

# MENU
menubar = tk.Menu(window)

filemenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='MENU', menu=filemenu)
filemenu.add_command(label='CRT', command=CRT)
window.config(menu=menubar)



editmenu = tk.Menu(menubar, tearoff=False)
menubar.add_cascade(label="Attack", menu=editmenu)
editmenu.add_command(label="Common_Mode", command=Common_Mode_attack)
editmenu.add_command(label="low_Encryption_Exponent", command=Low_Encryption_Exponent_attack)
editmenu.add_command(label="Low_Private_Exponent", command=Low_private_exponent)


window.mainloop()