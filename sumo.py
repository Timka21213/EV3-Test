#!/usr/bin/env python3

from ev3dev.ev3 import * #подлючение модулей
from time import sleep, time

distanceEnemy = 400 #расстояние до препядствия
speedNorm = 900 #скорость движения телеги
grayCalib = 20 #значение для учебного поля (черн = 3, белый = 37, калибровка = (3+37)/2)
timeSearch = 3 # время на поиск врагов

running = True
ledsState = True
timeStartSearch = 0

def AllMotorStop():
    motorLeft.stop(stop_action = 'hold') #останов
    motorRight.stop(stop_action = 'hold')

def AllMotorRunTime(speed, time):
    motorLeft.run_forever(speed_sp = speed) #едем прямо
    motorRight.run_forever(speed_sp = speed)
    sleep(time)
    AllMotorStop()

def Attack(forvard):
    Leds.set_color(Leds.LEFT, Leds.RED)
    Leds.set_color(Leds.RIGHT, Leds.RED)
    
    AllMotorStop()
    speedAttack = speedNorm
    colorSensor = colorFront
    if forvard == False:
        speedAttack = -speedNorm
        colorSensor = colorRear
        
    motorLeft.run_forever(speed_sp = speedAttack) #едем прямо
    motorRight.run_forever(speed_sp = speedAttack)
    while colorSensor.value() > grayCalib: #пока не уткнемся в линию 
        sleep(0.01)
            
    AllMotorStop()
    print ('Out of zone !!!')
    motorLeft.run_forever(speed_sp = -speedAttack) #отезжаем
    motorRight.run_forever(speed_sp = -speedAttack)
    sleep(2)
    AllMotorStop()

def StartSearchEnemy(direction = True): #стартуем поиск врага
    global timeStartSearch
    print ('Search enemy...')
    
    Leds.set_color(Leds.LEFT, Leds.GREEN)
    Leds.set_color(Leds.RIGHT, Leds.GREEN)
    
    speedRotate = speedNorm/2 #задаем направление вращения
    if direction == False:
        speedRotate = -speedRotate
        
    motorLeft.run_forever(speed_sp = -speedRotate) #разворот на месте
    motorRight.run_forever(speed_sp = speedRotate)
    timeStartSearch = time() #засекаем время начала поиска

def CheckTimeSearch(): #контроль времени поиска врагов
    if time() - timeStartSearch > timeSearch: #время истекло
        print ('Enemy not found... %d sec' % (time() - timeStartSearch))
        Leds.set_color(Leds.LEFT, Leds.YELLOW)
        Leds.set_color(Leds.RIGHT, Leds.YELLOW)
        AllMotorStop()
        motorLeft.run_forever(speed_sp = speedNorm/2) #медленно едем прямо 
        motorRight.run_forever(speed_sp = speedNorm/2)        
        sleep(1)
        AllMotorStop()
        StartSearchEnemy() #начинаем сканировать
        
motorLeft = LargeMotor('outA') #создаем левый мотор
assert motorLeft.connected, 'Connect left motor in port A'
motorRight = LargeMotor('outD') #создаем правый мотор
assert motorRight.connected, 'Connect right motor in port B'

colorFront = ColorSensor('in4')
assert colorFront.connected, 'Подключите датчик цвета EV3 в IN4'
# Переводим датчик в режим измерения освещенности
# в этом режиме датчик выдает освещенность 0..100%
colorFront.mode='COL-REFLECT'

colorRear = ColorSensor('in2')
assert colorRear.connected, 'Подключите датчик цвета EV3 в IN2'
# Переводим датчик в режим измерения освещенности
# в этом режиме датчик выдает освещенность 0..100%
colorRear.mode='COL-REFLECT'

sonicFront = UltrasonicSensor('in1') #создаем объект ультразвуковой дальномер
assert sonicFront.connected, 'Connect Sonic Sensor in port 1'
sonicFront.mode = 'US-DIST-CM' # Переводим УЗ датчик в режим измерения в ММ

sonicRear = UltrasonicSensor('in3') #создаем объект ультразвуковой дальномер
assert sonicRear.connected, 'Connect Sonic Sensor in port 3'
sonicRear.mode = 'US-DIST-CM' # Переводим УЗ датчик в режим измерения в ММ

btn = Button() #создаем объект кнопка

''' #для калибровки датчика
while running:
    print (colorFront.value())
    sleep(1)
'''

Sound.beep()

print ('Start rotate ?')

dirRotate = True #выбираем начальное направление вращения
while (not btn.left) and (not btn.right): #крутим цикл пока не нажата левая или правая кнопка
    if btn.left:
       dirRotate = False
    sleep(0.01)
       
Sound.beep()

sleep(1)

#перемигиваемся пока не нажмут какую либо кнопку
while not btn.any(): #ждем нажатия любой кнопки
    if ledsState: #моргаем светодиодами
        Leds.set_color(Leds.LEFT, Leds.GREEN)
        Leds.set_color(Leds.RIGHT, Leds.RED)
    else:
        Leds.set_color(Leds.LEFT, Leds.RED)
        Leds.set_color(Leds.RIGHT, Leds.GREEN)
    ledsState = not ledsState
    sleep(0.1)

sleep(5) #требование судей

#имперский марш для устрашения противника
Sound.tone([ \
    (392, 350, 100), (392, 350, 100), (392, 350, 100), (311.1, 250, 100), \
    (466.2, 25, 100), (392, 350, 100), (311.1, 250, 100), (466.2, 25, 100), \
    (392, 700, 100), (587.32, 350, 100), (587.32, 350, 100), \
    (587.32, 350, 100), (622.26, 250, 100), (466.2, 25, 100), \
    (369.99, 350, 100), (311.1, 250, 100), (466.2, 25, 100), (392, 700, 100), \
    (784, 350, 100), (392, 250, 100), (392, 25, 100), (784, 350, 100), \
    (739.98, 250, 100), (698.46, 25, 100), (659.26, 25, 100), \
    (622.26, 25, 100), (659.26, 50, 400), (415.3, 25, 200), (554.36, 350, 100), \
    (523.25, 250, 100), (493.88, 25, 100), (466.16, 25, 100), (440, 25, 100), \
    (466.16, 50, 400), (311.13, 25, 200), (369.99, 350, 100), \
    (311.13, 250, 100), (392, 25, 100), (466.16, 350, 100), (392, 250, 100), \
    (466.16, 25, 100), (587.32, 700, 100), (784, 350, 100), (392, 250, 100), \
    (392, 25, 100), (784, 350, 100), (739.98, 250, 100), (698.46, 25, 100), \
    (659.26, 25, 100), (622.26, 25, 100), (659.26, 50, 400), (415.3, 25, 200), \
    (554.36, 350, 100), (523.25, 250, 100), (493.88, 25, 100), \
    (466.16, 25, 100), (440, 25, 100), (466.16, 50, 400), (311.13, 25, 200), \
    (392, 350, 100), (311.13, 250, 100), (466.16, 25, 100), \
    (392.00, 300, 150), (311.13, 250, 100), (466.16, 25, 100), (392, 700) \
    ])

Leds.all_off()
       
print ('Start')

StartSearchEnemy(dirRotate) #начинаем крутится в поисках вражины

while running:    
    distanceFront = sonicFront.value() #получаем дистанции с датчиков расстояния
    distanceRear = sonicRear.value()
    
    if distanceFront < distanceEnemy:
        print ('Font attack!!!')
        Attack(True) #атакуем
        StartSearchEnemy() #начинаем крутится в поисках вражины
    elif distanceRear < distanceEnemy:
        print ('Rear attack!!!')
        Attack(False)
        StartSearchEnemy()
    
    CheckTimeSearch() #контроль времени поиска вражины
        
    if btn.any(): #если нажата проивольная кнопка то останов работы
        running = False
        
    sleep(0.01) #задержка главного цикла
    
Leds.all_off()
AllMotorStop() #Останов платформы
print('The END')
