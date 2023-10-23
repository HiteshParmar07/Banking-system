import mysql.connector
import getpass
from datetime import date

mydb = mysql.connector.connect(
    host='localhost', user='SURAJ', passwd='SAJANBAI0711', database='bank')


mycursor = mydb.cursor()

mycursor.execute(
    "create table if not exists Master(acno char(4) primary key ,passward char(4))")
mycursor.execute(
    "create table if not exists bank_master(acno char(4) ,name varchar(30),city char(20),mobileno char(10),balance int(6),doc date,foreign key (acno) references Master(acno))")
mycursor.execute(
    "create table if not exists banktrans(acno char (4),amount int(6),dot date ,ttype char(1),foreign key (acno) references Master(acno))")

mydb.commit()

Account = 0
flag = 0
login = 0


def auth():
    global flag, login
    acc = input("Enter Account number : ")
    pswd = getpass.getpass('Enter Pin : ')
    mycursor.execute("select * from master where acno='" +
                     acc+"' and pass='"+pswd+"'")
    result = mycursor.fetchone()
    if result:
        global Account
        Account = acc
        flag = 1
        login = 1
        return 1
    else:
        return 0


def CreateAccount():
    global flag
    print("All information prompted are mandatory to be filled")
    acno = str(input("Enter account number : "))
    acc = acno
    pswd = str(input("Create Your Password : "))
    name = input("Enter name(limit 35 characters) : ")
    city = str(input("Enter city name : "))
    mn = str(input("Enter mobile no. : "))
    doc = str(date.today())
    balance = 0
    mycursor.execute("insert into master values('"+acno+"','"+pswd+"')")
    mycursor.execute("insert into bank_master values('"+acc +
                     "','"+name+"','"+city+"','"+mn+"','"+str(balance)+"','"+doc+"')")

    mydb.commit()
    print("Account is successfully created!!!")
    global Account
    Account = acc
    flag = 1


def DepositeMoney():
    global Account
    acno = Account
    dp = int(input("Enter amount to be deposited:"))
    dot = str(date.today())
    ttype = "d"
    mycursor.execute("insert into banktrans values('"+acno +
                     "','"+str(dp)+"','"+dot+"','"+ttype+"')")
    mycursor.execute(
        "update bank_master set balance=balance+'"+str(dp)+"' where acno='"+acno+"'")
    mydb.commit()
    print("money has been deposited successully!!!")
    ch = int(input('Like you see your balance:\n\t1.Yes\n\t2.No\n'))
    if ch == 1:
        ShowBalance()
    else:
        return


def WithdrawMoney():
    global Account
    acno = Account
    wd = int(input("Enter amount to be withdrawn:"))
    dot = str(date.today())
    ttype = "w"
    mycursor.execute("select balance from bank_master where acno='"+acno+"'")
    res = mycursor.fetchone()
    res = res[0]
    if wd > res:
        print("insufficient balance")
        return 0
    mycursor.execute("insert into banktrans values('" +
                     acno+"','"+str(wd)+"','"+dot+"','"+ttype+"')")
    mycursor.execute(
        "update bank_master set balance=balance-'"+str(wd)+"' where acno='"+acno+"'")
    mydb.commit()
    ch = int(input('Like you see your balance:\n\t1.Yes\n\t2.No\n'))
    if ch == 1:
        ShowBalance()
    else:
        return


def ShowBalance():
    global Account
    acno = Account
    mycursor.execute("select balance from bank_master where acno='"+acno+"'")
    res = mycursor.fetchone()
    res = res[0]
    print('current balance : ', res)


def DisplayAcc():
    global Account
    acno = Account
    mycursor.execute("select * from bank_master where acno='"+acno+"'")
    res = mycursor.fetchall()
    print('Account Number : ', (res[0])[0])
    print('Account Holdar Name : ', (res[0])[1])
    print('Account Holdar City : ', (res[0])[2])
    print('Account Holdar Moblie number : ', (res[0])[3])
    print('Balance (in $): ', (res[0])[4])
    print('Date of Creation (yyyy-mm-dd): ', (res[0])[5])


def AccHistory():
    global Account
    acno = Account
    mycursor.execute("select * from banktrans where acno='"+acno+"'")
    res = mycursor.fetchall()

    print("amount\t\tdate\ttype")
    for i in res:
        print(i[1], '\t', i[2], '\t', i[3])


if __name__ == "__main__":

    ch = 100

    while ch != 0:
        print("\t1.Create Accont \n\t2.Deposit money \n\t3.Withdraw money \n\t4.Display account Details \n\t5.Account Yranstions\n\t0.Exit")
        ch = int(input("Enter Your Choice : "))
        if(ch == 1):
            if login == 1:
                print("Already Login \nChose different Option")
            else:
                CreateAccount()

        elif ch == 2:
            if flag == 0:
                if auth():
                    DepositeMoney()
                else:
                    print("Invalid Account number or pin")
                    break

            else:
                DepositeMoney()

        elif ch == 3:
            if flag == 0:
                if auth():
                    WithdrawMoney()
                else:
                    print("Invalid Account number or pin")
                    break

            else:
                WithdrawMoney()

        elif ch == 4:
            if flag == 0:
                if auth():
                    DisplayAcc()
                else:
                    print("Invalid Account number or pin")
                    break

            else:
                DisplayAcc()
        elif ch == 5:
            if flag == 0:
                if auth():
                    AccHistory()
                else:
                    print("Invalid Account number or pin")
                    break

            else:
                AccHistory()

        else:
            break
