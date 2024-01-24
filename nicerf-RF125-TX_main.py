import tkinter as tk
from tkinter import ttk
import serial
import threading

# A simple Information Window
class InformWindow:
    def __init__(self, informStr):
        self.window = tk.Tk()
        self.window.title("Information")
        self.window.geometry("220x60")
        label = tk.Label(self.window, text=informStr)
        buttonOK = tk.Button(self.window, text="OK", command=self.processButtonOK)
        label.pack(side=tk.TOP)
        buttonOK.pack(side=tk.BOTTOM)
        self.window.mainloop()

    def processButtonOK(self):
        self.window.destroy()

class mainGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("125HKz Tx Board App")
        self.uartState = False # is uart open or not

        # COM configuration frame
        frame_COMinf = tk.Frame(self.window)
        frame_COMinf.grid(row=1, column=1)

        labelCOM = tk.Label(frame_COMinf, text="COMx: ")
        self.COM = tk.StringVar(value="COM5")
        entryCOM = tk.Entry(frame_COMinf, textvariable=self.COM)
        labelCOM.grid(row=1, column=1, padx=5, pady=3)
        entryCOM.grid(row=1, column=2, padx=5, pady=3)

        labelBaudrate = tk.Label(frame_COMinf, text="Baudrate: ")
        self.Baudrate = tk.IntVar(value=9600)
        comboBaudrate = ttk.Combobox(frame_COMinf, width=17, textvariable=self.Baudrate)
        comboBaudrate["values"] = (9600, 115200)
        #entryBaudrate = tk.Entry(frame_COMinf, textvariable=self.Baudrate)
        labelBaudrate.grid(row=1, column=3, padx=5, pady=3)
        comboBaudrate.grid(row=1, column=4, padx=5, pady=3)

        labelParity = tk.Label(frame_COMinf, text="Parity: ")
        self.Parity = tk.StringVar(value="NONE")
        comboParity = ttk.Combobox(frame_COMinf, width=17, textvariable=self.Parity)
        comboParity["values"] = ("NONE", "ODD", "EVEN", "MARK", "SPACE")
        comboParity["state"] = "readonly"
        labelParity.grid(row=2, column=1, padx=5, pady=3)
        comboParity.grid(row=2, column=2, padx=5, pady=3)

        labelStopbits = tk.Label(frame_COMinf, text="Stopbits: ")
        self.Stopbits = tk.StringVar(value="1")
        comboStopbits = ttk.Combobox(frame_COMinf, width=17, textvariable=self.Stopbits)
        comboStopbits["values"] = ("1", "1.5", "2")
        comboStopbits["state"] = "readonly"
        labelStopbits.grid(row=2, column=3, padx=5, pady=3)
        comboStopbits.grid(row=2, column=4, padx=5, pady=3)

        self.buttonSS = tk.Button(frame_COMinf, text="Start", command=self.processButtonSS)
        self.buttonSS.grid(row=3, column=4, padx=5, pady=3, sticky=tk.E)
        
        # Config Board frame
        frameConfig = tk.Frame(self.window)
        frameConfig.grid(row=1, column=2)

        # Payload command
        labelPayload = tk.Label(frameConfig, text="Payload Data (hex, space-separated):")
        labelPayload.grid(row=1, column=1, padx=3, pady=2, sticky=tk.W)
        
        # Set a default value for the payload data
        defaultPayload = "01 02 03 04 05"
        self.payloadData = tk.StringVar(value=defaultPayload)
        entryPayload = tk.Entry(frameConfig, textvariable=self.payloadData, width=60)
        entryPayload.grid(row=2, column=1, padx=5, pady=3)

        buttonSendPayload = tk.Button(frameConfig, text="Send Payload Command", command=self.processPayloadCommand)
        buttonSendPayload.grid(row=3, column=1, padx=5, pady=3, sticky=tk.E)
        
        # Transmitter ID command
        labelPayload = tk.Label(frameConfig, text="Transmitter ID (hex, space-separated):")
        labelPayload.grid(row=4, column=1, padx=3, pady=2, sticky=tk.W)

        # Set a default value for the Transmitter ID
        defaultTransmitterID = "01"
        self.transmitterID = tk.StringVar(value=defaultTransmitterID)
        entryTransmitterID = tk.Entry(frameConfig, textvariable=self.transmitterID, width=60)
        entryTransmitterID.grid(row=5, column=1, padx=5, pady=3)
        
        buttonSendTransmitterID = tk.Button(frameConfig, text="Send Transmitter ID Command", command=self.processTransmitterIDCommand)
        buttonSendTransmitterID.grid(row=6, column=1, padx=5, pady=3, sticky=tk.W)
        
        buttonGetTransmitterID = tk.Button(frameConfig, text="Get Transmitter ID", command=self.processGetTransmitterID)
        buttonGetTransmitterID.grid(row=6, column=1, padx=0, pady=3, sticky=tk.E)
        
        # Time Interval command frame
        labelPayload = tk.Label(frameConfig, text="Time Interval (hex, space-separated) (Range: 0x00FA~0xEA60, 250ms ~60 seconds):")
        labelPayload.grid(row=7, column=1, padx=3, pady=2, sticky=tk.W)

        # Set a default value for the Time Interval
        defaultTimeInterval = "00 FA"
        self.timeInterval = tk.StringVar(value=defaultTimeInterval)
        entryTimeInterval = tk.Entry(frameConfig, textvariable=self.timeInterval, width=60)
        entryTimeInterval.grid(row=8, column=1, padx=5, pady=3)
        
        buttonSendTimeInterval = tk.Button(frameConfig, text="Send Time Interval Command", command=self.processTransmitterIDCommand)
        buttonSendTimeInterval.grid(row=9, column=1, padx=5, pady=3, sticky=tk.E)
        
        # Start and Stop Transmission Buttons
        
        buttonStartTransmission = tk.Button(frameConfig, text="Start Transmission", command=self.processStartTransmission)
        buttonStartTransmission.grid(row=10, column=1, padx=5, pady=3, sticky=tk.E)
        
        buttonStopTransmission = tk.Button(frameConfig, text="Stop Transmission", command=self.processStopTransmission)
        buttonStopTransmission.grid(row=11, column=1, padx=5, pady=3, sticky=tk.E)
        
        # Mode selection (ASCII or Binary)
        self.mode = tk.StringVar(value="Binary")
        self.checkMode = tk.Checkbutton(frameConfig, text="Binary Mode", 
                                        variable=self.mode, 
                                        onvalue="Binary", offvalue="ASCII",
                                        command=self.toggleMode)
        self.checkMode.grid(row=12, column=1, padx=5, pady=3)
        
        # Thread control flag
        self.running = True

        # Serial object
        self.ser = serial.Serial()
        # Serial read threading
        #self.ReadUARTThread = threading.Thread(target=self.ReadUART)
        #self.ReadUARTThread.start()
        
         # Create and start the read thread as a daemon
        self.ReadUARTThread = threading.Thread(target=self.ReadUART, daemon=True)
        self.ReadUARTThread.start()
        
        # Bind the closing event
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Received data frame
        frameRecv = tk.Frame(self.window)
        frameRecv.grid(row=2, column=1)
        labelOutText = tk.Label(frameRecv, text="Received Data:")
        labelOutText.grid(row=1, column=1, padx=3, pady=2, sticky=tk.W)
        frameRecvSon = tk.Frame(frameRecv)
        frameRecvSon.grid(row=2, column=1)
        scrollbarRecv = tk.Scrollbar(frameRecvSon)
        scrollbarRecv.pack(side=tk.RIGHT, fill=tk.Y)
        self.OutputText = tk.Text(frameRecvSon, wrap=tk.WORD, width=60, height=20, yscrollcommand=scrollbarRecv.set)
        self.OutputText.pack()

        # Transmit data frame
        frameTrans = tk.Frame(self.window)
        frameTrans.grid(row=3, column=1)
        labelInText = tk.Label(frameTrans, text="To Transmit Data:")
        labelInText.grid(row=1, column=1, padx=3, pady=2, sticky=tk.W)
        frameTransSon = tk.Frame(frameTrans)
        frameTransSon.grid(row=2, column=1)
        scrollbarTrans = tk.Scrollbar(frameTransSon)
        scrollbarTrans.pack(side=tk.RIGHT, fill=tk.Y)
        self.InputText = tk.Text(frameTransSon, wrap=tk.WORD, width=60, height=5, yscrollcommand=scrollbarTrans.set)
        self.InputText.pack()
        self.buttonSend = tk.Button(frameTrans, text="Send", command=self.processButtonSend)
        self.buttonSend.grid(row=3, column=1, padx=5, pady=3, sticky=tk.E)

        self.window.mainloop()
        
    def processGetTransmitterID(self):
        if self.uartState:
            # Construct the command
            cmd = [0x52] + [0x0D, 0x0A]

            # Send the command
            bytesToSend = bytes(cmd)
            self.ser.write(bytesToSend)
            print("Start Transmit Command Sent:", bytesToSend)
        else:
            InformWindow("Not Connected!")
        
    def processStartTransmission(self):
        if self.uartState:
            # Construct the command
            cmd = [0x73, 0x74, 0x61, 0x72, 0x74] + [0x0D, 0x0A]

            # Send the command
            bytesToSend = bytes(cmd)
            self.ser.write(bytesToSend)
            print("Start Transmit Command Sent:", bytesToSend)
        else:
            InformWindow("Not Connected!")
    
    def processStopTransmission(self):
        if self.uartState:
            # Construct the command
            cmd = [0x73, 0x74, 0x6F, 0x70] + [0x0D, 0x0A]

            # Send the command
            bytesToSend = bytes(cmd)
            self.ser.write(bytesToSend)
            print("Stop Transmit Command Sent:", bytesToSend)
        else:
            InformWindow("Not Connected!")
        
    def processTransmitterIDCommand(self):
        if self.uartState:
            payload_byte = self.transmitterID.get()
            if len(payload_byte) > 0x02:
                InformWindow("Transmitter ID too long!")
                return

            try:
                # Construct the command
                cmd = [0x58] + [int(payload_byte, 16)] + [0x0D, 0x0A]

                # Send the command
                bytesToSend = bytes(cmd)
                self.ser.write(bytesToSend)
                print("Transmitter ID Command Sent:", bytesToSend)
            except ValueError:
                InformWindow("Invalid Hex Input!")
        else:
            InformWindow("Not Connected!")
        
    def processTimeIntervalCommand(self):
        if self.uartState:
            payload_bytes = self.timeInterval.get().split()
            if len(payload_bytes) > 0x2D:
                InformWindow("Payload too long!")
                return

            try:
                # Construct the command
                cmd = [0x53] + [int(byte, 16) for byte in payload_bytes] + [0x0D, 0x0A]

                # Send the command
                bytesToSend = bytes(cmd)
                self.ser.write(bytesToSend)
                print("Time Interval Command Sent:", bytesToSend)
            except ValueError:
                InformWindow("Invalid Hex Input!")
        else:
            InformWindow("Not Connected!")

    def processPayloadCommand(self):
        if self.uartState:
            payload_bytes = self.payloadData.get().split()
            if len(payload_bytes) > 0x2D:
                InformWindow("Payload too long!")
                return

            try:
                # Construct the command
                length = len(payload_bytes) # Length of payload plus the two end bytes
                cmd = [0x57, length] + [int(byte, 16) for byte in payload_bytes] + [0x0D, 0x0A]

                # Send the command
                bytesToSend = bytes(cmd)
                self.ser.write(bytesToSend)
                print("Payload Command Sent:", bytesToSend)
            except ValueError:
                InformWindow("Invalid Hex Input!")
        else:
            InformWindow("Not Connected!")

    def toggleMode(self):
        mode = self.mode.get()
        print(f"Mode switched to: {mode}")

    def processButtonSS(self):
        if self.uartState:
            self.ser.close()
            self.buttonSS["text"] = "Start"
            self.uartState = False
        else:
            self.ser.port = self.COM.get()
            self.ser.baudrate = self.Baudrate.get()
            parity = self.Parity.get()
            self.ser.parity = serial.PARITY_NONE if parity == "NONE" else \
                              serial.PARITY_ODD if parity == "ODD" else \
                              serial.PARITY_EVEN if parity == "EVEN" else \
                              serial.PARITY_MARK if parity == "MARK" else \
                              serial.PARITY_SPACE
            stopbits = self.Stopbits.get()
            self.ser.stopbits = serial.STOPBITS_ONE if stopbits == "1" else \
                                serial.STOPBITS_ONE_POINT_FIVE if stopbits == "1.5" else \
                                serial.STOPBITS_TWO

            try:
                self.ser.open()
            except:
                InformWindow(f"Can't open {self.ser.port}")

            if self.ser.isOpen():
                self.buttonSS["text"] = "Stop"
                self.uartState = True

    def processButtonSend(self):
        if self.uartState:
            strToSend = self.InputText.get(1.0, tk.END).strip()

            if self.mode.get() == "Binary":
                try:
                    bytesToSend = bytes.fromhex(strToSend)
                except ValueError:
                    InformWindow("Invalid Hex Input!")
                    return
            else:
                bytesToSend = strToSend.encode('ascii')

            self.ser.write(bytesToSend)
            print("Sent:", bytesToSend)
        else:
            InformWindow("Not In Connect!")
            
    def on_closing(self):
        # Stop the thread
        self.running = False

        # Close the serial port if open
        if self.uartState:
            self.ser.close()

        # Destroy the window
        self.window.destroy()

    def ReadUART(self):
        while self.running:
            if self.uartState:
                try:
                    if self.ser.in_waiting:
                        data = self.ser.read(self.ser.in_waiting)
                        print("Received:", data)

                        hexStr = data.hex(' ')
                        asciiStr = data.decode('ascii', errors='replace')

                        displayStr = f"Binary: {hexStr}\nASCII: {asciiStr}\n" if self.mode.get() == "Binary" else f"{asciiStr}\n"

                        self.OutputText.insert(tk.END, displayStr)
                        # Scroll to the end of text box to make latest data visible
                        self.OutputText.see(tk.END)
                except Exception as e:
                    InformWindow(f"Receiving Error: {e}")
                    self.ser.close()
                    self.buttonSS["text"] = "Start"
                    self.uartState = False

mainGUI()
