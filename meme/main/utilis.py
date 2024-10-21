import bcrypt
#users=[]
def userExist(userdata,cursor):
    
    sql_quries=f'''
                    select * from users;
    
    '''
    try:
        cursor.execute(sql_quries)
        users=cursor.fetchall()
    except Exception as e:
        print("error",e)
    email=userdata['email']
    print(users)
    if len(users)==0:
        return {"response":False,"detail":{}}

    for user in users:
        if user[1]==email:
            return {"response":True,"detail":user}
    else:
        return {"response":False,"detail":{}}


def registerUser(userdata,cursor):
    result=userExist(userdata,cursor)
    
    if result['response']==True:
        return {"status":200,"message":"Already registered"}
    else:
        sql_quries=f'''
            insert into users values ('{userdata['name']}','{userdata['email']}','{userdata['password']}','{userdata['contact']}');
        
        '''
        try:
            cursor.execute(sql_quries)
        except Exception as e:
            print("error",e)

        return {"status":503,"message":"registered"}

def userLogin(userdata,cursor):
    result=userExist(userdata,cursor)
    
    if result['response']==True:
        if bcrypt.checkpw(userdata['password'].encode(),result['detail'][2].encode()):
            return {"status":200,"message":"Successfully login"}
        else:
            return {"status":503,"message":"password error"}
    else:
        return {"status":503,"message":"Not registered"}
   