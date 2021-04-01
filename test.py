from stegano import lsb

secret = lsb.hide("C://Users//Ambar//OneDrive//Pictures//Steg.docx", "Hello World")
secret.save("./enc_steg.docx")