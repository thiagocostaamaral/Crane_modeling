## GUINDASTE MOVEL
import math
from matplotlib import pyplot as plt
import turtle
#Função para pegar linha de uma matriz
def p_coluna(matriz,coluna):                 #pega determinado coluna de uma matriz
    a=[]
    for i in range (len(matriz)):
        a.append([matriz[i][coluna]])
    return a;
def inverte(matriz):
    p=len(matriz)
    q=len(matriz[0])
    a=[]
    for i in range (p):
        linha=[]
        for j in range(q):
            linha.append(-matriz[p][q])
        a.append(linha)
    return a
    
#--------CONSTANTES----------
pi=math.pi
g=9.81;         #Gravidade (m/s^2)
Mt=2500;        #Massa do carro (kg)
Ml=400;         #Massa da carga(kg)
Md=30;          #Massa do tambor (kg)
r=1;            #Raio do tambor(metros)
Td=3990;        #Torque do motor de içamento(N.m)
Ft=200;         #Força que atua sobre carro(N)
#E=420;         #Tensão sobre o circuito eletrico(V)
E=920;          #Tensão sobre o circuito eletrico(V)
R=10;           #Resistencia(oms)
L=0.50          #Indutancia(H)
Bc=0
Bs=80
K=10;
K1=1;         
I=(Md*r**2);    #Momento de Inercia do motor(kg.m^2)
Fl=Td/r;        #Força do tambor sobre o cabo(N)
Lf=7            #Comprimento final do cabo
#------CONDIÇÃO INICIAL-----
x=[[0,0,10,0]]  # x[0][0]=x;   x[0][1]=fi, x[0][2]=l, x[0][3]=q
dx=[[0,0,0,0]]
ddx=[[0,0,0,0]]
xl=[0]
yl=[-x[0][2]]
listazero=[0]

y=[[0,0,10,0]]  # y[0][0]=x;   y[0][1]=fi, y[0][2]=l, y[0][3]=q
dy=[[0,0,0,0]]
ddy=[[0,0,0,0]]
yxl=[0]
yyl=[-y[0][2]]

z=[[0,0,10,0]]  # y[0][0]=x;   y[0][1]=fi, y[0][2]=l, y[0][3]=q
dz=[[0,0,0,0]]
ddz=[[0,0,0,0]]
zxl=[0]
zyl=[-z[0][2]]


listazero=[0]
tlist=[0]
###     Gambiarra para facilitar a copiar solução linear
Mc=Mt
Ts=-Td
F=Ft
###
def main():
    print("Guindaste Móvel \n\n")
    #t=int(input("Informe o valor do tempo desejado"))
    tf=23
    h=0.0001           #Passo
    #----VARIAVEIS DE CONTROLE----
    n=int(tf/h)       #numero de interações
    t=0
    k=0
    E0=E
    #-----Variaveis Turtle-----
    #Guindaste
    gui=turtle.Pen()
    gui.speed(0)
    gui.goto(220,0)
    gui.goto(220,-20)
    gui.goto(20,-20)
    gui.goto(0,0)
    gui.goto(20,-20)
    gui.goto(40,0)
    gui.goto(60,-20)
    gui.goto(80,0)
    gui.goto(100,-20)
    gui.goto(120,0)
    gui.goto(140,-20)
    gui.goto(160,0)
    gui.goto(180,-20)
    gui.goto(200,0)
    gui.goto(220,-20)
    gui.goto(220,-180)
    gui.goto(230,-180)
    gui.goto(230,70)
    gui.goto(220,70)
    gui.goto(220,0)
    gui.goto(220,40)
    gui.pensize(3)
    gui.goto(30,0)
    gui.pensize(1)
    gui.goto(0,0)
    gui.goto(0,-20*x[0][2])
    gui.goto(50,-20*x[0][2])
    gui.goto(40,-20*x[0][2]-30)
    gui.goto(-40,-20*x[0][2]-30)
    gui.goto(-45,-20*x[0][2]-15)
    gui.color("blue")
    gui.goto(-100,-20*x[0][2]-15)
    gui.goto(-45,-20*x[0][2]-15)
    gui.color("black")
    gui.goto(-50,-20*x[0][2])
    gui.goto(50,-20*x[0][2])
    gui.goto(45,-20*x[0][2]-15)
    gui.color("blue")
    gui.goto(190,-20*x[0][2]-15)
    gui.color("black")
    gui.goto(190,-240)
    gui.goto(190,-180)
    gui.goto(260,-180)
    gui.goto(230,-180)
    gui.goto(230,0)
    gui.goto(290,0)
    gui.goto(290,-20)
    gui.goto(230,-20)
    gui.goto(230,0)
    gui.goto(250,-20)
    gui.goto(270,0)
    gui.goto(290,-20)
    gui.goto(230,-20)
    gui.goto(230,-180)
    gui.goto(310,-180)
    #Carro
    carro=turtle.Pen()
    carro.shape("square")
    carro.speed(0)
    #Carga
    carga=turtle.Pen()
    carga.shape("circle")
    carga.color("red")
    carga.speed(0)
    carga.left(270)
    carga.forward(20*x[0][2])
    carga.left(-270)
    #Cabo
    cabo=turtle.Pen()
    cabo.shape("square")
    cabo.shapesize(0.1,x[0][2])
    cabo.left(90)
    cabo.goto(0,-20*x[0][2]/2)
    carga.speed(0)
    ###Variaveis medias
    theta_barra=0
    Lbarra=0
    Lpbarra=0
    xpbarra=0
    controle=True
    for i in range(n):
        #bloco para printar barra dos carros
        if k==0 or i==n-1:
            horizontal=[xl[i],x[i][0]]
            vertical=[yl[i],0]
            plt.plot(horizontal,vertical,markerfacecolor='k',linestyle='-',c='black')
            k=n/5
        k=k-1
        Ft=K*dx[i][3]               # Força que age sobre o carro (função de corrente)
        F=Ft
        Ts=-Td
        #----Derivadas segundas----
        if t>6 and dx[i][0]>0 and controle:
            E0=-E
        if t>6 and dx[i][0]<0.1:
            E0=0
            controle=False

        ######NÃO LINEAR###########
        #-----Amortecido--------
        beta=1/(I*Mt+Mt*Ml*(r**2)+I*Ml*(math.sin(x[i][1])**2))
        cos=math.cos(x[i][1])
        sin=math.sin(x[i][1])
        if x[i][2]>Lf:
            ddx0=beta*(I*sin*(Ml*x[i][2]*dx[i][1]**2+g*Ml*cos) +  (I+Ml*r**2)*(-Bc*dx[i][0]+F) + Ml*sin*(Bs*dx[i][2]-r*Ts))
            ddx1=-cos*beta/x[i][2]*(I*sin*(Ml*x[i][2]*dx[i][1]**2 + g*Ml*cos) +(F-Bc*x[i][0])*(I+Ml*r**2) +Ml*sin*(Bs*x[i][2]-r*Ts))-1/x[i][2]*(2*dx[i][2]*dx[i][1]+g*sin)
            ddx2=beta*(Mc*(r**2)*(Ml*x[i][2]*(dx[i][1]**2) +g*Ml*cos) + (Mc+Ml*sin**2)*(-Bs*dx[i][2]+r*Ts) + r**2*sin*(Ml*Bc*dx[i][0]-Ml*F))
            ddx3=(E0-R*dx[i][3]-K1*dx[i][0])/L
        else:
            ddx0=1/Mt*(Ml*g*x[i][1]-Bc*dx[i][0]+K*dx[i][3])
            ddx1=1/Mt/Lf*(Bc*dx[i][0]-g*x[i][1]*(Mt+Ml))
            ddx2=0
            ddx3=(E0-R*dx[i][3]-K1*dx[i][0])/L
        xderivadas2=[ddx0,ddx1,ddx2,ddx3]


        #print(derivadas2)
        ddx.append(xderivadas2)
        #------Derivadas primeira-----
        dx0=ddx0*h + dx[i][0]
        dx1=ddx1*h + dx[i][1]
        dx2=ddx2*h + dx[i][2]
        if x[i][2]<Lf:
            dx2=0
        dx3=ddx3*h + dx[i][3]
        dx.append([dx0,dx1,dx2,dx3])

        #print(dx)
        
        #-----Termos sem derivadas------
        x0=dx0*h + x[i][0]
        x1=dx1*h + x[i][1]
        x2=dx2*h + x[i][2]
        x3=dx3*h + x[i][3]
        x.append([x0,x1,x2,x3])
        
        #----------------------------
        ### Variaveis da Carga
        xl.append(x0+x2*math.sin(x1))
        yl.append(-x2*math.cos(x1))
        theta_barra=theta_barra+x1
        Lbarra=Lbarra+x2
        Lpbarra=Lpbarra+dx2
        xpbarra=xpbarra+dx0
        ###
        t=t+h
        tlist.append(t)
        listazero.append(0)
    ######LINEAR#############################
    #print(x0)
    #print(x1)
    theta_barra=theta_barra/n
    Lbarra=Lbarra/n
    Lpbarra=Lpbarra/n
    xpbarra=xpbarra/n
    t=0
    print(Lbarra)
    print(theta_barra)
    print(Lpbarra)
    print(xpbarra)
    E0=E
    controle=True
    for i in range(n):
        if t>6 and dx[i][0]>0 and controle:
            E0=-E
        if t>6 and dx[i][0]<0.1:
            E0=0
            controle=False
        Ts=-Td
        if z[i][2]>Lf:
            ddz0=-Bc/Mc*(dz[i][0])+g*Ml/Mc*z[i][1]+K*dz[i][3]/Mc                  #X menina
            ddz1=-Bc/(Mc*Lbarra)*dz[i][0] -g*Ml/(Lbarra)*(1/Ml+1/Mc)*z[i][1]-1/(Mc*Lbarra)*K*dz[i][3]-2*Lpbarra*dz[i][1]/Lbarra -Bc*xpbarra*z[i][2]/(Mc*Lbarra**2)  
            ddz2=-Bs/(I+r**2*Ml)*dz[i][2] +1/(I/r+r*Ml)*(Ts+Ml*g*r) + r**2*Ml*Bc*xpbarra*z[i][1]/(I*Mc+Mc*Ml*r**2)
            ddz2=-Bs/(I+r**2*Ml)*dz[i][2] +1/(I/r+r*Ml)*(Ts+Ml*g*r) + r**2*Ml*Bc*xpbarra*z[i][1]/(I*Mc+Mc*Ml*r**2)
            ddz3=(E0-R*dz[i][3]-K1*dz[i][0])/L
        else:
            ddz0=1/Mt*(Ml*g*z[i][1]-Bc*dz[i][0]+K*dz[i][3])
            ddz1=1/Mt/Lf*(Bc*dz[i][0]-g*z[i][1]*(Mt+Ml))
            ddz2=0
            ddz3=(E0-R*dz[i][3]-K1*dz[i][0])/L
        zderivadas2=[ddz0,ddz1,ddz2,ddz3]

        dz0=ddz0*h + dz[i][0]
        dz1=ddz1*h + dz[i][1]
        dz2=ddz2*h + dz[i][2]
        if z[i][2]<Lf:
            dz2=0
        dz3=ddz3*h + dz[i][3]
        dz.append([dz0,dz1,dz2,dz3])
        
        z0=dz0*h + z[i][0]
        z1=dz1*h + z[i][1]
        z2=dz2*h + z[i][2]
        z3=dz3*h + z[i][3]
        z.append([z0,z1,z2,z3])
        
        zxl.append(z0+z2*math.sin(z1))
        zyl.append(-z2*math.cos(z1))
        t=t+h
##############MOVIMENTAÇÃO DOS TURTLES
    a1=0
    salva=90
    carga.color("red")
    for i in range(50):
        a2=int(i*(n/50))
        #--Movimento do cabo
        d=((xl[a2]-x[a2][0])**2+yl[a2]**2)**(1/2)
        #ang=math.asin(-yl[a2]/d)*180/pi
        ang=math.acos(-(xl[a2]-x[a2][0])/d)*180/pi
        cabo.penup()
        vira=ang-salva
        cabo.shapesize(0.1,d)
        cabo.left(vira)
        cabo.goto(20*(xl[a2]+(x[a2][0]-xl[a2])/2),20*yl[a2]/2)
        #--Movimento do carro
        carro.forward(20*(x[a2][0]-x[a1][0]))
        #--Movimento da carga 
        carga.goto(20*xl[a2],20*yl[a2])
        salva=ang
        a1=a2

    a1=0
    salva=0
    carga.color("black")
    carro.reset()
    cabo.reset()
    for i in range(50):
        if i==0:
            carga.penup()
        else:
            carga.pendown()
        a2=int(i*(n/50))
        #--Movimento do cabo
        d=((zxl[a2]-z[a2][0])**2+zyl[a2]**2)**(1/2)
        #ang=math.asin(-yl[a2]/d)*180/pi
        ang=math.acos(-(zxl[a2]-z[a2][0])/d)*180/pi
        cabo.penup()
        vira=ang-salva
        cabo.shapesize(0.1,d)
        cabo.left(vira)
        cabo.goto(20*(zxl[a2]+(z[a2][0]-zxl[a2])/2),20*zyl[a2]/2)
        #--Movimento do carro
        carro.forward(20*(z[a2][0]-z[a1][0]))
        #--Movimento da carga 
        carga.goto(20*zxl[a2],20*zyl[a2])
        salva=ang
        a1=a2
    
    #-----Movimento do sistema no Tempo------#
    xcar=p_coluna(x,0)
    plt.plot(xcar,listazero)
    plt.plot(xl,yl,markerfacecolor='k',linestyle='--')
    plt.plot(zxl,zyl,markerfacecolor='k',linestyle='--')
    plt.suptitle("Posição da carga")
    plt.xlabel("Horizontal (metros)")
    plt.ylabel("Vertical (metros)")
    plt.show()
    ##------Gráficos Posição x tempo carro------------------
    ycar=p_coluna(x,0)
    zcar=p_coluna(z,0)
    plt.plot(tlist,xcar)
    plt.plot(tlist,ycar)
    plt.plot(tlist,zcar)
    plt.suptitle("Posição do carro x Tempo ")
    plt.xlabel("Tempo (s)")
    plt.ylabel("Posição (m)")
    plt.show()
    ##------Gráficos Velociadde x tempo carro------------------
    dxcar=p_coluna(dx,0)
    dzcar=p_coluna(dz,0)
    plt.plot(tlist,dxcar)
    plt.plot(tlist,dzcar)
    plt.suptitle("Velocidade do carro x Tempo")
    plt.xlabel("Tempo (s)")
    plt.ylabel("Velocidade (m/s)")
    plt.show()   
    ##------Gráficos Angulo x tempo carga------------------
    xf=p_coluna(x,1)
    zf=p_coluna(z,1)
    plt.plot(tlist,xf)
    plt.plot(tlist,zf)
    plt.suptitle("Ângulo da carga x Tempo")
    plt.xlabel("Tempo (s)")
    plt.ylabel("Ângulo (rad)")
    plt.show()
    ##------Gráficos velocidade Angular x tempo carga------------------
    dxf=p_coluna(dx,1)
    dzf=p_coluna(dz,1)
    plt.plot(tlist,dxf)
    plt.plot(tlist,dzf)
    plt.suptitle("Velocidade angular da carga x Tempo")
    plt.xlabel("Tempo (s)")
    plt.ylabel("Velocidade (rad/s)")
    plt.show()
    ##------Gráficos comprimento x tempo do cabo------------------
    xcab=p_coluna(x,2)
    zcab=p_coluna(z,2)
    plt.plot(tlist,xcab)
    plt.plot(tlist,zcab)
    plt.suptitle("Comprimento do cabo x Tempo")
    plt.xlabel("Tempos (s)")
    plt.ylabel("Comprimento (m)")
    plt.show()
    ##---------Gráficos velocidade x tempo do cabo
    dxcab=p_coluna(dx,2)
    dzcab=p_coluna(dz,2)
    plt.plot(tlist,dxcab)
    plt.plot(tlist,dzcab)
    plt.suptitle("Velocidade do cabo x Tempo")
    plt.xlabel("Tempos (s)")
    plt.ylabel("Comprimento (m)")
    plt.show()
    ##------Gráficos corrente x tempo------------------
    dxi=p_coluna(dx,3)
    dzi=p_coluna(dz,3)
    plt.plot(tlist,dxi)
    plt.plot(tlist,dzi)
    plt.suptitle("Corrente do motor x Tempo")
    plt.xlabel("Tempo (s)")
    plt.ylabel("Corrente (A)")
    plt.show()
    return
main()