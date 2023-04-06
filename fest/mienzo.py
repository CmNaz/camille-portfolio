import c, config, time, threading
from uslov import viye
#from xuslov import viye as xviye
from HR import biHR
from MIN15 import bi15
from MIN5 import bi5MIN
from MIN1 import bi1MIN
import discord
from tkinter import *
from tkinter import ttk
import tkinter as tk
from discord.ext.commands import Bot
# thread1=biHR()
# thread2=bi15()
# thread3=pint()

# thread1.start()
# thread2.start()
# thread3.start()
dclient=discord.Client()


#COMMENT OUT THE USAGE OF 5MIN AND 3MIN

def red():
    a=0
    if a==0:
        a+=1
        print("@@@@@@@@@@@@@@@@@ RESTART TRIGGERED @@@@@@@@@@@@@@@@@")
    if c.restart:
        
        c.ctr=0

        for i in c.ex:
            c.threadv[c.ctr].stop()
            c.threadv[c.ctr].join()
            c.threadHr[c.ctr].stop()
            c.threadHr[c.ctr].join()
            c.threadMin[c.ctr].stop()
            c.threadMin[c.ctr].join()
            c.thread5MIN[c.ctr].stop()
            c.thread5MIN[c.ctr].join()
            c.thread1MIN[c.ctr].stop()
            c.thread1MIN[c.ctr].join()
            time.sleep(10)

            if not c.threadv[c.ctr].isAlive():
                print("PINT THREAD TERMINATED")
            if not c.threadHr[c.ctr].isAlive():
                print("HOUR THREAD TERMINATED")
            if not c.threadMin[c.ctr].isAlive():
                print("15-MIN THREAD TERMINATED")
            if not c.thread5MIN[c.ctr].isAlive():
                print("5-MIN THREAD TERMINATED")
            if not c.thread1MIN[c.ctr].isAlive():
                print("1-MIN THREAD TERMINATED")
            
            
            if not c.thread1MIN[c.ctr].isAlive() and not c.thread5MIN[c.ctr].isAlive()  and not c.threadMin[c.ctr].isAlive() and not c.threadHr[c.ctr].isAlive() and not c.threadv[c.ctr].isAlive():
                print("---------------- ALL THREADS TERMINATED ----------------")
            c.ctr+=1
     
        c.viy.clear()
        c.xviy.clear()
        c.threadv.clear()
        c.threadHr.clear()
        c.threadMin.clear
        c.thread5MIN.clear()
        c.thread1MIN.clear()

        c.ctr=0
        for i in c.ex:

            # viy[ctr]=viye()
            c.viy.append(viye())
            c.xviy.append(viye())
            c.yviy.append(viye())
            c.threadv.append(pint(c.viy[c.ctr], c.xviy[c.ctr], i, c.crypt[c.ctr]))
            c.threadv[c.ctr].start()

            c.threadHr.append(biHR(c.viy[c.ctr]))
            c.threadMin.append(bi15(c.viy[c.ctr], c.xviy[c.ctr]))
            
            c.thread5MIN.append(bi5MIN(c.xviy[c.ctr], c.yviy[c.ctr]))
            c.thread1MIN.append(bi1MIN(c.yviy[c.ctr]))

            c.threadHr[c.ctr].start()
            time.sleep(10)
            c.threadMin[c.ctr].start()
            time.sleep(5)
            c.thread5MIN[c.ctr].start()
            time.sleep(5)
            c.thread1MIN[c.ctr].start()
            time.sleep(5)
            c.ctr+=1
        c.restart=False
        c.recnt+=1
        
def disc():
    # client = Bot(command_prefix='-')

    # @client.command(pass_context=True)
    # async def purge(ctx, amount=7):
    #     channel = ctx.message.channel
    #     messages = []
    #     async for message in channel.history(limit=amount + 1):
    #             messages.append(message)

    #     await channel.delete_messages(messages)
    #     await ctx.send(f'{amount} messages have been purged by {ctx.message.author.mention}')
    @dclient.event
    async def on_ready():
        print("!!!!!!!!!!DISCORD ALSO WORKS!!!!!!!!!!")
        print('We have logged in as {0.user}'.format(dclient))

    @dclient.event
    async def on_message(message):
        username=str(message.author).split('#')[0]
        user_message=str(message.content)
        channel=str(message.channel.name)
        print(f'{username}: {user_message} ({channel})')


        if message.author == dclient.user:
            return
        if message.channel.name=='bs':
            if user_message.lower()=='!purge':
                messages = []
                async for msg in message.channel.history(limit=15 + 1):
                        messages.append(msg)

                await message.channel.delete_messages(messages)
                return

            elif user_message.lower()=='hello':
                await message.channel.send(f'Hello {username}!')
                return

            elif user_message.lower()=='bye':
                await message.channel.send(f'See you later {username}!')
                return
            
            elif user_message.lower()=='!ree':
                await message.channel.send(f'Restart: {c.restart}')
                c.restart=True
                await message.channel.send(f'Restart: {c.restart}')
                await message.channel.send(f'Restart: {c.restart}')
                # await message.channel.send(f'********OPERATION RED SUCCESS!!!********')
                return

            elif user_message.lower()=='!error':
                await message.channel.send("ERROR MESSAGE IN KDJ: ")
                await message.channel.send(c.errmsg)

            elif user_message.lower()=='!status':
                response=f'\nRestart: {c.restart}, No. of Restarts: {c.recnt}\nStatus1: {c.status1}, Status2: {c.status2}, Status3: {c.status3}, Status4:{c.status4}'
                await message.channel.send(response)
                ctr=0
                for i in c.ex:
                    resp=f'\nTHREAD NO. {ctr+1}\nPINT: {c.threadv[ctr].isAlive()}, HOUR: {c.threadHr[ctr].isAlive()}, 15-MIN: {c.threadMin[ctr].isAlive()}, 5-MIN: {c.thread5MIN[ctr].isAlive()}, 1-MIN:{c.thread1MIN[ctr].isAlive()}'
                    await message.channel.send(resp)
                    ctr+=1
                
                
                
                return

            elif user_message.lower()=='!stats':
                c.strl=("==================================================================================="
                +"\n\nAll 1-hour closes:\r\r"+"\n{}".format(c.closesTHR_1[-5:])+"\nPast Trades: {}".format(c.pasTrades[-7:])+"\n\nTrack Test: {}".format(c.trackTest[-7:])
                +"\nCurrent 1-hour RSI 6 is: {}".format(c.rsi6_1)+"\nCurrent 1-hour RSI 12 is: {}".format(c.rsi12_1)+"\nCurrent 1-hour RSI 24 is: {}".format(c.rsi24_1)+
                "\n\nXCTR: {}".format(c.xctr)+"\nUsual: {}".format(c.usual))
                if not c.usual and c.zctr<10 and c.zctr>6:
                    c.strl2=("==================================================================================="
                    +"\n\nAll 15-MIN closes:\r\r"+"\n{}".format(c.closesTHR_2[-5:])+"\nPast Trades: {}".format(c.pasTrades[-7:])+"\n\nTrack Test: {}".format(c.trackTest[-7:])
                    +"\nCurrent 15-MIN RSI 6 is: {}".format(c.rsi6_2)+"\nCurrent 15-MIN RSI 12 is: {}".format(c.rsi12_2)+"\nCurrent 15-MIN RSI 24 is: {}".format(c.rsi24_2))
                if not c.usual and c.zctr>9:
                    c.strl3=("==================================================================================="
                    +"\n\nAll 5-MIN closes:\r\r"+"\n{}".format(c.closesTHR_1[-5:])+"\nPast Trades: {}".format(c.pasTrades[-7:])+"\n\nTrack Test: {}".format(c.trackTest[-7:])
                    +"\nCurrent 5-MIN RSI 6 is: {}".format(c.rsi6_3)+"\nCurrent 5-MIN RSI 12 is: {}".format(c.rsi12_3)+"\nCurrent 5-MIN RSI 24 is: {}".format(c.rsi24_3))
                kdj=("==================================================================================="
                +"\n\nupTrend: {}".format(c.upTrend)+"         KEPP: {}".format(c.total)
                +"\nRSI Uptrend Strength: {}".format(c.strupTrend)+"   RSI Downtrend Strength: {}".format(c.strdownTrend)
                +"\nKDJ Uptrend Strength: {}".format(c.kdjstrupTrend)+"   KDJ Downtrend Strength: {}".format(c.kdjstrdownTrend)
                +"\n1-HOUR \nK: {}".format(c.kay[-5:])+"\nD: {}".format(c.dee[-5:])+"\nJ: {}".format(c.jay[-5:])
                +"\n15-MIN \nK: {}".format(c.kay_15[-5:])+"\nD: {}".format(c.dee_15[-5:])+"\nJ: {}".format(c.jay_15[-5:])
                +"\n5-MIN \nK: {}".format(c.kay_5[-5:])+"\nD: {}".format(c.dee_5[-5:])+"\nJ: {}".format(c.jay_5[-5:])
                +"\nLongHalt: {}".format(c.longHalt)+"\nShortHalt: {}".format(c.shortHalt)+"\nLongJatkaa: {}".format(c.longJatkaa)+"\nShortJatkaa: {}".format(c.shortJatkaa)
                )
                await message.channel.send(kdj)
                await message.channel.send(c.strl)
                await message.channel.send(c.strl2)
                await message.channel.send(c.strl3)
                await message.channel.send(c.strl4)
                return

        if user_message.lower()=='!anywhere':
            await message.channel.send('This can be used anywhere!')
            return
    dclient.run(config.DISC)
    # client.run(config.DISC)
    



class pint(threading.Thread):
    def __init__(self,u,u2,u3,symbol,crypt):
        super(pint, self).__init__()
        self.lock=threading.Lock()
        self.u=u
        self.u2=u2
        self.u3=u3
        self.u.TRADE_SYMBOL=symbol
        self.u.CRYPT=crypt
        self.u.thread=15
        self.u2.TRADE_SYMBOL=symbol
        self.u2.CRYPT=crypt
        self.u2.thread=5
        self.u3.TRADE_SYMBOL=symbol
        self.u3.CRYPT=crypt
        self.u3.thread=1

        self._stop = threading.Event()
        self.death=False
 
    # function using _stop function
    def stop(self):
        self.death=True
        return
 

    def run(self):
        x=0
        
        while True:
        
            # if self.u.geste:
            #     self.u.do()
            # elif self.u2.geste:
            #     self.u2.do()
            if x==0:
                time.sleep(40)
                x+=1
                
            #
            if c.status1 and c.status2 and c.status3 and c.status4 :#x
                c.restart=False
            else:
                c.restart=True
            if c.restart:
                red()

            if self.death:
                return
            
            
            


       

def do():
    
    for i in c.ex:

        # viy[ctr]=viye()
        c.viy.append(viye())
        c.xviy.append(viye())
        c.yviy.append(viye())
        c.threadv.append(pint(c.viy[c.ctr], c.xviy[c.ctr], c.yviy[c.ctr],i, c.crypt[c.ctr]))
        c.threadv[c.ctr].start()

        c.threadHr.append(biHR(c.viy[c.ctr]))
        c.threadMin.append(bi15(c.viy[c.ctr], c.xviy[c.ctr]))
        
        c.thread5MIN.append(bi5MIN(c.xviy[c.ctr], c.yviy[c.ctr]))
        c.thread1MIN.append(bi1MIN(c.yviy[c.ctr]))

        c.threadHr[c.ctr].start()
        time.sleep(10)
        c.threadMin[c.ctr].start()
        time.sleep(5)
        c.thread5MIN[c.ctr].start()
        time.sleep(5)
        c.thread1MIN[c.ctr].start()
        time.sleep(5)
        c.ctr+=1
    time.sleep(3)
    disc()
    time.sleep(5)
    
        

    