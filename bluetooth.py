#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import glob
import time
import RPi.GPIO as GPIO
from bluetooth import *
led = 19
GPIO.setmode(GPIO.BCM)
GPIO.setup(led, GPIO.OUT)

# 50Hz PWM Frequency

pwm_led = GPIO.PWM(led, 50)


pwm_led.start(0)

server_sock = BluetoothSocket(RFCOMM)
server_sock.bind(('', PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = '94f39d29-7d6d-437d-973b-fba39e49d4ee'

advertise_service(server_sock, 'AquaPiServer', service_id=uuid,
                  service_classes=[uuid, SERIAL_PORT_CLASS],
                  profiles=[SERIAL_PORT_PROFILE])

#                   protocols = [ OBEX_UUID ]

while True:
    print 'Aguardando a conexao RFCOMM canal: %d' % port

    (client_sock, client_info) = server_sock.accept()
    print 'Conexao aceita de ', client_info

    try:
        data = client_sock.recv(1024)
        if len(data) == 0:
            break
        print 'Recebido: [%s]' % data

        if data == 'temp':
            print 'Bluetooth Desconectado com Sucesso!!!'
            client_sock.close()
            server_sock.close()
            GPIO.cleanup()
            break
        elif data == 'lightOff1':
            duty = int(0)
            pwm_led.ChangeDutyCycle(duty)
            data = 'light off1!'
            client_sock.send(data)
            print 'Enviado: [%s]' % data
        elif data == 'lightOn1':
            duty = int(100)
            pwm_led.ChangeDutyCycle(duty)
            data = 'light on1!'
            client_sock.send(data)
            print 'Enviado: [%s]' % data
        else:
            duty = int(data)
            pwm_led.ChangeDutyCycle(duty)
            data = 'cursor!'
            client_sock.send(data)
            print 'enviando [%s]' % data
    except IOError:

        pass
    except KeyboardInterrupt:

        print 'desconectado'

        client_sock.close()
        server_sock.close()
        print 'all done'

        break
